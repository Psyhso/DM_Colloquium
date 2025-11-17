import pytest
from ..my_math.natural_module import NaturalModule



# Тесты для COM_NN_D (N-1)
@pytest.mark.parametrize("n1,A1,n2,A2,expected", [
    (3, [4, 3, 2, 1], 2, [7, 6, 5], 2),      # 1234 > 567
    (2, [3, 2, 1], 2, [7, 6, 5], 1),          # 123 < 567
    (2, [3, 2, 1], 2, [3, 2, 1], 0),          # 123 == 123
    (0, [5], 0, [3], 2),                      # 5 > 3
    (1, [9, 9], 0, [9], 2)                    # 99 > 9
])
def test_com_nn_d(n1, A1, n2, A2, expected):
    """COM_NN_D: Сравнение натуральных чисел"""
    num1 = NaturalModule(n1, A1)
    num2 = NaturalModule(n2, A2)
    assert num1.COM_NN_D(num2) == expected



# Тесты для NZER_N_B (N-2)
@pytest.mark.parametrize("n,A,expected", [
    (0, [0], False),                          # 0 - ноль
    (0, [5], True),                           # 5 - не ноль
    (2, [3, 2, 1], True),                     # 123 - не ноль
    (1, [0, 1], True),                        # 10 - не ноль
    (3, [4, 3, 2, 1], True)                   # 1234 - не ноль
])
def test_nzer_n_b(n, A, expected):
    """NZER_N_B: Проверка на ноль"""
    num = NaturalModule(n, A)
    assert num.NZER_N_B() == expected



# Тесты для ADD_1N_N (N-3)
@pytest.mark.parametrize("n,A,expected_n,expected_A", [
    (0, [5], 0, [6]),                         # 5 + 1 = 6
    (0, [9], 1, [0, 1]),                      # 9 + 1 = 10
    (2, [9, 9, 9], 3, [0, 0, 0, 1]),          # 999 + 1 = 1000
    (1, [8, 2], 1, [9, 2]),                   # 28 + 1 = 29
    (2, [3, 2, 1], 2, [4, 2, 1])              # 123 + 1 = 124
])
def test_add_1n_n(n, A, expected_n, expected_A):
    """ADD_1N_N: Добавление 1 к натуральному числу"""
    num = NaturalModule(n, A.copy())
    result = num.ADD_1N_N()
    assert result.n == expected_n
    assert result.A == expected_A



# Тесты для MUL_ND_N (N-6)
@pytest.mark.parametrize("n,A,d,expected_n,expected_A", [
    (2, [3, 2, 1], 0, 0, [0]),                # 123 * 0 = 0
    (2, [3, 2, 1], 2, 2, [6, 4, 2]),          # 123 * 2 = 246
    (1, [5, 1], 3, 1, [5, 4]),                # 15 * 3 = 45
    (0, [9], 9, 1, [1, 8]),                   # 9 * 9 = 81
    (1, [7, 3], 4, 2, [8, 4, 1])              # 37 * 4 = 148
])
def test_mul_nd_n(n, A, d, expected_n, expected_A):
    """MUL_ND_N: Умножение натурального числа на цифру"""
    num = NaturalModule(n, A.copy())
    result = num.MUL_ND_N(d)
    assert result.n == expected_n
    assert result.A == expected_A



# Тесты для MUL_Nk_N (N-7)
@pytest.mark.parametrize("n,A,k,expected_n,expected_A", [
    (0, [0], 3, 0, [0]),                      # 0 * 10^3 = 0
    (2, [3, 2, 1], 2, 4, [0, 0, 3, 2, 1]),    # 123 * 100 = 12300
    (0, [5], 1, 1, [0, 5]),                   # 5 * 10 = 50
    (1, [7, 4], 3, 4, [0, 0, 0, 7, 4]),       # 47 * 1000 = 47000
    (0, [9], 0, 0, [9])                       # 9 * 1 = 9
])
def test_mul_nk_n(n, A, k, expected_n, expected_A):
    """MUL_Nk_N: Умножение натурального числа на 10^k"""
    num = NaturalModule(n, A.copy())
    result = num.MUL_Nk_N(k)
    assert result.n == expected_n
    assert result.A == expected_A



