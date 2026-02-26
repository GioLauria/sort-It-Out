import pytest

from scripts.gen_data import generate_data
from sort_it_out import merge_sort, time_sort
from sort_it_out.algorithms import ALGORITHMS


@pytest.mark.parametrize("alg", list(ALGORITHMS.values()))
def test_algorithms_sort_correctly(alg):
    data = generate_data(count=200, lo=-1000, hi=1000)
    expected = sorted(data)
    result = alg(data)
    assert result == expected


def test_time_sort_returns_float():
    data = generate_data(count=100, lo=1, hi=100)
    t = time_sort(merge_sort, data, repeat=2)
    assert isinstance(t, float)
    assert t >= 0.0
