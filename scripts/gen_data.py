import argparse
import random
import time


def main(
    path: str = "data.txt", count: int = 1000, lo: int = 0, hi: int = 1_000_000_000
) -> None:
    """Generate `count` random integers in range [lo, hi] and write to `path`.

    Defaults: 1000 numbers between 0 and 1_000_000_000.
    """
    random.seed()
    t0 = time.perf_counter()
    with open(path, "w", encoding="utf-8") as fh:
        for _ in range(count):
            fh.write(str(random.randint(lo, hi)) + "\n")
    t1 = time.perf_counter()
    elapsed = t1 - t0
    print(f"Wrote {count} integers to '{path}' in {elapsed:.4f} seconds")


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
