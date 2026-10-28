#!/usr/bin/env python3
"""Bo-02 Kernel Registry SOT Deep Module CLI Tool.

Provides deterministic, zero-dependency Python stdlib utilities for:
1. fingerprint: Capture ORIGINAL_TREE_FINGERPRINT SHA-256 across a document/registry tree.
2. audit-freshness: Verify SHA-256 source hashes & TTL for L1 facts and propagate STALE to L2/L3.
3. eval-l2: Compute L2 derived facts via a strict AST Safe Math Evaluator (0% raw eval()).
4. sync-feature-map: Synchronize L1/L2/L3 SOT records and hashes with Bo-03 Feature Map.
5. --self-test: In-memory verification suite (<200ms) including AST security tests.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
import operator
import os
import re
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

TOOL_NAME = "bo02_registry_tool"
VERSION = "2.1.0"

IGNORED_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "_Archive", "_Delete"}
IGNORED_FILES = {".DS_Store"}

SAFE_BINARY_OPS: Dict[type, Callable[[Any, Any], Any]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

SAFE_UNARY_OPS: Dict[type, Callable[[Any], Any]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

SAFE_FUNCTIONS: Dict[str, Callable[..., Any]] = {
    "min": min,
    "max": max,
    "round": round,
    "sum": sum,
    "abs": abs,
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


def sha256_file_stream(path: Path) -> str:
    """Compute SHA-256 hex digest of a file using 64KB streaming chunks."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def dump_yaml_compat(data: Any) -> str:
    """Serialize data to clean YAML using PyYAML if available, else stdlib emitter."""
    try:
        import yaml  # type: ignore

        return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    except Exception:
        return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def load_structured_text(raw: str) -> Any:
    """Parse JSON or YAML text using stdlib JSON first, then PyYAML, then stdlib fallback."""
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
    return _stdlib_parse_nested_yaml(stripped)


def _stdlib_parse_nested_yaml(text: str) -> Dict[str, Any]:
    """Minimal indentation-aware YAML parser for L1/L2 template structures."""
    result: Dict[str, Any] = {}
    current_section: Optional[str] = None
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.strip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if indent == 0 and ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()
            if "#" in v and not (v.startswith('"') or v.startswith("'")):
                v = v.split("#", 1)[0].strip()
            if not v:
                result[k] = {}
                current_section = k
            else:
                result[k] = _parse_scalar(v)
                current_section = None
        elif indent > 0 and current_section is not None:
            sec = result.get(current_section)
            if line.startswith("- "):
                val = _parse_scalar(line[2:].strip())
                if isinstance(sec, dict) and not sec:
                    result[current_section] = [val]
                elif isinstance(result[current_section], list):
                    result[current_section].append(val)
                elif isinstance(sec, dict) and "inputs" in sec and isinstance(sec["inputs"], list):
                    sec["inputs"].append(val)
            elif ":" in line and isinstance(sec, dict):
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip()
                if "#" in v and not (v.startswith('"') or v.startswith("'")):
                    v = v.split("#", 1)[0].strip()
                if not v and k == "inputs":
                    sec[k] = []
                else:
                    sec[k] = _parse_scalar(v)
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
    try:
        if "." in val:
            return float(val)
        return int(val)
    except ValueError:
        return val


