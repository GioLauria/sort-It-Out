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
    "Bubble": bubble_sort,
    "Quick": quick_sort,
    "Merge": merge_sort,
    "Selection": selection_sort,
    "Insertion": insertion_sort,
    "Heap": heap_sort,
    "Shell": shell_sort,
    "Counting": counting_sort,
    "Radix": radix_sort,
    "Bucket": bucket_sort,
    "Comb": comb_sort,
    "Cocktail": cocktail_sort,
    "Gnome": gnome_sort,
}

# Case-insensitive lookup mapping to preserve backward compatibility
ALGORITHMS_LOWER: Dict[str, Callable[[List], List]] = {
    name.lower(): func for name, func in ALGORITHMS.items()
}

__all__ = ["ALGORITHMS", "ALGORITHMS_LOWER"]
