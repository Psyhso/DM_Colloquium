import pytest
from my_math.real_module import RealModule
from my_math.natural_module import NaturalModule
from my_math.integer_module import IntegerModule

def create_natural_from_int(num: int):
    """Создает NaturalModule из целого числа"""
    if num == 0:
        return NaturalModule(0, [0])
    
    digits = [int(d) for d in str(num)[::-1]]
    return NaturalModule(len(digits) - 1, digits)

def create_rational(numerator: int, denominator: int = 1):
    """Создает рациональное число из целых чисел"""
    # Правильно обрабатываем знак и создаем цифры в правильном порядке
    sign = 1 if numerator < 0 else 0
    abs_numerator = abs(numerator)
    
    if abs_numerator == 0:
        num_digits = [0]
        num_len = 0
    else:
        num_digits = [int(d) for d in str(abs_numerator)[::-1]]
        num_len = len(num_digits) - 1
    
    if denominator == 1:
        den_digits = [1]
        den_len = 0
    else:
        den_digits = [int(d) for d in str(denominator)[::-1]]
        den_len = len(den_digits) - 1
    
    num_int = IntegerModule(sign, num_len, num_digits)
    den_nat = NaturalModule(den_len, den_digits)
    return RationalModule(num_int, den_nat)

def create_polynomial(coefficients: list) -> RealModule:
    """Создает многочлен из списка рациональных чисел"""
    return RealModule(len(coefficients) - 1, coefficients)

def test_ADD_PP_P_with_negative_coefficients():
    """Тест сложения с отрицательными коэффициентами"""
    # P1: -x + 1
    neg_one = create_rational(-1)
    p1 = create_polynomial([create_rational(1), neg_one])
    
    # P2: 2x - 1
    neg_one_2 = create_rational(-1)
    p2 = create_polynomial([neg_one_2, create_rational(2)])
    
    result = p1.ADD_PP_P(p2)
    # Ожидаем: x + 0
    assert result.DEG_P_N() == 1
    assert result.C[0].up.A == [0]  # 1 + (-1) = 0
    assert result.C[1].up.A == [1] and result.C[1].up.b == 0  # -1 + 2 = 1
    print("✓ test_ADD_PP_P_with_negative_coefficients - пройден")

def test_SUB_PP_P_with_negative_coefficients():
    """Тест вычитания с отрицательными коэффициентами"""
    # P1: -2x - 3
    p1 = create_polynomial([create_rational(-3), create_rational(-2)])
    # P2: -x - 1
    p2 = create_polynomial([create_rational(-1), create_rational(-1)])
    result = p1.SUB_PP_P(p2)
    # Ожидаем: -x - 2
    assert result.DEG_P_N() == 1
    assert result.C[0].up.A == [2] and result.C[0].up.b == 1  # -3 - (-1) = -2
    assert result.C[1].up.A == [1] and result.C[1].up.b == 1  # -2 - (-1) = -1
    print("✓ test_SUB_PP_P_with_negative_coefficients - пройден")

def test_MUL_Pxk_P_with_negative_coefficients():
    """Тест умножения на x^k многочлена с отрицательными коэффициентами"""
    # P: -x^2 + 2x - 3
    p = create_polynomial([
        create_rational(-3), 
        create_rational(2), 
        create_rational(-1)
    ])
    result = p.MUL_Pxk_P(2)
    # Ожидаем: -x^4 + 2x^3 - 3x^2
    assert result.DEG_P_N() == 4
    assert len(result.C) == 5
    assert result.C[0].up.A == [0]  # свободный член
    assert result.C[1].up.A == [0]  # коэффициент при x
    assert result.C[2].up.A == [3] and result.C[2].up.b == 1  # -3
    assert result.C[3].up.A == [2] and result.C[3].up.b == 0  # 2
    assert result.C[4].up.A == [1] and result.C[4].up.b == 1  # -1
    print("✓ test_MUL_Pxk_P_with_negative_coefficients - пройден")

