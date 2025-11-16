import re
import sys
from pathlib import Path
from .math_expression_parser import MathExpressionParser
sys.path.append(str(Path(__file__).parent.parent.parent))
from my_math.natural_module import NaturalModule


class NatExpressionParser(MathExpressionParser):
    def __init__(self):
        # Приоритеты операций (чем больше число, тем выше приоритет)
        self.priority = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '%': 2,
            '>': 0
        }
        
        # Список поддерживаемых функций
        self.functions = {'НОД', 'НОК', 'GCD', 'LCM', 'nod', 'nok', 'NZER', 'TM'}
    
   
    def evaluate(self, expression: str, module_class: NaturalModule):
        """
        Вычисляет выражение в ОПН используя NaturalModule
        """
        stack = []
        postfix = self.to_postfix(expression)
        
        for token in postfix:
            # Если число - создаем NaturalModule и помещаем в стек
            if token.isdigit():
                # Преобразуем строку в NaturalModule
                digits = [int(d) for d in token][::-1]  # Младший разряд первый
                n = len(digits) - 1
                num = module_class(n, digits)
                stack.append(num)
            
            # Если бинарный оператор
            elif token in ['+', '-', '*', '/', '%', '^', '>']:
                right = stack.pop()
                left = stack.pop()
                
                # Создаем копию для сохранения исходных значений
                result = module_class(left.n, left.A.copy())
                
                if token == '+':
                    result.ADD_NN_N(right)
                elif token == '-':
                    if result.COM_NN_D(right) != 1:
                        result.SUB_NN_N(right)
                    else:
                        raise Exception("Нельзя из меньшего вычесть большее!")
                elif token == '*':
                    result.MUL_NN_N(right)
                elif token == '/':
                    result.DIV_NN_N(right)
                elif token == '%':
                    result.MOD_NN_N(right)
                elif token == '>':
                    temp = result.COM_NN_D(right)
                    result.A = reversed([int(i) for i in str(temp)])
                    result.n = len(str(temp)) - 1
                
                stack.append(result)
            
            # Если функция НОД или НОК
            elif token in ['НОД', 'GCD', 'NOD']:
                # НОД принимает 2 аргумента
                right = stack.pop()
                left = stack.pop()
                result = module_class(left.n, left.A.copy())
                result.GCF_NN_N(right)
                stack.append(result)
            
            elif token in ['НОК', 'LCM', 'NOK']:
                # НОК принимает 2 аргумента
                right = stack.pop()
                left = stack.pop()
                
                # Вычисляем НОД
                lcm = module_class(left.n, left.A.copy())
                lcm.LCM_NN_N(module_class(right.n, right.A.copy()))

                stack.append(lcm)

            elif token in ['NZER']:
                # NZER принимает 1 аргумент
                number = stack.pop()

                result = module_class(number.n, number.A.copy()).NZER_N_B()
                stack.append(int(result))

            elif token in ['TM']:
                # TM принимает 2 аргумента
                right = stack.pop()
                left = stack.pop()
                print(right, left)
                result = module_class(left.n, left.A.copy()).MUL_Nk_N(int(str(right)))
                stack.append(result)

        
        return str(stack[0]) if stack else None
