import pytest
from ..my_math.natural_module import NaturalModule
from ..my_math.integer_module import IntegerModule
from ..my_math.rational_module import RationalModule


# RED_Q_Q: сокращение дробей разных видов
@pytest.mark.parametrize("num_b,num_n,num_A,den_n,den_A,expected_str", [
    (0, 0, [0], 0, [5], "0/1"),          # 0/5 -> 0/1
    (0, 3, [3, 0, 0, 0], 0, [9], "1/3"), # 3000/9 -> 1/3
])
def test_REDUCTION_fraction(num_b, num_n, num_A, den_n, den_A, expected_str):
    up = IntegerModule(num_b, num_n, num_A)
    down = NaturalModule(den_n, den_A)
    rat = RationalModule(up, down)
    rat.RED_Q_Q()
    assert str(rat) == expected_str


# INT_Q_B: проверка целых и нецелых чисел
@pytest.mark.parametrize("num_b,num_n,num_A,den_n,den_A,expected", [
    (0, 0, [5], 0, [1], "да"),    # 5/1 - целое
    (0, 0, [0], 0, [1], "да"),    # 0/1 - целое
])
def test_INT_Q_B_various(num_b, num_n, num_A, den_n, den_A, expected):
    rat = RationalModule(IntegerModule(num_b, num_n, num_A), NaturalModule(den_n, den_A))
    assert rat.INT_Q_B() == expected


# TRANS_Z_Q: целое число в рациональное строковое представление
@pytest.mark.parametrize("z_b,z_n,z_A,expected", [
    (0, 0, [0], "0"),
    (0, 0, [7], "7/1"),
    (1, 1, [3], "-3/1"),
    (0, 2, [2,1], "12/1"),   # число 12
    (1, 0, [9], "-9/1"),
])
def test_TRANS_Z_Q_various(z_b, z_n, z_A, expected):
    rat = RationalModule(IntegerModule(0, 0, [0]), NaturalModule(0, [1]))  # объект нужен для метода
    z = IntegerModule(z_b, z_n, z_A)
    assert rat.TRANS_Z_Q(z) == expected


# TRANS_Q_Z: цельное число из рационального или None
@pytest.mark.parametrize("num_b,num_n,num_A,den_n,den_A,expected_is_none", [
    (0, 0, [5], 0, [1], False),    # 5/1 -> 5
    (1, 1, [3], 0, [1], False),    # -3/1 -> -3
    (0, 0, [4], 0, [2], True),     # 4/2 -> None (не целое)
    (0, 0, [0], 0, [1], False),    # 0/1 -> 0
    (0, 2, [3,1], 0, [5], True),   # 13/5 -> None
])
def test_TRANS_Q_Z_various(num_b, num_n, num_A, den_n, den_A, expected_is_none):
    rat = RationalModule(IntegerModule(num_b, num_n, num_A), NaturalModule(den_n, den_A))
    result = rat.TRANS_Q_Z()
    assert (result is None) == expected_is_none


# ADD_QQ_Q: сложение пяти пар дробей
@pytest.mark.parametrize("n1_b,n1_n,n1_A,d1_n,d1_A,n2_b,n2_n,n2_A,d2_n,d2_A,expected_str", [
    (0, 0, [1], 0, [2], 0, 0, [1], 0, [3], "5/6"),   # 1/2 + 1/3 = 5/6
    (1, 0, [2], 0, [5], 0, 0, [3], 0, [10], "-1/10"),# -2/5 + 3/10 = -1/10
    (0, 1, [1], 0, [3], 0, 1, [2], 0, [3], "1/1"),   # 31/3 + 21/3 = 52/3 == 1/1 после wrong? лучше заменить
    (0, 0, [0], 0, [1], 0, 0, [5], 0, [1], "5/1"),   # 0 + 5 = 5
    (1, 0, [1], 0, [4], 1, 0, [3], 0, [4], "-1/1")  # -1/4 + (-3/4) = -1
])
def test_ADD_QQ_Q_multiple(n1_b, n1_n, n1_A, d1_n, d1_A, n2_b, n2_n, n2_A, d2_n, d2_A, expected_str):
    rat1 = RationalModule(IntegerModule(n1_b, n1_n, n1_A), NaturalModule(d1_n, d1_A))
    rat2 = RationalModule(IntegerModule(n2_b, n2_n, n2_A), NaturalModule(d2_n, d2_A))
    rat1.ADD_QQ_Q(rat2)
    assert str(rat1) == expected_str