def test_LED_P_Q_with_negative_leading_coefficient():
    """Тест старшего коэффициента при отрицательном старшем коэффициенте"""
    # P: -3x^2 + 2x + 1
    p = create_polynomial([
        create_rational(1), 
        create_rational(2), 
        create_rational(-3)
    ])
    led = p.LED_P_Q()
    # Ожидаем -3
    assert led.up.A == [3] and led.up.b == 1
    print("✓ test_LED_P_Q_with_negative_leading_coefficient - пройден")

def test_FAC_P_Q_with_mixed_negative_fractions():
    """Тест вынесения множителя для смешанных дробных коэффициентов с отрицательными значениями"""
    # P: (-3/4)x^2 + (1/2)x - 2
    p = create_polynomial([
        create_rational(-2),  # -2
        create_rational(1, 2),  # 1/2
        create_rational(-3, 4)  # -3/4
    ])
    fac = p.FAC_P_Q()
    # НОК знаменателей: НОК(1,2,4)=4
    # НОД числителей: НОД(2,1,3)=1
    # Ожидаем 4/1
    assert fac.up.A == [4] and fac.up.b == 0
    assert fac.down.A == [1]
    print("✓ test_FAC_P_Q_with_mixed_negative_fractions - пройден")

def test_ADD_PP_P_negative_and_positive():
    """Тест сложения многочленов с положительными и отрицательными коэффициентами"""
    # P1: -2x^2 + 3x - 1
    p1 = create_polynomial([
        create_rational(-1),
        create_rational(3),
        create_rational(-2)
    ])
    # P2: x^2 - 2x + 4
    p2 = create_polynomial([
        create_rational(4),
        create_rational(-2),
        create_rational(1)
    ])
    
    result = p1.ADD_PP_P(p2)
    # Ожидаем: -x^2 + x + 3
    assert result.DEG_P_N() == 2
    assert result.C[0].up.A == [3] and result.C[0].up.b == 0  # -1 + 4 = 3
    assert result.C[1].up.A == [1] and result.C[1].up.b == 0  # 3 + (-2) = 1
    assert result.C[2].up.A == [1] and result.C[2].up.b == 1  # -2 + 1 = -1
    print("✓ test_ADD_PP_P_negative_and_positive - пройден")

def test_SUB_PP_P_all_negative():
    """Тест вычитания многочленов с полностью отрицательными коэффициентами"""
    # P1: -x^2 - 2x - 3
    p1 = create_polynomial([
        create_rational(-3),
        create_rational(-2),
        create_rational(-1)
    ])
    # P2: -2x^2 - x - 1
    p2 = create_polynomial([
        create_rational(-1),
        create_rational(-1),
        create_rational(-2)
    ])
    
    result = p1.SUB_PP_P(p2)
    # Ожидаем: x^2 - x - 2
    assert result.DEG_P_N() == 2
    assert result.C[0].up.A == [2] and result.C[0].up.b == 1  # -3 - (-1) = -2
    assert result.C[1].up.A == [1] and result.C[1].up.b == 1  # -2 - (-1) = -1
    assert result.C[2].up.A == [1] and result.C[2].up.b == 0  # -1 - (-2) = 1
    print("✓ test_SUB_PP_P_all_negative - пройден")

def test_polynomial_with_all_negative_coefficients():
    """Тест многочлена со всеми отрицательными коэффициентами"""
    # P: -5x^3 - 4x^2 - 3x - 2
    p = create_polynomial([
        create_rational(-2),
        create_rational(-3),
        create_rational(-4),
        create_rational(-5)
    ])
    
    # Проверяем степень
    assert p.DEG_P_N() == 3
    
    # Проверяем старший коэффициент
    led = p.LED_P_Q()
    assert led.up.A == [5] and led.up.b == 1
    
    # Проверяем все коэффициенты
    assert p.C[0].up.A == [2] and p.C[0].up.b == 1
    assert p.C[1].up.A == [3] and p.C[1].up.b == 1
    assert p.C[2].up.A == [4] and p.C[2].up.b == 1
    assert p.C[3].up.A == [5] and p.C[3].up.b == 1
    
    print("✓ test_polynomial_with_all_negative_coefficients - пройден")

