import pytest

from scripts.gen_data import generate_data
from sort_it_out import time_sort
from sort_it_out.algorithms import ALGORITHMS


@pytest.mark.parametrize("name,alg", list(ALGORITHMS.items()))
def test_algorithms_sort_correctly(name, alg):
    # Bucket sort implementation expects floats in [0, 1). Provide
    # appropriate input for that case; otherwise use integer data.
    if name.lower().startswith("bucket"):
        ints = generate_data(count=200, lo=0, hi=999)
        data = [x / 1000.0 for x in ints]
    else:
        data = generate_data(count=200, lo=-1000, hi=1000)

    expected = sorted(data)
    data_copy = list(data)
    result = alg(data_copy)
    if result is None:
        result = data_copy
    assert result == expected


def test_time_sort_returns_float():
    data = generate_data(count=100, lo=1, hi=100)
    # Get the Merge implementation from the central registry
    merge = ALGORITHMS.get("Merge")
    t = time_sort(merge, data, repeat=2)
    assert isinstance(t, float)
    assert t >= 0.0
