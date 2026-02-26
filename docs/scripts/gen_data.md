# gen_data.py

Purpose
- Generate random integer data for use with the CLI, tests, or benchmarks.

Functions
- `main(path, count, lo, hi)`: write `count` random integers in [lo, hi] to `path`.
- `generate_data(count, lo, hi) -> List[int]`: return a list of random integers (useful for in-memory usage such as tests).

Usage
- From the command line (writes `data.txt` by default):

```bash
python scripts/gen_data.py -n 1000 --min 0 --max 1000000 -o data.txt
```

Or use the helper from Python code:

```python
from scripts.gen_data import generate_data
data = generate_data(count=200, lo=-1000, hi=1000)
```

Notes
- The script seeds the RNG with the system time by default; tests can seed explicitly for deterministic behavior.