def run_all_tests():
    """Запускает все тесты и выводит результаты"""
    test_count = 0
    passed_count = 0
    
    print("Запуск тестов для RealModule...")
    
    # Список всех тестовых функций
    test_functions = [
        test_ADD_PP_P_with_negative_coefficients,
        test_SUB_PP_P_with_negative_coefficients,
        test_MUL_Pxk_P_with_negative_coefficients,
        test_LED_P_Q_with_negative_leading_coefficient,
        test_FAC_P_Q_with_mixed_negative_fractions,
        test_ADD_PP_P_negative_and_positive,
        test_SUB_PP_P_all_negative,
        test_polynomial_with_all_negative_coefficients,
    ]
    
    for test_func in test_functions:
        try:
            test_func()
            passed_count += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} - не пройден: {e}")
        test_count += 1
    
    # Итоги
    print(f"\nРезультаты тестирования:")
    print(f"Пройдено: {passed_count}/{test_count} тестов")
    
    if passed_count == test_count:
        print("🎉 Все тесты пройдены успешно!")
    else:
        print(f"❌ Не пройдено: {test_count - passed_count} тестов")
    
    return passed_count == test_count

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

""" Тесты Альберта """

def test_mul_pp_p_basic():
    """
    Тестируем MUL_PP_P
    Тест 1: (x + 1) * (x - 1) = x^2 - 1
    """
    p1 = create_polynomial([create_rational(1), create_rational(1)])    # x + 1
    p2 = create_polynomial([create_rational(-1), create_rational(1)])   # x - 1

    res = p1.MUL_PP_P(p2)

    # Проверяем степень
    assert res.DEG_P_N() == 2

    # Проверяем коэффициенты: [-1, 0, 1]
    assert res.C[0].up.A == [1] and res.C[0].up.b == 1   # -1
    assert res.C[1].up.A == [0]                          # 0
    assert res.C[2].up.A == [1] and res.C[2].up.b == 0   # +1

def test_mul_pp_p_with_zero():
    """Тест 2: (x^2 + 2x + 3) * 0 = 0"""
    p1 = create_polynomial([
        create_rational(3),
        create_rational(2),
        create_rational(1)
    ])  # x^2 + 2x + 3

    zero_poly = create_polynomial([
        create_rational(0)
    ])  # 0

    res = p1.MUL_PP_P(zero_poly)

    # Ожидаем нулевой многочлен
    assert res.DEG_P_N() == 0
    assert res.C[0].up.A == [0]

def test_mul_pp_p_different_degrees():
    """Тест 3: (2x + 3) * (x^2 + 1) = 2x^3 + 3x^2 + 2x + 3"""
    p1 = create_polynomial([create_rational(3), create_rational(2)])  # 2x + 3
    p2 = create_polynomial([create_rational(1), create_rational(0), create_rational(1)])  # x^2 + 1

    res = p1.MUL_PP_P(p2)

    # Проверяем коэффициенты: [3, 2, 3, 2]
    # => 2x^3 + 3x^2 + 2x + 3
    assert res.DEG_P_N() == 3
    assert [int(''.join(map(str, c.up.A[::-1]))) * (-1 if c.up.b else 1) for c in res.C] == [3, 2, 3, 2]


def test_div_pp_p_basic():
    """
    Тестируем DIV_PP_P
    Тест 1: (x^2 - 1) / (x - 1) = x + 1
    """
    p1 = create_polynomial([
        create_rational(-1), 
        create_rational(0), 
        create_rational(1)
    ])  # x^2 - 1
    
    p2 = create_polynomial([
        create_rational(-1), 
        create_rational(1)
    ])  # x - 1

    res = p1.DIV_PP_P(p2)

    # Проверяем степень
    assert res.DEG_P_N() == 1
    
    # Проверяем коэффициенты: [1, 1] (x + 1)
    assert res.C[0].up.A == [1] and res.C[0].up.b == 0  # +1
    assert res.C[1].up.A == [1] and res.C[1].up.b == 0  # +1

