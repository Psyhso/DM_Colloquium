import pytest
from ..my_math.integer_module import IntegerModule


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
    result = num.TRANS_Z_N()
    assert result.n == expected_n
    assert result.A == expected_A


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


# Тесты для ADD_ZZ_Z (Z-6)
@pytest.mark.parametrize("b1,n1,A1,b2,n2,A2,expected_b,expected_n,expected_A", [
    (0, 0, [5], 0, 0, [3], 0, 0, [8]),           # 5 + 3 = 8
    (1, 1, [1, 2], 1, 0, [5], 1, 1, [6, 2]),     # -21 + (-5) = -26
    (0, 0, [5], 1, 0, [3], 0, 0, [2]),           # 5 + (-3) = 2
    (1, 0, [5], 0, 0, [3], 1, 0, [2]),           # -5 + 3 = -2
    (0, 2, [9, 9, 9], 0, 0, [1], 0, 3, [0, 0, 0, 1])  # 999 + 1 = 1000
])
def test_add_zz_z(b1, n1, A1, b2, n2, A2, expected_b, expected_n, expected_A):
    """ADD_ZZ_Z: Сложение целых чисел"""
    num1 = IntegerModule(b1, n1, A1)
    num2 = IntegerModule(b2, n2, A2)
    result = num1.ADD_ZZ_Z(num2)
    assert result.b == expected_b
    assert result.n == expected_n
    assert result.A == expected_A


# Тесты для SUB_ZZ_Z (Z-7)
@pytest.mark.parametrize("b1,n1,A1,b2,n2,A2,expected_b,expected_n,expected_A", [
    (0, 0, [5], 0, 0, [3], 0, 0, [2]),           # 5 - 3 = 2
    (0, 0, [3], 0, 0, [5], 1, 0, [2]),           # 3 - 5 = -2
    (1, 0, [5], 1, 0, [3], 1, 0, [2]),           # -5 - (-3) = -2
    (1, 0, [3], 1, 0, [5], 0, 0, [2]),           # -3 - (-5) = 2
    (0, 0, [5], 1, 0, [3], 0, 0, [8]),           # 5 - (-3) = 8
    (1, 0, [5], 0, 0, [3], 1, 0, [8]),           # -5 - 3 = -8
])
def test_sub_zz_z(b1, n1, A1, b2, n2, A2, expected_b, expected_n, expected_A):
    """SUB_ZZ_Z: Вычитание целых чисел"""
    num1 = IntegerModule(b1, n1, A1)
    num2 = IntegerModule(b2, n2, A2)
    result = num1.SUB_ZZ_Z(num2)
    assert result.b == expected_b
    assert result.n == expected_n
    assert result.A == expected_A


# Тесты для MUL_ZZ_Z (Z-8)
@pytest.mark.parametrize("b1,n1,A1,b2,n2,A2,expected_b,expected_n,expected_A", [
    (0, 0, [5], 0, 0, [3], 0, 1, [5, 1]),        # 5 * 3 = 15
    (1, 0, [5], 1, 0, [3], 0, 1, [5, 1]),        # -5 * -3 = 15
    (0, 0, [5], 1, 0, [3], 1, 1, [5, 1]),        # 5 * -3 = -15
    (1, 0, [5], 0, 0, [3], 1, 1, [5, 1]),        # -5 * 3 = -15
    (0, 0, [5], 0, 0, [0], 0, 0, [0]),           # 5 * 0 = 0
    (1, 0, [5], 0, 0, [0], 0, 0, [0]),           # -5 * 0 = 0
])
def test_mul_zz_z(b1, n1, A1, b2, n2, A2, expected_b, expected_n, expected_A):
    """MUL_ZZ_Z: Умножение целых чисел"""
    num1 = IntegerModule(b1, n1, A1)
    num2 = IntegerModule(b2, n2, A2)
    result = num1.MUL_ZZ_Z(num2)
    assert result.b == expected_b
    assert result.n == expected_n
    assert result.A == expected_A


# Тесты для DIV_ZZ_Z (Z-9)
@pytest.mark.parametrize("b1,n1,A1,b2,n2,A2,expected_b,expected_n,expected_A", [
    (0, 1, [5, 1], 0, 0, [5], 0, 0, [3]),        # 15 / 5 = 3
    (0, 0, [7], 0, 0, [3], 0, 0, [2]),           # 7 / 3 = 2
    (1, 0, [7], 0, 0, [3], 1, 0, [3]),           # -7 / 3 = -3
    (0, 0, [7], 0, 0, [1], 0, 0, [7]),           # 7 / 1 = 7
    (1, 0, [7], 0, 0, [1], 1, 0, [7]),           # -7 / 1 = -7
])
def test_div_zz_z(b1, n1, A1, b2, n2, A2, expected_b, expected_n, expected_A):
    """DIV_ZZ_Z: Деление целых чисел"""
    num1 = IntegerModule(b1, n1, A1)
    num2 = IntegerModule(b2, n2, A2)
    result = num1.DIV_ZZ_Z(num2)
    assert result.b == expected_b
    assert result.n == expected_n
    assert result.A == expected_A


# Тесты для MOD_ZZ_Z (Z-10)
@pytest.mark.parametrize("b1,n1,A1,b2,n2,A2,expected_b,expected_n,expected_A", [
    (0, 0, [7], 0, 0, [3], 0, 0, [1]),           # 7 % 3 = 1
    (0, 0, [8], 0, 0, [4], 0, 0, [0]),           # 8 % 4 = 0
    (1, 0, [8], 1, 0, [4], 0, 0, [0]),           # -8 % -4 = 0
])
def test_mod_zz_z(b1, n1, A1, b2, n2, A2, expected_b, expected_n, expected_A):
    """MOD_ZZ_Z: Остаток от деления целых чисел"""
    num1 = IntegerModule(b1, n1, A1)
    num2 = IntegerModule(b2, n2, A2)
    result = num1.MOD_ZZ_Z(num2)
    assert result.b == expected_b
    assert result.n == expected_n
    assert result.A == expected_A


# Тест на деление на ноль
def test_div_by_zero():
    """DIV_ZZ_Z: Деление на ноль должно вызывать исключение"""
    num1 = IntegerModule(0, 0, [5])
    num2 = IntegerModule(0, 0, [0])
    with pytest.raises(Exception, match="Деление на ноль запрещено"):
        num1.DIV_ZZ_Z(num2)

def test_mod_by_zero():
    """MOD_ZZ_Z: Остаток от деления на ноль должен вызывать исключение"""
    num1 = IntegerModule(0, 0, [5])
    num2 = IntegerModule(0, 0, [0])
    with pytest.raises(Exception, match="Деление на ноль"):
        num1.MOD_ZZ_Z(num2)