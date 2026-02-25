
"""SortItOut package.

Expose basic sorting helpers and timing utilities.
"""

from .sorts import (
	bubble_sort,
	quick_sort,
	merge_sort,
	time_sort,
	compare_algorithms,
)

__all__ = [
	"bubble_sort",
	"quick_sort",
	"merge_sort",
	"time_sort",
	"compare_algorithms",
]

__version__ = "0.1.0"
