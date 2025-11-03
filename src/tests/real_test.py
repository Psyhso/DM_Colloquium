""""ТЕСТЫ АЛЬБЕРТА"""
@pytest.mark.parametrize("polinom, expected", [
    (RealModule(1, [10, 5]), 1),
    (RealModule(3, [24, 5, 0, 2]), 3),
    (RealModule(0, [0]), 0),
    (RealModule(5, [1, 5, 5, 0, 0, 0]), 5),
    (RealModule(10, [101, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0]), 10),
    (RealModule(2, [1, 2, 3]), 2)
])
def test_DEG_P_N(polinom, expected):
    """Тестирование DEG_P_N - степени многочлена"""
    p = polinom
    res = p.DEG_P_N()
    print(f"Степень: {res}, Ожидается: {expected}")
    assert res == expected


@pytest.mark.parametrize("polinom, expected_degree, expected_coeffs", [
    # (x^2 + 2x + 3)' = 2x + 2
    (RealModule(2, [1, 2, 3]), 1, [2, 2]),
    # (5x^3 + 3x^2 + x + 7)' = 15x^2 + 6x + 1
    (RealModule(3, [5, 3, 1, 7]), 2, [15, 6, 1]),
    # Константа (5)' = 0
    (RealModule(0, [5]), 0, [0]),
    # (10x^4 + 0x^3 + 2x^2 + 0x + 1)' = 40x^3 + 0x^2 + 4x + 0
    (RealModule(4, [10, 0, 2, 0, 1]), 3, [40, 0, 4, 0]),
    # (x)' = 1
    (RealModule(1, [1, 0]), 0, [1]),
    # Многочлен с нулевыми коэффициентами (3x^2 + 0x + 0)' = 6x + 0
    (RealModule(2, [3, 0, 0]), 1, [6, 0])
])
def test_DER_P_P(polinom, expected_degree, expected_coeffs):
    """Тестирование DER_P_P - производной многочлена"""
    p = polinom
    res = p.DER_P_P()
    print(f"Результат: степень={res.m}, коэффициенты={res.C}")
    print(
        f"Ожидается: степень={expected_degree}, коэффициенты={expected_coeffs}")
    assert res.m == expected_degree and res.C == expected_coeffs