def test_div_pp_p_same_polynomial():
    """
    Тест 2: (x^2 + 2x + 1) / (x + 1) = x + 1
    """
    p1 = create_polynomial([
        create_rational(1), 
        create_rational(2), 
        create_rational(1)
    ])  # x^2 + 2x + 1
    
    p2 = create_polynomial([
        create_rational(1), 
        create_rational(1)
    ])  # x + 1

    res = p1.DIV_PP_P(p2)

    # Проверяем степень
    assert res.DEG_P_N() == 1
    
    # Проверяем коэффициенты: [1, 1] (x + 1)
    assert res.C[0].up.A == [1] and res.C[0].up.b == 0  # +1
    assert res.C[1].up.A == [1] and res.C[1].up.b == 0  # +1

def test_div_pp_p_higher_degree_divisor():
    """
    Тест 3: (x + 1) / (x^2 + 1) = 0 (целая часть)
    Когда степень делителя больше степени делимого
    """
    p1 = create_polynomial([
        create_rational(1), 
        create_rational(1)
    ])  # x + 1
    
    p2 = create_polynomial([
        create_rational(1), 
        create_rational(0), 
        create_rational(1)
    ])  # x^2 + 1

    res = p1.DIV_PP_P(p2)

    # Ожидаем нулевой многочлен (целая часть деления)
    assert res.DEG_P_N() == 0
    assert res.C[0].up.A == [0]  # 0

def test_div_pp_p_constants():
    """
    Тест 4: (6x + 9) / 3 = 2x + 3
    Деление на константу
    """
    p1 = create_polynomial([
        create_rational(9), 
        create_rational(6)
    ])  # 6x + 9
    
    p2 = create_polynomial([
        create_rational(3)
    ])  # 3

    res = p1.DIV_PP_P(p2)

    # Проверяем коэффициенты: [3, 2] (2x + 3)
    assert res.DEG_P_N() == 1
    assert res.C[0].up.A == [3] and res.C[0].up.b == 0  # +3
    assert res.C[1].up.A == [2] and res.C[1].up.b == 0  # +2

def test_mod_pp_p_basic():
    """
    Тестируем MOD_PP_P
    Тест 1: (x^2 - 1) % (x - 1) = 0
    """
    p1 = create_polynomial([
        create_rational(-1), 
        create_rational(0), 
        create_rational(1)
    ])  # x^2 - 1
    
    p2 = create_polynomial([
        create_rational(-1), 
        create_rational(1)
    ])  # x - 1

    res = p1.MOD_PP_P(p2)

    # Ожидаем нулевой остаток
    assert res.DEG_P_N() == 0
    assert res.C[0].up.A == [0]  # 0

def test_mod_pp_p_with_remainder():
    """
    Тест 2: (x^2 + x + 1) % (x - 1) = 3
    """
    p1 = create_polynomial([
        create_rational(1), 
        create_rational(1), 
        create_rational(1)
    ])  # x^2 + x + 1
    
    p2 = create_polynomial([
        create_rational(-1), 
        create_rational(1)
    ])  # x - 1

    res = p1.MOD_PP_P(p2)

    # Проверяем остаток: 3
    assert res.DEG_P_N() == 0
    assert res.C[0].up.A == [3] and res.C[0].up.b == 0  # +3

def test_mod_pp_p_higher_degree_divisor():
    """
    Тест 3: (x + 1) % (x^2 + 1) = x + 1
    Когда степень делителя больше степени делимого, остаток = делимое
    """
    p1 = create_polynomial([
        create_rational(1), 
        create_rational(1)
    ])  # x + 1
    
    p2 = create_polynomial([
        create_rational(1), 
        create_rational(0), 
        create_rational(1)
    ])  # x^2 + 1

    res = p1.MOD_PP_P(p2)

    # Ожидаем исходный многочлен как остаток
    assert res.DEG_P_N() == 1
    assert res.C[0].up.A == [1] and res.C[0].up.b == 0  # +1
    assert res.C[1].up.A == [1] and res.C[1].up.b == 0  # +1

