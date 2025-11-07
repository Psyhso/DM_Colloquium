class NaturalModule:

    def __init__(self, n: int, A: list):
        """
        Инициализация натурального числа.
        
        Параметры:
        n (int): номер старшей позиции
        A (list): массив цифр
        """
        self.n = n
        self.A = A
    
    def COM_NN_D(self, other):
        """
        Баневич 4384

        Принимает на вход: другое натуральное число (other)
        Возвращает: 2 - если первое больше, 0 - равны, 1 - второе больше
        """
        if self.n > other.n:
            return 2
        elif self.n < other.n:
            return 1
        
        # Если одинаковое количество цифр, сравниваем поразрядно от старшей
        for i in range(self.n, -1, -1):
            if self.A[i] > other.A[i]:
                return 2
            elif self.A[i] < other.A[i]:
                return 1
        return 0
    
    def NZER_N_B(self):
        """
        Баневич 4384
        
        Возвращает: False если число равно нулю, True иначе
        """
        if self.n == 0 and self.A[0] == 0:
            return False
        return True
    
    def ADD_1N_N(self):
        """
        Баневич 4384
        
        Добавляет 1 к текущему натуральному числу.
        Возвращает: self (изменённый объект)
        """
        carry = 1
        
        # Проходим от младшей цифры
        for i in range(self.n + 1):
            self.A[i] += carry
            if self.A[i] < 10:
                carry = 0
                break
            else:
                self.A[i] = 0
                carry = 1
        # Если остался перенос, добавляем новую цифру
        if carry == 1:
            self.A.append(1)
            self.n += 1
        return self
    
    def MUL_ND_N(self, d: int):
        """
        Баневич 4384

        Принимает на вход: d - цифра (0-9)
        Возвращает: self (изменённый объект)
        """
        if d == 0:
            self.n = 0
            self.A = [0]
            return self
        
        new_A = []
        carry = 0
        
        # Умножаем каждую цифру на d
        for i in range(self.n + 1):
            temp = self.A[i] * d + carry
            new_A.append(temp % 10)
            carry = temp // 10
        
        # Если остался перенос, добавляем его
        while carry > 0:
            new_A.append(carry % 10)
            carry = carry // 10
        self.A = new_A
        self.n = len(new_A) - 1
        return self
    
    def MUL_Nk_N(self, k: int):
        """
        Баневич 4384
        
        Принимает на вход: k - степень десятки
        Возвращает: self (изменённый объект)
        """
        if self.n == 0 and self.A[0] == 0:
            return self
        
        # Добавляем k нулей в начало массива
        self.A = [0] * k + self.A
        self.n = self.n + k
        
        return self
    
    def ADD_NN_N(self, other):
        """
        Баневич 4384
        
        Принимает на вход: другое натуральное число (other)
        Возвращает: self (изменённый объект)
        """
        result_A = []
        carry = 0
        max_len = max(self.n, other.n) + 1
        
        # Складываем цифры с учётом переноса
        for i in range(max_len):
            digit1 = self.A[i] if i <= self.n else 0
            digit2 = other.A[i] if i <= other.n else 0
            temp = digit1 + digit2 + carry
            result_A.append(temp % 10)
            carry = temp // 10
        
        # Если последний перенос, добавляем его
        if carry:
            result_A.append(carry)
        
        self.A = result_A
        self.n = len(result_A) - 1
        return self
    
    def SUB_NN_N(self, other):
        """
        Баневич 4384
        
        Принимает на вход: другое натуральное число (other)
        Возвращает: self (изменённый объект)
        """
        result_A = []
        borrow = 0 #переменная для заимствования 
        
        for i in range(self.n + 1):
            digit1 = self.A[i]
            digit2 = other.A[i] if i <= other.n else 0
            temp = digit1 - digit2 - borrow
            
            # Если результат отрицательный, занимаем из старшей позиции
            if temp < 0:
                temp += 10
                borrow = 1
            else:
                borrow = 0
            
            result_A.append(temp)
        
        # Удаляем ведущие нули
        while len(result_A) > 1 and result_A[-1] == 0:
            result_A.pop()
        
        self.A = result_A
        self.n = len(result_A) - 1
        return self
    
    def MUL_NN_N(self, other):
        """
        Баневич 4384
        
        Принимает на вход: другое натуральное число (other)
        Возвращает: self (изменённый объект)

        Использование в других методах: 1
        """
        # Используем метод умножения столбиком
        result_A = [0] * (self.n + other.n + 2)
        
        for i in range(self.n + 1):
            for j in range(other.n + 1):
                result_A[i + j] += self.A[i] * other.A[j]
        
        # Обрабатывем переносы
        for i in range(len(result_A) - 1):
            result_A[i + 1] += result_A[i] // 10
            result_A[i] %= 10
        
        # Удаляем ведущие нули
        while len(result_A) > 1 and result_A[-1] == 0:
            result_A.pop()
        
        self.A = result_A
        self.n = len(result_A) - 1
        return self
    
    def SUB_NDN_N(self, other, d: int):
        """
        Баневич 4384
        
        Принимает на вход: другое натуральное число (other), цифра d (0-9)
        Возвращает: self (изменённый объект)
        """
        # Вспомогательный объект для вычисления other * d
        temp = NaturalModule(other.n, other.A.copy())
        temp.MUL_ND_N(d)
        
        self.SUB_NN_N(temp)
        return self
    
    def DIV_NN_Dk(self, other):
        """
        Баневич 4384
        
        Принимает на вход: другое натуральное число (other)
        Возвращает: (d, k) - первая цифра частного и степень 10^k
        """
        k = self.n - other.n
        
        # Если делимое меньше делителя, частное пустое
        if k < 0:
            return (0, 0)
        
        # Подбираем максимальную цифру d: d * other * 10^k <= self
        for d in range(9, -1, -1):
            temp = NaturalModule(other.n, other.A.copy())
            temp.MUL_ND_N(d)
            temp.MUL_Nk_N(k)
            
            if temp.COM_NN_D(self) <= 1:
                return (d, k)
        
        return (0, k)
    
    def DIV_NN_N(self, other):
        """
        Баневич 4384
        
        Принимает на вход: другое натуральное число (other)
        Возвращает: self (изменённый объект) - неполное частное
        """
        quotient_A = []
        remainder = NaturalModule(0, [0])
        
        # Процесс длинного деления
        for i in range(self.n, -1, -1):
            # Сдвигаем остаток влево и добавляем следующую цифру
            if not (remainder.n == 0 and remainder.A[0] == 0):
                remainder.MUL_Nk_N(1)
            remainder.A[0] = self.A[i]
            
            # Обновляем n для остатка
            while len(remainder.A) > 1 and remainder.A[-1] == 0:
                remainder.A.pop()
            remainder.n = len(remainder.A) - 1
            
            # Находим максимальную цифру d
            d = 0
            for test_d in range(9, -1, -1):
                temp = NaturalModule(other.n, other.A.copy())
                temp.MUL_ND_N(test_d)
                if temp.COM_NN_D(remainder) != 2:  # temp <= remainder
                    d = test_d
                    break
            
            quotient_A.append(d)
            
            # Вычитаем d * other из остатка
            if d > 0:
                temp = NaturalModule(other.n, other.A.copy())
                temp.MUL_ND_N(d)
                remainder.SUB_NN_N(temp)
        
        quotient_A.reverse()
    
        # Удаляем ведущие нули
        while len(quotient_A) > 1 and quotient_A[-1] == 0:
            quotient_A.pop()
        
        self.A = quotient_A
        self.n = len(quotient_A) - 1
        return self
    
    def MOD_NN_N(self, other):
        """
        Баневич 4384
        
        Принимает на вход: другое натуральное число (other)
        Возвращает: self (изменённый объект) - остаток
        """
        # Формула: остаток = делимое - (делимое // делитель) * делитель
        quotient = NaturalModule(self.n, self.A.copy())
        quotient.DIV_NN_N(other)
        
        temp = NaturalModule(quotient.n, quotient.A.copy())
        temp.MUL_NN_N(other)
        
        self.SUB_NN_N(temp)
        return self
    
    def GCF_NN_N(self, other):
        """
        Баневич 4384
        
        Принимает на вход: другое натуральное число (other)
        Возвращает: self (изменённый объект) - НОД

        Использование в других методах: 1
        """
        # Алгоритм Евклида: НОД(a,b) = НОД(b, a mod b)
        while other.NZER_N_B():
            remainder = NaturalModule(self.n, self.A.copy())
            remainder.MOD_NN_N(other)
            
            self.n = other.n
            self.A = other.A.copy()
            
            other.n = remainder.n
            other.A = remainder.A.copy()
        
        return self


    def LCM_NN_N(self, other):
        """
        Водолазко 4384

        Принимает на вход: другое натуральное число (other)
        Возвращает: res - НОК
        """
        other_1 = NaturalModule(other.n, other.A)
        # Формула связи НОК и НОД: НОК(a,b) = (a*b)/НОД(a,b)
        temp = NaturalModule(self.n, self.A.copy())
        temp.GCF_NN_N(other)  # temp = НОД(a,b)

        self.MUL_NN_N(other_1)  # self = a * b        

        self.DIV_NN_N(temp)  # self = (a*b) / НОД(a,b)

        return self

    def __str__(self):
        return "".join([str(i) for i in self.A])[::-1]