# Тесты для ADD_NN_N (N-4)
@pytest.mark.parametrize("n1,A1,n2,A2,expected_n,expected_A", [
    (2, [3, 2, 1], 2, [7, 6, 5], 2, [0, 9, 6]),       # 123 + 567 = 690
    (0, [9], 0, [1], 1, [0, 1]),                      # 9 + 1 = 10
    (2, [9, 9, 9], 0, [1], 3, [0, 0, 0, 1]),          # 999 + 1 = 1000
    (1, [5, 4], 1, [5, 5], 2, [0, 0, 1]),             # 45 + 55 = 100
    (0, [0], 0, [0], 0, [0])                          # 0 + 0 = 0
])
def test_add_nn_n(n1, A1, n2, A2, expected_n, expected_A):
    """ADD_NN_N: Сложение натуральных чисел"""
    num1 = NaturalModule(n1, A1.copy())
    num2 = NaturalModule(n2, A2.copy())
    result = num1.ADD_NN_N(num2)
    assert result.n == expected_n
    assert result.A == expected_A



# Тесты для SUB_NN_N (N-5)
@pytest.mark.parametrize("n1,A1,n2,A2,expected_n,expected_A", [
    (2, [3, 2, 1], 2, [0, 0, 1], 1, [3, 2]),          # 123 - 100 = 23 (ИСПРАВЛЕНО)
    (2, [7, 6, 5], 2, [3, 2, 1], 2, [4, 4, 4]),       # 567 - 123 = 444
    (1, [0, 5], 1, [5, 2], 1, [5, 2]),                # 50 - 25 = 25
    (2, [3, 2, 1], 0, [1], 2, [2, 2, 1]),             # 123 - 1 = 122
    (1, [0, 1], 0, [5], 0, [5])                       # 10 - 5 = 5
])
def test_sub_nn_n(n1, A1, n2, A2, expected_n, expected_A):
    """SUB_NN_N: Вычитание натуральных чисел"""
    num1 = NaturalModule(n1, A1.copy())
    num2 = NaturalModule(n2, A2.copy())
    result = num1.SUB_NN_N(num2)
    assert result.n == expected_n
    assert result.A == expected_A



# Тесты для MUL_NN_N (N-8)
@pytest.mark.parametrize("n1,A1,n2,A2,expected_n,expected_A", [
    (1, [2, 1], 1, [3, 2], 2, [6, 7, 2]),             # 12 * 23 = 276
    (0, [5], 0, [4], 1, [0, 2]),                      # 5 * 4 = 20
    (2, [3, 2, 1], 0, [2], 2, [6, 4, 2]),             # 123 * 2 = 246
    (1, [9, 9], 1, [9, 9], 3, [1, 0, 8, 9]),          # 99 * 99 = 9801 (ИСПРАВЛЕНО)
    (0, [0], 2, [3, 2, 1], 0, [0])                    # 0 * 123 = 0
])
def test_mul_nn_n(n1, A1, n2, A2, expected_n, expected_A):
    """MUL_NN_N: Умножение натуральных чисел"""
    num1 = NaturalModule(n1, A1.copy())
    num2 = NaturalModule(n2, A2.copy())
    result = num1.MUL_NN_N(num2)
    assert result.n == expected_n
    assert result.A == expected_A



# Тесты для SUB_NDN_N (N-9)
@pytest.mark.parametrize("n1,A1,n2,A2,d,expected_n,expected_A", [
    (2, [0, 0, 1], 1, [2, 1], 3, 1, [4, 6]),          # 100 - (12*3) = 100 - 36 = 64
    (2, [0, 5, 1], 1, [0, 2], 2, 2, [0, 1, 1]),       # 150 - (20*2) = 150 - 40 = 110
    (1, [0, 5], 0, [5], 4, 1, [0, 3]),                # 50 - (5*4) = 50 - 20 = 30
    (2, [0, 0, 2], 1, [0, 5], 3, 1, [0, 5])           # 200 - (50*3) = 200 - 150 = 50 (ИСПРАВЛЕНО)
])
def test_sub_ndn_n(n1, A1, n2, A2, d, expected_n, expected_A):
    """SUB_NDN_N: Вычитание из натурального другого, умноженного на цифру"""
    num1 = NaturalModule(n1, A1.copy())
    num2 = NaturalModule(n2, A2.copy())
    result = num1.SUB_NDN_N(num2, d)
    assert result.n == expected_n
    assert result.A == expected_A



# Тесты для DIV_NN_Dk (N-10)
@pytest.mark.parametrize("n1,A1,n2,A2,expected_d,expected_k", [
    (2, [6, 5, 4], 1, [2, 1], 3, 1),                  # 456 / 12 -> (3, 1) т.к. 3*12*10=360<=456
    (1, [0, 5], 0, [5], 1, 1),                        # 50 / 5 -> (1, 1) т.к. 1*5*10=50
    (2, [0, 0, 2], 1, [0, 2], 1, 1),                  # 200 / 20 -> (1, 1) т.к. 1*20*10=200
    (0, [5], 1, [0, 1], 0, 0)                         # 5 / 10 -> (0, 0) т.к. делимое меньше
])