def test_mod_pp_p_complex_division():
    """
    Тест 4: (x^3 + 2x^2 + 3x + 4) % (x^2 + 1) = x + 3
    """
    p1 = create_polynomial([
        create_rational(4), 
        create_rational(3), 
        create_rational(2), 
        create_rational(1)
    ])  # x^3 + 2x^2 + 3x + 4
    
    p2 = create_polynomial([
        create_rational(1), 
        create_rational(0), 
        create_rational(1)
    ])  # x^2 + 1

    res = p1.MOD_PP_P(p2)

    # Проверяем остаток: x + 2
    assert res.DEG_P_N() == 1
    assert res.C[0].up.A == [2] and res.C[0].up.b == 0  # +2
    assert res.C[1].up.A == [2] and res.C[1].up.b == 0  # +2

def test_mod_pp_p_identity():
    """
    Тест 5: Проверка тождества: делимое = делитель * частное + остаток
    (x^3 - 2x^2 + x - 1) % (x^2 + 1)
    """
    p1 = create_polynomial([
        create_rational(-1), 
        create_rational(1), 
        create_rational(-2), 
        create_rational(1)
    ])  # x^3 - 2x^2 + x - 1
    
    p2 = create_polynomial([
        create_rational(1), 
        create_rational(0), 
        create_rational(1)
    ])  # x^2 + 1

    # Вычисляем частное и остаток
    quotient = p1.DIV_PP_P(p2)
    remainder = p1.MOD_PP_P(p2)

    # Проверяем тождество: p1 = p2 * quotient + remainder
    product = p2.MUL_PP_P(quotient)
    reconstructed = product.ADD_PP_P(remainder)

    # Сравниваем коэффициенты реконструированного многочлена с исходным
    assert reconstructed.DEG_P_N() == p1.DEG_P_N()
    for i in range(len(p1.C)):
        assert reconstructed.C[i].up.A == p1.C[i].up.A
        assert reconstructed.C[i].up.b == p1.C[i].up.b

def test_der_p_p_simple():
    """Производная x^3 + 2x^2 + 3x + 4 = 3x^2 + 4x + 3"""
    p = create_polynomial([
        create_rational(4),
        create_rational(3),
        create_rational(2),
        create_rational(1)
    ])
    d = p.DER_P_P()

    assert d.DEG_P_N() == 2
    values = [int(''.join(map(str, c.up.A[::-1]))) for c in d.C]
    assert values == [3, 4, 3]


def test_der_p_p_constant():
    """Производная константы = 0"""
    p = create_polynomial([
        create_rational(5)
    ])
    d = p.DER_P_P()

    assert d.DEG_P_N() == 0
    assert d.C[0].up.A == [0]

def test_gcf_pp_p_normalized():
    """
    Тест: НОД должен быть нормализован (старший коэффициент = 1)
    """
    # НОД(2x^2 + 4x + 2, x^2 + 2x + 1) должен быть x^2 + 2x + 1, а не 2x^2 + 4x + 2
    p1 = create_polynomial([
        create_rational(2), 
        create_rational(4), 
        create_rational(2)
    ])  # 2x^2 + 4x + 2
    
    p2 = create_polynomial([
        create_rational(1), 
        create_rational(2), 
        create_rational(1)
    ])  # x^2 + 2x + 1

    result = p1.GCF_PP_P(p2)
    
    # Проверяем, что результат нормализован (старший коэффициент = 1)
    leading_coef = result.LED_P_Q()
    assert leading_coef.up.A == [1] and leading_coef.up.b == 0  # +1
    
    # Ожидаем: x^2 + 2x + 1
    assert result.DEG_P_N() == 2
    assert result.C[0].up.A == [1] and result.C[0].up.b == 0  # +1
    assert result.C[1].up.A == [2] and result.C[1].up.b == 0  # +2  
    assert result.C[2].up.A == [1] and result.C[2].up.b == 0  # +1

