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