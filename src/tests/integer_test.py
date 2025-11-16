import pytest
from my_math.integer_module import IntegerModule


# Тесты для ABS_Z_Z (Z-1)
@pytest.mark.parametrize("b,n,A,expected_b", [
    (1, 2, [3, 2, 1], 0),   # -123 -> 123
    (0, 2, [3, 2, 1], 0),   # 123 -> 123
    (1, 0, [5], 0),         # -5 -> 5
    (0, 0, [0], 0)          # 0 -> 0
])
def test_abs_z_z(b, n, A, expected_b):
    """ABS_Z_Z: Абсолютная величина числа"""
    num = IntegerModule(b, n, A)
    result = num.ABS_Z_Z()
    assert result.b == expected_b
    assert result.n == n
    assert result.A == A


# Тесты для POZ_Z_D (Z-2)
@pytest.mark.parametrize("b,n,A,expected", [
    (0, 2, [1, 2, 3], 1),   # 321 - положительное
    (1, 2, [1, 2, 3], -1),  # -321 - отрицательное
    (0, 0, [0], 0),         # 0 - ноль
    (0, 1, [5, 9], 1),      # 95 - положительное
    (1, 0, [7], -1)         # -7 - отрицательное
])
def test_poz_z_d(b, n, A, expected):
    """POZ_Z_D: Определение положительности числа"""
    num = IntegerModule(b, n, A)
    assert num.POZ_Z_D() == expected


# Тесты для MUL_ZM_Z (Z-3)
@pytest.mark.parametrize("b,n,A,expected_b", [
    (0, 2, [1, 2, 3], 1),   # 321 -> -321
    (1, 2, [1, 2, 3], 0),   # -321 -> 321
    (0, 0, [5], 1),         # 5 -> -5
    (1, 0, [7], 0),         # -7 -> 7
    (0, 0, [0], 0)          # 0 -> 0
])
def test_mul_zm_z(b, n, A, expected_b):
    """MUL_ZM_Z: Умножение на -1"""
    num = IntegerModule(b, n, A)
    result = num.MUL_ZM_Z()
    assert result.b == expected_b
    assert result.n == n
    assert result.A == A


# Тесты для TRANS_N_Z (Z-4)
@pytest.mark.parametrize("natural_n,natural_A,expected_b,expected_n", [
    (2, [1, 2, 3], 0, 2),   # 321 -> +321
    (0, [5], 0, 0),         # 5 -> +5
    (3, [0, 0, 1, 2], 0, 3),# 2100 -> +2100
    (1, [7, 8], 0, 1),      # 87 -> +87
    (0, [0], 0, 0)          # 0 -> +0
])
def test_trans_n_z(natural_n, natural_A, expected_b, expected_n):
    """TRANS_N_Z: Преобразование натурального в целое"""
    num = IntegerModule(1, 0, [1])  # Исходное состояние не важно
    result = num.TRANS_N_Z(natural_n, natural_A)
    assert result.b == expected_b
    assert result.n == expected_n
    assert result.A == natural_A


# Тесты для TRANS_Z_N (Z-5)
@pytest.mark.parametrize("b,n,A,expected_n,expected_A", [
    (0, 2, [1, 2, 3], 2, [1, 2, 3]),        # 321 -> (2, [1,2,3])
    (0, 0, [5], 0, [5]),                    # 5 -> (0, [5])
    (0, 3, [0, 0, 1, 2], 3, [0, 0, 1, 2])   # 2100 -> (3, [0,0,1,2])
])
def test_trans_z_n_valid(b, n, A, expected_n, expected_A):
    """TRANS_Z_N: Преобразование неотрицательного целого в натуральное"""
    num = IntegerModule(b, n, A)
    result_n, result_A = num.TRANS_Z_N()
    assert result_n == expected_n
    assert result_A == expected_A


@pytest.mark.parametrize("b,n,A", [
    (1, 2, [1, 2, 3]),      # -321
    (1, 0, [7]),            # -7
    (1, 1, [0, 5])          # -50
])
def test_trans_z_n_negative_raises_error(b, n, A):
    """TRANS_Z_N: Ошибка при отрицательном числе"""
    num = IntegerModule(b, n, A)
    with pytest.raises(ValueError, match="Отрицательное число не подходит для преобразования в натуральное"):
        num.TRANS_Z_N()