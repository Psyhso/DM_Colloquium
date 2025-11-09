import pytest
from my_math.real_module import RealModule
from my_math.natural_module import NaturalModule
from my_math.integer_module import IntegerModule
from my_math.rational_module import RationalModule

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