def test_gcf_pp_p_coprime_normalized():
    """
    Тест: НОД взаимно простых многочленов должен быть нормализованной константой 1
    """
    p1 = create_polynomial([
        create_rational(1), 
        create_rational(0), 
        create_rational(1)
    ])  # x^2 + 1
    
    p2 = create_polynomial([
        create_rational(1), 
        create_rational(1)
    ])  # x + 1

    result = p1.GCF_PP_P(p2)
    
    # Ожидаем нормализованную константу 1
    assert result.DEG_P_N() == 0
    assert result.C[0].up.A == [1] and result.C[0].up.b == 0  # +1

def run_complete_nmr_test_suite():
    """
    Полный набор тестов для NMR_P_P
    """
    print("=" * 60)
    print("ПОЛНЫЙ ТЕСТ NMR_P_P")
    print("=" * 60)
    
    # Тест 1: Простой кратный корень (x^2 -> x)
    print("\n1. Простой кратный корень:")
    poly1 = create_polynomial([create_rational(0), create_rational(0), create_rational(1)])
    result1 = poly1.NMR_P_P()
    print(f"   x^2 -> {[str(c) for c in result1.C]}")
    assert result1.DEG_P_N() == 1
    assert result1.C[1].up.A == [1] and result1.C[1].up.b == 0
    
    # Тест 2: Двойной корень ((x-1)^2 -> (x-1))
    print("\n2. Двойной корень:")
    poly2 = create_polynomial([create_rational(1), create_rational(-2), create_rational(1)])
    result2 = poly2.NMR_P_P()
    print(f"   (x-1)^2 -> {[str(c) for c in result2.C]}")
    assert result2.DEG_P_N() == 1
    assert result2.C[0].up.A == [1] and result2.C[0].up.b == 1
    
    # Тест 3: Тройной корень ((x-1)^3 -> (x-1))
    print("\n3. Тройной корень:")
    poly3 = create_polynomial([create_rational(-1), create_rational(3), create_rational(-3), create_rational(1)])
    result3 = poly3.NMR_P_P()
    print(f"   (x-1)^3 -> {[str(c) for c in result3.C]}")
    assert result3.DEG_P_N() == 1
    assert result3.C[0].up.A == [1] and result3.C[0].up.b == 1
    
    # Тест 4: Простые корни ((x-1)(x-2) не изменяется)
    print("\n4. Простые корни:")
    poly4 = create_polynomial([create_rational(2), create_rational(-3), create_rational(1)])
    result4 = poly4.NMR_P_P()
    print(f"   (x-1)(x-2) -> {[str(c) for c in result4.C]}")
    assert result4.DEG_P_N() == 2
    assert result4.C[0].up.A == [2] and result4.C[0].up.b == 0
    
    # Тест 5: Константа (не изменяется)
    print("\n5. Константа:")
    poly5 = create_polynomial([create_rational(5)])
    result5 = poly5.NMR_P_P()
    print(f"   5 -> {[str(c) for c in result5.C]}")
    assert result5.DEG_P_N() == 0
    assert result5.C[0].up.A == [5] and result5.C[0].up.b == 0
    
    # Тест 6: Нулевой многочлен (не изменяется)
    print("\n6. Нулевой многочлен:")
    poly6 = create_polynomial([create_rational(0)])
    result6 = poly6.NMR_P_P()
    print(f"   0 -> {[str(c) for c in result6.C]}")
    assert result6.DEG_P_N() == 0
    assert result6.C[0].up.A == [0]
    
    print("\n" + "=" * 60)
    print("🎉 ВСЕ ТЕСТЫ NMR_P_P УСПЕШНО ПРОЙДЕНЫ!")
    print("=" * 60)

if __name__ == "__main__":
    run_complete_nmr_test_suite()