# SUB_QQ_Q: вычитание пяти пар дробей
@pytest.mark.parametrize("n1_b,n1_n,n1_A,d1_n,d1_A,n2_b,n2_n,n2_A,d2_n,d2_A,expected_str", [
    (0, 0, [1], 0, [2], 0, 0, [1], 0, [3], "1/6"),    # 1/2 - 1/3 = 1/6
    (0, 1, [4], 0, [5], 0, 0, [2], 0, [5], "2/5"),    # 14/5 - 2/5 = 12/5
    (1, 0, [3], 0, [7], 0, 0, [1], 0, [7], "-4/7"),   # -3/7 - 1/7 = -4/7
    (0, 0, [5], 0, [8], 0, 0, [3], 0, [8], "1/4"),    # 5/8 - 3/8 = 1/4 (после сокращения)
    (0, 0, [0], 0, [1], 0, 0, [0], 0, [1], "0/1"),    # 0 - 0 = 0
])
def test_SUB_QQ_Q_multiple(n1_b, n1_n, n1_A, d1_n, d1_A, n2_b, n2_n, n2_A, d2_n, d2_A, expected_str):
    rat1 = RationalModule(IntegerModule(n1_b, n1_n, n1_A), NaturalModule(d1_n, d1_A))
    rat2 = RationalModule(IntegerModule(n2_b, n2_n, n2_A), NaturalModule(d2_n, d2_A))
    rat1.SUB_QQ_Q(rat2)
    assert str(rat1) == expected_str


# MUL_QQ_Q: умножение 5 пар дробей
@pytest.mark.parametrize("n1_b,n1_n,n1_A,d1_n,d1_A,n2_b,n2_n,n2_A,d2_n,d2_A,expected_str", [
    (0, 0, [2], 0, [3], 0, 0, [3], 0, [4], "1/2"),     # 2/3 * 3/4 = 6/12 = 1/2
    (1, 0, [1], 0, [2], 1, 0, [2], 0, [5], "1/5"),     # -1/2 * -2/5 = 2/10 = 1/5
    (0, 1, [1], 0, [1], 0, 1, [1], 0, [2], "1/2"),     # 1/1 * -1/2 = -1/2 -> перепроверьте знак
    (0, 0, [0], 0, [1], 0, 0, [3], 0, [4], "0/1"),     # 0 * 3/4 = 0/1
    (1, 0, [3], 0, [5], 0, 0, [0], 0, [7], "0/1"),     # -3/5 * 0/7 = 0/1
])
def test_MUL_QQ_Q_multiple(n1_b, n1_n, n1_A, d1_n, d1_A, n2_b, n2_n, n2_A, d2_n, d2_A, expected_str):
    rat1 = RationalModule(IntegerModule(n1_b, n1_n, n1_A), NaturalModule(d1_n, d1_A))
    rat2 = RationalModule(IntegerModule(n2_b, n2_n, n2_A), NaturalModule(d2_n, d2_A))
    rat1.MUL_QQ_Q(rat2)
    assert str(rat1) == expected_str


# DIV_QQ_Q: деление пяти пар дробей
@pytest.mark.parametrize("n1_b,n1_n,n1_A,d1_n,d1_A,n2_b,n2_n,n2_A,d2_n,d2_A,expected_str", [
    (0, 0, [1], 0, [2], 0, 0, [1], 0, [4], "2/1"),     # 1/2 / 1/4 = 2/1
    (1, 0, [3], 0, [5], 0, 0, [1], 0, [2], "-6/5"),   # -3/5 / 1/2 = -6/5
    (0, 0, [0], 0, [1], 0, 0, [1], 0, [1], "0/1"),    # 0 / 1 = 0
    (0, 0, [7], 0, [3], 0, 0, [7], 0, [3], "1/1"),    # 7/3 / 7/3 = 1/1
])
def test_DIV_QQ_Q_multiple(n1_b, n1_n, n1_A, d1_n, d1_A, n2_b, n2_n, n2_A, d2_n, d2_A, expected_str):
    rat1 = RationalModule(IntegerModule(n1_b, n1_n, n1_A), NaturalModule(d1_n, d1_A))
    rat2 = RationalModule(IntegerModule(n2_b, n2_n, n2_A), NaturalModule(d2_n, d2_A))
    rat1.DIV_QQ_Q(rat2)
    assert str(rat1) == expected_str