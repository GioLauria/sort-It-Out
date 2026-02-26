import argparse
import random
import time
from typing import List


def main(
    path: str = "data.txt", count: int = 1000, lo: int = 0, hi: int = 1_000_000_000
) -> None:
    """Generate `count` random integers in range [lo, hi] and write to `path`.

    Defaults: 1000 numbers between 0 and 1_000_000_000.
    """
    # Write `count` integers to `path` using the generator below.
    random.seed()
    t0 = time.perf_counter()
    with open(path, "w", encoding="utf-8") as fh:
        for n in generate_data(count, lo, hi):
            fh.write(str(n) + "\n")
    t1 = time.perf_counter()
    elapsed = t1 - t0
    print(f"Wrote {count} integers to '{path}' in {elapsed:.4f} seconds")


def generate_data(count: int = 1000, lo: int = 0, hi: int = 1_000_000_000) -> List[int]:
    """Return a list of `count` random integers in range [lo, hi].

    This lets callers generate data in-memory without writing files.
    """
    return [random.randint(lo, hi) for _ in range(count)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random integer data file")
    parser.add_argument("-o", "--output", default="data.txt", help="output file path")
    parser.add_argument(
        "-n", "--count", type=int, default=1000, help="number of integers to generate"
    )
    parser.add_argument(
        "--min", type=int, default=0, help="minimum integer (inclusive)"
    )
    parser.add_argument(
        "--max",
        type=int,
        default=1_000_000_000,
        help="maximum integer (inclusive)",
    )
    args = parser.parse_args()
    main(path=args.output, count=args.count, lo=args.min, hi=args.max)
