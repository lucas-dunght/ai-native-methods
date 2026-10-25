#!/usr/bin/env python3
"""
Unified Search Pool v2.0 (Local FastMCP Proxy) - Smart Multi-Signal & Auto-Failover Engine
------------------------------------------------------------------------------------------
1. Định tuyến đa tín hiệu có trọng số (Weighted Multi-Signal Intent Router):
   - Tavily (General/Legal Fact): Pháp lý Việt Nam, văn bản luật, thuế, bảo hiểm, bảng lương, thông tin địa phương, Q&A.
   - Tavily (Realtime News): Tin tức nóng, thời sự hôm nay, giá vàng, tỷ giá, chứng khoán, thời tiết.
   - Exa (Academic Paper): Bài báo khoa học, arXiv, luận án, whitepaper, SOTA.
   - Exa (Code & Tech): Lập trình, mã nguồn, GitHub repo, SDK/API, lỗi kỹ thuật, thuật toán.
   - Exa (Company & Startup): Hồ sơ startup, vòng gọi vốn, nhà sáng lập, đối thủ cạnh tranh B2B.
   - Linkup (Deep Synthesis): Nghiên cứu chuyên sâu (Deep Dive), phân tích toàn diện, tổng hợp đa nguồn.
   - Hybrid Mode: Chạy song song 2 công cụ đầu bảng, khử trùng lặp URL và hợp nhất kết quả.
2. Nguyên tắc xoay vòng thông minh (Smart Intra-Provider Round-Robin + Failover):
   - Xoay vòng con trỏ (Round-Robin) giữa các API Key trong CÙNG 1 CÔNG CỤ để chia tải đều.
   - Thử hết toàn bộ các key khỏe mạnh của công cụ ưu tiên trước khi chuyển sang công cụ tiếp theo.
   - Nếu công cụ trả về 0 kết quả (Empty Results - 204): Không phạt key, lập tức chuyển sang công cụ kế tiếp để tiết kiệm credit.
3. Tiered Circuit Breaker & Persistent State:
   - Phân tầng thời gian cách ly: Quota/Auth (401/402/403/432/433) -> 3600s; Rate Limit (429) -> 60s; Server Error (5xx) -> 30s.
   - Lưu trạng thái đồng bộ tại /tmp/unified_search_pool_state.json để chia sẻ giữa nhiều tiến trình/agents.
4. TTL Cache (300s) & HTTP Connection Pooling giúp tiết kiệm credit và tăng tốc phản hồi.
"""

import asyncio
import hashlib
import json
import logging
import os
import re
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, urlunparse

import httpx
from fastmcp import FastMCP

# Setup logging to stderr so stdio MCP transport is never polluted
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("unified-search")


# 1. Tự động nạp biến môi trường từ ~/.mcp_env (Hot-reload thông minh theo mtime)
_last_env_mtime: float = 0.0


def load_mcp_env(force: bool = False):
    global _last_env_mtime
    env_file = Path.home() / ".mcp_env"
    if not env_file.exists():
        return
    try:
        mtime = env_file.stat().st_mtime
        if not force and mtime <= _last_env_mtime:
            return
        _last_env_mtime = mtime
        content = env_file.read_text(encoding="utf-8")
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[7:].strip()
            if "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("'\"")
                if key:
                    os.environ[key] = val
    except Exception as e:
        logger.warning(f"Không thể đọc ~/.mcp_env: {e}")


load_mcp_env(force=True)


# 2. Quản lý Circuit Breaker, Round-Robin & Persistent State
COOLDOWN_QUOTA_SECONDS = 3600   # 1 giờ cho lỗi hết credit / key hỏng (401, 402, 403, 432, 433)
COOLDOWN_RATELIMIT_SECONDS = 60 # 60 giây cho lỗi giới hạn tốc độ ngắn hạn (429)
COOLDOWN_TRANSIENT_SECONDS = 30 # 30 giây cho lỗi máy chủ / timeout tạm thời (5xx)
CACHE_TTL_SECONDS = 300         # 5 phút cache cho truy vấn trùng lặp

STATE_FILE = Path(tempfile.gettempdir()) / "unified_search_pool_state.json"


def key_id(key: str) -> str:
    """Khoá state 1 chiều cho API key — KHÔNG bao giờ ghi raw key ra đĩa."""
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


