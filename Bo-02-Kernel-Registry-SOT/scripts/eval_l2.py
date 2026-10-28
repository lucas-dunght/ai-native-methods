#!/usr/bin/env python3
"""Backward-compatible CLI entrypoint for L2 Derived Fact evaluation.

Delegates directly to `bo02_registry_tool.py eval-l2` (or `--self-test` / `--help`)
so `python3 scripts/eval_l2.py --id L2-domain-key-NNN` works out of the box.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bo02_registry_tool  # noqa: E402


def main() -> int:
    argv = sys.argv[1:]
    if "--self-test" in argv or "--version" in argv:
        return bo02_registry_tool.main(argv)
    if not argv or argv[0] != "eval-l2":
        argv = ["eval-l2"] + argv
    return bo02_registry_tool.main(argv)


if __name__ == "__main__":
    sys.exit(main())
