from natural_module import NaturalModule

class IntegerModule:
    def __init__(self, b: int, n: int, A: list):
        self.b = b  # знак числа (1 - минус, 0 - плюс)
        self.n = n  # номер старшей позиции
        self.A = A  # массив цифр

    def ABS_Z_Z(self):
        """
        Овчаренко 4384

        Алгоритм: для положительных чисел и нуля возвращаем само число, для отрицательных - меняем знак на плюс.
        """
        if self.b:
            self.b = 0
        return self

    def POZ_Z_D(self) -> int:
        """
        Овчаренко 4384

        Алгоритм: проверяем, является ли число нулем (все цифры равны 0), затем смотрим знак.
        """
        # Проверяем, является ли число нулем
        is_zero = True
        for el in self.A:
            if el != 0:
                is_zero = False
                break

        if is_zero:
            return 0
        elif self.b:
            return -1
        else:
            return 1

    def MUL_ZM_Z(self):
        """
        Овчаренко 4384

        Алгоритм: меняем знак числа на противоположный.
        Если число было положительным - становится отрицательным и наоборот.
        Если число является нулём - возвращаем само число.
        """
        # Проверяем, является ли число нулем
        is_zero = True
        for el in self.A:
            if el != 0:
                is_zero = False
                break

        if not is_zero:
            self.b = 1 - self.b
        return self

    def TRANS_N_Z(self, n: int, A: list):
        """
        Овчаренко 4384

        Натуральное число становится неотрицательным целым с тем же массивом цифр.
        Принимает на вход:
            n: номер старшей позиции натурального числа
            A: массив цифр натурального числа
        """
        self.b = 0
        self.n = n
        self.A = A
        return self

    def TRANS_Z_N(self) -> NaturalModule:
        """
        Овчаренко 4384

        Алгоритм: проверяем, что число неотрицательное, затем возвращаем его цифровое представление без знака.
        """
        if self.b:
            raise ValueError("Отрицательное число не подходит для преобразования в натуральное")
        return NaturalModule(self.n, self.A)
    
    def ADD_ZZ_Z(self, other):
        """
        Водолазко 4384

        Принимаемые значения: другое целое число (other)
        Возвращает: результат сложения
        """
        # Определяем знаки чисел
        sign_a = self.POZ_Z_D()
        sign_b = other.POZ_Z_D()
        
        # Если одно из чисел равно нулю
        if sign_a == 0:
            return other
        if sign_b == 0:
            return self
        
        # Получаем натуральные модули чисел
        abs_a = self.ABS_Z_Z().TRANS_Z_N()
        abs_b = other.ABS_Z_Z().TRANS_Z_N()
        
        # Оба числа положительные
        if sign_a == 1 and sign_b == 1:
            result_abs = abs_a.ADD_NN_N(abs_b)
            return IntegerModule(0, result_abs.n, result_abs.A)
        
        # Оба числа отрицательные  
        if sign_a == -1 and sign_b == -1:
            result_abs = abs_a.ADD_NN_N(abs_b)
            return IntegerModule(1, result_abs.n, result_abs.A)
        
        # Числа разных знаков
        comparison = abs_a.COM_NN_D(abs_b)

        # Модули равны - результат ноль
        if comparison == 0:
            return IntegerModule(0, 0, [0])
        
        # Модуль первого числа больше
        if comparison == 2:
            result_abs = abs_a.SUB_NN_N(abs_b)
            # Результат имеет знак первого числа
            if sign_a == 1:
                return IntegerModule(0, result_abs.n, result_abs.A)
            else:
                return IntegerModule(1, result_abs.n, result_abs.A)
        
        # Модуль второго числа больше
        if comparison == 1:
            result_abs = abs_b.SUB_NN_N(abs_a)
            # Результат имеет знак второго числа
            if sign_a == 1:
                return IntegerModule(0, result_abs.n, result_abs.A)
            else:
                return IntegerModule(1, result_abs.n, result_abs.A)

    def SUB_ZZ_Z(self, other):
        """
        Водолазко 4384

        Принимаемые значения: другое целое число (other)
        Возвращает: результ разности
        """
        # Вычитание это сложение с противоположным числом: a - b = a + (-b)
        negative_other = other.MUL_ZM_Z()  # Получаем -other
        return self.ADD_ZZ_Z(negative_other)  # Возвращаем self + (-other)

    def MUL_ZZ_Z(self, other):
        """
        Водолазко 4384

        Принимаемые значения: другое целое число (other)
        Возвращает: результат умножения
        """
        sign_self = self.POZ_Z_D()
        sign_other = other.POZ_Z_D()
        
        # Если одно из чисел равно нулю, результат - ноль
        if sign_self == 0 or sign_other == 0:
            return IntegerModule(0, 0, [0])
        
        # Получаем модули чисел
        abs_self = (self.ABS_Z_Z()).TRANS_Z_N()
        abs_other = (other.ABS_Z_Z()).TRANS_Z_N()
        
        # Умножаем модули (натуральные числа)
        abs_self.MUL_NN_N(abs_other)
        abs_result = NaturalModule(abs_self.n, abs_self.A)
        
        # Создаем целое число с результатом (пока положительное)
        result = IntegerModule(0, abs_result.n, abs_result.A)
        
        # Определяем знак результата
        if (sign_self == -1 and sign_other == 1) or (sign_self == 1 and sign_other == -1):
            # Если знаки разные, результат отрицательный
            result = result.MUL_ZM_Z()
        
        return result

    def DIV_ZZ_Z(self, other):
        """
        Водолазко 4384

        Принимаемые значения: другое целое число (other)
        Возвращает: неполное частное
        """
        # Проверка деления на ноль
        if other.POZ_Z_D() == 0:
            raise Exception("Деление на ноль запрещено")

        sign_a = self.POZ_Z_D()
        sign_b = other.POZ_Z_D()

        # Если делимое равно нулю
        if sign_a == 0:
            return IntegerModule(0, 0, [0])

        # Получаем модули чисел
        abs_a = self.ABS_Z_Z().TRANS_Z_N()
        abs_b = other.ABS_Z_Z().TRANS_Z_N()

        # Сравниваем модули
        comparison = abs_a.COM_NN_D(abs_b)

        # Если модуль делимого меньше модуля делителя
        if comparison == 1:
            # |a| < |b|
            if sign_a == 1 and sign_b == 1:
                return IntegerModule(0, 0, [0])  # 0
            elif sign_a == 1 and sign_b == -1:
                return IntegerModule(1, 0, [0])  # -0 (но исправим на 0)
            elif sign_a == -1 and sign_b == 1:
                # Для отрицательного делимого и положительного делителя
                # результат должен быть -1
                return IntegerModule(1, 0, [1])  # -1
            else:  # оба отрицательные
                return IntegerModule(0, 0, [1])  # 1
        else:
            # Вычисляем частное и остаток от деления модулей
            q0 = abs_a.DIV_NN_N(abs_b)
            product = abs_b.MUL_NN_N(q0)
            r0 = abs_a.SUB_NN_N(product)

            # Проверяем, равен ли остаток нулю
            is_zero_remainder = (r0.n == 0 and r0.A[0] == 0)

            # Определяем знак и корректируем частное
            if sign_a == 1 and sign_b == 1:
                # Оба положительные - результат положительный
                result_sign = 0
                q_result = q0
            elif sign_a == 1 and sign_b == -1:
                # Делимое положительное, делитель отрицательный - результат отрицательный
                result_sign = 1
                q_result = q0
            elif sign_a == -1 and sign_b == 1:
                # Делимое отрицательное, делитель положительный
                if is_zero_remainder:
                    result_sign = 1
                    q_result = q0
                else:
                    # Увеличиваем частное на 1 и делаем отрицательным
                    result_sign = 1
                    one = NaturalModule(0, [1])
                    q_result = q0.ADD_NN_N(one)
            else:
                # Оба отрицательные
                if is_zero_remainder:
                    result_sign = 0
                    q_result = q0
                else:
                    # Увеличиваем частное на 1 и делаем положительным
                    result_sign = 0
                    one = NaturalModule(0, [1])
                    q_result = q0.ADD_NN_N(one)

            # Если частное равно нулю, устанавливаем положительный знак
            if q_result.n == 0 and q_result.A[0] == 0:
                result_sign = 0

            return IntegerModule(result_sign, q_result.n, q_result.A)

    def MOD_ZZ_Z(self, other):
        """
        Водолазко 4384

        Принимаемые значения: другое целое число (other)
        Возвращает: остаток от деления self на other
        """
        a = IntegerModule(self.b, self.n, self.A)
        # Проверка деления на ноль
        if other.POZ_Z_D() == 0:
            raise Exception("Деление на ноль")

        # Вычисляем частное
        q = self.DIV_ZZ_Z(other)

        # Вычисляем произведение other * q
        product = other.MUL_ZZ_Z(q)

        # Вычисляем остаток как self - product
        remainder = a.SUB_ZZ_Z(product)

        return remainder

    def __str__(self) -> str:
        """
        Водолазко 4384

        Метод вывода строкого представления целого числа
        """
        res = ""
        if self.b and self.A != [0]:
            res += "-"
        for i in self.A[::-1]:
            res += str(i)

        return res