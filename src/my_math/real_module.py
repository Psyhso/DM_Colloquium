from natural_module import NaturalModule
from integer_module import IntegerModule
from rational_module import RationalModule


class RealModule:
    def __init__(self, m: int, C: list):
        self.m = m  # степень многочлена
        self.C = C  # коэффициенты (объекты RationalModule)

    def ADD_PP_P(self, other):
        """
        Сложение многочленов
        Боков 4384

        Алгоритм:
        1. Определить максимальную степень среди двух многочленов
        2. Для каждой степени от 0 до максимальной:
           - Взять коэффициенты при одинаковых степенях из обоих многочленов
           - Если коэффициент отсутствует, считать его равным нулю
           - Сложить коэффициенты 
        3. Вернуть новый многочлен с полученными коэффициентами
        """
        max_degree = max(self.DEG_P_N(), other.DEG_P_N())
        new_C = []

        for i in range(max_degree + 1):
            # Получаем коэффициенты или нулевые если вышли за границы
            coef1 = self.C[i] if i < len(self.C) else RationalModule(
                IntegerModule(0, 0, [0]), NaturalModule(0, [1]))
            coef2 = other.C[i] if i < len(other.C) else RationalModule(
                IntegerModule(0, 0, [0]), NaturalModule(0, [1]))

            # Создаем копии коэффициентов
            coef1_copy = RationalModule(
                IntegerModule(coef1.up.b, coef1.up.n, coef1.up.A.copy()),
                NaturalModule(coef1.down.n, coef1.down.A.copy())
            )
            coef2_copy = RationalModule(
                IntegerModule(coef2.up.b, coef2.up.n, coef2.up.A.copy()),
                NaturalModule(coef2.down.n, coef2.down.A.copy())
            )

            # Складываем коэффициенты
            result_coef = coef1_copy.ADD_QQ_Q(coef2_copy)
            new_C.append(result_coef)

        return RealModule(max_degree, new_C)

    def SUB_PP_P(self, other):
        """
        Вычитание многочленов
        Боков 4384

        Алгоритм:
        1. Определить максимальную степень среди двух многочленов
        2. Для каждой степени от 0 до максимальной:
           - Взять коэффициенты при одинаковых степенях из обоих многочленов
           - Если коэффициент отсутствует, считать его равным нулю
           - Вычесть коэффициенты 
        3. Вернуть новый многочлен с полученными коэффициентами
        """
        max_degree = max(self.DEG_P_N(), other.DEG_P_N())
        new_C = []

        for i in range(max_degree + 1):
            # Получаем коэффициенты или нулевые если вышли за границы
            coef1 = self.C[i] if i < len(self.C) else RationalModule(
                IntegerModule(0, 0, [0]), NaturalModule(0, [1]))
            coef2 = other.C[i] if i < len(other.C) else RationalModule(
                IntegerModule(0, 0, [0]), NaturalModule(0, [1]))

            # Создаем копии коэффициентов
            coef1_copy = RationalModule(
                IntegerModule(coef1.up.b, coef1.up.n, coef1.up.A.copy()),
                NaturalModule(coef1.down.n, coef1.down.A.copy())
            )
            coef2_copy = RationalModule(
                IntegerModule(coef2.up.b, coef2.up.n, coef2.up.A.copy()),
                NaturalModule(coef2.down.n, coef2.down.A.copy())
            )

            # Вычитаем коэффициенты
            result_coef = coef1_copy.SUB_QQ_Q(coef2_copy)
            new_C.append(result_coef)

        return RealModule(max_degree, new_C)

    def MUL_PQ_P(self, q: RationalModule):
        """
        Умножение многочлена на рациональное число
        Боков 4384

        Алгоритм:
        1. Если множитель равен нулю, вернуть нулевой многочлен
        2. Для каждого коэффициента многочлена:
        - Умножить коэффициент на заданное рациональное число 
        3. Вернуть новый многочлен с полученными коэффициентами
        """
        # Если умножаем на ноль, возвращаем нулевой многочлен
        if q.up.POZ_Z_D() == 0:
            return RealModule(0, [RationalModule(IntegerModule(0, 0, [0]), NaturalModule(0, [1]))])

        # СОЗДАЕМ КОПИЮ рационального числа, чтобы не изменять исходный
        q_copy = RationalModule(
            IntegerModule(q.up.b, q.up.n, q.up.A.copy()),
            NaturalModule(q.down.n, q.down.A.copy())
        )

        new_C = []

        for coef in self.C:
            # Создаем копию коэффициента
            coef_copy = RationalModule(
                IntegerModule(coef.up.b, coef.up.n, coef.up.A.copy()),
                NaturalModule(coef.down.n, coef.down.A.copy())
            )

            # Умножаем на копию рационального числа
            result_coef = coef_copy.MUL_QQ_Q(q_copy)
            new_C.append(result_coef)

        return RealModule(self.m, new_C)

    def MUL_Pxk_P(self, k: int):
        """
        Боков 4384
        Умножение многочлена на x^k

        Алгоритм:
        1. Проверить, что k неотрицательное
        2. Если k = 0, вернуть исходный многочлен
        3. Добавить k нулевых коэффициентов в начало массива коэффициентов
        4. Вернуть новый многочлен с увеличенной степенью
        """
        if k < 0:
            raise ValueError("k must be non-negative")

        if k == 0:
            return self

        # Создаем k нулевых коэффициентов
        zero_coef = RationalModule(
            IntegerModule(0, 0, [0]),
            NaturalModule(0, [1])
        )
        new_C = [zero_coef] * k + self.C

        return RealModule(self.m + k, new_C)

    def LED_P_Q(self):
        """
        Боков 4384
        Старший коэффициент многочлена

        Алгоритм:
        1. Если массив коэффициентов пуст, вернуть нулевое рациональное число
        2. Иначе вернуть последний коэффициент массива (старший коэффициент)
        """
        if not self.C:
            return RationalModule(
                IntegerModule(0, 0, [0]),
                NaturalModule(0, [1])
            )
        return self.C[-1]

    def DEG_P_N(self):
        """
        Боков 4384
        Степень многочлена
        """
        return len(self.C) - 1

    def FAC_P_Q(self):
        """
        Боков 4384
        Вынесение из многочлена НОК знаменателей коэффициентов и НОД числителей

        Алгоритм:
        1. Если все коэффициенты нулевые, вернуть 1/1
        2. Найти НОК всех знаменателей коэффициентов 
        3. Найти НОД всех числителей коэффициентов (взятых по модулю) 
           - Для каждого числителя получить его модуль 
           - Вычислить НОД полученных натуральных чисел
        4. Преобразовать НОК знаменателей в целое число 
        5. Вернуть рациональное число: НОК знаменателей / НОД числителей
        """
        # Если многочлен нулевой, возвращаем 1/1
        if all(coef.up.A == [0] for coef in self.C):
            one_int = IntegerModule(0, 0, [1])
            one_natural = NaturalModule(0, [1])
            return RationalModule(one_int, one_natural)

        # Находим НОК всех знаменателей
        lcm_denom = None
        for coef in self.C:
            if coef.up.A != [0]:  # Пропускаем нулевые коэффициенты
                if lcm_denom is None:
                    lcm_denom = NaturalModule(coef.down.n, coef.down.A.copy())
                else:
                    current_denom = NaturalModule(
                        coef.down.n, coef.down.A.copy())
                    lcm_denom = lcm_denom.LCM_NN_N(current_denom)

        # Находим НОД всех числителей (взятых по модулю)
        gcd_num = None
        for coef in self.C:
            if coef.up.A != [0]:  # Пропускаем нулевые коэффициенты
                # Получаем модуль числителя
                abs_num = coef.up.ABS_Z_Z()  # Используем ABS_Z_Z для получения модуля

                if gcd_num is None:
                    gcd_num = NaturalModule(abs_num.n, abs_num.A.copy())
                else:
                    current_num = NaturalModule(abs_num.n, abs_num.A.copy())
                    gcd_num = gcd_num.GCF_NN_N(current_num)

        # Если все коэффициенты нулевые
        if lcm_denom is None:
            one_int = IntegerModule(0, 0, [1])
            one_natural = NaturalModule(0, [1])
            return RationalModule(one_int, one_natural)

        # Преобразуем НОК знаменателей в целое число
        lcm_int = IntegerModule(0, 0, [0])
        lcm_int = lcm_int.TRANS_N_Z(lcm_denom.n, lcm_denom.A.copy())

        # Создаем результирующее рациональное число
        return RationalModule(lcm_int, gcd_num)

    def MUL_PP_P(self, other):
        """
        Шакуров 4384
        Умножение многочленов
        Использует: MUL_PQ_P, MUL_Pxk_P, ADD_PP_P
        """
        # Нулевой результат
        zero = RationalModule(IntegerModule(0, 0, [0]), NaturalModule(0, [1]))
        result = RealModule(0, [zero])

        # Перебираем все коэффициенты первого многочлена
        for i, coef in enumerate(self.C):
            # Умножаем второй многочлен на коэффициент coef
            temp = other.MUL_PQ_P(coef)
            # Сдвигаем на x^i
            temp = temp.MUL_Pxk_P(i)
            # Прибавляем к результату
            result = result.ADD_PP_P(temp)
        # Если результат — нулевой многочлен, обрезаем его до степени 0
        if all(c.up.A == [0] for c in result.C):
            result = RealModule(0, [zero])

        return result

    def DIV_PP_P(self, other):
        """
        Шакуров 4384
        Деление многочленов
        """
        if all(c.up.A == [0] for c in other.C):
            raise ZeroDivisionError("Деление на нулевой многочлен")

        R = RealModule(self.m, [RationalModule(
            IntegerModule(c.up.b, c.up.n, c.up.A.copy()),
            NaturalModule(c.down.n, c.down.A.copy())
        ) for c in self.C])

        Q = RealModule(
            0, [RationalModule(IntegerModule(0, 0, [0]), NaturalModule(0, [1]))])

        max_degree_diff = self.DEG_P_N() - other.DEG_P_N()
        max_iterations = max_degree_diff + 10  # Запас на случай проблем с округлением

        iteration = 0

        while R.DEG_P_N() >= other.DEG_P_N() and iteration < max_iterations:
            iteration += 1

            # Проверяем, что остаток не нулевой
            if all(c.up.A == [0] for c in R.C):
                break

            lc_R = R.LED_P_Q()
            lc_B = other.LED_P_Q()

            # Деление старших коэффициентов
            coef = RationalModule(
                IntegerModule(lc_R.up.b, lc_R.up.n, lc_R.up.A.copy()),
                NaturalModule(lc_R.down.n, lc_R.down.A.copy())
            )
            coef.DIV_QQ_Q(lc_B)

            k = R.DEG_P_N() - other.DEG_P_N()

            # Формируем одночлен
            term = RealModule(0, [coef]).MUL_Pxk_P(k)

            # Добавляем к частному
            Q = Q.ADD_PP_P(term)

            # Вычитаем
            subtrahend = other.MUL_PQ_P(coef).MUL_Pxk_P(k)
            R = R.SUB_PP_P(subtrahend)

            # Удаляем ведущие нули в остатке
            while len(R.C) > 1:
                last_coef = R.C[-1]
                if last_coef.up.A == [0] or (last_coef.up.n == 0 and last_coef.up.A[0] == 0):
                    R.C.pop()
                else:
                    break
            R.m = len(R.C) - 1

        return Q

    def DER_P_P(self):
        """
        Шакуров 4384
        Вычисляет производную многочлена.
        Не использует другие функции.
        Возвращает новый многочлен (RealModule).
        """
        # Если многочлен константа — производная равна 0
        if self.m == 0:
            zero = RationalModule(
                IntegerModule(0, 0, [0]),
                NaturalModule(0, [1])
            )
            return RealModule(0, [zero])

        new_coeffs = []

        # Для каждого коэффициента начиная со второго (a1*x^1, a2*x^2, ...)
        for i in range(1, len(self.C)):
            coef = self.C[i]
            # умножаем коэффициент на степень i (натуральное число)
            # создаём новый RationalModule вручную
            new_up = IntegerModule(
                coef.up.b,  # знак
                coef.up.n,
                coef.up.A.copy()
            )

            # умножаем числитель на i
            # простое целочисленное умножение (без MUL_ZZ_Z)
            carry = 0
            res = []
            A = new_up.A.copy()
            for digit in A:
                prod = digit * i + carry
                res.append(prod % 10)
                carry = prod // 10
            while carry > 0:
                res.append(carry % 10)
                carry //= 10
            new_up.A = res
            new_up.n = len(res)

            # знаменатель не меняется
            new_down = NaturalModule(coef.down.n, coef.down.A.copy())

            new_coeffs.append(RationalModule(new_up, new_down))

        # создаём новый многочлен
        deg = len(new_coeffs) - 1
        return RealModule(deg, new_coeffs)

    def MOD_PP_P(self, other):
        """
        Шакуров 4384
        Остаток от деления
        """
        def is_zero_poly(p):
            return all(coef.up.POZ_Z_D() == 0 for coef in p.C)

        if is_zero_poly(other):
            raise ZeroDivisionError("Деление на нулевой многочлен")

        # Используем существующий DIV_PP_P и проверяем результат
        Q = self.DIV_PP_P(other)

        product = other.MUL_PP_P(Q)

        remainder = self.SUB_PP_P(product)

        # Удаляем ведущие нули
        while len(remainder.C) > 1 and remainder.C[-1].up.POZ_Z_D() == 0:
            remainder.C.pop()
        remainder.m = len(remainder.C) - 1

        return remainder

    def GCF_PP_P(self, other):
        """
        Шакуров 4384
        НОД многочленов с нормализацией
        """
        # Создаем копии многочленов для работы
        A = RealModule(self.m, [RationalModule(
            IntegerModule(c.up.b, c.up.n, c.up.A.copy()),
            NaturalModule(c.down.n, c.down.A.copy())
        ) for c in self.C])

        B = RealModule(other.m, [RationalModule(
            IntegerModule(c.up.b, c.up.n, c.up.A.copy()),
            NaturalModule(c.down.n, c.down.A.copy())
        ) for c in other.C])

        def is_zero_poly(p):
            """Проверка: все коэффициенты равны 0?"""
            for coef in p.C:
                if not (coef.up.n == 0 and coef.up.A[0] == 0):
                    return False
            return True

        # Алгоритм Евклида с улучшенными условиями остановки
        max_iterations = 100
        iteration = 0

        while not is_zero_poly(B) and iteration < max_iterations:
            iteration += 1

            # Если степень B больше степени A, меняем местами
            if B.DEG_P_N() > A.DEG_P_N():
                A, B = B, A
                continue

            R = A.MOD_PP_P(B)

            # Если остаток имеет степень меньше чем B, продолжаем
            if R.DEG_P_N() < B.DEG_P_N():
                A, B = B, R
            else:
                # Если степени равны, возможно, мы нашли НОД
                break

        if iteration >= max_iterations:
            print(
                f"⚠️  Достигнут предел итераций. Возвращаем последний ненулевой остаток.")

        # Если B стал нулевым, НОД = A, иначе НОД = B
        result = A if is_zero_poly(B) else B

        # Нормализация
        if not is_zero_poly(result):
            leading_coef = result.LED_P_Q()

            if not (leading_coef.up.n == 0 and leading_coef.up.A[0] == 1 and leading_coef.up.b == 0):
                new_coeffs = []
                for coef in result.C:
                    coef_copy = RationalModule(
                        IntegerModule(coef.up.b, coef.up.n, coef.up.A.copy()),
                        NaturalModule(coef.down.n, coef.down.A.copy())
                    )
                    coef_copy.DIV_QQ_Q(leading_coef)
                    new_coeffs.append(coef_copy)

                result = RealModule(result.m, new_coeffs)

        return result

    def NMR_P_P(self):
        """
        Шакуров 4384
        Преобразование многочлена — кратные корни в простые
        """
        if self.DEG_P_N() <= 0:
            return self

        derivative = self.DER_P_P()
        gcd = self.GCF_PP_P(derivative)

        # Если НОД - константа, значит корни простые, возвращаем исходный многочлен
        if gcd.DEG_P_N() == 0:
            return self

        # Иначе делим на НОД
        return self.DIV_PP_P(gcd)

    def __str__(self):
        """
        Красивое строковое представление многочлена
        """
        if self.DEG_P_N() == 0:
            # Константный многочлен
            return str(self.C[0])

        terms = []

        # Проходим по коэффициентам от старшей степени к младшей
        for i in range(len(self.C) - 1, -1, -1):
            coef = self.C[i]

            # Пропускаем нулевые коэффициенты
            if coef.up.POZ_Z_D() == 0:
                continue

            degree = i

            # Используем существующий __str__ для RationalModule
            coef_str = str(coef)

            # Упрощаем запись для коэффициента 1 и -1
            if coef_str == "1/1":
                coef_str = "1"
            elif coef_str == "-1/1":
                coef_str = "-1"

            # Форматируем член многочлена
            if degree == 0:
                term = coef_str
            elif degree == 1:
                if coef_str == "1" or coef_str == "-1":
                    term = "x" if coef_str == "1" else "-x"
                else:
                    term = f"{coef_str}x"
            else:
                if coef_str == "1" or coef_str == "-1":
                    term = f"x^{degree}" if coef_str == "1" else f"-x^{degree}"
                else:
                    term = f"{coef_str}x^{degree}"

            # Добавляем знак (уже учтен в coef_str для первого члена)
            if terms:  # Не первый член
                if coef_str.startswith('-'):
                    terms.append(f" - {term[1:]}")
                else:
                    terms.append(f" + {term}")
            else:  # Первый член
                terms.append(term)

        if not terms:  # Все коэффициенты нулевые
            return "0"

        return "".join(terms)
