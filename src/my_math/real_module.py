class RealModule:
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
