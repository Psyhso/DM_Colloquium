class NaturalModule:
    def COM_NN_D(self, n1: int, A1: list, n2: int, A2: list) -> int:
        """
        Баневич 4384

        Принимает на вход: два числа (n1, A1) и (n2, A2)
        Возвращает: 2 - если первое больше, 0 - равны, 1 - второе больше
        """
        if n1 > n2:
            return 2
        elif n1 < n2:
            return 1
        
        # Если одинаковое количество цифр, сравниваем поразрядно от старшей
        for i in range(n1, -1, -1):
            if A1[i] > A2[i]:
                return 2
            elif A1[i] < A2[i]:
                return 1
        return 0
        
    def NZER_N_B(self, n: int, A: list) -> bool:
        """
        Баневич 4384
        
        Принимает на вход: n - номер старшей позиции, A - массив цифр
        Возвращает False если число равно нулю, True иначе.
        """
        if n == 0 and A[0] == 0:
            return False
        return True
    
    def ADD_1N_N(self, n: int, A: list) -> tuple:
        """
        Баневич 4384
        
        Принимает на вход: n - номер старшей позиции, A - массив цифр
        Возвращает: (new_n, new_A) - новое число
        """
        # Копируем массив чтобы не изменять исходный
        new_A = A.copy()
        carry = 1  
        
        # Проходим от младшей цифры
        for i in range(n + 1):
            new_A[i] += carry
            if new_A[i] < 10:
                # Нет переноса, выходим
                carry = 0
                break
            else:
                new_A[i] = 0
                carry = 1
        
        # Если остался перенос, добавляем новую цифру
        if carry == 1:
            new_A.append(1)
            return (n + 1, new_A)
        
        return (n, new_A)
    
    def MUL_ND_N(self, n: int, A: list, d: int) -> tuple:
        """
        Баневич 4384

        Принимает на вход: n, A - число, d - цифра (0-9)
        Возвращает: (new_n, new_A) - результат умножения
        """
        if d == 0:
            return (0, [0])
        
        new_A = []
        carry = 0  # перенос
        
        # Умножаем каждую цифру на d
        for i in range(n + 1):
            temp = A[i] * d + carry
            new_A.append(temp % 10)
            carry = temp // 10
        
        # Если остался перенос, добавляем его
        while carry > 0:
            new_A.append(carry % 10)
            carry = carry // 10
        
        # Определяем новую старшую позицию
        new_n = len(new_A) - 1
        return (new_n, new_A)
    
    def MUL_Nk_N(self, n: int, A: list, k: int) -> tuple:
        """
        Баневич 4384
        
        Принимает на вход: n, A - число, k - степень десятки
        Возвращает: (new_n, new_A) - результат умножения
        """
        # Умножение на 10^k = добавление k нулей справа (в начало массива)
        
        if n == 0 and A[0] == 0:
            return (0, [0])
        
        # Добавляем k нулей в начало массива
        new_A = [0] * k + A
        new_n = n + k
        
        return (new_n, new_A)
