"""Central registry of available sorting algorithms.

Put algorithm mappings here so the CLI, GUI and other tools use a single
source of truth for available algorithm names.
"""
from typing import Callable, Dict, List

from .sorts import (
    bubble_sort,
    bucket_sort,
    cocktail_sort,
    comb_sort,
    counting_sort,
    gnome_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    radix_sort,
    selection_sort,
    shell_sort,
)

ALGORITHMS: Dict[str, Callable[[List], List]] = {
    "bubble": bubble_sort,
    "quick": quick_sort,
    "merge": merge_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "heap": heap_sort,
    "shell": shell_sort,
    "counting": counting_sort,
    "radix": radix_sort,
    "bucket": bucket_sort,
    "comb": comb_sort,
    "cocktail": cocktail_sort,
    "gnome": gnome_sort,
}

__all__ = ["ALGORITHMS"]
