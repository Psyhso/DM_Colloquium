import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
import re
from my_math.natural_module import NaturalModule


class MathExpressionParser:
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
    
    def tokenize(self, expression: str) -> list:
        """
        Разбивает выражение на токены: числа, операторы, функции, скобки, запятые
        """
        # Паттерн для: функции, числа, операторы, скобки, запятые
        pattern = r'([А-Яа-яA-Za-z_][А-Яа-яA-Za-z0-9_]*|\d+|[+\-*/%(),>^])'
        tokens = re.findall(pattern, expression.replace(' ', ''))
        return tokens
    
    def to_postfix(self, expression: str) -> list:
        """
        Преобразует инфиксное выражение в постфиксное (ОПН)
        с поддержкой функций НОД и НОК
        """
        tokens = self.tokenize(expression)
        output = []       # Выходная очередь
        stack = []        # Стек операторов
        
        for i, token in enumerate(tokens):
            # 1. Если число - добавляем в выход
            if token.isdigit():
                output.append(token)
            
            # 2. Если функция - помещаем в стек
            elif token in self.functions or token.upper() in self.functions:
                stack.append(token.upper())
            
            # 3. Если запятая - выталкиваем до открывающей скобки
            elif token == ',':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                # Запятая НЕ попадает в выход
            
            # 4. Если открывающая скобка
            elif token == '(':
                stack.append(token)
            
            # 5. Если закрывающая скобка
            elif token == ')':
                # Выталкиваем до открывающей скобки
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                
                if stack and stack[-1] == '(':
                    stack.pop()  # Удаляем '('
                
                # Если после скобки была функция - добавляем её в выход
                if stack and stack[-1] in self.functions:
                    output.append(stack.pop())
            
            # 6. Если оператор
            elif token in self.priority:
                # Выталкиваем операторы с >= приоритетом
                while (stack and 
                       stack[-1] != '(' and 
                       stack[-1] in self.priority and
                       self.priority[stack[-1]] >= self.priority[token]):
                    output.append(stack.pop())
                stack.append(token)
        
        # 7. Выталкиваем оставшиеся операторы
        while stack:
            if stack[-1] != '(':
                output.append(stack.pop())
            else:
                stack.pop()
        
        return output
    
    def evaluate(self, expression: str, natural_module_class: NaturalModule):
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
                num = natural_module_class(n, digits)
                stack.append(num)
            
            # Если бинарный оператор
            elif token in ['+', '-', '*', '/', '%', '^', '>']:
                right = stack.pop()
                left = stack.pop()
                
                # Создаем копию для сохранения исходных значений
                result = natural_module_class(left.n, left.A.copy())
                
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
                result = natural_module_class(left.n, left.A.copy())
                result.GCF_NN_N(right)
                stack.append(result)
            
            elif token in ['НОК', 'LCM', 'NOK']:
                # НОК принимает 2 аргумента
                right = stack.pop()
                left = stack.pop()
                
                # Вычисляем НОД
                lcm = natural_module_class(left.n, left.A.copy())
                lcm.LCM_NN_N(natural_module_class(right.n, right.A.copy()))

                stack.append(lcm)

            elif token in ['NZER']:
                # NZER принимает 1 аргумент
                number = stack.pop()

                result = natural_module_class(number.n, number.A.copy()).NZER_N_B()
                stack.append(int(result))

            elif token in ['TM']:
                # TM принимает 2 аргумента
                right = stack.pop()
                left = stack.pop()
                print(right, left)
                result = natural_module_class(left.n, left.A.copy()).MUL_Nk_N(int(str(right)))
                stack.append(result)

        
        return str(stack[0]) if stack else None
