"""Sorting algorithms and timing utilities for SortItOut.

Functions operate on sequences of comparable items and return a new list
with the sorted result. Timing helpers measure execution time using
`time.perf_counter`.
"""
from __future__ import annotations

from typing import Callable, Iterable, List, Dict
import time


def bubble_sort(data: Iterable) -> List:
    arr = list(data)
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def quick_sort(data: Iterable) -> List:
    arr = list(data)
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def merge_sort(data: Iterable) -> List:
    arr = list(data)
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def time_sort(algorithm: Callable[[Iterable], List], data: Iterable, repeat: int = 3) -> float:
    """Time `algorithm` on `data`, running `repeat` times and returning average seconds."""
    if repeat <= 0:
        raise ValueError("repeat must be >= 1")
    total = 0.0
    for _ in range(repeat):
        to_run = list(data)
        start = time.perf_counter()
        algorithm(to_run)
        end = time.perf_counter()
        total += (end - start)
    return total / repeat


def compare_algorithms(algorithms: Dict[str, Callable[[Iterable], List]], data: Iterable, repeat: int = 3) -> Dict[str, float]:
    """Return a mapping algorithm_name -> average_time_seconds for each algorithm."""
    results: Dict[str, float] = {}
    for name, alg in algorithms.items():
        results[name] = time_sort(alg, data, repeat=repeat)
    return results


__all__ = [
    "bubble_sort",
    "quick_sort",
    "merge_sort",
    "time_sort",
    "compare_algorithms",
]
