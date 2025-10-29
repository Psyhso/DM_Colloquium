import pytest


@pytest.mark.parametrize("arr, n, expected", [
    (array('i', [1, 2, 3, 4, 5]), 5, array('i', [5, 4, 3, 2, 1])),
    (array('i', [5, 4, 3, 2, 1]), 5, array('i', [5, 4, 3, 2, 1])),
    (array('i', [-1, -2, -3, -4, -5]), 5, array('i', [-5, -4, -3, -2, -1])),

    (array('i', [1, -2, 3, -4, 5]), 5, array('i', [5, -4, 3, -2, 1])),
])

def test_timsort_basic(arr, n, expected):
    """Тестирование Timsort с различными входными данными"""
    sorted_array = timsort(arr, n)
    print(sorted_array)
    print(expected)
    assert sorted_array == expected