class KeyPoolManager:
    def __init__(self):
        # {key_id(key): {"expire_at": float, "reason": str, "status": int}}
        self.cooldowns: Dict[str, dict] = {}
        # Con trỏ Round-Robin cho từng provider: {"tavily": 0, "exa": 0, "linkup": 0}
        self.rr_cursor: Dict[str, int] = {"tavily": 0, "exa": 0, "linkup": 0}
        # Thống kê số lần gọi thành công/thất bại theo từng key đã mask
        self.stats: Dict[str, Dict[str, int]] = {}
        self._load_state()

    def _load_state(self):
        if not STATE_FILE.exists():
            return
        try:
            data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            now = time.time()
            raw_cd = data.get("cooldowns", {})
            # Chỉ giữ cooldown còn hiệu lực VÀ khoá đúng dạng key_id (16 hex).
            # Bộ lọc này đồng thời dọn các bản ghi cũ lưu raw key (từng lọt ra đĩa).
            self.cooldowns = {
                k: v for k, v in raw_cd.items()
                if isinstance(v, dict) and v.get("expire_at", 0) > now
                and re.fullmatch(r"[0-9a-f]{16}", k)
            }
            for p in ("tavily", "exa", "linkup"):
                if p in data.get("rr_cursor", {}):
                    self.rr_cursor[p] = int(data["rr_cursor"][p])
            self.stats = data.get("stats", {})
        except Exception:
            pass

    def _save_state(self):
        try:
            now = time.time()
            active_cd = {
                k: v for k, v in self.cooldowns.items()
                if isinstance(v, dict) and v.get("expire_at", 0) > now
                and re.fullmatch(r"[0-9a-f]{16}", k)
            }
            payload = {
                "cooldowns": active_cd,
                "rr_cursor": self.rr_cursor,
                "stats": self.stats,
                "updated_at": now,
            }
            STATE_FILE.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            try:
                os.chmod(STATE_FILE, 0o600)
            except Exception:
                pass
        except Exception:
            pass

    def parse_pool(self, env_pool_var: str, single_var: str) -> List[str]:
        """Lấy danh sách key từ biến Pool (phân tách dấu phẩy) hoặc fallback về biến đơn lẻ."""
        load_mcp_env()
        raw_pool = os.environ.get(env_pool_var, "").strip()
        keys = []
        if raw_pool:
            for k in raw_pool.split(","):
                k = k.strip()
                if k and k not in keys:
                    keys.append(k)
        if not keys:
            single = os.environ.get(single_var, "").strip()
            if single:
                keys.append(single)
        return keys

    def get_keys(self, provider: str) -> List[str]:
        provider = provider.lower()
        if provider == "tavily":
            return self.parse_pool("TAVILY_KEY_POOL", "TAVILY_API_KEY")
        elif provider == "exa":
            return self.parse_pool("EXA_KEY_POOL", "EXA_API_KEY")
        elif provider == "linkup":
            return self.parse_pool("LINKUP_KEY_POOL", "LINKUP_API_KEY")
        return []

    def get_ordered_keys(self, provider: str) -> List[Tuple[int, str]]:
        """
        Trả về danh sách [(original_1based_index, key)] theo thứ tự Round-Robin.
        Giúp phân tải đều giữa 6 key của cùng 1 công cụ nhưng vẫn thử đủ 100% key của công cụ đó.
        """
        self._load_state()
        provider = provider.lower()
        keys = self.get_keys(provider)
        n = len(keys)
        if n == 0:
            return []
        start_idx = self.rr_cursor.get(provider, 0) % n
        # Xoay con trỏ cho lần gọi kế tiếp
        self.rr_cursor[provider] = (start_idx + 1) % n
        self._save_state()

        ordered = []
        for offset in range(n):
            actual_idx = (start_idx + offset) % n
            ordered.append((actual_idx + 1, keys[actual_idx]))
        return ordered

    def is_cooled_down(self, key: str) -> bool:
        kid = key_id(key)
        info = self.cooldowns.get(kid)
        if not info:
            return False
        if time.time() < info.get("expire_at", 0):
            return True
        del self.cooldowns[kid]
        self._save_state()
        return False

    def record_success(self, provider: str, key: str):
        masked = f"{provider.lower()}:{self.mask_key(key)}"
        entry = self.stats.setdefault(masked, {"ok": 0, "err": 0})
        entry["ok"] = entry.get("ok", 0) + 1
        kid = key_id(key)
        if kid in self.cooldowns:
            del self.cooldowns[kid]
        self._save_state()

    def mark_failure(self, provider: str, key: str, status_code: int, error_msg: str):
        masked_key = self.mask_key(key)
        stat_key = f"{provider.lower()}:{masked_key}"
        entry = self.stats.setdefault(stat_key, {"ok": 0, "err": 0})
        entry["err"] = entry.get("err", 0) + 1

        # Phân tầng thời gian Cooldown theo đúng chuẩn mã lỗi của Tavily / Exa / Linkup
        if status_code in (401, 402, 403, 432, 433):
            cd_sec = COOLDOWN_QUOTA_SECONDS
            reason = f"Quota/Auth (HTTP {status_code})"
        elif status_code == 429:
            cd_sec = COOLDOWN_RATELIMIT_SECONDS
            reason = "Rate Limit (HTTP 429)"
        else:
            cd_sec = COOLDOWN_TRANSIENT_SECONDS
            reason = f"Transient/Server (HTTP {status_code})"

        self.cooldowns[key_id(key)] = {
            "expire_at": time.time() + cd_sec,
            "reason": reason,
            "status": status_code,
        }
        self._save_state()
        logger.warning(
            f"[{provider}] Key {masked_key} gặp lỗi {reason}: {error_msg[:120]} -> Cooldown {cd_sec}s."
        )

    @staticmethod
    def mask_key(key: str) -> str:
        if len(key) <= 8:
            return "***"
        return f"{key[:4]}...{key[-4:]}"


pool_mgr = KeyPoolManager()


# 3. Bộ nhớ đệm TTL (In-Memory Cache) & Shared HTTP Client
class TTLCache:
    def __init__(self, ttl_seconds: int = CACHE_TTL_SECONDS, max_entries: int = 128):
        self.ttl = ttl_seconds
        self.max_entries = max_entries
        self.store: Dict[str, Tuple[float, str]] = {}

    def get(self, cache_key: str) -> Optional[str]:
        item = self.store.get(cache_key)
        if not item:
            return None
        expire_at, val = item
        if time.time() < expire_at:
            return val
        del self.store[cache_key]
        return None

    def set(self, cache_key: str, val: str):
        if len(self.store) >= self.max_entries:
            # Xóa bớt mục cũ nhất
            oldest_k = min(self.store.keys(), key=lambda k: self.store[k][0])
            del self.store[oldest_k]
        self.store[cache_key] = (time.time() + self.ttl, val)


search_cache = TTLCache()

_shared_client: Optional[httpx.AsyncClient] = None


def get_http_client() -> httpx.AsyncClient:
    global _shared_client
    if _shared_client is None or _shared_client.is_closed:
        _shared_client = httpx.AsyncClient(
            timeout=httpx.Timeout(25.0, connect=8.0),
            limits=httpx.Limits(max_keepalive_connections=15, max_connections=30),
            follow_redirects=True,
        )
    return _shared_client