def test_div_nn_dk(n1, A1, n2, A2, expected_d, expected_k):
    """DIV_NN_Dk: Первая цифра деления"""
    num1 = NaturalModule(n1, A1.copy())
    num2 = NaturalModule(n2, A2.copy())
    d, k = num1.DIV_NN_Dk(num2)
    assert d == expected_d
    assert k == expected_k



# Тесты для DIV_NN_N (N-11)
@pytest.mark.parametrize("n1,A1,n2,A2,expected_n,expected_A", [
    (2, [6, 5, 4], 1, [2, 1], 1, [8, 3]),             # 456 / 12 = 38
    (2, [0, 0, 1], 1, [0, 5], 0, [2]),                # 100 / 50 = 2
    (1, [0, 2], 0, [5], 0, [4]),                      # 20 / 5 = 4
    (2, [1, 8, 9], 1, [9, 9], 0, [9]),                # 981 / 99 = 9 (остаток 90)
    (0, [5], 0, [2], 0, [2])                          # 5 / 2 = 2
])
def test_div_nn_n(n1, A1, n2, A2, expected_n, expected_A):
    """DIV_NN_N: Неполное частное от деления"""
    num1 = NaturalModule(n1, A1.copy())
    num2 = NaturalModule(n2, A2.copy())
    result = num1.DIV_NN_N(num2)
    assert result.n == expected_n
    assert result.A == expected_A



# Тесты для MOD_NN_N (N-12)
@pytest.mark.parametrize("n1,A1,n2,A2,expected_n,expected_A", [
    (2, [6, 5, 4], 1, [2, 1], 0, [0]),                # 456 % 12 = 0
    (1, [3, 2], 0, [5], 0, [3]),                      # 23 % 5 = 3
    (2, [0, 0, 1], 1, [0, 3], 1, [0, 1]),             # 100 % 30 = 10
    (0, [7], 0, [3], 0, [1]),                         # 7 % 3 = 1
    (2, [1, 8, 9], 1, [9, 9], 1, [0, 9])              # 981 % 99 = 90
])
def test_mod_nn_n(n1, A1, n2, A2, expected_n, expected_A):
    """MOD_NN_N: Остаток от деления"""
    num1 = NaturalModule(n1, A1.copy())
    num2 = NaturalModule(n2, A2.copy())
    result = num1.MOD_NN_N(num2)
    assert result.n == expected_n
    assert result.A == expected_A



# Тесты для GCF_NN_N (N-13)
@pytest.mark.parametrize("n1,A1,n2,A2,expected_n,expected_A", [
    (1, [8, 4], 1, [8, 1], 0, [6]),                   # НОД(48, 18) = 6
    (1, [0, 2], 1, [5, 1], 0, [5]),                   # НОД(20, 15) = 5
    (2, [0, 0, 1], 1, [0, 5], 1, [0, 5]),             # НОД(100, 50) = 50
    (1, [2, 1], 0, [8], 0, [4]),                      # НОД(12, 8) = 4
    (0, [7], 0, [7], 0, [7])                          # НОД(7, 7) = 7
])
def test_gcf_nn_n(n1, A1, n2, A2, expected_n, expected_A):
    """GCF_NN_N: НОД натуральных чисел"""
    num1 = NaturalModule(n1, A1.copy())
    num2 = NaturalModule(n2, A2.copy())
    result = num1.GCF_NN_N(num2)
    assert result.n == expected_n
    assert result.A == expected_A
    

# Тесты для LCM_NN_N (N-14)
@pytest.mark.parametrize("n1,A1,n2,A2,expected_n,expected_A", [
    (1, [2], 1, [3], 1, [6]),                    # НОК(2, 3) = 6
    (1, [3], 1, [5], 1, [5, 1]),                 # НОК(3, 5) = 15
    (1, [4], 1, [6], 1, [2, 1]),                # НОК(4, 6) = 12
    (1, [9], 3, [0, 0, 1], 3, [0, 0, 1]),       # НОК(9, 100) = 900
    (1, [7], 1, [8], 1, [6, 5]),                # НОК(7, 8) = 56
    (1, [9], 1, [4], 1, [6, 3]),                # НОК(9, 4) = 36
])
def test_lcm_nn_n(n1, A1, n2, A2, expected_n, expected_A):
    """LCM_NN_N: Наименьшее общее кратное натуральных чисел"""
    num1 = NaturalModule(n1, A1.copy())
    num2 = NaturalModule(n2, A2.copy())
    
    result = num1.LCM_NN_N(num2)
    
    assert result.n == expected_n
    assert result.A == expected_A