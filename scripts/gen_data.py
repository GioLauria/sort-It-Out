import random


def main(
    path: str = "data.txt", count: int = 1000, lo: int = 0, hi: int = 1_000_000
) -> None:
    random.seed()
    with open(path, "w", encoding="utf-8") as fh:
        for _ in range(count):
            fh.write(str(random.randint(lo, hi)) + "\n")


if __name__ == "__main__":
    main()
