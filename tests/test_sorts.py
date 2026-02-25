import random
import pytest

from sort_it_out import (
    bubble_sort,
    quick_sort,
    merge_sort,
    selection_sort,
    insertion_sort,
    heap_sort,
    shell_sort,
    counting_sort,
    radix_sort,
    comb_sort,
    cocktail_sort,
    gnome_sort,
    time_sort,
)


@pytest.mark.parametrize(
    "alg",
    [
        bubble_sort,
        quick_sort,
        merge_sort,
        selection_sort,
        insertion_sort,
        heap_sort,
        shell_sort,
        counting_sort,
        radix_sort,
        comb_sort,
        cocktail_sort,
        gnome_sort,
    ],
)
def test_algorithms_sort_correctly(alg):
    data = [random.randint(-1000, 1000) for _ in range(200)]
    expected = sorted(data)
    result = alg(data)
    assert result == expected


def test_time_sort_returns_float():
    data = list(range(100, 0, -1))
    t = time_sort(merge_sort, data, repeat=2)
    assert isinstance(t, float)
    assert t >= 0.0
