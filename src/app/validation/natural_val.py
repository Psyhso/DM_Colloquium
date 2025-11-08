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
            '%': 2
        }
        
        # Список поддерживаемых функций
        self.functions = {'НОД', 'НОК', 'GCF', 'LCM', 'nod', 'nok'}
    
    def tokenize(self, expression):
        """
        Разбивает выражение на токены: числа, операторы, функции, скобки, запятые
        """
        # Паттерн для: функции, числа, операторы, скобки, запятые
        pattern = r'([А-Яа-яA-Za-z_][А-Яа-яA-Za-z0-9_]*|\d+|[+\-*/%(),])'
        tokens = re.findall(pattern, expression.replace(' ', ''))
        return tokens
    
    def to_postfix(self, expression):
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
    
    def evaluate(self, expression, natural_module_class):
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
            elif token in ['+', '-', '*', '/', '%']:
                right = stack.pop()
                left = stack.pop()
                
                # Создаем копию для сохранения исходных значений
                result = natural_module_class(left.n, left.A.copy())
                
                if token == '+':
                    result.ADD_NN_N(right)
                elif token == '-':
                    result.SUB_NN_N(right)
                elif token == '*':
                    result.MUL_NN_N(right)
                elif token == '/':
                    result.DIV_NN_N(right)
                elif token == '%':
                    result.MOD_NN_N(right)
                
                stack.append(result)
            
            # Если функция НОД или НОК
            elif token in ['НОД', 'GCF', 'NOD']:
                # НОД принимает 2 аргумента
                right = stack.pop()
                left = stack.pop()
                result = natural_module_class(left.n, left.A.copy())
                result.GCF_NN_N(right)
                stack.append(result)
            
            elif token in ['НОК', 'LCM', 'NOK']:
                # НОК принимает 2 аргумента
                # НОК(a,b) = (a*b) / НОД(a,b)
                right = stack.pop()
                left = stack.pop()
                
                # Вычисляем НОД
                gcd = natural_module_class(left.n, left.A.copy())
                gcd.GCF_NN_N(natural_module_class(right.n, right.A.copy()))
                
                # Вычисляем a*b
                product = natural_module_class(left.n, left.A.copy())
                product.MUL_NN_N(right)
                
                # НОК = (a*b) / НОД
                product.DIV_NN_N(gcd)
                stack.append(product)
        
        return str(stack[0]) if stack else None


# parser = MathExpressionParser()
# out = parser.evaluate("10+14", NaturalModule)
# print(type(out))

# a = NaturalModule(1, [0, 5])
# b = NaturalModule(0, [5])
# print(b)

# print(a.GCF_NN_N(b).A, a.GCF_NN_N(b).n)
# print(val_natural("НОД(7, 13)").A, val_natural("НОД(7, 13)").n)