# 4. Bộ Định Tuyến Đa Tín Hiệu Có Trọng Số (Weighted Multi-Signal Query Router)
class QueryRouter:
    """
    Phân tích đa tín hiệu câu truy vấn bằng hệ thống chấm điểm trọng số (Weighted Scoring),
    khắc phục triệt để lỗi bắt nhầm từ khóa đơn lẻ (ví dụ: câu hỏi pháp lý/thuế có chữ 'công ty').
    """

    # 1. Tín hiệu Pháp lý / Hành chính / Đời sống Việt Nam (Ưu tiên tuyệt đối Tavily General + AI Answer)
    RE_LEGAL_VN = re.compile(
        r"\b(luật|nghị định|thông tư|quy định|bộ luật|pháp luật|điều khoản|bảo hiểm xã hội|bhxh|"
        r"bhyt|bhtn|thuế thu nhập|thuế gtgt|vat|quyết toán thuế|bảng lương|lương cơ sở|"
        r"lương tối thiểu|mức phạt|xử phạt|thủ tục|hồ sơ|công văn|chính phủ|quốc hội|"
        r"bộ lao động|bộ tài chính|đóng bảo hiểm|người lao động|hợp đồng lao động)\b",
        re.IGNORECASE,
    )

    # 2. Tín hiệu Thời sự / Tin nóng / Giá cả thời gian thực (Ưu tiên Tavily News/Realtime)
    RE_BREAKING_NEWS = re.compile(
        r"\b(hôm nay|ngày mai|tin tức|thời sự|thời tiết|mới nhất|vừa mới|vừa qua|giá vàng|"
        r"chứng khoán|vn-index|vnindex|tỷ giá|ngoại tệ|giá xăng|giá dầu|lịch thi đấu|"
        r"kết quả bóng đá|breaking news|latest news|weather today|stock price|gold price|"
        r"exchange rate|current price)\b",
        re.IGNORECASE,
    )

    # 3. Tín hiệu Học thuật / Bài báo khoa học (Ưu tiên Exa Research Paper)
    RE_ACADEMIC = re.compile(
        r"\b(arxiv|research paper|scientific paper|whitepaper|luận án|luận văn|bài báo khoa học|"
        r"hội thảo khoa học|peer-reviewed|journal|ieee|acm|neurips|icml|iclr|cvpr|"
        r"state of the art|sota|literature review|doi:|citation|abstract)\b",
        re.IGNORECASE,
    )

    # 4. Tín hiệu Lập trình / Kỹ thuật / Mã nguồn (Ưu tiên Exa Neural/Auto Code)
    RE_CODE_TECH = re.compile(
        r"\b(github|gitlab|git repo|repository|source code|mã nguồn|python|javascript|typescript|"
        r"golang|rust|c\+\+|java|swift|kotlin|fastapi|nextjs|react|vue|svelte|tailwind|"
        r"sdk|api|npm|pypi|cargo|package|library|framework|thuật toán|algorithm|data structure|"
        r"exception|stack trace|traceback|error code|segfault|dockerfile|docker compose|"
        r"kubernetes|k8s|terraform|mcp server|fastmcp|langchain|llamaindex|pytorch|tensorflow)\b",
        re.IGNORECASE,
    )

    # 5. Tín hiệu GitHub chuyên biệt (Chỉ bật category='github' khi thực sự tìm repo)
    RE_GITHUB_EXPLICIT = re.compile(
        r"\b(github|github\.com|git repo|open source repo|mã nguồn mở trên github)\b",
        re.IGNORECASE,
    )

    # 6. Tín hiệu Hồ sơ Startup / Venture / Đối thủ cạnh tranh (Exa Company)
    RE_COMPANY_STARTUP = re.compile(
        r"\b(startup|start-up|venture capital|series a|series b|series c|seed round|funding round|"
        r"gọi vốn|nhà sáng lập|co-founder|founder of|crunchbase|pitchbook|y combinator|"
        r"đối thủ cạnh tranh|competitors of|market landscape|b2b saas|unicorn|kỳ lân công nghệ|"
        r"hồ sơ doanh nghiệp|company profile)\b",
        re.IGNORECASE,
    )

    # 7. Tín hiệu Nghiên cứu chuyên sâu / Tổng hợp đa chiều (Linkup Deep Synthesis)
    RE_DEEP_SYNTHESIS = re.compile(
        r"\b(tìm hiểu sâu|phân tích toàn diện|tổng hợp chi tiết|deep dive|comprehensive analysis|"
        r"in-depth analysis|detailed comparison|so sánh toàn diện|so sánh chi tiết|"
        r"đánh giá chuyên sâu|báo cáo phân tích|báo cáo tổng hợp|chiến lược toàn diện|"
        r"nghiên cứu thị trường chuyên sâu)\b",
        re.IGNORECASE,
    )

    @classmethod
    def route(
        cls,
        query: str,
        manual_provider: Optional[str] = None,
        manual_mode: Optional[str] = None,
    ) -> Tuple[List[str], str, dict]:
        """
        Trả về:
            1. provider_order: Thứ tự nhà cung cấp ưu tiên (VD: ['tavily', 'linkup', 'exa'])
            2. intent_label: Tên định tuyến rõ ràng
            3. provider_params: Tham số tối ưu riêng cho từng công cụ
        """
        q = query.strip()
        q_lower = q.lower()

        # 1. Ghi đè thủ công nhà cung cấp (nếu truyền provider='tavily' | 'exa' | 'linkup')
        if manual_provider and manual_provider.lower() in ("tavily", "exa", "linkup"):
            primary = manual_provider.lower()
            others = [p for p in ["tavily", "exa", "linkup"] if p != primary]
            return (
                [primary] + others,
                f"Thủ công chỉ định ({primary.upper()})",
                cls._default_params(q_lower),
            )

        # 2. Ghi đè thủ công chế độ tìm kiếm (mode)
        if manual_mode:
            m = manual_mode.lower()
            if m in ("academic", "paper"):
                return (
                    ["exa", "linkup", "tavily"],
                    "Nghiên cứu học thuật (Exa #1 - Paper)",
                    {
                        "exa": {"category": "research paper", "search_type": "auto"},
                        "tavily": {"topic": "general", "include_answer": True, "search_depth": "advanced"},
                        "linkup": {"depth": "standard", "output_type": "searchResults"},
                    },
                )
            elif m in ("code", "tech"):
                cat = "github" if cls.RE_GITHUB_EXPLICIT.search(q_lower) else None
                return (
                    ["exa", "tavily", "linkup"],
                    "Lập trình & Kỹ thuật (Exa #1 - Code/Tech)",
                    {
                        "exa": {"category": cat, "search_type": "auto"},
                        "tavily": {"topic": "general", "include_answer": False, "search_depth": "basic"},
                        "linkup": {"depth": "standard", "output_type": "searchResults"},
                    },
                )
            elif m == "company":
                return (
                    ["exa", "linkup", "tavily"],
                    "Doanh nghiệp & Startup (Exa #1 - Company)",
                    {
                        "exa": {"category": "company", "search_type": "auto"},
                        "linkup": {"depth": "standard", "output_type": "searchResults"},
                        "tavily": {"topic": "general", "include_answer": True},
                    },
                )
            elif m in ("news", "realtime"):
                return (
                    ["tavily", "linkup", "exa"],
                    "Thời sự & Tin tức (Tavily #1 - News)",
                    {
                        "tavily": {"topic": "news", "include_answer": True, "search_depth": "basic"},
                        "linkup": {"depth": "standard", "output_type": "searchResults"},
                        "exa": {"category": "news", "search_type": "auto"},
                    },
                )
            elif m in ("legal", "law"):
                return (
                    ["tavily", "linkup", "exa"],
                    "Pháp lý & Quy định (Tavily #1 - Legal RAG)",
                    {
                        "tavily": {"topic": "general", "include_answer": True, "search_depth": "advanced"},
                        "linkup": {"depth": "standard", "output_type": "searchResults"},
                        "exa": {"category": None, "search_type": "auto"},
                    },
                )
            elif m in ("deep", "analysis", "synthesis"):
                return (
                    ["linkup", "exa", "tavily"],
                    "Nghiên cứu chuyên sâu (Linkup #1 - Sourced Answer)",
                    {
                        "linkup": {"depth": "standard", "output_type": "sourcedAnswer"},
                        "exa": {"category": None, "search_type": "auto"},
                        "tavily": {"topic": "general", "include_answer": True, "search_depth": "advanced"},
                    },
                )

        # 3. Chấm điểm đa tín hiệu (Multi-Signal Weighted Scoring)
        legal_hits = len(cls.RE_LEGAL_VN.findall(q_lower))
        news_hits = len(cls.RE_BREAKING_NEWS.findall(q_lower))
        academic_hits = len(cls.RE_ACADEMIC.findall(q_lower))
        code_hits = len(cls.RE_CODE_TECH.findall(q_lower))
        company_hits = len(cls.RE_COMPANY_STARTUP.findall(q_lower))
        deep_hits = len(cls.RE_DEEP_SYNTHESIS.findall(q_lower))

        scores = {
            "legal": legal_hits * 4.0,          # Ưu tiên cao nhất khi có từ khóa luật/bảo hiểm/thuế
            "academic": academic_hits * 3.5,    # Ưu tiên cao cho arxiv/paper
            "code": code_hits * 3.0,            # Ưu tiên cho lập trình/github/sdk
            "deep": deep_hits * 3.2,            # Ưu tiên cho phân tích tổng hợp chuyên sâu
            "news": news_hits * 2.5,            # Tin tức thời sự / giá cả hôm nay
            "company": company_hits * 2.5,      # Startup / Venture / Competitors
        }

        # Quy tắc chống bắt nhầm (Anti-Hijacking Rules):
        # - Nếu có tín hiệu pháp lý/thuế/bảo hiểm (legal_hits > 0), tuyệt đối không đẩy vào company
        if legal_hits > 0:
            scores["company"] = 0
            if news_hits > 0:
                scores["legal"] += 2.0  # VD: "quy định đóng BHXH mới nhất năm 2026" -> vẫn giữ ở nhánh Legal (topic='general') để lấy trang luật

        # - Nếu có tín hiệu tin tức hôm nay kèm tên công ty (VD: "tin tức mới nhất về công ty VinFast hôm nay") -> ưu tiên News
        if news_hits > 0 and company_hits > 0:
            scores["news"] += 2.0

        best_intent = max(scores, key=scores.get)
        best_score = scores[best_intent]

        # Nếu không có tín hiệu đặc biệt nào (best_score == 0) -> Tìm kiếm tổng quát qua Tavily
        if best_score <= 0:
            return (
                ["tavily", "exa", "linkup"],
                "Tìm kiếm tổng quát (Tavily #1 - Fact RAG)",
                {
                    "tavily": {"topic": "general", "include_answer": True, "search_depth": "basic"},
                    "exa": {"category": None, "search_type": "auto"},
                    "linkup": {"depth": "standard", "output_type": "searchResults"},
                },
            )

        # Ánh xạ Intent cao điểm nhất sang cấu hình tối ưu
        if best_intent == "legal":
            return (
                ["tavily", "linkup", "exa"],
                "Pháp lý & Quy định chính sách (Tavily #1 - Legal/Policy RAG)",
                {
                    "tavily": {"topic": "general", "include_answer": True, "search_depth": "basic"},
                    "linkup": {"depth": "standard", "output_type": "searchResults"},
                    "exa": {"category": None, "search_type": "auto"},
                },
            )

        if best_intent == "news":
            # Nếu là tra cứu giá vàng, tỷ giá, thời tiết, lịch thi đấu ở VN -> dùng topic='general' cho độ phủ trang Việt Nam tốt hơn topic='news' thuần tiếng Anh
            is_vn_realtime = bool(
                re.search(r"(giá vàng|tỷ giá|thời tiết|giá xăng|chứng khoán|hôm nay|mới nhất)", q_lower)
            )
            tavily_topic = "general" if is_vn_realtime else "news"
            return (
                ["tavily", "linkup", "exa"],
                "Thời sự & Dữ liệu thời gian thực (Tavily #1 - Realtime)",
                {
                    "tavily": {"topic": tavily_topic, "include_answer": True, "search_depth": "basic"},
                    "linkup": {"depth": "standard", "output_type": "searchResults"},
                    "exa": {"category": None, "search_type": "auto"},
                },
            )

        if best_intent == "academic":
            return (
                ["exa", "linkup", "tavily"],
                "Học thuật & Bài báo khoa học (Exa #1 - Research Paper)",
                {
                    "exa": {"category": "research paper", "search_type": "auto"},
                    "linkup": {"depth": "standard", "output_type": "searchResults"},
                    "tavily": {"topic": "general", "include_answer": True, "search_depth": "basic"},
                },
            )

        if best_intent == "code":
            cat = "github" if cls.RE_GITHUB_EXPLICIT.search(q_lower) else None
            return (
                ["exa", "tavily", "linkup"],
                "Lập trình & Tài liệu kỹ thuật (Exa #1 - Code/Docs)",
                {
                    "exa": {"category": cat, "search_type": "auto"},
                    "tavily": {"topic": "general", "include_answer": False, "search_depth": "basic"},
                    "linkup": {"depth": "standard", "output_type": "searchResults"},
                },
            )

        if best_intent == "company":
            # Chỉ khóa category='company' khi truy vấn bằng tiếng Anh về startup/competitors;
            # Với tiếng Việt dùng search_type='auto' không khóa category để không bị mất báo cáo tài chính trong nước.
            has_vn_chars = bool(re.search(r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]", q_lower))
            cat = None if has_vn_chars else "company"
            return (
                ["exa", "linkup", "tavily"],
                "Doanh nghiệp & Thị trường Startup (Exa #1 - Market Intelligence)",
                {
                    "exa": {"category": cat, "search_type": "auto"},
                    "linkup": {"depth": "standard", "output_type": "searchResults"},
                    "tavily": {"topic": "general", "include_answer": True, "search_depth": "basic"},
                },
            )

        if best_intent == "deep":
            return (
                ["linkup", "exa", "tavily"],
                "Tổng hợp & Phân tích chuyên sâu (Linkup #1 - Deep Synthesis)",
                {
                    "linkup": {"depth": "standard", "output_type": "sourcedAnswer"},
                    "exa": {"category": None, "search_type": "auto"},
                    "tavily": {"topic": "general", "include_answer": True, "search_depth": "advanced"},
                },
            )

        return (
            ["tavily", "exa", "linkup"],
            "Tìm kiếm tổng quát (Tavily #1 - Fact RAG)",
            cls._default_params(q_lower),
        )

    @staticmethod
    def _default_params(q_lower: str) -> dict:
        return {
            "tavily": {"topic": "general", "include_answer": True, "search_depth": "basic"},
            "exa": {"category": None, "search_type": "auto"},
            "linkup": {"depth": "standard", "output_type": "searchResults"},
        }


# 5. Provider Search Clients (Async với Shared HTTPX Client & Empty Result Detection)
async def search_tavily(
    query: str,
    key: str,
    num_results: int = 5,
    topic: str = "general",
    include_answer: bool = True,
    search_depth: str = "basic",
) -> Tuple[bool, str, int]:
    """Tìm kiếm qua Tavily Search API."""
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": key,
        "query": query,
        "search_depth": search_depth,
        "max_results": num_results,
        "topic": topic,
        "include_answer": include_answer,
    }
    try:
        client = get_http_client()
        resp = await client.post(url, json=payload, timeout=12.0)
        if resp.status_code != 200:
            return False, resp.text, resp.status_code
        data = resp.json()

        output_lines = []
        if data.get("answer"):
            output_lines.append(f"💡 **Tóm tắt trực tiếp (Tavily AI):**\n{data['answer']}\n")

        results = []
        for r in data.get("results", []):
            title = (r.get("title") or "No title").strip()
            u = (r.get("url") or "").strip()
            content = (r.get("content") or "").strip()
            results.append(f"- [{title}]({u})\n  {content}")

        if results:
            output_lines.append("\n\n".join(results))
        elif not output_lines:
            # Trả về mã 204 để báo hiệu 0 kết quả -> tự động chuyển sang provider kế tiếp mà không phạt key
            return False, "EMPTY_RESULTS", 204

        return True, "\n".join(output_lines), 200
    except httpx.TimeoutException:
        return False, "Timeout khi kết nối tới Tavily API", 504
    except Exception as e:
        return False, str(e), 500


