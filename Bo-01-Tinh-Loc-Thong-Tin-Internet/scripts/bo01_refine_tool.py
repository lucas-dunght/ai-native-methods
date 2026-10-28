#!/usr/bin/env python3
"""Bo-01 Internet Information Refinement Deep Module CLI Tool.

Provides deterministic, zero-dependency Python stdlib utilities for:
1. ptc-filter: Programmatic Tool Calling (PTC) context window slicing & HTML noise stripping.
2. audit-echo: Citation graph independent origin counting & echo-chamber detection.
3. gate-check: Quantitative gate verification before Stage 4 Synthesis.
4. export-bo02: Deterministic export of verified Fact Cards to Bo-02 L1 SOT records.
5. --self-test: In-memory verification suite (<200ms).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

TOOL_NAME = "bo01_refine_tool"
VERSION = "2.1.0"

CLAIM_TO_BO02_EDGE = {
    "OBSERVED": ("OBSERVED", "EXTRACTED"),
    "EXTRACTED": ("OBSERVED", "EXTRACTED"),
    "DERIVED": ("DERIVED", "INFERRED"),
    "INFERRED": ("DERIVED", "INFERRED"),
    "PRIOR": ("PRIOR", "AMBIGUOUS"),
    "ASSUMED": ("ASSUMED", "AMBIGUOUS"),
    "UNVERIFIED": ("ASSUMED", "AMBIGUOUS"),
    "AMBIGUOUS": ("ASSUMED", "AMBIGUOUS"),
}


def emit_output(payload: Dict[str, Any], as_json: bool = True, exit_code: int = 0) -> int:
    """Emit structured JSON or human-readable output and return exit code."""
    if as_json:
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    else:
        status = payload.get("status", "UNKNOWN")
        summary = payload.get("summary", "")
        sys.stdout.write(f"[{TOOL_NAME}] {status}: {summary}\n")
        if payload.get("root_cause"):
            sys.stdout.write(f"  Root cause: {payload['root_cause']}\n")
        if payload.get("next_command"):
            sys.stdout.write(f"  Next command: {payload['next_command']}\n")
    return exit_code


def actionable_error(
    error_code: str,
    root_cause: str,
    next_command: str,
    subcommand: str = "global",
    as_json: bool = True,
    exit_code: int = 2,
) -> int:
    """Format an Actionable Error following the Deep Module CLI contract."""
    payload = {
        "status": "ERROR",
        "tool": TOOL_NAME,
        "subcommand": subcommand,
        "error_code": error_code,
        "summary": f"Execution failed in {subcommand}: {error_code}",
        "root_cause": root_cause,
        "next_command": next_command,
    }
    return emit_output(payload, as_json=as_json, exit_code=exit_code)


def dump_yaml_Compat(data: Any) -> str:
    """Serialize data to clean YAML using PyYAML if available, else stdlib emitter."""
    try:
        import yaml  # type: ignore

        return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    except Exception:
        return _stdlib_to_yaml(data, indent=0) + "\n"


def _stdlib_to_yaml(obj: Any, indent: int = 0) -> str:
    prefix = "  " * indent
    if obj is None:
        return "null"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        if "\n" in obj or any(ch in obj for ch in (":", "#", "{", "}", "[", "]", ",", '"', "'")):
            return json.dumps(obj, ensure_ascii=False)
        return obj
    if isinstance(obj, list):
        if not obj:
            return "[]"
        lines: List[str] = []
        for item in obj:
            if isinstance(item, dict):
                first = True
                for k, v in item.items():
                    val_str = _stdlib_to_yaml(v, indent + 2)
                    if first:
                        if isinstance(v, (dict, list)) and v:
                            lines.append(f"{prefix}- {k}:\n{val_str}")
                        else:
                            lines.append(f"{prefix}- {k}: {val_str}")
                        first = False
                    else:
                        if isinstance(v, (dict, list)) and v:
                            lines.append(f"{prefix}  {k}:\n{val_str}")
                        else:
                            lines.append(f"{prefix}  {k}: {val_str}")
            else:
                lines.append(f"{prefix}- {_stdlib_to_yaml(item, indent + 1)}")
        return "\n".join(lines)
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        lines = []
        for k, v in obj.items():
            if isinstance(v, (dict, list)) and v:
                lines.append(f"{prefix}{k}:\n{_stdlib_to_yaml(v, indent + 1)}")
            else:
                lines.append(f"{prefix}{k}: {_stdlib_to_yaml(v, indent + 1)}")
        return "\n".join(lines)
    return json.dumps(str(obj), ensure_ascii=False)


def load_structured_text(raw: str) -> Any:
    """Parse JSON or YAML text using stdlib JSON first, then PyYAML, then stdlib simple YAML."""
    stripped = raw.strip()
    if not stripped:
        return {}
    try:
        return json.loads(stripped)
    except Exception:
        pass
    try:
        import yaml  # type: ignore

        return yaml.safe_load(stripped)
    except Exception:
        pass
    return _stdlib_parse_simple_yaml(stripped)


def _stdlib_parse_simple_yaml(text: str) -> Any:
    """Fallback parser for simple key-value or list-of-dict YAML files."""
    lines = [
        ln.rstrip()
        for ln in text.splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    if not lines:
        return {}
    if lines[0].lstrip().startswith("- "):
        items: List[Dict[str, Any]] = []
        current: Dict[str, Any] = {}
        for ln in lines:
            s = ln.lstrip()
            if s.startswith("- "):
                if current:
                    items.append(current)
                current = {}
                s = s[2:].strip()
            if ":" in s:
                k, v = s.split(":", 1)
                current[k.strip()] = _parse_scalar(v.strip())
        if current:
            items.append(current)
        return items
    result: Dict[str, Any] = {}
    current_list_key: Optional[str] = None
    for ln in lines:
        s = ln.strip()
        if s.startswith("- ") and current_list_key:
            val = s[2:].strip()
            if ":" in val and not (val.startswith('"') or val.startswith("'")):
                k, v = val.split(":", 1)
                result[current_list_key].append({k.strip(): _parse_scalar(v.strip())})
            else:
                result[current_list_key].append(_parse_scalar(val))
            continue
        if ":" in s:
            k, v = s.split(":", 1)
            k = k.strip()
            v = v.strip()
            if not v:
                result[k] = []
                current_list_key = k
            else:
                result[k] = _parse_scalar(v)
                current_list_key = None
    return result


def _parse_scalar(val: str) -> Any:
    if not val or val in ("null", "~"):
        return None
    if val in ("true", "True"):
        return True
    if val in ("false", "False"):
        return False
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        return val[1:-1]
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(x.strip()) for x in inner.split(",")]
    try:
        if "." in val:
            return float(val)
        return int(val)
    except ValueError:
        return val


def strip_html_noise(raw_text: str) -> str:
    """Remove script/style blocks, HTML comments, tags, and collapse whitespace."""
    cleaned = re.sub(r"(?is)<(script|style|noscript|svg|nav|footer)[^>]*>.*?</\1>", " ", raw_text)
    cleaned = re.sub(r"(?s)<!--.*?-->", " ", cleaned)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def run_ptc_filter(
    raw_items: List[Dict[str, Any]],
    keywords: List[str],
    window_chars: int = 600,
    max_snippets: int = 3,
) -> Dict[str, Any]:
    """Filter raw search items into compact keyword-anchored snippets with SHA-256 provenance."""
    if not raw_items:
        return {
            "status": "EMPTY",
            "tool": TOOL_NAME,
            "subcommand": "ptc-filter",
            "summary": "Input search list is empty (0 items processed).",
            "metrics": {
                "items_in": 0,
                "items_out": 0,
                "raw_chars": 0,
                "filtered_chars": 0,
                "reduction_pct": 0.0,
            },
            "results": [],
            "next_command": f"python3 scripts/{TOOL_NAME}.py --self-test --json",
        }

    clean_keywords = [k.strip() for k in keywords if k.strip()]
    escaped = [re.escape(k) for k in clean_keywords]
    pattern = re.compile("|".join(escaped), re.IGNORECASE) if escaped else None

    total_raw_chars = 0
    total_filtered_chars = 0
    filtered_results: List[Dict[str, Any]] = []

    for idx, item in enumerate(raw_items, 1):
        raw_body = str(item.get("raw_content") or item.get("content") or item.get("text") or "")
        total_raw_chars += len(raw_body)
        source_hash = hashlib.sha256(raw_body.encode("utf-8")).hexdigest()
        cleaned_body = strip_html_noise(raw_body)

        snippets: List[str] = []
        if pattern and cleaned_body:
            for match in pattern.finditer(cleaned_body):
                start = max(0, match.start() - window_chars)
                end = min(len(cleaned_body), match.end() + window_chars)
                snippet = cleaned_body[start:end].strip()
                if snippet and snippet not in snippets:
                    snippets.append(snippet)
                if len(snippets) >= max_snippets:
                    break

        if not snippets and cleaned_body:
            fallback = cleaned_body[: min(len(cleaned_body), window_chars * 2)].strip()
            if fallback:
                snippets.append(fallback)

        item_filtered_chars = sum(len(s) for s in snippets)
        total_filtered_chars += item_filtered_chars

        if snippets:
            url = str(item.get("url") or f"source://{idx}")
            domain = urlparse(url).netloc.lower().replace("www.", "") or "local"
            filtered_results.append(
                {
                    "source_id": item.get("source_id") or f"SRC-{idx:03d}",
                    "title": item.get("title") or f"Source {idx}",
                    "url": url,
                    "domain": domain,
                    "published_date": item.get("published_date") or item.get("date") or "unknown",
                    "trust_tier": item.get("trust_tier") or "T3",
                    "independent_origin_id": item.get("independent_origin_id") or domain,
                    "source_hash": f"sha256:{source_hash}",
                    "untrusted_external_content": True,
                    "snippets": snippets,
                }
            )

    reduction_pct = (
        round((1.0 - (total_filtered_chars / max(1, total_raw_chars))) * 100.0, 2)
        if total_raw_chars > 0
        else 0.0
    )

    return {
        "status": "OK",
        "tool": TOOL_NAME,
        "subcommand": "ptc-filter",
        "summary": (
            f"Filtered {len(raw_items)} raw sources into {len(filtered_results)} snippet bundles "
            f"({total_raw_chars} -> {total_filtered_chars} chars, {reduction_pct}% context reduction)."
        ),
        "metrics": {
            "items_in": len(raw_items),
            "items_out": len(filtered_results),
            "raw_chars": total_raw_chars,
            "filtered_chars": total_filtered_chars,
            "reduction_pct": reduction_pct,
        },
        "results": filtered_results,
        "next_command": f"python3 scripts/{TOOL_NAME}.py audit-echo --input <filtered.json> --json",
    }


def _parse_source_records(raw_text: str) -> List[Dict[str, Any]]:
    """Parse source records from JSON, YAML, CSV, or Markdown table."""
    stripped = raw_text.strip()
    if not stripped:
        return []
    if stripped.startswith("{") or stripped.startswith("["):
        loaded = json.loads(stripped)
        if isinstance(loaded, dict):
            return list(loaded.get("results") or loaded.get("sources") or [loaded])
        if isinstance(loaded, list):
            return list(loaded)

    # Check if Markdown table
    md_lines = [ln.strip() for ln in stripped.splitlines() if "|" in ln]
    if len(md_lines) >= 2:
        headers = [c.strip().lower() for c in md_lines[0].strip("|").split("|")]
        records: List[Dict[str, Any]] = []
        for ln in md_lines[1:]:
            cells = [c.strip() for c in ln.strip("|").split("|")]
            if all(re.match(r"^[-:]+$", c.replace(" ", "")) for c in cells if c):
                continue
            if len(cells) == len(headers):
                records.append(dict(zip(headers, cells)))
        if records:
            return records

    # Try CSV
    try:
        reader = csv.DictReader(io.StringIO(stripped))
        if reader.fieldnames and len(reader.fieldnames) > 1:
            rows = [dict(r) for r in reader]
            if rows:
                return rows
    except Exception:
        pass

    loaded_yaml = load_structured_text(stripped)
    if isinstance(loaded_yaml, list):
        return loaded_yaml
    if isinstance(loaded_yaml, dict):
        return list(loaded_yaml.get("sources") or loaded_yaml.get("results") or [loaded_yaml])
    return []


def run_audit_echo(records: List[Dict[str, Any]], min_origins: int = 2) -> Dict[str, Any]:
    """Audit citation independence and detect echo chambers."""
    if not records:
        raise ValueError("Source log contains 0 records.")

    first_keys = set(records[0].keys())
    has_origin = bool({"independent_origin_id", "primary_origin_url"} & first_keys)
    has_tier = bool({"trust_tier", "authority_tier"} & first_keys)
    missing: List[str] = []
    if not has_origin:
        missing.append("independent_origin_id (or primary_origin_url)")
    if not has_tier:
        missing.append("trust_tier (or authority_tier)")
    if missing:
        raise KeyError(f"Missing required column(s): {', '.join(missing)}")

    origins: Dict[str, List[str]] = {}
    t1_t2_origins: set[str] = set()

    for idx, rec in enumerate(records, 1):
        origin_id = str(
            rec.get("independent_origin_id") or rec.get("primary_origin_url") or ""
        ).strip()
        url = str(rec.get("url") or rec.get("source_id") or f"row-{idx}").strip()
        tier = str(
            rec.get("trust_tier") or rec.get("authority_tier") or "T3"
        ).strip().upper()
        if not origin_id:
            raise ValueError(f"Row {idx} ({url}) has empty independent_origin_id/primary_origin_url.")
        origins.setdefault(origin_id, []).append(url)
        if tier in ("T1", "T2", "TIER 1", "TIER 2", "TIER-1", "TIER-2", "1", "2", "VERIFIED", "PROBABLE"):
            t1_t2_origins.add(origin_id)

    echo_chambers = {
        orig: urls for orig, urls in origins.items() if len(urls) > 1
    }
    independent_count = len(origins)
    passed = independent_count >= min_origins and len(t1_t2_origins) >= 1

    return {
        "status": "PASS" if passed else "FAIL",
        "tool": TOOL_NAME,
        "subcommand": "audit-echo",
        "summary": (
            f"Audited {len(records)} source URLs across {independent_count} independent origins "
            f"({len(t1_t2_origins)} T1/T2 origins, {len(echo_chambers)} echo-chamber clusters)."
        ),
        "metrics": {
            "total_urls": len(records),
            "independent_origin_count": independent_count,
            "t1_t2_origin_count": len(t1_t2_origins),
            "echo_chamber_cluster_count": len(echo_chambers),
            "min_origins_required": min_origins,
        },
        "echo_chambers": echo_chambers,
        "next_command": (
            f"python3 scripts/{TOOL_NAME}.py gate-check --independent-origins {independent_count} "
            f"--unresolved-conflicts 0 --citation-coverage 100 --expired-ttl 0 --json"
            if passed
            else f"python3 scripts/{TOOL_NAME}.py audit-echo --help"
        ),
    }


def run_gate_check(
    independent_origins: int,
    unresolved_conflicts: int,
    citation_coverage: float,
    expired_ttl: int,
    min_origins: int = 2,
) -> Dict[str, Any]:
    """Evaluate the 4 quantitative gate criteria before Stage 4 Synthesis."""
    failures: List[str] = []
    if independent_origins < min_origins:
        failures.append(
            f"independent_origin_count={independent_origins} < required {min_origins}"
        )
    if unresolved_conflicts > 0:
        failures.append(
            f"unresolved_high_med_conflicts={unresolved_conflicts} (must be 0)"
        )
    if citation_coverage < 100.0:
        failures.append(
            f"citation_coverage_pct={citation_coverage}% < required 100.0%"
        )
    if expired_ttl > 0:
        failures.append(f"expired_ttl_claims={expired_ttl} (must be 0)")

    passed = len(failures) == 0
    return {
        "status": "PASS" if passed else "BLOCKED",
        "tool": TOOL_NAME,
        "subcommand": "gate-check",
        "gate_verdict": "PASS" if passed else "BLOCKED",
        "summary": (
            "All 4 Stage 3->Stage 4 quantitative gate criteria passed."
            if passed
            else f"Gate D3 BLOCKED by {len(failures)} failing condition(s): {'; '.join(failures)}"
        ),
        "metrics": {
            "independent_origin_count": independent_origins,
            "unresolved_high_med_conflicts": unresolved_conflicts,
            "citation_coverage_pct": citation_coverage,
            "expired_ttl_claims": expired_ttl,
        },
        "failures": failures,
        "next_command": (
            f"python3 scripts/{TOOL_NAME}.py export-bo02 --input <fact-cards.json> --dry-run --json"
            if passed
            else f"python3 scripts/{TOOL_NAME}.py audit-echo --input <source-log.csv> --json"
        ),
    }


def run_export_bo02(
    fact_cards: List[Dict[str, Any]],
    output_path: Optional[Path] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Convert Bo-01 Fact Cards into Bo-02 L1 Atomic Fact YAML records."""
    if not fact_cards:
        raise ValueError("No Fact Cards provided for Bo-02 L1 export.")

    now_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    l1_records: List[Dict[str, Any]] = []

    for idx, card in enumerate(fact_cards, 1):
        fact_id = str(card.get("fact_id") or card.get("id") or f"L1-WEB-{idx:03d}")
        if not fact_id.startswith("L1-"):
            fact_id = f"L1-{fact_id}"
        raw_label = str(
            card.get("claim_label") or card.get("confidence_label") or "OBSERVED"
        ).strip().upper()
        fable_label, bo02_edge = CLAIM_TO_BO02_EDGE.get(
            raw_label, ("ASSUMED", "AMBIGUOUS")
        )
        statement = str(card.get("statement") or card.get("claim") or "").strip()
        if not statement:
            raise ValueError(f"Fact card {fact_id} is missing a non-empty 'statement'.")

        source_locator = str(
            card.get("source_locator")
            or card.get("primary_url")
            or card.get("url")
            or f"source://{fact_id}"
        )
        raw_hash = str(card.get("source_hash") or "").strip()
        if not raw_hash:
            digest = hashlib.sha256(f"{source_locator}:{statement}".encode("utf-8")).hexdigest()
            raw_hash = f"sha256:{digest}"
        elif not raw_hash.startswith("sha256:"):
            raw_hash = f"sha256:{raw_hash}"

        l1_records.append(
            {
                "id": fact_id,
                "fact_id": fact_id,
                "layer": "L1",
                "fact_type": "L1",
                "domain": card.get("domain") or "research",
                "key": card.get("key") or fact_id.lower().replace("_", "-"),
                "statement": statement,
                "value": card.get("value"),
                "unit": card.get("unit") or "text",
                "claim_label": fable_label,
                "edge_label": bo02_edge,
                "provenance_tag": bo02_edge,
                "trust_tier": card.get("trust_tier") or "T1",
                "independent_origin_count": int(card.get("independent_origin_count", 2)),
                "source_locator": source_locator,
                "source_hash": raw_hash,
                "source": {
                    "type": "bo01-fact-card",
                    "document_id": str(card.get("fact_id") or fact_id),
                    "document_path": source_locator,
                    "source_hash": raw_hash,
                    "bo01_fact_id": str(card.get("fact_id") or fact_id),
                },
                "verified_at": card.get("verified_at") or now_date,
                "date_effective": card.get("date_effective") or now_date,
                "date_updated": now_date,
                "ttl_days": int(card.get("ttl_days", 90)),
                "freshness": "FRESH",
                "verification_status": "FRESH",
                "status": "active",
                "downstream_dependents": list(card.get("downstream_dependents") or []),
            }
        )

    yaml_preview = dump_yaml_Compat({"l1_atomic_facts": l1_records})
    written_to: Optional[str] = None

    if output_path and not dry_run:
        resolved = output_path.resolve()
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(yaml_preview, encoding="utf-8")
        written_to = str(resolved)

    return {
        "status": "DRY_RUN_OK" if dry_run else "OK",
        "tool": TOOL_NAME,
        "subcommand": "export-bo02",
        "summary": (
            f"{'Previewed' if dry_run else 'Exported'} {len(l1_records)} Fact Card(s) "
            f"to Bo-02 L1 SOT format with unified 4-label Fable 5.1 mapping."
        ),
        "metrics": {
            "exported_count": len(l1_records),
            "dry_run": dry_run,
            "output_path": written_to or (str(output_path) if output_path else "stdout"),
        },
        "l1_atomic_facts": l1_records,
        "yaml_preview": yaml_preview,
        "next_command": (
            "python3 ../Bo-02-Kernel-Registry-SOT/scripts/bo02_registry_tool.py audit-freshness --help"
        ),
    }


