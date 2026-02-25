"""Sorting algorithms and timing utilities for SortItOut.

Functions operate on sequences of comparable items and return a new list
with the sorted result. Timing helpers measure execution time using
`time.perf_counter`.
"""
from __future__ import annotations

import time
from typing import Callable, Dict, Iterable, List


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


def selection_sort(data: Iterable) -> List:
    arr = list(data)
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(data: Iterable) -> List:
    arr = list(data)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def heap_sort(data: Iterable) -> List:
    arr = list(data)

    def heapify(n, i):
        largest = i
        left_idx = 2 * i + 1
        right_idx = 2 * i + 2
        if left_idx < n and arr[left_idx] > arr[largest]:
            largest = left_idx
        if right_idx < n and arr[right_idx] > arr[largest]:
            largest = right_idx
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(i, 0)
    return arr


def shell_sort(data: Iterable) -> List:
    arr = list(data)
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


def counting_sort(data: Iterable) -> List:
    arr = list(data)
    if not arr:
        return []
    # Counting sort only works with integers
    if not all(isinstance(x, int) for x in arr):
        raise TypeError("counting_sort requires integer inputs")
    min_val = min(arr)
    max_val = max(arr)
    offset = -min_val
    size = max_val - min_val + 1
    counts = [0] * size
    for x in arr:
        counts[x + offset] += 1
    res: List[int] = []
    for i, c in enumerate(counts):
        res.extend([i - offset] * c)
    return res


def radix_sort(data: Iterable) -> List:
    arr = list(data)
    if not arr:
        return []
    if not all(isinstance(x, int) for x in arr):
        raise TypeError("radix_sort requires integer inputs")
    # Handle negatives by offsetting
    neg = [x for x in arr if x < 0]
    pos = [x for x in arr if x >= 0]

    def _radix(ls: List[int]) -> List[int]:
        if not ls:
            return []
        max_val = max(ls)
        exp = 1
        res = list(ls)
        while max_val // exp > 0:
            buckets = [[] for _ in range(10)]
            for num in res:
                buckets[(num // exp) % 10].append(num)
            res = [v for bucket in buckets for v in bucket]
            exp *= 10
        return res

    pos_sorted = _radix(pos)
    # For negatives, sort absolute values then reverse
    neg_sorted = _radix([abs(x) for x in neg])
    neg_sorted = [-x for x in reversed(neg_sorted)]
    return neg_sorted + pos_sorted


def bucket_sort(data: Iterable) -> List:
    arr = list(data)
    if not arr:
        return []
    # This implementation expects floats in [0, 1)
    if not all(isinstance(x, float) for x in arr):
        raise TypeError("bucket_sort expects floats in [0, 1)")
    n = len(arr)
    buckets: List[List[float]] = [[] for _ in range(n)]
    for x in arr:
        idx = min(n - 1, int(x * n))
        buckets[idx].append(x)
    res: List[float] = []
    for b in buckets:
        res.extend(sorted(b))
    return res


def comb_sort(data: Iterable) -> List:
    arr = list(data)
    n = len(arr)
    gap = n
    shrink = 1.3
    sorted_flag = False
    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True
        i = 0
        while i + gap < n:
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted_flag = False
            i += 1
    return arr


def cocktail_sort(data: Iterable) -> List:
    arr = list(data)
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        start += 1
    return arr


def gnome_sort(data: Iterable) -> List:
    arr = list(data)
    i = 1
    n = len(arr)
    while i < n:
        if arr[i] >= arr[i - 1]:
            i += 1
        else:
            arr[i], arr[i - 1] = arr[i - 1], arr[i]
            i -= 1
            if i == 0:
                i = 1
    return arr


def time_sort(
    algorithm: Callable[[Iterable], List],
    data: Iterable,
    repeat: int = 3,
) -> float:
    """Time ``algorithm`` on ``data``.

    Runs ``algorithm`` ``repeat`` times and returns the average elapsed
    time in seconds.
    """
    if repeat <= 0:
        raise ValueError("repeat must be >= 1")
    total = 0.0
    for _ in range(repeat):
        to_run = list(data)
        start = time.perf_counter()
        algorithm(to_run)
        end = time.perf_counter()
        total += end - start
    return total / repeat


def compare_algorithms(
    algorithms: Dict[str, Callable[[Iterable], List]],
    data: Iterable,
    repeat: int = 3,
) -> Dict[str, float]:
    """Return a mapping algorithm_name -> average_time_seconds for each
    algorithm.
    """
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