async def search_exa(
    query: str,
    key: str,
    num_results: int = 5,
    category: Optional[str] = None,
    search_type: str = "auto",
) -> Tuple[bool, str, int]:
    """Tìm kiếm qua Exa Search API với chế độ Auto/Neural và Highlights/Text."""
    url = "https://api.exa.ai/search"
    headers = {
        "x-api-key": key,
        "Content-Type": "application/json",
    }
    payload = {
        "query": query,
        "numResults": num_results,
        "type": search_type,
        "contents": {
            "text": {
                "maxCharacters": 1000,
            }
        },
    }
    if category:
        payload["category"] = category

    try:
        client = get_http_client()
        resp = await client.post(url, json=payload, headers=headers, timeout=14.0)
        if resp.status_code != 200:
            return False, resp.text, resp.status_code
        data = resp.json()
        results = []
        for r in data.get("results", []):
            title = (r.get("title") or "No title").strip()
            u = (r.get("url") or "").strip()
            text = (r.get("text") or "").strip()
            # Làm sạch khoảng trắng thừa trong snippet
            text = re.sub(r"\s+", " ", text)[:600]
            results.append(f"- [{title}]({u})\n  {text}")
        if not results:
            return False, "EMPTY_RESULTS", 204
        return True, "\n\n".join(results), 200
    except httpx.TimeoutException:
        return False, "Timeout khi kết nối tới Exa API", 504
    except Exception as e:
        return False, str(e), 500


