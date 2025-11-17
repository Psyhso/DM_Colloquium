import pytest
from ..my_math.rational_module import RationalModule
from ..my_math.integer_module import IntegerModule
from ..my_math.natural_module import NaturalModule


def test_int_q_b():
    """Тест проверки целого числа"""
    print("=== ТЕСТ ПРОВЕРКИ ЦЕЛОГО ЧИСЛА (INT_Q_B) ===")

    # Тест 1: 5/1 - целое
    up1 = IntegerModule(0, 0, [5])      # 5
    down1 = NaturalModule(0, [1])       # 1
    rational1 = RationalModule(up1, down1)
    result1 = rational1.INT_Q_B()
    print(f"5/1 = {result1}")

    # Тест 2: 3/2 - не целое
    up2 = IntegerModule(0, 0, [3])      # 3
    down2 = NaturalModule(0, [2])       # 2
    rational2 = RationalModule(up2, down2)
    result2 = rational2.INT_Q_B()
    print(f"3/2 = {result2}")

    # Тест 3: -4/1 - целое
    up3 = IntegerModule(1, 0, [4])      # -4
    down3 = NaturalModule(0, [1])       # 1
    rational3 = RationalModule(up3, down3)
    result3 = rational3.INT_Q_B()
    print(f"-4/1 = {result3} ")

    print()


def test_trans_z_q():
    """Тест преобразования целого в рациональное"""
    print("=== ТЕСТ ПРЕОБРАЗОВАНИЯ ЦЕЛОГО В РАЦИОНАЛЬНОЕ (TRANS_Z_Q) ===")

    # Тест 1: 5 -> 5/1
    z1 = IntegerModule(0, 0, [5])       # 5
    rational1 = RationalModule(z1, NaturalModule(0, [1]))
    result1 = rational1.TRANS_Z_Q(z1)
    print(f"5 = {result1}")

    # Тест 2: -3 -> -3/1
    z2 = IntegerModule(1, 0, [3])       # -3
    rational2 = RationalModule(z2, NaturalModule(0, [1]))
    result2 = rational2.TRANS_Z_Q(z2)
    print(f"-3 = {result2}")

    # Тест 3: 0 -> 0
    z3 = IntegerModule(0, 0, [0])       # 0
    rational3 = RationalModule(z3, NaturalModule(0, [1]))
    result3 = rational3.TRANS_Z_Q(z3)
    print(f"0 = {result3}")

    print()


def test_trans_q_z():
    """Тест преобразования рационального в целое"""
    print("=== ТЕСТ ПРЕОБРАЗОВАНИЯ РАЦИОНАЛЬНОГО В ЦЕЛОЕ (TRANS_Q_Z) ===")

    # Тест 1: 5/1 -> 5
    up1 = IntegerModule(0, 0, [5])      # 5
    down1 = NaturalModule(0, [1])       # 1
    rational1 = RationalModule(up1, down1)
    result1 = rational1.TRANS_Q_Z()
    print(f"5/1 -> {result1}")

    # Тест 2: -3/1 -> -3
    up2 = IntegerModule(1, 0, [3])      # -3
    down2 = NaturalModule(0, [1])       # 1
    rational2 = RationalModule(up2, down2)
    result2 = rational2.TRANS_Q_Z()
    print(f"-3/1 -> {result2}")

    # Тест 3: 3/2 -> None (не целое)
    up3 = IntegerModule(0, 0, [3])      # 3
    down3 = NaturalModule(0, [2])       # 2
    rational3 = RationalModule(up3, down3)
    result3 = rational3.TRANS_Q_Z()
    print(f"3/2 -> {result3}")

    print()
