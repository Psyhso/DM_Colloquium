import pytest
from my_math.real_module import RealModule

@pytest.mark.parametrize("polinom, k, expected", [
    (RealModule(1, [10, 5]), 5, RealModule(6, [10, 5, 0, 0, 0, 0, 0])),
    (RealModule(1, [10, 5]), -5, RealModule(1, [10, 5])),
    (RealModule(1, [10, 5]), 0, RealModule(1, [10, 5])),
    (RealModule(1, [10, 5]), 1, RealModule(2, [10, 5, 0])),
    (RealModule(10, [10, 5, 0, 0, 0, 0, 6, 0, 0, 0]), 8, RealModule(18, [10, 5, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
])

def test_MUL_Pxk_P(polinom, k, expected):
    """Тестирование MUL_Pxk_P"""
    p = polinom 
    k = k
    res = p.MUL_Pxk_P(k)
    print(res.m, res.C)
    print(expected.m, expected.C)
    assert (res.m == expected.m and res.C == expected.C)


@pytest.mark.parametrize("polinom, k, expected", [
    (RealModule(1, [10, 5]), 10),
    (RealModule(3, [24, 5, 0, 2]), 24),
    (RealModule(0, [0]), 0),
    (RealModule(5, [1, 5, 5, 0, 0]), 1),
    (RealModule(10, [101, 5, 0, 0, 0, 0, 0, 0, 0, 0]), 101)
])

def test_LED_P_Q(polinom, expected):
    """Тестирование LED_P_Q"""
    p = polinom 
    res = p.LED_P_Q()
    print(res)
    print(expected)
    assert (res == expected)