async def search_linkup(
    query: str,
    key: str,
    num_results: int = 5,
    depth: str = "standard",
    output_type: str = "searchResults",
) -> Tuple[bool, str, int]:
    """Tìm kiếm qua Linkup API hỗ trợ standard / deep search và sourcedAnswer."""
    url = "https://api.linkup.so/v1/search"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    payload = {
        "q": query,
        "depth": depth,
        "outputType": output_type,
    }
    timeout_sec = 25.0 if (depth == "deep" or output_type == "sourcedAnswer") else 14.0
    try:
        client = get_http_client()
        resp = await client.post(url, headers=headers, json=payload, timeout=timeout_sec)
        if resp.status_code != 200:
            return False, resp.text, resp.status_code
        data = resp.json()

        # Trường hợp Linkup trả về câu trả lời tổng hợp (sourcedAnswer)
        if data.get("answer"):
            lines = [f"💡 **Phân tích tổng hợp (Linkup Deep Synthesis):**\n{data['answer']}\n"]
            sources = data.get("sources", [])
            if sources:
                lines.append("**Nguồn tham khảo trích dẫn:**")
                for s in sources[:num_results]:
                    name = (s.get("name") or s.get("title") or "Nguồn web").strip()
                    u = (s.get("url") or "").strip()
                    snippet = (s.get("snippet") or s.get("content") or "").strip()
                    if snippet:
                        snippet = re.sub(r"\s+", " ", snippet)[:350]
                        lines.append(f"- [{name}]({u})\n  {snippet}")
                    else:
                        lines.append(f"- [{name}]({u})")
            return True, "\n".join(lines), 200

        # Trường hợp Linkup trả về danh sách searchResults
        results = []
        for r in data.get("results", [])[:num_results]:
            name = (r.get("name") or r.get("title") or "No title").strip()
            u = (r.get("url") or "").strip()
            content = (r.get("content") or "").strip()
            results.append(f"- [{name}]({u})\n  {content}")

        if not results:
            return False, "EMPTY_RESULTS", 204
        return True, "\n\n".join(results), 200
    except httpx.TimeoutException:
        return False, "Timeout khi kết nối tới Linkup API", 504
    except Exception as e:
        return False, str(e), 500


