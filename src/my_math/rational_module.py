from natural_module import NaturalModule
from integer_module import IntegerModule

class RationalModule:
    def __init__(self, up: IntegerModule, down: NaturalModule):
        if not down.NZER_N_B():
            raise ValueError("Знаменатель не может быть равен нулю")
        self.up = up
        self.down = down

    def RED_Q_Q(self):
        """
        Овчаренко 4384

        Алгоритм: Находим НОД модуля числителя и знаменателя, затем сокращаем дробь, деля числитель и знаменатель на НОД
        """
        abs_up = NaturalModule(self.up.n, self.up.A)
        gcd = abs_up.GCF_NN_N(NaturalModule(self.down.n, self.down.A))
        if not (gcd.A[0] == 1 and gcd.n == 0):
            self.up = self.up.DIV_ZZ_Z(IntegerModule(0, gcd.n, gcd.A))
            self.down.DIV_NN_N(gcd)
        return self

    def INT_Q_B(self) -> str:
        """
        Боков 4384
        Проверяет, является ли рациональное число целым
        использует числитель и знаменатель из инициализации, возвращает "да" если
        знаменатель=1 (рациональное=целое) иначе "нет"
        """
        if self.down.n == 0 and self.down.A[0] == 1:
            return "да"
        else:
            return "нет"

    def TRANS_Z_Q(self, z: IntegerModule) -> str:
        """
        Боков 4384
        Преобразует целое число в рациональное
        использует целое число z из инициализации, если оно = 0 возвращает "0" 
        иначе переданное число/1
        """
        if z.A[0] == 0 and z.n == 0:
            return "0"
        else:
            return f'{z}/1'

    def TRANS_Q_Z(self) -> IntegerModule:
        """
        Боков 4384
        Преобразует рациональное число в целое (если возможно)
        использует числитель и знаменатель из инициализации, возвращает числитель если
        знаменатель=1 иначе возвращает None
        """
        if self.down.n == 0 and self.down.A[0] == 1:
            return self.up
        else:
            return None
        
    def ADD_QQ_Q(self, other):
        """
        Овчаренко 4384

        Принимает на вход: другую дробь (other)
        Алгоритм: Находим НОК знаменателей, вычисляем дополнительные множители, затем приводим дроби к общему знаменателю и складываем
        """
        lcm = NaturalModule(self.down.n, self.down.A)
        lcm.LCM_NN_N(NaturalModule(other.down.n, other.down.A))

        m1 = NaturalModule(lcm.n, lcm.A).DIV_NN_N(self.down)
        m2 = NaturalModule(lcm.n, lcm.A).DIV_NN_N(other.down)
        
        new_up1 = self.up.MUL_ZZ_Z(IntegerModule(0, m1.n, m1.A))
        new_up2 = other.up.MUL_ZZ_Z(IntegerModule(0, m2.n, m2.A))

        self.up = new_up1.ADD_ZZ_Z(new_up2)
        self.down = lcm
        return self.RED_Q_Q()

    def SUB_QQ_Q(self, other):
        """
        Овчаренко 4384

        Принимает на вход: другую дробь (other)
        Алгоритм: Находим НОК знаменателей, вычисляем дополнительные множители, затем приводим дроби к общему знаменателю и вычитаем
        """
        lcm = NaturalModule(self.down.n, self.down.A)
        lcm.LCM_NN_N(NaturalModule(other.down.n, other.down.A))
        
        m1 = NaturalModule(lcm.n, lcm.A).DIV_NN_N(self.down)
        m2 = NaturalModule(lcm.n, lcm.A).DIV_NN_N(other.down)
        
        new_up1 = self.up.MUL_ZZ_Z(IntegerModule(0, m1.n, m1.A))
        new_up2 = other.up.MUL_ZZ_Z(IntegerModule(0, m2.n, m2.A))

        self.up = new_up1.SUB_ZZ_Z(new_up2)
        self.down = lcm
        return self.RED_Q_Q()

    def MUL_QQ_Q(self, other):
        """
        Овчаренко 4384

        Принимает на вход: другую дробь (other)
        Алгоритм: Умножаем числители и знаменатели части дробей, затем сокращаем дробь
        """
        # СОЗДАЕМ КОПИЮ other, чтобы не изменять исходный объект
        other_copy = RationalModule(
            IntegerModule(other.up.b, other.up.n, other.up.A.copy()),
            NaturalModule(other.down.n, other.down.A.copy())
        )
        
        # Умножаем числители
        new_up = self.up.MUL_ZZ_Z(other_copy.up)
        
        # Умножаем знаменатели  
        new_down = NaturalModule(self.down.n, self.down.A.copy())
        new_down.MUL_NN_N(other_copy.down)
        
        # Обновляем текущий объект
        self.up = new_up
        self.down = new_down
        
        return self.RED_Q_Q()

    def DIV_QQ_Q(self, other):
        """
        Деление рациональных чисел
        """
        # Проверка деления на ноль
        if other.up.POZ_Z_D() == 0:
            raise ZeroDivisionError("Деление на ноль")
        
        # Создаем копии для безопасности
        self_up_copy = IntegerModule(self.up.b, self.up.n, self.up.A.copy())
        self_down_copy = NaturalModule(self.down.n, self.down.A.copy())
        other_up_copy = IntegerModule(other.up.b, other.up.n, other.up.A.copy())
        other_down_copy = NaturalModule(other.down.n, other.down.A.copy())
        
        # Умножаем на обратную дробь: (a/b) / (c/d) = (a*d) / (b*c)
        
        # Преобразуем other_down_copy в IntegerModule для умножения
        other_down_int = IntegerModule(0, other_down_copy.n, other_down_copy.A.copy())
        new_up = self_up_copy.MUL_ZZ_Z(other_down_int)
        
        new_down = NaturalModule(self_down_copy.n, self_down_copy.A.copy())
        
        # Для знаменателя используем модуль числителя other
        other_up_abs = other_up_copy.ABS_Z_Z().TRANS_Z_N()
        new_down.MUL_NN_N(other_up_abs)
        
        # Учитываем знак other
        if other_up_copy.b == 1:  # Если other отрицательный
            new_up = new_up.MUL_ZM_Z()
        
        # Обновляем объект
        self.up = new_up
        self.down = new_down
        
        return self.RED_Q_Q()

    def __str__(self):
        sign = "-" if self.up.b else ""
        return f"{sign}{''.join(map(str, self.up.A[::-1]))}/{''.join(map(str, self.down.A[::-1]))}"