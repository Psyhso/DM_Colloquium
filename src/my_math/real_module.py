class RealModule:

    def __init__(self, m : int, C : list):
        self.m = m
        self.C = C
    
    def MUL_Pxk_P(self, k : int):
        """
        Водолазко 4384
        Принимает на вход натуральное число k, степень на которую необходимо умножить полином
        """
        if k < 0:
            print("k должно быть положительным")
            return self
        new_C = self.C + [0] * k
        self.C = new_C
        self.m += k
        return self
    
    def LED_P_Q(self):
        """
        Водолазко 4384
        Возвращает старший коэффициент полинома
        """
        return self.C[0]
    
    def DEG_P_N(self):
        """
        Шакуров 4384 
        Возвращает степень многочлена (количество коэффициентов - 1)
        """
        return len(self.C) - 1

    def DER_P_P(self):
        """
        Шакуров 4384
        Возвращает производную многочлена
        Если многочлен константа, его производная = 0
        Иначе каждый коэффициент (кроме свободного члена) умножаем на степень
        """
        if len(self.C) == 1:
            self.C = [0]
            self.m = 0
            return self
        for i in range(len(self.C) - 1):
            power = len(self.C) - 1 - i
            self.C[i] = self.C[i] * power
        self.C = self.C[:-1]
        self.m -= 1
        return self

