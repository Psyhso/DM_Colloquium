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

        Параметры:
        - self: первый многочлен (текущий объект)
        - other: второй многочлен (объект того же класса)

        Возвращает:
        - result: произведение многочленов self × other
        """
        # Создаем нулевой рациональный коэффициент 0/1
        zero = RationalModule(IntegerModule(0, 0, [0]), NaturalModule(0, [1]))

        # Создаем нулевой многочлен степени 0 с коэффициентом 0
        # RealModule(0, [zero]) - многочлен степени 0 с одним коэффициентом [0]
        result = RealModule(0, [zero])

        # Перебираем все коэффициенты первого многочлена self
        # i - степень (индекс коэффициента)
        # coef - коэффициент при x^i в первом многочлене
        for i, coef in enumerate(self.C):
            # Шаг 1: Умножаем весь второй многочлен на коэффициент coef
            # MUL_PQ_P - умножение многочлена на рациональное число (скаляр)
            # temp = other × coef (каждый коэффициент other умножается на coef)
            temp = other.MUL_PQ_P(coef)

            # Шаг 2: Сдвигаем полученный многочлен на i позиций вправо
            # MUL_Pxk_P - умножение многочлена на x^k (сдвиг коэффициентов)
            # temp = temp × x^i (добавляет i нулевых коэффициентов в начало)
            temp = temp.MUL_Pxk_P(i)

            # Шаг 3: Прибавляем полученный многочлен к текущему результату
            # ADD_PP_P - сложение двух многочленов
            # result = result + temp
            result = result.ADD_PP_P(temp)

        # Проверяем, что все коэффициенты равны нулю
        # c.up.A - числитель рационального числа (коэффициента)
        # [0] - представление нуля в модуле целых чисел
        if all(c.up.A == [0] for c in result.C):
            # Если все коэффициенты нулевые, создаем канонический нулевой многочлен
            # степени 0 с одним нулевым коэффициентом
            result = RealModule(0, [zero])

        return result

    def DIV_PP_P(self, other):
        """
        Шакуров 4384
        Деление многочленов (алгоритм деления в столбик)
        Вычисляет частное от деления self на other

        Параметры:
        - self: делимое (многочлен)
        - other: делитель (многочлен)

        Возвращает:
        - Q: частное от деления

        Использует: DEG_P_N, LED_P_Q, DIV_QQ_Q, MUL_Pxk_P, ADD_PP_P, SUB_PP_P
        """
        # Проверка деления на нулевой многочлен
        # Если все коэффициенты делителя равны нулю, вызываем ошибку
        if all(c.up.A == [0] for c in other.C):
            raise ZeroDivisionError("Деление на нулевой многочлен")

        # Создаем глубокую копию делимого (self) для работы с остатком R
        # Это нужно, чтобы не изменять исходный многочлен
        # Копируем каждый коэффициент с сохранением всех свойств
        R = RealModule(self.m, [RationalModule(
            IntegerModule(c.up.b, c.up.n, c.up.A.copy()),  # Копируем числитель
            # Копируем знаменатель
            NaturalModule(c.down.n, c.down.A.copy())
        ) for c in self.C])

        # Инициализируем частное Q как нулевой многочлен
        # RationalModule(IntegerModule(0, 0, [0]), NaturalModule(0, [1])) - создает рациональный 0
        Q = RealModule(
            0, [RationalModule(IntegerModule(0, 0, [0]), NaturalModule(0, [1]))])

        # Вычисляем максимально возможную разницу степеней для оценки количества итераций
        max_degree_diff = self.DEG_P_N() - other.DEG_P_N()
        # Устанавливаем максимальное количество итераций с запасом
        # Запас нужен для обработки возможных проблем с округлением при работе с дробями
        max_iterations = max_degree_diff + 10

        iteration = 0  # Счетчик итераций для защиты от бесконечного цикла

        # Основной цикл деления в столбик
        # Продолжаем, пока степень остатка >= степени делителя
        while R.DEG_P_N() >= other.DEG_P_N() and iteration < max_iterations:
            iteration += 1

            # Проверяем, не стал ли остаток нулевым
            # Если все коэффициенты остатка равны нулю, деление завершено
            if all(c.up.A == [0] for c in R.C):
                break

            # Получаем старшие коэффициенты (leading coefficients) остатка и делителя
            # LED_P_Q() возвращает коэффициент при старшей степени
            lc_R = R.LED_P_Q()  # Старший коэффициент остатка
            lc_B = other.LED_P_Q()  # Старший коэффициент делителя

            # Создаем копию старшего коэффициента остатка для деления
            coef = RationalModule(
                IntegerModule(lc_R.up.b, lc_R.up.n, lc_R.up.A.copy()),
                NaturalModule(lc_R.down.n, lc_R.down.A.copy())
            )
            # Делим старший коэффициент остатка на старший коэффициент делителя
            # Это дает коэффициент для следующего члена частного
            coef.DIV_QQ_Q(lc_B)

            # Вычисляем степень, на которую нужно сдвинуть
            # Разность степеней остатка и делителя определяет степень x в текущем члене
            k = R.DEG_P_N() - other.DEG_P_N()

            # Формируем одночлен для добавления к частному
            # Создаем многочлен из одного коэффициента coef и сдвигаем его на k позиций
            term = RealModule(0, [coef]).MUL_Pxk_P(k)

            # Добавляем полученный одночлен к частному
            Q = Q.ADD_PP_P(term)

            # Вычисляем вычитаемое: делитель × coef × x^k
            subtrahend = other.MUL_PQ_P(coef).MUL_Pxk_P(k)

            # Вычитаем из остатка полученное выражение
            # Это эквивалентно вычитанию в алгоритме деления в столбик
            R = R.SUB_PP_P(subtrahend)

            # Удаляем ведущие нулевые коэффициенты из остатка
            # Это важно для корректного определения степени на следующей итерации
            while len(R.C) > 1:
                last_coef = R.C[-1]  # Берем старший коэффициент
                # Проверяем, является ли коэффициент нулевым
                if last_coef.up.A == [0] or (last_coef.up.n == 0 and last_coef.up.A[0] == 0):
                    R.C.pop()  # Удаляем нулевой коэффициент
                else:
                    break  # Встретили ненулевой коэффициент - останавливаемся

            # Обновляем степень многочлена остатка
            R.m = len(R.C) - 1

        # Возвращаем частное от деления
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
            # простое целочисленное умножение
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
        Вычисляет остаток от деления многочлена self на многочлен other

        Параметры:
        - self: делимое (многочлен)
        - other: делитель (многочлен)

        Возвращает:
        - remainder: остаток от деления self на other

        Использует: DIV_PP_P, MUL_PP_P, SUB_PP_P, POZ_Z_D
        """

        # Вспомогательная функция для проверки, является ли многочлен нулевым
        def is_zero_poly(p):
            """
            Проверяет, является ли многочлен нулевым
            POZ_Z_D() возвращает:
            - 0 если число равно нулю
            - 1 если число положительное  
            - 2 если число отрицательное
            """
            return all(coef.up.POZ_Z_D() == 0 for coef in p.C)

        # Проверка деления на нулевой многочлен
        if is_zero_poly(other):
            raise ZeroDivisionError("Деление на нулевой многочлен")

        # Шаг 1: Вычисляем частное от деления
        # DIV_PP_P реализует алгоритм деления многочленов в столбик
        # и возвращает частное (целую часть от деления)
        Q = self.DIV_PP_P(other)

        # Шаг 2: Вычисляем произведение делителя на частное
        # Это должно дать нам ту часть делимого, которая делится нацело
        # MUL_PP_P - умножение многочленов
        product = other.MUL_PP_P(Q)

        # Шаг 3: Вычисляем остаток
        # Остаток - это разность между исходным многочленом и произведением делителя на частное
        # SUB_PP_P - вычитание многочленов
        remainder = self.SUB_PP_P(product)

        # Шаг 4: Удаляем ведущие нулевые коэффициенты из остатка
        # Это необходимо для канонического представления многочлена

        # Пока в остатке больше одного коэффициента и старший коэффициент равен нулю
        while len(remainder.C) > 1 and remainder.C[-1].up.POZ_Z_D() == 0:
            remainder.C.pop()  # Удаляем нулевой старший коэффициент

        # Обновляем степень многочлена (степень = количество коэффициентов - 1)
        remainder.m = len(remainder.C) - 1

        # Возвращаем остаток от деления
        return remainder

    def GCF_PP_P(self, other):
        """
        Шакуров 4384
        НОД многочленов с нормализацией
        Вычисляет наибольший общий делитель двух многочленов

        Параметры:
        - self: первый многочлен
        - other: второй многочлен

        Возвращает:
        - result: НОД многочленов, нормализованный (старший коэффициент = 1)

        Использует: DEG_P_N, MOD_PP_P, LED_P_Q, DIV_QQ_Q
        """
        # Создаем глубокие копии многочленов для работы
        # Это необходимо, чтобы не изменять исходные многочлены
        A = RealModule(self.m, [RationalModule(
            IntegerModule(c.up.b, c.up.n, c.up.A.copy()),  # Копируем числитель
            # Копируем знаменатель
            NaturalModule(c.down.n, c.down.A.copy())
        ) for c in self.C])

        B = RealModule(other.m, [RationalModule(
            IntegerModule(c.up.b, c.up.n, c.up.A.copy()),  # Копируем числитель
            # Копируем знаменатель
            NaturalModule(c.down.n, c.down.A.copy())
        ) for c in other.C])

        def is_zero_poly(p):
            """Проверка: все коэффициенты равны 0?"""
            for coef in p.C:
                # Проверяем, что коэффициент не равен нулю
                # coef.up.n == 0 - длина массива цифр = 0 (число 0)
                # coef.up.A[0] == 0 - единственная цифра = 0
                if not (coef.up.n == 0 and coef.up.A[0] == 0):
                    return False
            return True

        # Алгоритм Евклида с улучшенными условиями остановки
        max_iterations = 100  # Защита от бесконечного цикла
        iteration = 0

        # Основной цикл алгоритма Евклида
        # Продолжаем, пока B не станет нулевым многочленом
        while not is_zero_poly(B) and iteration < max_iterations:
            iteration += 1

            # Если степень B больше степени A, меняем местами
            # Это гарантирует, что A всегда имеет большую или равную степень
            if B.DEG_P_N() > A.DEG_P_N():
                A, B = B, A
                continue

            # Вычисляем остаток от деления A на B
            # R = A mod B (остаток от деления A на B)
            R = A.MOD_PP_P(B)

            # Если остаток имеет степень меньше чем B, продолжаем алгоритм
            if R.DEG_P_N() < B.DEG_P_N():
                A, B = B, R  # Переходим к следующей итерации: A = B, B = R
            else:
                # Если степени равны, возможно, мы нашли НОД
                # Это условие выхода для случая, когда дальнейшее деление не уменьшает степень
                break

        # Предупреждение при достижении предела итераций
        if iteration >= max_iterations:
            print(
                f"⚠️  Достигнут предел итераций. Возвращаем последний ненулевой остаток.")

        # Определяем результат:
        # Если B стал нулевым, то НОД = A
        # Иначе НОД = B (последний ненулевой остаток)
        result = A if is_zero_poly(B) else B

        # Нормализация результата (делаем старший коэффициент равным 1)
        if not is_zero_poly(result):
            # Получаем старший коэффициент многочлена
            leading_coef = result.LED_P_Q()

            # Проверяем, не равен ли уже старший коэффициент 1
            # Если нет - нормализуем весь многочлен
            if not (leading_coef.up.n == 0 and leading_coef.up.A[0] == 1 and leading_coef.up.b == 0):
                # Создаем новый список коэффициентов, поделенных на старший коэффициент
                new_coeffs = []
                for coef in result.C:
                    # Создаем копию коэффициента
                    coef_copy = RationalModule(
                        IntegerModule(coef.up.b, coef.up.n, coef.up.A.copy()),
                        NaturalModule(coef.down.n, coef.down.A.copy())
                    )
                    # Делим коэффициент на старший коэффициент
                    coef_copy.DIV_QQ_Q(leading_coef)
                    new_coeffs.append(coef_copy)

                # Создаем нормализованный многочлен
                result = RealModule(result.m, new_coeffs)

        return result

    def NMR_P_P(self):
        """
        Шакуров 4384
        Преобразование многочлена — кратные корни в простые
        Возвращает многочлен с теми же корнями, но без кратности

        Математическая основа:
        Если P(x) = (x - a)ᵏ * Q(x), где Q(a) ≠ 0,
        то после преобразования получим P(x) / НОД(P, P') = (x - a) * Q(x)

        Возвращает:
        - Многочлен с простыми корнями (все корни имеют кратность 1)
        """
        # Проверка для многочленов степени 0 или отрицательной
        # Если многочлен константный (степень ≤ 0), преобразование не требуется
        # Константные многочлены не имеют корней или имеют бесконечно много корней
        if self.DEG_P_N() <= 0:
            return self

        # Шаг 1: Вычисляем производную многочлена
        # DER_P_P() вычисляет формальную производную многочлена
        # Например: если P(x) = x³, то P'(x) = 3x²
        derivative = self.DER_P_P()

        # Шаг 2: Вычисляем НОД исходного многочлена и его производной
        # GCF_PP_P() находит наибольший общий делитель двух многочленов
        # Если многочлен имеет кратные корни, то НОД(P, P') будет содержать
        # эти корни с кратностью на 1 меньше
        gcd = self.GCF_PP_P(derivative)

        # Шаг 3: Проверяем, является ли НОД константой (многочленом степени 0)
        # Если НОД - константа, это означает, что у исходного многочлена
        # все корни простые (не имеют кратности)
        if gcd.DEG_P_N() == 0:
            # В этом случае возвращаем исходный многочлен без изменений
            return self

        # Шаг 4: Делим исходный многочлен на НОД(P, P')
        # Это удаляет кратность корней:
        # Если P(x) = (x - a)ᵏ * Q(x), то:
        # - P'(x) содержит (x - a)ᵏ⁻¹ как множитель
        # - НОД(P, P') = (x - a)ᵏ⁻¹
        # - P(x) / НОД(P, P') = (x - a) * Q(x)
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
