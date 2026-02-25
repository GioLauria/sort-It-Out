"""Command-line interface for SortItOut.

Usage: sortItOut [-i INPUT] [-s ALGORITHM]

Reads a newline-separated data file (or stdin) and outputs the sorted values.
"""
from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from . import gui
from .algorithms import ALGORITHMS
from .sorts import time_sort


def _parse_value(s: str):
    s = s.strip()
    if s == "":
        return s
    # Try int, then float, fallback to original string
    try:
        return int(s)
    except Exception:
        pass
    try:
        return float(s)
    except Exception:
        return s


def read_input(path: Optional[str]) -> List:
    lines: List[str]
    # Accept None (no -i passed) or '-' to read from stdin
    if path and path != "-":
        with open(path, "r", encoding="utf-8") as fh:
            lines = [line.rstrip("\n") for line in fh]
    else:
        lines = [line.rstrip("\n") for line in sys.stdin]
    return [_parse_value(x) for x in lines if x is not None]


def main(argv: Optional[List[str]] = None) -> int:
    # If invoked with no CLI arguments (direct `sortItOut`), open GUI by default
    if argv is None and len(sys.argv) == 1:
        try:
            gui.run_gui()
        except Exception as exc:
            print(f"Error launching GUI: {exc}")
            return 3
        return 0

    parser = argparse.ArgumentParser(prog="sortItOut")
    parser.add_argument(
        "-i",
        "--input",
        help="input file (one value per line). If omitted or '-' reads stdin.",
    )
    parser.add_argument(
        "-s",
        "--sort",
        default="merge",
        help="sorting algorithm to use (default: merge)",
    )
    parser.add_argument(
        "--time", action="store_true", help="print average timing instead of values"
    )
    parser.add_argument("--gui", action="store_true", help="run graphical interface")
    parser.add_argument(
        "-o",
        "--output",
        help="output file to write sorted values (one per line).",
    )
    parser.add_argument(
        "-r",
        "--repeat",
        type=int,
        default=3,
        help="repeat times for timing (default: 3)",
    )
    ns = parser.parse_args(argv)

    if ns.gui:
        try:
            gui.run_gui()
        except Exception as exc:
            print(f"Error launching GUI: {exc}")
            return 3
        return 0

    alg_name = ns.sort.lower()
    if alg_name not in ALGORITHMS:
        names = ", ".join(sorted(ALGORITHMS.keys()))
        print(f"Unknown algorithm: {ns.sort}\nAvailable: {names}")
        return 2

    data = read_input(ns.input)
    algorithm = ALGORITHMS[alg_name]

    if ns.time:
        try:
            t = time_sort(algorithm, data, repeat=ns.repeat)
        except Exception as exc:
            print(f"Error while timing: {exc}")
            return 3
        print(f"{alg_name}: {t:.6f} sec (avg over {ns.repeat} runs)")
    else:
        try:
            out = algorithm(data)
        except Exception as exc:
            print(f"Error while sorting: {exc}")
            return 3
        # If an output file is provided, write results there; otherwise print to stdout
        if ns.output:
            try:
                with open(ns.output, "w", encoding="utf-8") as fh:
                    for item in out:
                        fh.write(f"{item}\n")
            except Exception as exc:
                print(f"Error writing output file: {exc}")
                return 3
        else:
            for item in out:
                print(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