async def _execute_single_provider(
    provider_name: str,
    query: str,
    num_results: int,
    custom_cfg: dict,
    errors_out: List[str],
) -> Optional[Tuple[str, int, str]]:
    """
    Thực thi tìm kiếm trên 1 nhà cung cấp cụ thể với cơ chế Round-Robin giữa các key.
    Trả về (provider_name, key_index, content) nếu thành công, hoặc None nếu thất bại/rỗng.
    """
    ordered_keys = pool_mgr.get_ordered_keys(provider_name)
    if not ordered_keys:
        errors_out.append(f"{provider_name.capitalize()}: Chưa cấu hình key nào.")
        return None

    for idx, key in ordered_keys:
        if pool_mgr.is_cooled_down(key):
            continue

        success = False
        content = ""
        status = 500

        if provider_name == "tavily":
            topic = custom_cfg.get("topic", "general")
            inc_ans = custom_cfg.get("include_answer", True)
            s_depth = custom_cfg.get("search_depth", "basic")
            success, content, status = await search_tavily(
                query, key, num_results, topic=topic, include_answer=inc_ans, search_depth=s_depth
            )
        elif provider_name == "exa":
            cat = custom_cfg.get("category", None)
            stype = custom_cfg.get("search_type", "auto")
            success, content, status = await search_exa(
                query, key, num_results, category=cat, search_type=stype
            )
        elif provider_name == "linkup":
            depth = custom_cfg.get("depth", "standard")
            out_type = custom_cfg.get("output_type", "searchResults")
            success, content, status = await search_linkup(
                query, key, num_results, depth=depth, output_type=out_type
            )

        if success:
            pool_mgr.record_success(provider_name, key)
            return provider_name, idx, content

        # Nếu công cụ trả về 204 EMPTY_RESULTS: Key vẫn sống tốt, chỉ là công cụ này không có dữ liệu
        # -> Không phạt key và thoát ngay sang công cụ tiếp theo để không đốt thêm key của cùng công cụ!
        if status == 204:
            logger.info(
                f"[{provider_name.upper()}] Key #{idx} trả về 0 kết quả -> Chuyển ngay sang công cụ kế tiếp."
            )
            errors_out.append(f"{provider_name.capitalize()} #{idx}: 0 kết quả phù hợp (Empty).")
            break

        # Nếu gặp lỗi HTTP thực sự (401/402/429/5xx) -> Đưa key vào Cooldown và thử key tiếp theo của CÙNG công cụ
        pool_mgr.mark_failure(provider_name, key, status, content)
        errors_out.append(f"{provider_name.capitalize()} #{idx} (HTTP {status}): {content[:80]}")

    return None


def _normalize_url(u: str) -> str:
    try:
        p = urlparse(u.strip().lower())
        clean_path = p.path.rstrip("/")
        return urlunparse((p.scheme, p.netloc.replace("www.", ""), clean_path, "", "", ""))
    except Exception:
        return u.strip().lower()


def _deduplicate_markdown_blocks(blocks: List[str]) -> str:
    """Khử trùng lặp các mục kết quả có cùng URL khi gộp từ nhiều công cụ ở chế độ Hybrid."""
    seen_urls = set()
    merged_lines = []
    url_pattern = re.compile(r"^- \[.*?\]\((https?://[^\)]+)\)")

    for block in blocks:
        for chunk in block.split("\n\n"):
            chunk = chunk.strip()
            if not chunk:
                continue
            m = url_pattern.match(chunk)
            if m:
                norm_u = _normalize_url(m.group(1))
                if norm_u in seen_urls:
                    continue
                seen_urls.add(norm_u)
            merged_lines.append(chunk)

    return "\n\n".join(merged_lines)


# 6. MCP Tools
mcp = FastMCP("Unified Search Pool")