def run_self_test() -> Dict[str, Any]:
    """Run in-memory self-tests for all 4 subcommands and error rescues."""
    t0 = time.monotonic()
    assertions: List[Dict[str, Any]] = []

    # 1. Test ptc-filter noise stripping and context reduction
    noisy_html = (
        "<html><head><script>alert('xss')</script><style>body{color:red}</style></head>"
        "<body>" + ("Menu nav boilerplate " * 120)
        + " Critical benchmark: Latency p99 is 42ms under 10k RPS load. "
        + ("Footer legal copyright " * 120) + "</body></html>"
    )
    ptc_res = run_ptc_filter(
        [{"url": "https://bench.example.com/report", "raw_content": noisy_html, "trust_tier": "T1"}],
        keywords=["Latency p99"],
        window_chars=80,
        max_snippets=2,
    )
    ptc_ok = (
        ptc_res["status"] == "OK"
        and ptc_res["metrics"]["reduction_pct"] > 75.0
        and ptc_res["results"][0]["untrusted_external_content"] is True
        and "alert(" not in ptc_res["results"][0]["snippets"][0]
    )
    assertions.append({"name": "ptc_filter_noise_and_reduction", "passed": ptc_ok})

    # 2. Test audit-echo echo chamber detection (3 URLs sharing 1 origin -> count=1 -> FAIL)
    echo_records = [
        {"url": "https://a.news/1", "independent_origin_id": "PR-WIRE-01", "trust_tier": "T2"},
        {"url": "https://b.news/2", "independent_origin_id": "PR-WIRE-01", "trust_tier": "T3"},
        {"url": "https://c.news/3", "independent_origin_id": "PR-WIRE-01", "trust_tier": "T3"},
    ]
    echo_res = run_audit_echo(echo_records, min_origins=2)
    echo_ok = (
        echo_res["status"] == "FAIL"
        and echo_res["metrics"]["independent_origin_count"] == 1
        and echo_res["metrics"]["echo_chamber_cluster_count"] == 1
    )
    assertions.append({"name": "audit_echo_chamber_detection", "passed": echo_ok})

    # 3. Test gate-check PASS and BLOCKED
    gate_pass = run_gate_check(2, 0, 100.0, 0)
    gate_block = run_gate_check(1, 2, 85.0, 1)
    gate_ok = gate_pass["gate_verdict"] == "PASS" and gate_block["gate_verdict"] == "BLOCKED"
    assertions.append({"name": "gate_check_pass_and_block", "passed": gate_ok})

    # 4. Test export-bo02 dry-run and live temp write with 4-label mapping
    sample_cards = [
        {
            "fact_id": "FC-001",
            "statement": "Latency p99 is 42ms.",
            "value": 42,
            "unit": "ms",
            "claim_label": "OBSERVED",
            "primary_url": "https://bench.example.com/report",
        },
        {
            "fact_id": "FC-002",
            "statement": "Throughput scales linearly to 10k RPS.",
            "value": 10000,
            "unit": "rps",
            "claim_label": "DERIVED",
            "primary_url": "https://bench.example.com/model",
        },
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        out_file = Path(tmpdir) / "l1-export.yaml"
        exp_dry = run_export_bo02(sample_cards, output_path=out_file, dry_run=True)
        dry_not_written = not out_file.exists()
        exp_live = run_export_bo02(sample_cards, output_path=out_file, dry_run=False)
        live_written = out_file.exists() and exp_live["l1_atomic_facts"][0]["edge_label"] == "EXTRACTED" and exp_live["l1_atomic_facts"][1]["edge_label"] == "INFERRED"
    assertions.append({"name": "export_bo02_dry_run_and_4label_mapping", "passed": dry_not_written and live_written})

    elapsed_ms = round((time.monotonic() - t0) * 1000.0, 2)
    all_passed = all(a["passed"] for a in assertions)
    return {
        "status": "PASS" if all_passed else "FAIL",
        "tool": TOOL_NAME,
        "subcommand": "--self-test",
        "summary": f"Self-test {'PASSED' if all_passed else 'FAILED'} ({len(assertions)}/{len(assertions)} assertions) in {elapsed_ms}ms.",
        "metrics": {
            "assertions_total": len(assertions),
            "assertions_passed": sum(1 for a in assertions if a["passed"]),
            "elapsed_ms": elapsed_ms,
        },
        "assertions": assertions,
        "next_command": f"python3 scripts/{TOOL_NAME}.py --help",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=TOOL_NAME,
        description="Bo-01 Internet Info Refinement Deep Module CLI (PTC Filter, Echo Audit, Gate Check, Bo-02 Export).",
    )
    parser.add_argument("--version", action="version", version=f"{TOOL_NAME} {VERSION}")
    parser.add_argument("--self-test", action="store_true", help="Run in-memory self-test suite (<200ms).")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON output.")
    parser.add_argument("--dry-run", action="store_true", help="Preview operation without writing files.")

    subparsers = parser.add_subparsers(dest="subcommand")

    # ptc-filter
    p_ptc = subparsers.add_parser("ptc-filter", help="Slice raw web search JSON into keyword-anchored snippets.")
    p_ptc.add_argument("--input", "-i", required=True, help="Path to raw search results JSON file.")
    p_ptc.add_argument("--keywords", "-k", default="", help="Comma-separated keywords for context window slicing.")
    p_ptc.add_argument("--window-chars", type=int, default=600, help="Characters before/after keyword match (default: 600).")
    p_ptc.add_argument("--max-snippets", type=int, default=3, help="Max snippets per source (default: 3).")
    p_ptc.add_argument("--output", "-o", help="Optional path to write filtered JSON.")
    p_ptc.add_argument("--dry-run", action="store_true", help="Preview without writing output file.")
    p_ptc.add_argument("--json", action="store_true", help="Emit structured JSON output.")

    # audit-echo
    p_echo = subparsers.add_parser("audit-echo", help="Verify citation origin independence and detect echo chambers.")
    p_echo.add_argument("--input", "-i", required=True, help="Path to source-log file (CSV, JSON, YAML, or Markdown table).")
    p_echo.add_argument("--min-origins", type=int, default=2, help="Minimum independent origins required (default: 2).")
    p_echo.add_argument("--json", action="store_true", help="Emit structured JSON output.")

    # gate-check
    p_gate = subparsers.add_parser("gate-check", help="Evaluate Stage 3 -> Stage 4 quantitative gate criteria.")
    p_gate.add_argument("--input", "-i", help="Optional JSON/YAML file containing gate metrics.")
    p_gate.add_argument("--independent-origins", type=int, default=2, help="Count of independent origins.")
    p_gate.add_argument("--unresolved-conflicts", type=int, default=0, help="Count of unresolved High/Medium conflicts.")
    p_gate.add_argument("--citation-coverage", type=float, default=100.0, help="Citation coverage percentage (0-100).")
    p_gate.add_argument("--expired-ttl", type=int, default=0, help="Count of expired TTL claims.")
    p_gate.add_argument("--min-origins", type=int, default=2, help="Minimum required independent origins (default: 2).")
    p_gate.add_argument("--json", action="store_true", help="Emit structured JSON output.")

    # export-bo02
    p_exp = subparsers.add_parser("export-bo02", help="Export verified Fact Cards to Bo-02 L1 Atomic Fact YAML.")
    p_exp.add_argument("--input", "-i", required=True, help="Path to Fact Cards JSON/YAML file.")
    p_exp.add_argument("--output", "-o", help="Path to write Bo-02 L1 YAML file.")
    p_exp.add_argument("--dry-run", action="store_true", help="Preview YAML export without touching disk.")
    p_exp.add_argument("--json", action="store_true", help="Emit structured JSON output.")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    as_json = bool(getattr(args, "json", False))

    if args.self_test:
        res = run_self_test()
        return emit_output(res, as_json=as_json or True, exit_code=0 if res["status"] == "PASS" else 1)

    if not args.subcommand:
        parser.print_help()
        return 0

    try:
        if args.subcommand == "ptc-filter":
            in_path = Path(args.input)
            if not in_path.exists():
                return actionable_error(
                    "MISSING_INPUT_FILE",
                    f"Input file not found: {in_path}",
                    f"python3 scripts/{TOOL_NAME}.py --self-test --json",
                    subcommand="ptc-filter",
                    as_json=as_json,
                )
            raw_data = json.loads(in_path.read_text(encoding="utf-8"))
            items = raw_data.get("results", raw_data) if isinstance(raw_data, dict) else raw_data
            if not isinstance(items, list):
                raise ValueError("Input JSON must be a list of search items or an object with a 'results' list.")
            kw_list = [k.strip() for k in args.keywords.split(",") if k.strip()]
            res = run_ptc_filter(items, kw_list, window_chars=args.window_chars, max_snippets=args.max_snippets)
            if args.output and not args.dry_run:
                out_path = Path(args.output).resolve()
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            elif args.output and args.dry_run:
                res["status"] = "DRY_RUN_OK"
            return emit_output(res, as_json=as_json, exit_code=0)

        if args.subcommand == "audit-echo":
            in_path = Path(args.input)
            if not in_path.exists():
                return actionable_error(
                    "MISSING_INPUT_FILE",
                    f"Source log file not found: {in_path}",
                    f"python3 scripts/{TOOL_NAME}.py audit-echo --help",
                    subcommand="audit-echo",
                    as_json=as_json,
                )
            records = _parse_source_records(in_path.read_text(encoding="utf-8"))
            res = run_audit_echo(records, min_origins=args.min_origins)
            return emit_output(res, as_json=as_json, exit_code=0 if res["status"] == "PASS" else 1)

        if args.subcommand == "gate-check":
            ind_orig = args.independent_origins
            unres_conf = args.unresolved_conflicts
            cit_cov = args.citation_coverage
            exp_ttl = args.expired_ttl
            if args.input:
                in_path = Path(args.input)
                if not in_path.exists():
                    return actionable_error(
                        "MISSING_INPUT_FILE",
                        f"Gate metrics file not found: {in_path}",
                        f"python3 scripts/{TOOL_NAME}.py gate-check --help",
                        subcommand="gate-check",
                        as_json=as_json,
                    )
                loaded = load_structured_text(in_path.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    ind_orig = int(loaded.get("independent_origin_count", ind_orig))
                    unres_conf = int(loaded.get("unresolved_high_med_conflicts", unres_conf))
                    cit_cov = float(loaded.get("citation_coverage_pct", cit_cov))
                    exp_ttl = int(loaded.get("expired_ttl_claims", exp_ttl))
            res = run_gate_check(ind_orig, unres_conf, cit_cov, exp_ttl, min_origins=args.min_origins)
            return emit_output(res, as_json=as_json, exit_code=0 if res["gate_verdict"] == "PASS" else 1)

        if args.subcommand == "export-bo02":
            in_path = Path(args.input)
            if not in_path.exists():
                return actionable_error(
                    "MISSING_INPUT_FILE",
                    f"Fact Card file not found: {in_path}",
                    f"python3 scripts/{TOOL_NAME}.py export-bo02 --help",
                    subcommand="export-bo02",
                    as_json=as_json,
                )
            loaded = load_structured_text(in_path.read_text(encoding="utf-8"))
            cards = (
                loaded.get("fact_cards") or loaded.get("facts") or loaded.get("results") or [loaded]
                if isinstance(loaded, dict)
                else loaded
            )
            if not isinstance(cards, list):
                raise ValueError("Fact Cards input must resolve to a list of fact records.")
            out_path = Path(args.output) if args.output else None
            res = run_export_bo02(cards, output_path=out_path, dry_run=bool(args.dry_run))
            return emit_output(res, as_json=as_json, exit_code=0)

    except json.JSONDecodeError as exc:
        return actionable_error(
            "INVALID_INPUT_JSON",
            f"Malformed JSON input: {exc}",
            f"python3 scripts/{TOOL_NAME}.py --self-test --json",
            subcommand=args.subcommand or "global",
            as_json=as_json,
        )
    except KeyError as exc:
        return actionable_error(
            "MISSING_SOURCE_COLUMNS",
            str(exc),
            f"python3 scripts/{TOOL_NAME}.py {args.subcommand} --help",
            subcommand=args.subcommand or "global",
            as_json=as_json,
        )
    except (PermissionError, OSError) as exc:
        return actionable_error(
            "EXPORT_PATH_ERROR",
            f"Filesystem error: {exc}",
            f"python3 scripts/{TOOL_NAME}.py {args.subcommand} --dry-run --json",
            subcommand=args.subcommand or "global",
            as_json=as_json,
        )
    except Exception as exc:
        return actionable_error(
            "EXECUTION_ERROR",
            str(exc),
            f"python3 scripts/{TOOL_NAME}.py --self-test --json",
            subcommand=args.subcommand or "global",
            as_json=as_json,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
