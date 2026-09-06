#!/usr/bin/env python3
"""Run actual author/CI software checks; never certify independent acceptance."""
from __future__ import annotations
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import unittest

from check_docs import check_docs
from create_demo import CASES, create_demo
from validate_demo import check_demo


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    suite = unittest.defaultTestLoader.discover(str(root / "tests"))
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(suite)
    docs = check_docs(root)
    demos = {}
    with tempfile.TemporaryDirectory(prefix="factory-fixture-check-") as directory:
        for case in CASES:
            target = Path(directory) / case
            create_demo(target, case)
            demos[case] = check_demo(target)
    try:
        sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, text=True,
          capture_output=True, check=True, timeout=10).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        sha = "NOT_AVAILABLE_SNAPSHOT_RUN"
    passed = result.wasSuccessful() and docs["status"] == "PASS" and all(
      item["status"] == "VALID" for item in demos.values())
    summary = {"status": "PASS" if passed else "FAIL", "scope": "AUTHOR_OR_CI_CHECKS_ONLY",
      "git_head": sha, "python": platform.python_version(), "platform": platform.system(),
      "tests": {"run": result.testsRun, "passed": result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),
                "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped)},
      "documentation": docs, "generated_variants": demos,
      "actual_fresh_agent_run": False, "independent_privacy_approved": False,
      "publication_authorized": False}
    print(json.dumps(summary, sort_keys=True, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