@mcp.tool()
async def web_search(
    query: str,
    num_results: int = 5,
    provider: Optional[str] = "auto",
    mode: Optional[str] = "auto",
) -> str:
    """Tìm kiếm thông tin web thông minh (v2): Tự động chấm điểm đa tín hiệu để chọn công cụ tối ưu
    (Tavily/Exa/Linkup), xoay vòng cân bằng tải (Round-Robin) các API Key trong cùng một công cụ trước
    khi failover sang công cụ khác.

    Args:
        query: Từ khóa hoặc câu hỏi cần tra cứu.
        num_results: Số lượng kết quả mong muốn (mặc định 5, tối đa 15).
        provider: Chỉ định công cụ ('auto', 'tavily', 'exa', 'linkup'). Mặc định 'auto'.
        mode: Chế độ tìm kiếm ('auto', 'news', 'legal', 'academic', 'code', 'company', 'deep', 'hybrid'). Mặc định 'auto'.
    """
    num_results = max(1, min(int(num_results or 5), 15))
    manual_p = None if provider in (None, "auto", "") else provider.strip().lower()
    manual_m = None if mode in (None, "auto", "") else mode.strip().lower()

    # Kiểm tra TTL Cache (5 phút)
    cache_key = f"{query.strip().lower()}|{num_results}|{manual_p or 'auto'}|{manual_m or 'auto'}"
    cached_resp = search_cache.get(cache_key)
    if cached_resp:
        logger.info(f"Cache HIT cho truy vấn: '{query[:50]}'")
        return cached_resp

    provider_order, intent_label, provider_custom_params = QueryRouter.route(
        query, manual_provider=manual_p, manual_mode=manual_m
    )

    errors_encountered: List[str] = []

    # Chế độ HYBRID: Gọi song song 2 công cụ đầu bảng và gộp kết quả khử trùng lặp URL
    if manual_m == "hybrid":
        top_two = provider_order[:2]
        logger.info(f"Chế độ HYBRID: Chạy song song {top_two[0].upper()} + {top_two[1].upper()}")
        tasks = [
            _execute_single_provider(
                p, query, num_results, provider_custom_params.get(p, {}), errors_encountered
            )
            for p in top_two
        ]
        results = await asyncio.gather(*tasks)
        valid_results = [r for r in results if r is not None]

        if valid_results:
            sources_tag = " + ".join([f"{r[0].upper()} (Key #{r[1]})" for r in valid_results])
            merged_body = _deduplicate_markdown_blocks([r[2] for r in valid_results])
            final_text = (
                f"### [Nguồn: HYBRID ({sources_tag}) | Định tuyến: {intent_label}]\n\n{merged_body}"
            )
            search_cache.set(cache_key, final_text)
            return final_text

    # Chế độ TIÊU CHUẨN / AUTO: Thử từng công cụ theo thứ tự ưu tiên, trong mỗi công cụ thử hết 6 keys
    logger.info(
        f"Định tuyến: {intent_label} | Thứ tự ưu tiên: {' -> '.join([p.upper() for p in provider_order])}"
    )

    for provider_name in provider_order:
        custom_cfg = provider_custom_params.get(provider_name, {})
        res = await _execute_single_provider(
            provider_name, query, num_results, custom_cfg, errors_encountered
        )
        if res is not None:
            p_used, key_idx, content = res
            logger.info(
                f"Tìm kiếm thành công với {p_used.upper()} [Key #{key_idx}] ({intent_label})"
            )
            header = f"### [Nguồn: {p_used.upper()} | Định tuyến: {intent_label} | Key #{key_idx}]\n\n"
            final_text = header + content
            search_cache.set(cache_key, final_text)
            return final_text

    # Nếu tất cả các keys và tất cả các providers đều thất bại
    err_summary = "\n".join([f"- {e}" for e in errors_encountered])
    return (
        "⚠️ Không thể lấy kết quả tìm kiếm: Tất cả các API Key của Tavily, Exa và Linkup "
        "đều đã cạn hạn mức (Quota Exceeded), gặp Rate Limit hoặc không tìm thấy dữ liệu.\n\n"
        f"Chi tiết ghi nhận:\n{err_summary}"
    )


@mcp.tool()
async def web_extract(url: str) -> str:
    """Trích xuất toàn bộ nội dung văn bản từ một URL cụ thể thông qua Tavily Extract hoặc Exa Contents
    với cơ chế xoay vòng Round-Robin các API key.

    Args:
        url: Đường dẫn trang web cần bóc tách nội dung.
    """
    logger.info(f"Bắt đầu web_extract: {url}")
    client = get_http_client()

    # 1. Thử Tavily Extract trước (Xoay vòng Round-Robin toàn bộ key Tavily)
    for idx, key in pool_mgr.get_ordered_keys("tavily"):
        if pool_mgr.is_cooled_down(key):
            continue
        try:
            resp = await client.post(
                "https://api.tavily.com/extract",
                json={"api_key": key, "urls": [url]},
                timeout=15.0,
            )
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                if results and results[0].get("raw_content"):
                    pool_mgr.record_success("tavily", key)
                    raw = results[0]["raw_content"]
                    if len(raw) > 25000:
                        raw = (
                            raw[:25000]
                            + "\n\n... *(Nội dung dài, đã rút gọn 25,000 ký tự đầu tiên để tiết kiệm token)*"
                        )
                    return f"### [Nguồn: Tavily Extract (Key #{idx}) | {url}]\n\n{raw}"
            else:
                pool_mgr.mark_failure("Tavily Extract", key, resp.status_code, resp.text)
        except Exception as e:
            pool_mgr.mark_failure("Tavily Extract", key, 500, str(e))

    # 2. Fallback sang Exa Contents (Xoay vòng Round-Robin toàn bộ key Exa)
    for idx, key in pool_mgr.get_ordered_keys("exa"):
        if pool_mgr.is_cooled_down(key):
            continue
        try:
            headers = {"x-api-key": key, "Content-Type": "application/json"}
            resp = await client.post(
                "https://api.exa.ai/contents",
                json={"urls": [url], "text": {"maxCharacters": 8000}},
                headers=headers,
                timeout=15.0,
            )
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                if results and results[0].get("text"):
                    pool_mgr.record_success("exa", key)
                    raw = results[0]["text"]
                    if len(raw) > 25000:
                        raw = (
                            raw[:25000]
                            + "\n\n... *(Nội dung dài, đã rút gọn 25,000 ký tự đầu tiên để tiết kiệm token)*"
                        )
                    return f"### [Nguồn: Exa Contents (Key #{idx}) | {url}]\n\n{raw}"
            else:
                pool_mgr.mark_failure("Exa Contents", key, resp.status_code, resp.text)
        except Exception as e:
            pool_mgr.mark_failure("Exa Contents", key, 500, str(e))

    return f"Không thể trích xuất nội dung từ URL {url} qua các key hiện có."


