"""SortItOut package.

Expose basic sorting helpers and timing utilities.
"""

from .sorts import (
    bubble_sort,
    bucket_sort,
    cocktail_sort,
    comb_sort,
    compare_algorithms,
    counting_sort,
    gnome_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    radix_sort,
    selection_sort,
    shell_sort,
    time_sort,
)

__all__ = [
    "bubble_sort",
    "quick_sort",
    "merge_sort",
    "time_sort",
    "compare_algorithms",
    "selection_sort",
    "insertion_sort",
    "heap_sort",
    "shell_sort",
    "counting_sort",
    "radix_sort",
    "bucket_sort",
    "comb_sort",
    "cocktail_sort",
    "gnome_sort",
    "run",
]

# Version handling: prefer a generated `_version.py` created by setuptools_scm
# at build/install time, otherwise try to read the latest git tag. Falls back
# to a sensible default if neither is available.
try:
    from ._version import version as __version__  # type: ignore
except Exception:
    import os
    import subprocess

    def _git_tag_version():
        try:
            git = os.environ.get("GIT", "git")
            args = [git, "describe", "--tags", "--abbrev=0"]
            out = subprocess.check_output(args, stderr=subprocess.DEVNULL)
            tag = out.decode().strip()
            return tag[1:] if tag.startswith("v") else tag
        except Exception:
            return "0.0.0"

    __version__ = _git_tag_version()


def run(argv: list | None = None) -> int:
    """Programmatic entrypoint to run the command-line interface.

    Example:
        import sort_it_out
        sort_it_out.run(["-s", "bubble", "-i", "data.txt"])  # returns exit code
    """
    # Import cli lazily to avoid circular imports during package import
    from . import cli as _cli

    return _cli.main(argv)
