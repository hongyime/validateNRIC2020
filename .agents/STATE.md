# Validate NRIC 2020

Updated 2026-09-16 SGT. Baseline triage by Sisyphus-Junior.

## Current State
- HEAD: 7ef12bb (chore(deps): bump actions/setup-python from 6 to 7 #80)
- Branch: master, clean, synced with origin
- Stack: Python / Flask 3.1.3, python-barcode 0.16.1, Pillow 12.3.0
- Open PRs: 0  |  Open Issues: 0
- Secrets scan: clean  |  npm audit: N/A

## Issue Found
- `__pycache__/` and `*.pyc` missing from .gitignore — compiled Python files were tracked
  and caused `git pull` to block. Fix PR opened: fix/validateNRIC2020-baseline-20260916

## Next
- Merge fix PR to keep working tree clean

## Privacy maintenance - 2026-09-27

Remove the optional personal security contact while retaining private vulnerability-reporting guidance. The narrow documentation patch is prepared from the current default branch; staged whitespace and the inherited identity hook are publication checks. Application behavior is unchanged.