def safe_eval_math_ast(expression: str, variables: Dict[str, float]) -> float:
    """Evaluate an arithmetic expression strictly via AST whitelist (0% raw eval)."""
    if not expression or not expression.strip():
        raise ValueError("Formula expression cannot be empty.")

    # Normalize hyphenated L1 IDs (e.g. L1-rev-01 -> L1_rev_01) when matching known variables
    normalized_expr = expression
    norm_vars: Dict[str, float] = {}
    for k, v in sorted(variables.items(), key=lambda item: len(str(item[0])), reverse=True):
        safe_key = re.sub(r"[^A-Za-z0-9_]", "_", k)
        norm_vars[safe_key] = float(v)
        norm_vars[k] = float(v)
        if "-" in k and k in normalized_expr:
            normalized_expr = normalized_expr.replace(k, safe_key)

    try:
        tree = ast.parse(normalized_expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid formula syntax '{expression}': {exc}") from exc

    def _eval_node(node: ast.AST) -> Any:
        if isinstance(node, ast.Expression):
            return _eval_node(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                return float(node.value)
            raise ValueError(f"Unsupported constant type in formula: {type(node.value).__name__}")
        if isinstance(node, ast.Name):
            if node.id in norm_vars:
                return norm_vars[node.id]
            raise KeyError(f"Unknown or missing L1 input variable in formula: '{node.id}'")
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in SAFE_BINARY_OPS:
                raise ValueError(f"Disallowed binary operator: {op_type.__name__}")
            left_val = _eval_node(node.left)
            right_val = _eval_node(node.right)
            if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right_val == 0:
                raise ZeroDivisionError(f"Division by zero in formula '{expression}'.")
            return float(SAFE_BINARY_OPS[op_type](left_val, right_val))
        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in SAFE_UNARY_OPS:
                raise ValueError(f"Disallowed unary operator: {op_type.__name__}")
            return float(SAFE_UNARY_OPS[op_type](_eval_node(node.operand)))
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in SAFE_FUNCTIONS:
                func_name = getattr(node.func, "id", type(node.func).__name__)
                raise ValueError(f"Disallowed function call in formula: '{func_name}'")
            if node.keywords:
                raise ValueError("Keyword arguments are not permitted in L2 math formulas.")
            args = [_eval_node(arg) for arg in node.args]
            if node.func.id == "sum" and len(args) > 1:
                return float(sum(args))
            return float(SAFE_FUNCTIONS[node.func.id](*args))
        if isinstance(node, (ast.List, ast.Tuple)):
            return [_eval_node(elt) for elt in node.elts]
        raise ValueError(f"Disallowed AST node in formula: {type(node).__name__}")

    return float(_eval_node(tree))


def run_fingerprint(target_dir: Path) -> Dict[str, Any]:
    """Compute deterministic ORIGINAL_TREE_FINGERPRINT SHA-256 across all files in target_dir."""
    if not target_dir.exists() or not target_dir.is_dir():
        raise FileNotFoundError(f"Target directory does not exist: {target_dir}")

    file_hashes: List[Dict[str, str]] = []
    manifest_lines: List[str] = []

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIRS)
        for fname in sorted(files):
            if fname in IGNORED_FILES or fname.endswith(".pyc"):
                continue
            fpath = Path(root) / fname
            rel_path = fpath.relative_to(target_dir).as_posix()
            digest = sha256_file_stream(fpath)
            file_hashes.append({"path": rel_path, "sha256": f"sha256:{digest}"})
            manifest_lines.append(f"{digest}  {rel_path}")

    tree_digest = hashlib.sha256("\n".join(manifest_lines).encode("utf-8")).hexdigest()
    return {
        "status": "OK",
        "tool": TOOL_NAME,
        "subcommand": "fingerprint",
        "summary": f"Computed ORIGINAL_TREE_FINGERPRINT across {len(file_hashes)} file(s).",
        "original_tree_fingerprint": f"sha256:{tree_digest}",
        "metrics": {
            "files_hashed": len(file_hashes),
            "target_dir": str(target_dir.resolve()),
        },
        "files": file_hashes,
        "next_command": f"python3 scripts/{TOOL_NAME}.py audit-freshness --help",
    }


def run_audit_freshness(
    l1_records: List[Dict[str, Any]],
    base_dir: Path,
    dep_rows: Optional[List[Dict[str, str]]] = None,
    reference_date: Optional[str] = None,
) -> Dict[str, Any]:
    """Audit L1 source file SHA-256 hashes & expiration dates, and propagate STALE to L2/L3."""
    today_str = reference_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    audited: List[Dict[str, Any]] = []
    stale_ids: Set[str] = set()
    fresh_count = 0
    stale_count = 0
    expired_count = 0

    for rec in l1_records:
        fact_id = str(rec.get("fact_id") or rec.get("id") or "UNKNOWN")
        src_block = rec.get("source") if isinstance(rec.get("source"), dict) else {}
        doc_path_str = str(
            src_block.get("document_path")
            or rec.get("source_locator")
            or ""
        ).strip()
        expected_hash = str(
            src_block.get("source_hash")
            or rec.get("source_hash")
            or ""
        ).strip()
        date_expires = str(rec.get("date_expires") or "").strip()

        status = "FRESH"
        reason = "Source hash verified and within validity window."

        if date_expires and re.match(r"^\d{4}-\d{2}-\d{2}$", date_expires):
            if date_expires < today_str:
                status = "EXPIRED"
                reason = f"date_expires ({date_expires}) < current date ({today_str})"

        if status == "FRESH" and doc_path_str and not doc_path_str.startswith(("http://", "https://", "source://")):
            candidate_path = (base_dir / doc_path_str).resolve()
            if not candidate_path.exists():
                status = "STALE"
                reason = "MISSING_SOURCE_FILE"
            elif expected_hash:
                actual_hex = sha256_file_stream(candidate_path)
                expected_hex = expected_hash.replace("sha256:", "")
                if not actual_hex.startswith(expected_hex):
                    status = "STALE"
                    reason = f"SOURCE_HASH_MISMATCH (expected {expected_hex[:12]}..., got {actual_hex[:12]}...)"

        if status == "FRESH":
            fresh_count += 1
        elif status == "EXPIRED":
            expired_count += 1
            stale_ids.add(fact_id)
        else:
            stale_count += 1
            stale_ids.add(fact_id)

        audited.append(
            {
                "fact_id": fact_id,
                "verification_status": status,
                "freshness": status,
                "reason": reason,
                "document_path": doc_path_str,
            }
        )

    # Propagate STALE/EXPIRED along dependency-index.csv edges
    propagated_dependents: List[Dict[str, str]] = []
    if dep_rows and stale_ids:
        changed = True
        while changed:
            changed = False
            for row in dep_rows:
                from_id = str(row.get("from_id") or "").strip()
                to_id = str(row.get("to_id") or "").strip()
                rel = str(row.get("relationship") or "derives-from").strip()
                impact = str(row.get("impact_if_stale") or "recompute-l2").strip()
                if to_id in stale_ids and from_id and from_id not in stale_ids:
                    stale_ids.add(from_id)
                    propagated_dependents.append(
                        {
                            "dependent_id": from_id,
                            "stale_upstream_id": to_id,
                            "relationship": rel,
                            "required_action": impact,
                        }
                    )
                    changed = True

    overall = "FRESH" if (stale_count == 0 and expired_count == 0) else "STALE"
    return {
        "status": overall,
        "tool": TOOL_NAME,
        "subcommand": "audit-freshness",
        "summary": (
            f"Audited {len(l1_records)} L1 record(s): {fresh_count} FRESH, {stale_count} STALE, "
            f"{expired_count} EXPIRED; propagated to {len(propagated_dependents)} downstream L2/L3/Skill item(s)."
        ),
        "metrics": {
            "total_l1": len(l1_records),
            "fresh_count": fresh_count,
            "stale_count": stale_count,
            "expired_count": expired_count,
            "propagated_dependents_count": len(propagated_dependents),
        },
        "audited_records": audited,
        "propagated_dependents": propagated_dependents,
        "next_command": (
            f"python3 scripts/{TOOL_NAME}.py eval-l2 --help"
            if overall == "FRESH"
            else f"python3 scripts/{TOOL_NAME}.py sync-feature-map --dry-run --json"
        ),
    }


def run_eval_l2(
    l2_record: Dict[str, Any],
    l1_lookup: Dict[str, Dict[str, Any]],
    tolerance: float = 1e-6,
    output_path: Optional[Path] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Deterministically evaluate an L2 Derived Fact from L1 inputs using AST Safe Math."""
    fact_id = str(l2_record.get("fact_id") or l2_record.get("id") or "L2-UNKNOWN")
    formula_block = l2_record.get("formula")
    if isinstance(formula_block, dict):
        expression = str(formula_block.get("expression") or "")
        declared_inputs = list(formula_block.get("inputs") or [])
    else:
        expression = str(formula_block or l2_record.get("expression") or "")
        declared_inputs = list(l2_record.get("inputs") or [])

    if not expression:
        raise ValueError(f"L2 record '{fact_id}' is missing formula.expression.")

    variables: Dict[str, float] = {}
    input_hashes: Dict[str, str] = {}
    stale_inputs: List[str] = []

    for inp_id, inp_rec in l1_lookup.items():
        val = inp_rec.get("value")
        if val is not None:
            variables[inp_id] = float(val)
        src_block = inp_rec.get("source") if isinstance(inp_rec.get("source"), dict) else {}
        h_val = str(src_block.get("source_hash") or inp_rec.get("source_hash") or "sha256:unknown")
        input_hashes[inp_id] = h_val
        v_status = str(inp_rec.get("verification_status") or inp_rec.get("freshness") or "FRESH").upper()
        if v_status != "FRESH":
            stale_inputs.append(inp_id)

    for req_id in declared_inputs:
        req_str = str(req_id)
        if req_str not in variables and req_str.replace("-", "_") not in variables:
            raise KeyError(f"Required L1 input '{req_str}' for '{fact_id}' not found in L1 lookup.")

    computed_value = safe_eval_math_ast(expression, variables)
    if computed_value.is_integer():
        computed_out: Any = int(computed_value)
    else:
        computed_out = round(computed_value, 6)

    cache_block = l2_record.get("computed_cache") if isinstance(l2_record.get("computed_cache"), dict) else {}
    cached_val = cache_block.get("last_computed_value", l2_record.get("value"))
    drift_detected = False
    if cached_val is not None:
        drift_detected = abs(float(computed_value) - float(cached_val)) > tolerance

    derived_status = "STALE_DEPENDENCY" if stale_inputs else "FRESH"
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    assignment_str = ", ".join(f"{k}={v}" for k, v in sorted(variables.items()) if not declared_inputs or k in declared_inputs)
    audit_trace = f"{expression} [{assignment_str}] = {computed_out}"

    updated_record = dict(l2_record)
    updated_record["verification_status"] = derived_status
    updated_record["computed_cache"] = {
        "last_computed_value": computed_out,
        "unit": cache_block.get("unit") or l2_record.get("unit") or "scalar",
        "computed_at": now_iso,
        "input_hashes": {k: input_hashes[k] for k in declared_inputs if k in input_hashes} or input_hashes,
        "audit_trace": audit_trace,
    }

    if output_path and not dry_run:
        resolved = output_path.resolve()
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(dump_yaml_compat(updated_record), encoding="utf-8")

    return {
        "status": "DRY_RUN_OK" if dry_run else ("STALE" if stale_inputs else "OK"),
        "tool": TOOL_NAME,
        "subcommand": "eval-l2",
        "fact_id": fact_id,
        "summary": (
            f"Evaluated {fact_id}: {audit_trace} "
            f"(status={derived_status}, drift_detected={drift_detected})."
        ),
        "metrics": {
            "computed_value": computed_out,
            "previous_cached_value": cached_val,
            "drift_detected": drift_detected,
            "derived_freshness": derived_status,
            "stale_inputs": stale_inputs,
        },
        "audit_trace": audit_trace,
        "updated_l2_record": updated_record,
        "next_command": f"python3 scripts/{TOOL_NAME}.py sync-feature-map --dry-run --json",
    }


def run_sync_feature_map(
    sot_records: List[Dict[str, Any]],
    feature_map_path: Optional[Path] = None,
    dry_run: bool = True,
) -> Dict[str, Any]:
    """Synchronize Bo-02 SOT records (L1/L2/L3) with Bo-03 Feature Map."""
    stale_sot = [
        str(r.get("fact_id") or r.get("id"))
        for r in sot_records
        if str(r.get("verification_status") or r.get("freshness") or "FRESH").upper() != "FRESH"
    ]
    sync_entries: List[Dict[str, str]] = []
    for r in sot_records:
        fid = str(r.get("fact_id") or r.get("id") or "SOT-ITEM")
        vstat = str(r.get("verification_status") or r.get("freshness") or "FRESH").upper()
        src = r.get("source") if isinstance(r.get("source"), dict) else {}
        shash = str(src.get("source_hash") or r.get("source_hash") or "sha256:computed")
        sync_entries.append(
            {
                "sot_id": fid,
                "layer": str(r.get("fact_type") or r.get("layer") or "L1"),
                "verification_status": vstat,
                "source_hash": shash,
                "bo03_gate_impact": "BLOCK_RELEASE_AND_REVERIFY" if vstat != "FRESH" else "READY_FOR_SPEC",
            }
        )

    if feature_map_path and not dry_run:
        resolved = feature_map_path.resolve()
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(json.dumps({"sot_feature_bridge": sync_entries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "status": "DRY_RUN_OK" if dry_run else ("STALE" if stale_sot else "OK"),
        "tool": TOOL_NAME,
        "subcommand": "sync-feature-map",
        "summary": (
            f"Synchronized {len(sync_entries)} SOT record(s) with Bo-03 Feature Map "
            f"({len(stale_sot)} STALE/EXPIRED item(s) flagged)."
        ),
        "metrics": {
            "total_synced": len(sync_entries),
            "stale_flagged": len(stale_sot),
            "dry_run": dry_run,
        },
        "sot_feature_bridge": sync_entries,
        "next_command": "python3 ../Bo-03-Vibecode-Kit-v6/scripts/bo03_vibecode_tool.py maintain-features --help",
    }


def _load_dep_csv(path: Path) -> List[Dict[str, str]]:
    lines = [
        ln for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    if not lines:
        return []
    reader = csv.DictReader(io.StringIO("\n".join(lines)))
    return [dict(r) for r in reader]


def run_self_test() -> Dict[str, Any]:
    """Run in-memory verification suite (<200ms) including AST security tests."""
    t0 = time.monotonic()
    assertions: List[Dict[str, Any]] = []

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        doc_a = tmp_path / "pricing.txt"
        doc_a.write_text("Product A Q4 Revenue = 150000000 VND\n", encoding="utf-8")
        hash_a = sha256_file_stream(doc_a)

        # 1. Test fingerprint determinism
        fp1 = run_fingerprint(tmp_path)
        fp2 = run_fingerprint(tmp_path)
        fp_ok = (
            fp1["status"] == "OK"
            and fp1["original_tree_fingerprint"] == fp2["original_tree_fingerprint"]
            and fp1["metrics"]["files_hashed"] == 1
        )
        assertions.append({"name": "tree_fingerprint_determinism", "passed": fp_ok})

        # 2. Test freshness audit & STALE propagation across dependency-index
        l1_list = [
            {
                "fact_id": "L1-rev-A",
                "value": 150000000,
                "source": {"document_path": "pricing.txt", "source_hash": f"sha256:{hash_a}"},
                "date_expires": "2099-12-31",
            }
        ]
        dep_edges = [
            {
                "from_id": "L2-total-rev",
                "to_id": "L1-rev-A",
                "relationship": "derives-from",
                "impact_if_stale": "recompute-l2",
            }
        ]
        fresh_res = run_audit_freshness(l1_list, tmp_path, dep_edges, reference_date="2026-10-28")
        # Modify source file to trigger STALE propagation
        doc_a.write_text("Product A Q4 Revenue = 180000000 VND (edited)\n", encoding="utf-8")
        stale_res = run_audit_freshness(l1_list, tmp_path, dep_edges, reference_date="2026-10-28")
        audit_ok = (
            fresh_res["status"] == "FRESH"
            and stale_res["status"] == "STALE"
            and len(stale_res["propagated_dependents"]) == 1
            and stale_res["propagated_dependents"][0]["dependent_id"] == "L2-total-rev"
        )
        assertions.append({"name": "freshness_audit_and_stale_propagation", "passed": audit_ok})

        # 3. Test AST Safe L2 Evaluator (valid math PASS)
        l2_sample = {
            "fact_id": "L2-total-rev",
            "formula": {
                "type": "sum",
                "expression": "L1-rev-A + L1-rev-B",
                "inputs": ["L1-rev-A", "L1-rev-B"],
            },
            "computed_cache": {"last_computed_value": 360000000, "unit": "VND"},
        }
        l1_map = {
            "L1-rev-A": {"value": 150000000, "verification_status": "FRESH", "source_hash": "sha256:111"},
            "L1-rev-B": {"value": 210000000, "verification_status": "FRESH", "source_hash": "sha256:222"},
        }
        eval_res = run_eval_l2(l2_sample, l1_map, dry_run=True)
        eval_ok = (
            eval_res["metrics"]["computed_value"] == 360000000
            and eval_res["metrics"]["drift_detected"] is False
        )
        assertions.append({"name": "eval_l2_deterministic_math", "passed": eval_ok})

        # 4. Test AST Safe Evaluator blocks unsafe code execution (__import__)
        unsafe_blocked = False
        try:
            safe_eval_math_ast("__import__('os').system('id')", {})
        except ValueError:
            unsafe_blocked = True
        assertions.append({"name": "ast_whitelist_blocks_arbitrary_code", "passed": unsafe_blocked})

        # 5. Test sync-feature-map
        sync_res = run_sync_feature_map([{"fact_id": "L2-total-rev", "verification_status": "FRESH"}], dry_run=True)
        assertions.append({"name": "sync_feature_map_bridge", "passed": sync_res["status"] == "DRY_RUN_OK"})

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
        description="Bo-02 Kernel Registry SOT Deep Module CLI (Fingerprint, Freshness Audit, AST Safe eval-l2, Feature Map Sync).",
    )
    parser.add_argument("--version", action="version", version=f"{TOOL_NAME} {VERSION}")
    parser.add_argument("--self-test", action="store_true", help="Run in-memory self-test suite (<200ms).")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON output.")
    parser.add_argument("--dry-run", action="store_true", help="Preview operation without writing files.")

    subparsers = parser.add_subparsers(dest="subcommand")

    # fingerprint
    p_fp = subparsers.add_parser("fingerprint", help="Compute ORIGINAL_TREE_FINGERPRINT SHA-256 across a directory.")
    p_fp.add_argument("--dir", "-d", default=".", help="Target directory to fingerprint (default: current directory).")
    p_fp.add_argument("--json", action="store_true", help="Emit structured JSON output.")

    # audit-freshness
    p_af = subparsers.add_parser("audit-freshness", help="Audit L1 SHA-256 hashes & expiration and propagate STALE across dependency-index.csv.")
    p_af.add_argument("--l1-file", "-i", required=True, help="Path to L1 YAML/JSON file or directory of L1 files.")
    p_af.add_argument("--base-dir", "-b", default=".", help="Base directory for resolving relative document_path values.")
    p_af.add_argument("--dependency-index", "-d", help="Optional path to dependency-index.csv for STALE propagation.")
    p_af.add_argument("--json", action="store_true", help="Emit structured JSON output.")

    # eval-l2
    p_l2 = subparsers.add_parser("eval-l2", help="Deterministically compute L2 Derived Fact via AST Safe Math Evaluator.")
    p_l2.add_argument("--id", help="Fact ID of the L2 derived fact (e.g. L2-domain-key-001).")
    p_l2.add_argument("--l2-file", help="Path to L2 YAML/JSON file (defaults to templates/L2-derived-fact.yaml if present).")
    p_l2.add_argument("--l1-file", help="Optional path to L1 inputs YAML/JSON file.")
    p_l2.add_argument("--vars", help="Optional inline JSON object of L1 input values, e.g. '{\"L1_input_1\": 100}'.")
    p_l2.add_argument("--output", "-o", help="Optional path to write updated L2 record.")
    p_l2.add_argument("--dry-run", action="store_true", help="Preview evaluation without writing to disk.")
    p_l2.add_argument("--json", action="store_true", help="Emit structured JSON output.")

    # sync-feature-map
    p_sync = subparsers.add_parser("sync-feature-map", help="Synchronize L1/L2/L3 SOT status with Bo-03 Feature Map.")
    p_sync.add_argument("--input", "-i", required=True, help="Path to SOT records YAML/JSON file.")
    p_sync.add_argument("--output", "-o", help="Optional path to write bridge JSON.")
    p_sync.add_argument("--dry-run", action="store_true", help="Preview sync without writing files.")
    p_sync.add_argument("--json", action="store_true", help="Emit structured JSON output.")

    return parser


def _load_records_from_path(path: Path) -> List[Dict[str, Any]]:
    if path.is_dir():
        records: List[Dict[str, Any]] = []
        for fpath in sorted(path.glob("*.y*ml")) + sorted(path.glob("*.json")):
            loaded = load_structured_text(fpath.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                if "l1_atomic_facts" in loaded and isinstance(loaded["l1_atomic_facts"], list):
                    records.extend(loaded["l1_atomic_facts"])
                else:
                    records.append(loaded)
            elif isinstance(loaded, list):
                records.extend(loaded)
        return records
    loaded = load_structured_text(path.read_text(encoding="utf-8"))
    if isinstance(loaded, list):
        return loaded
    if isinstance(loaded, dict):
        for key in ("l1_atomic_facts", "records", "facts", "sot_records"):
            if key in loaded and isinstance(loaded[key], list):
                return loaded[key]
        return [loaded]
    return []


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
        if args.subcommand == "fingerprint":
            res = run_fingerprint(Path(args.dir))
            return emit_output(res, as_json=as_json, exit_code=0)

        if args.subcommand == "audit-freshness":
            l1_path = Path(args.l1_file)
            if not l1_path.exists():
                return actionable_error(
                    "MISSING_L1_INPUT",
                    f"L1 path does not exist: {l1_path}",
                    f"python3 scripts/{TOOL_NAME}.py --self-test --json",
                    subcommand="audit-freshness",
                    as_json=as_json,
                )
            l1_records = _load_records_from_path(l1_path)
            dep_rows = None
            if args.dependency_index:
                dep_path = Path(args.dependency_index)
                if dep_path.exists():
                    dep_rows = _load_dep_csv(dep_path)
            res = run_audit_freshness(l1_records, Path(args.base_dir), dep_rows=dep_rows)
            return emit_output(res, as_json=as_json, exit_code=0 if res["status"] == "FRESH" else 1)

        if args.subcommand == "eval-l2":
            l2_path: Optional[Path] = Path(args.l2_file) if args.l2_file else None
            if not l2_path:
                default_tpl = Path(__file__).resolve().parent.parent / "templates" / "L2-derived-fact.yaml"
                if default_tpl.exists():
                    l2_path = default_tpl
            if not l2_path or not l2_path.exists():
                return actionable_error(
                    "MISSING_L2_FILE",
                    f"L2 file not found: {l2_path}",
                    f"python3 scripts/{TOOL_NAME}.py eval-l2 --help",
                    subcommand="eval-l2",
                    as_json=as_json,
                )
            l2_loaded = load_structured_text(l2_path.read_text(encoding="utf-8"))
            if isinstance(l2_loaded, list):
                target_id = args.id
                matched = [r for r in l2_loaded if str(r.get("fact_id") or r.get("id")) == target_id] if target_id else l2_loaded
                if not matched:
                    raise KeyError(f"L2 fact_id '{target_id}' not found in {l2_path}.")
                l2_rec = matched[0]
            elif isinstance(l2_loaded, dict):
                l2_rec = l2_loaded
                if args.id:
                    l2_rec["fact_id"] = args.id
            else:
                raise ValueError(f"Could not parse L2 record from {l2_path}.")

            l1_lookup: Dict[str, Dict[str, Any]] = {}
            if args.l1_file:
                l1_p = Path(args.l1_file)
                if not l1_p.exists():
                    return actionable_error(
                        "MISSING_L1_FILE",
                        f"L1 input file not found: {l1_p}",
                        f"python3 scripts/{TOOL_NAME}.py eval-l2 --help",
                        subcommand="eval-l2",
                        as_json=as_json,
                    )
                for rec in _load_records_from_path(l1_p):
                    fid = str(rec.get("fact_id") or rec.get("id") or "")
                    if fid:
                        l1_lookup[fid] = rec
            if args.vars:
                raw_vars = json.loads(args.vars)
                for k, v in raw_vars.items():
                    l1_lookup[str(k)] = {"fact_id": str(k), "value": float(v), "verification_status": "FRESH"}

            # If running against template with default sample values and no explicit L1 file provided, populate template demo defaults
            if not l1_lookup and l2_path.name == "L2-derived-fact.yaml":
                l1_lookup = {
                    "L1_input_1": {"value": 150000000, "verification_status": "FRESH", "source_hash": "sha256:1a2b3c4d"},
                    "L1_input_2": {"value": 210000000, "verification_status": "FRESH", "source_hash": "sha256:5e6f7a8b"},
                    "L1_input_3": {"value": 125000000, "verification_status": "FRESH", "source_hash": "sha256:9c0d1e2f"},
                    "L1-domain-input-1": {"value": 150000000, "verification_status": "FRESH", "source_hash": "sha256:1a2b3c4d"},
                    "L1-domain-input-2": {"value": 210000000, "verification_status": "FRESH", "source_hash": "sha256:5e6f7a8b"},
                    "L1-domain-input-3": {"value": 125000000, "verification_status": "FRESH", "source_hash": "sha256:9c0d1e2f"},
                }

            out_path = Path(args.output) if args.output else None
            res = run_eval_l2(l2_rec, l1_lookup, output_path=out_path, dry_run=bool(args.dry_run))
            return emit_output(res, as_json=as_json, exit_code=0)

        if args.subcommand == "sync-feature-map":
            in_path = Path(args.input)
            if not in_path.exists():
                return actionable_error(
                    "MISSING_SOT_INPUT",
                    f"SOT input file not found: {in_path}",
                    f"python3 scripts/{TOOL_NAME}.py sync-feature-map --help",
                    subcommand="sync-feature-map",
                    as_json=as_json,
                )
            sot_records = _load_records_from_path(in_path)
            out_path = Path(args.output) if args.output else None
            res = run_sync_feature_map(sot_records, feature_map_path=out_path, dry_run=bool(args.dry_run))
            return emit_output(res, as_json=as_json, exit_code=0)

    except (SyntaxError, ZeroDivisionError, ValueError, KeyError) as exc:
        return actionable_error(
            "UNSAFE_OR_INVALID_FORMULA",
            str(exc),
            f"python3 scripts/{TOOL_NAME}.py {args.subcommand or '--self-test'} --help",
            subcommand=args.subcommand or "global",
            as_json=as_json,
        )
    except FileNotFoundError as exc:
        return actionable_error(
            "FILE_NOT_FOUND",
            str(exc),
            f"python3 scripts/{TOOL_NAME}.py --self-test --json",
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