@mcp.tool()
def pool_status() -> str:
    """Kiểm tra tình trạng danh sách Key Pool, con trỏ cân bằng tải Round-Robin, thống kê sử dụng,
    trạng thái Cooldown phân tầng và bảng quy tắc định tuyến thông minh v2."""
    pool_mgr._load_state()
    now = time.time()
    tavily_keys = pool_mgr.get_keys("tavily")
    exa_keys = pool_mgr.get_keys("exa")
    linkup_keys = pool_mgr.get_keys("linkup")

    def format_provider(p_code: str, name: str, keys: List[str], desc: str) -> str:
        if not keys:
            return f"**{name}** ({desc}): 0 key được cấu hình"
        active = 0
        cooled = 0
        next_idx = (pool_mgr.rr_cursor.get(p_code, 0) % len(keys)) + 1
        details = []
        for idx, k in enumerate(keys, 1):
            masked = pool_mgr.mask_key(k)
            stat = pool_mgr.stats.get(f"{p_code}:{masked}", {"ok": 0, "err": 0})
            stat_str = f"OK: {stat.get('ok', 0)} | Lỗi: {stat.get('err', 0)}"
            pointer_mark = " 🎯 *(Key kế tiếp)*" if idx == next_idx else ""

            cd_info = pool_mgr.cooldowns.get(key_id(k))
            if cd_info and now < cd_info.get("expire_at", 0):
                rem = int(cd_info["expire_at"] - now)
                reason = cd_info.get("reason", "Cooldown")
                cooled += 1
                details.append(
                    f"  - Key #{idx} (`{masked}`): ⏳ {reason} - còn {rem}s [{stat_str}]{pointer_mark}"
                )
            else:
                active += 1
                details.append(
                    f"  - Key #{idx} (`{masked}`): ✅ Sẵn sàng [{stat_str}]{pointer_mark}"
                )
        lines = [
            f"**{name}** ({desc}): {len(keys)} key ({active} khả dụng, {cooled} cooldown) | Con trỏ kế tiếp: **Key #{next_idx}**"
        ]
        lines.extend(details)
        return "\n".join(lines)

    report = [
        "## Trạng thái Unified Search Key Pool v2.0 (Smart Multi-Signal Engine)",
        f"- Thời gian kiểm tra: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- File trạng thái chia sẻ: `{STATE_FILE}`",
        "",
        "### 1. Tình trạng Kho API Key & Cân bằng tải (Round-Robin):",
        format_provider("tavily", "Tavily", tavily_keys, "Pháp lý VN, thời sự, dữ liệu thực tế, Q&A RAG"),
        "",
        format_provider("exa", "Exa", exa_keys, "Bài báo khoa học/arXiv, GitHub/code, Startup, Neural search"),
        "",
        format_provider("linkup", "Linkup", linkup_keys, "Nghiên cứu chuyên sâu (Deep Synthesis), báo cáo đa nguồn"),
        "",
        "### 2. Ma trận Định tuyến Đa Tín Hiệu Có Trọng Số (v2):",
        "- **Pháp lý / Thuế / Bảo hiểm / Chính sách VN ('luật', 'nghị định', 'bhxh', 'thuế'...)**: `Tavily (General + Answer) -> Linkup -> Exa` *(Chống bắt nhầm vào Company khi có từ 'công ty'/'doanh nghiệp')*",
        "- **Thời sự / Tin nóng / Giá cả hôm nay ('hôm nay', 'mới nhất', 'giá vàng', 'thời tiết'...)**: `Tavily (Realtime) -> Linkup -> Exa`",
        "- **Học thuật / Bài báo khoa học ('arxiv', 'research paper', 'luận án', 'sota'...)**: `Exa (Research Paper) -> Linkup -> Tavily`",
        "- **Lập trình / Kỹ thuật / Mã nguồn ('github', 'python', 'sdk', 'api', 'traceback'...)**: `Exa (Auto/Code) -> Tavily -> Linkup`",
        "- **Hồ sơ Startup / Gọi vốn / Đối thủ ('startup', 'series a', 'founder', 'competitors'...)**: `Exa (Market) -> Linkup -> Tavily`",
        "- **Nghiên cứu chuyên sâu ('tìm hiểu sâu', 'phân tích toàn diện', 'deep dive'...)**: `Linkup (Sourced Answer) -> Exa -> Tavily`",
        "- **Chế độ Hybrid (`mode='hybrid'`)**: Chạy song song 2 công cụ đầu bảng, khử trùng lặp URL và gộp kết quả.",
        "",
        "### 3. Cơ chế Tự phục hồi & Tiết kiệm Credit:",
        "- **Round-Robin nội bộ**: Tự động xoay vòng Key #1 -> #6 trong cùng một công cụ để phân tán tải đều, thử đủ 6 key trước khi chuyển công cụ.",
        "- **Empty-Result Fast-Jump (HTTP 204)**: Nếu công cụ trả về 0 kết quả, không phạt key và nhảy ngay sang công cụ tiếp theo.",
        "- **Cooldown phân tầng**: Hết quota/sai key (`401/402/403/432/433`) cách ly 3600s; Rate limit (`429`) cách ly 60s; Lỗi mạng (`5xx`) cách ly 30s.",
    ]
    return "\n".join(report)


if __name__ == "__main__":
    mcp.run()
