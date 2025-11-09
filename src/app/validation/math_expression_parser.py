import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
import re
from abc import ABC, abstractmethod
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
        pattern = r'([А-Яа-яA-Za-z_][А-Яа-яA-Za-z0-9_]*|\d+|[+\-*/%(),>])'
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
    
    @abstractmethod
    def evaluate(self, expression: str, module_class):
        pass
