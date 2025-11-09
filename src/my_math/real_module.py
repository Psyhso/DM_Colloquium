from integer_module import *
from rational_module import *
from natural_module import *

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
            coef1 = self.C[i] if i < len(self.C) else RationalModule(IntegerModule(0, 0, [0]), NaturalModule(0, [1]))
            coef2 = other.C[i] if i < len(other.C) else RationalModule(IntegerModule(0, 0, [0]), NaturalModule(0, [1]))
            
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
            coef1 = self.C[i] if i < len(self.C) else RationalModule(IntegerModule(0, 0, [0]), NaturalModule(0, [1]))
            coef2 = other.C[i] if i < len(other.C) else RationalModule(IntegerModule(0, 0, [0]), NaturalModule(0, [1]))
            
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
        
        new_C = []
        
        for coef in self.C:
            # Создаем копию коэффициента
            coef_copy = RationalModule(
                IntegerModule(coef.up.b, coef.up.n, coef.up.A.copy()),
                NaturalModule(coef.down.n, coef.down.A.copy())
            )
            
            # Умножаем на заданное рациональное число
            result_coef = coef_copy.MUL_QQ_Q(q)
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
                    current_denom = NaturalModule(coef.down.n, coef.down.A.copy())
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