from my_math.rational_module import RationalModule
from my_math.integer_module import IntegerModule
from my_math.natural_module import NaturalModule
import sys
from pathlib import Path
from .math_expression_parser import MathExpressionParser
import re

sys.path.append(str(Path(__file__).parent.parent.parent))


class RatExpressionParser(MathExpressionParser):
    def __init__(self):
        self.priority = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '~': 3  # Унарный минус
        }
        self.functions = {'RED', 'INT'}  # Функции для рациональных чисел

    def tokenize(self, expression: str) -> list:
        """
        Токенизация с правильной обработкой минуса
        """
        expression = expression.replace(' ', '')
        tokens = []
        i = 0
        
        while i < len(expression):
            # Пропускаем пробелы
            if expression[i] == ' ':
                i += 1
                continue
            
            # Проверяем, может ли это быть отрицательная дробь
            # (минус унарный, если перед ним оператор, скобка или начало строки)
            if expression[i] == '-':
                # Смотрим, что было перед минусом
                if i == 0 or (tokens and tokens[-1] in ['(', '+', '-', '*', '/', ',']):
                    # Это может быть унарный минус - проверяем, есть ли дробь после
                    match = re.match(r'-\d+/\d+', expression[i:])
                    if match:
                        tokens.append(match.group())
                        i += len(match.group())
                        continue
                    # Или просто отрицательное число
                    match = re.match(r'-\d+', expression[i:])
                    if match:
                        tokens.append(match.group())
                        i += len(match.group())
                        continue
                
                # Если не унарный минус, добавляем как оператор
                tokens.append('-')
                i += 1
                continue
            
            # Проверяем положительную дробь
            match = re.match(r'\d+/\d+', expression[i:])
            if match:
                tokens.append(match.group())
                i += len(match.group())
                continue
            
            # Проверяем целое число
            match = re.match(r'\d+', expression[i:])
            if match:
                tokens.append(match.group())
                i += len(match.group())
                continue
            
            # Проверяем функции
            match = re.match(r'(RED|INT)', expression[i:])
            if match:
                tokens.append(match.group())
                i += len(match.group())
                continue
            
            # Проверяем операторы и скобки
            if expression[i] in '+*/(),':
                tokens.append(expression[i])
                i += 1
                continue
            
            # Неизвестный символ - пропускаем
            i += 1
        
        return tokens

    def parse_rational(self, token: str) -> RationalModule:
        """
        Парсинг токена в объект RationalModule
        """
        if '/' in token:
            # Парсим дробь
            parts = token.split('/')
            numerator_str = parts[0]
            denominator_str = parts[1]

            # Обрабатываем числитель (может быть отрицательным)
            is_negative = numerator_str.startswith('-')
            if is_negative:
                numerator_str = numerator_str[1:]

            # Создаем IntegerModule для числителя
            num_digits = [int(d) for d in numerator_str][::-1]
            numerator = IntegerModule(
                1 if is_negative else 0,
                len(num_digits) - 1,
                num_digits
            )

            # Создаем NaturalModule для знаменателя
            den_digits = [int(d) for d in denominator_str][::-1]
            denominator = NaturalModule(
                len(den_digits) - 1,
                den_digits
            )

            return RationalModule(numerator, denominator)
        else:
            # Парсим целое число как дробь с знаменателем 1
            is_negative = token.startswith('-')
            if is_negative:
                token = token[1:]

            digits = [int(d) for d in token][::-1]
            numerator = IntegerModule(
                1 if is_negative else 0,
                len(digits) - 1,
                digits
            )

            denominator = NaturalModule(0, [1])

            return RationalModule(numerator, denominator)

    def to_postfix(self, expression: str) -> list:
        """
        Преобразование инфиксной записи в постфиксную с поддержкой дробей
        """
        tokens = self.tokenize(expression)
        output = []
        stack = []

        for i, token in enumerate(tokens):
            # Проверяем, является ли токен числом или дробью
            if re.match(r'-?\d+(/\d+)?$', token):
                output.append(token)

            elif token in self.functions or token.upper() in self.functions:
                stack.append(token.upper())

            elif token == ',':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())

            elif token == '(':
                stack.append(token)

            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()
                if stack and stack[-1] in self.functions:
                    output.append(stack.pop())

            elif token == '-':
                # УЛУЧШЕННАЯ проверка унарного минуса
                # Минус унарный, если:
                # 1. Стоит в начале выражения
                # 2. После оператора
                # 3. После открывающей скобки
                # 4. После запятой
                prev_token = tokens[i-1] if i > 0 else None
                
                is_unary = (
                    i == 0 or
                    prev_token in self.priority or
                    prev_token == '(' or
                    prev_token == ','
                )
                
                # КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ: если предыдущий токен - число или дробь,
                # то минус БИНАРНЫЙ
                if prev_token and re.match(r'-?\d+(/\d+)?$', prev_token):
                    is_unary = False

                if is_unary:
                    while (stack and
                        stack[-1] != '(' and
                        stack[-1] in self.priority and
                        self.priority[stack[-1]] >= self.priority['~']):
                        output.append(stack.pop())
                    stack.append('~')
                else:
                    while (stack and
                        stack[-1] != '(' and
                        stack[-1] in self.priority and
                        self.priority[stack[-1]] >= self.priority[token]):
                        output.append(stack.pop())
                    stack.append(token)

            elif token in self.priority:
                while (stack and
                    stack[-1] != '(' and
                    stack[-1] in self.priority and
                    self.priority[stack[-1]] >= self.priority[token]):
                    output.append(stack.pop())
                stack.append(token)

        while stack:
            if stack[-1] != '(':
                output.append(stack.pop())
            else:
                stack.pop()

        return output

    def evaluate(self, expression: str) -> str:
        """
        Вычисление выражения с рациональными числами
        """
        stack = []
        postfix = self.to_postfix(expression)

        for token in postfix:
            # Если токен - число или дробь
            if re.match(r'-?\d+(/\d+)?', token):
                rational = self.parse_rational(token)
                stack.append(rational)

            elif token == '~':  # Унарный минус
                operand = stack.pop()
                # Меняем знак числителя
                result = RationalModule(
                    IntegerModule(
                        1 - operand.up.b,
                        operand.up.n,
                        operand.up.A.copy()
                    ),
                    NaturalModule(
                        operand.down.n,
                        operand.down.A.copy()
                    )
                )
                stack.append(result)

            elif token in ['+', '-', '*', '/']:
                right = stack.pop()
                left = stack.pop()

                # Создаем копии для безопасности
                left_copy = RationalModule(
                    IntegerModule(left.up.b, left.up.n, left.up.A.copy()),
                    NaturalModule(left.down.n, left.down.A.copy())
                )

                if token == '+':
                    result = left_copy.ADD_QQ_Q(right)
                elif token == '-':
                    result = left_copy.SUB_QQ_Q(right)
                elif token == '*':
                    result = left_copy.MUL_QQ_Q(right)
                elif token == '/':
                    result = left_copy.DIV_QQ_Q(right)

                stack.append(result)

            elif token == 'RED':
                # Сокращение дроби
                operand = stack.pop()
                result = operand.RED_Q_Q()
                stack.append(result)

            elif token == 'INT':
                # Проверка на целое число
                operand = stack.pop()
                # Возвращаем результат проверки как строку
                is_integer = operand.INT_Q_B()
                # Для дальнейших вычислений оставляем операнд в стеке
                stack.append(1 if is_integer == 'да' else 0)

        return str(stack[0]) if stack else None
