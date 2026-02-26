import os
import sys

# Ensure the project's `src` directory is on sys.path for imports during tests.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
# Also ensure the repository root is on sys.path so top-level helper packages
# (e.g. `scripts`) can be imported during CI runs.
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
