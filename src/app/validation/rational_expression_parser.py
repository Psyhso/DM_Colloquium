from my_math.rational_module import RationalModule
from my_math.integer_module import IntegerModule
from my_math.natural_module import NaturalModule
import sys
from pathlib import Path
from .math_expression_parser import MathExpressionParser
import re


# Добавляем корень проекта в sys.path, чтобы модули my_math корректно импортировались
sys.path.append(str(Path(__file__).parent.parent.parent))


class RatExpressionParser(MathExpressionParser):
    def __init__(self):
        # Таблица приоритетов операторов:
        # чем больше число — тем выше приоритет
        self.priority = {
            '+': 1,   # сложение
            '-': 1,   # вычитание (бинарный минус)
            '*': 2,   # умножение
            '/': 2,   # деление
            '~': 3    # унарный минус (специальный внутренний оператор)
        }
        # Множество имён функций, которые поддерживаются поверх рациональных чисел
        # RED – сокращение дроби, INT – проверка, является ли дробь целым числом
        self.functions = {'RED', 'INT'}  # Функции для рациональных чисел

    def tokenize(self, expression: str) -> list:
        """
        Токенизация с правильной обработкой минуса.

        Разбивает строку на токены:
        - целые числа и дроби (в т.ч. с ведущим минусом, если он унарный),
        - имена функций RED/INT,
        - знаки операций и скобки.

        Важный момент: минус может быть частью числа (унарный) или отдельным
        оператором вычитания (бинарный). Здесь сразу пытаемся "прикрепить"
        унарный минус к числу / дроби.
        """
        # Удаляем пробелы на всякий случай
        expression = expression.replace(' ', '')
        tokens = []
        i = 0

        while i < len(expression):
            # На этот момент пробелов уже нет, но оставляем защиту
            if expression[i] == ' ':
                i += 1
                continue

            # Обработка символа '-': он может быть началом отрицательного числа/дроби
            # или отдельным оператором вычитания.
            if expression[i] == '-':
                # Смотрим, что было до минуса:
                # - начало строки,
                # - оператор или открывающая скобка,
                # - запятая (аргументы функции)
                if i == 0 or (tokens and tokens[-1] in ['(', '+', '-', '*', '/', ',']):
                    # Пытаемся распознать отрицательную дробь вида -a/b
                    match = re.match(r'-\d+/\d+', expression[i:])
                    if match:
                        tokens.append(match.group())
                        i += len(match.group())
                        continue
                    # Иначе пытаемся распознать просто отрицательное целое -a
                    match = re.match(r'-\d+', expression[i:])
                    if match:
                        tokens.append(match.group())
                        i += len(match.group())
                        continue

                # Если выше не сработало — минус считался бинарным оператором
                tokens.append('-')
                i += 1
                continue

            # Положительная дробь a/b
            match = re.match(r'\d+/\d+', expression[i:])
            if match:
                tokens.append(match.group())
                i += len(match.group())
                continue

            # Положительное целое число a
            match = re.match(r'\d+', expression[i:])
            if match:
                tokens.append(match.group())
                i += len(match.group())
                continue

            # Функции RED или INT
            match = re.match(r'(RED|INT)', expression[i:])
            if match:
                tokens.append(match.group())
                i += len(match.group())
                continue

            # Операторы и скобки
            if expression[i] in '+*/(),':
                tokens.append(expression[i])
                i += 1
                continue

            # Если символ не узнали — просто пропускаем его
            i += 1

        return tokens

    def parse_rational(self, token: str) -> RationalModule:
        """
        Парсинг строкового токена в объект RationalModule.

        Поддерживаем два формата:
        - дробь: 'a/b' или '-a/b'
        - целое: 'a' или '-a' (интерпретируется как a/1)
        """
        if '/' in token:
            # Формат дроби: числитель/знаменатель
            parts = token.split('/')
            numerator_str = parts[0]      # может быть с минусом
            denominator_str = parts[1]

            # Проверяем знак числителя
            is_negative = numerator_str.startswith('-')
            if is_negative:
                # убираем '-' для разбора цифр
                numerator_str = numerator_str[1:]

            # Создаём IntegerModule для числителя
            num_digits = [int(d) for d in numerator_str][::-1]
            numerator = IntegerModule(
                1 if is_negative else 0,       # 1 – отрицательное, 0 – положительное
                len(num_digits) - 1,
                num_digits
            )

            # Создаём NaturalModule для знаменателя
            den_digits = [int(d) for d in denominator_str][::-1]
            denominator = NaturalModule(
                len(den_digits) - 1,
                den_digits
            )

            return RationalModule(numerator, denominator)
        else:
            # Токен – целое число (со знаком или без), приводим к виду a/1
            is_negative = token.startswith('-')
            if is_negative:
                token = token[1:]

            digits = [int(d) for d in token][::-1]
            numerator = IntegerModule(
                1 if is_negative else 0,
                len(digits) - 1,
                digits
            )

            # Знаменатель = 1
            denominator = NaturalModule(0, [1])

            return RationalModule(numerator, denominator)

    def to_postfix(self, expression: str) -> list:
        """
        Преобразование инфиксной записи в постфиксную (ОПЗ) с поддержкой дробей
        и унарного минуса.

        На вход: строка вида '1/2-3/4+RED(5/6)'.
        На выход: список токенов в обратной польской записи.
        """
        tokens = self.tokenize(expression)
        output = []  # сюда пишем результат
        stack = []   # стек операторов и функций

        for i, token in enumerate(tokens):
            # Если токен – число или дробь (включая возможный ведущий '-'),
            # отправляем его сразу в выход.
            if re.match(r'-?\d+(/\d+)?$', token):
                output.append(token)

            # Функции (RED, INT) кладём в стек
            elif token in self.functions or token.upper() in self.functions:
                stack.append(token.upper())

            # Запятая – разделитель аргументов функции:
            # выталкиваем всё до ближайшей '('
            elif token == ',':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())

            # Открывающая скобка — просто в стек
            elif token == '(':
                stack.append(token)

            # Закрывающая скобка — выталкиваем до '(',
            # затем, если на вершине стека функция, отправляем её в выход
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()
                if stack and stack[-1] in self.functions:
                    output.append(stack.pop())

            # Обработка '-' как возможного унарного/бинарного оператора
            elif token == '-':
                # Минус считается унарным, если:
                #   - стоит в начале выражения,
                #   - после оператора,
                #   - после '(',
                #   - после запятой.
                prev_token = tokens[i - 1] if i > 0 else None

                is_unary = (
                    i == 0 or
                    prev_token in self.priority or
                    prev_token == '(' or
                    prev_token == ','
                )

                # ВАЖНЫЙ МОМЕНТ:
                # если перед минусом уже стоит число/дробь (в т.ч. с минусом),
                # то это точно бинарный минус.
                if prev_token and re.match(r'-?\d+(/\d+)?$', prev_token):
                    is_unary = False

                if is_unary:
                    # Для унарного минуса используем искусственный оператор '~'
                    while (stack and
                           stack[-1] != '(' and
                           stack[-1] in self.priority and
                           self.priority[stack[-1]] >= self.priority['~']):
                        output.append(stack.pop())
                    stack.append('~')
                else:
                    # Обычный бинарный минус
                    while (stack and
                           stack[-1] != '(' and
                           stack[-1] in self.priority and
                           self.priority[stack[-1]] >= self.priority[token]):
                        output.append(stack.pop())
                    stack.append(token)

            # Любой другой оператор из таблицы приоритетов (+, *, /)
            elif token in self.priority:
                while (stack and
                       stack[-1] != '(' and
                       stack[-1] in self.priority and
                       self.priority[stack[-1]] >= self.priority[token]):
                    output.append(stack.pop())
                stack.append(token)

        # Выталкиваем оставшиеся операторы из стека
        while stack:
            if stack[-1] != '(':
                output.append(stack.pop())
            else:
                stack.pop()

        return output

    def evaluate(self, expression: str) -> str:
        """
        Вычисление выражения с рациональными числами.

        1. Строка переводится в постфиксную форму.
        2. Постфикс вычисляется, используя стек объектов RationalModule.
        3. Возвращается строковое представление результата (через __str__ у RationalModule)
           либо строка с результатом INT/RED в зависимости от выражения.
        """
        stack = []
        postfix = self.to_postfix(expression)

        for token in postfix:
            # Число или дробь → объект RationalModule → в стек
            if re.match(r'-?\d+(/\d+)?', token):
                rational = self.parse_rational(token)
                stack.append(rational)

            # Унарный минус '~': меняем знак числителя
            elif token == '~':
                operand = stack.pop()
                # Создаём новый RationalModule с противоположным знаком числителя
                result = RationalModule(
                    IntegerModule(
                        1 - operand.up.b,      # инвертируем бит знака
                        operand.up.n,
                        operand.up.A.copy()
                    ),
                    NaturalModule(
                        operand.down.n,
                        operand.down.A.copy()
                    )
                )
                stack.append(result)

            # Бинарные операторы над рациональными
            elif token in ['+', '-', '*', '/']:
                right = stack.pop()
                left = stack.pop()

                # Делаем копию левого операнда, чтобы не портить исходный объект
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

            # RED: сокращаем дробь
            elif token == 'RED':
                operand = stack.pop()
                result = operand.RED_Q_Q()
                stack.append(result)

            # INT: проверяем, является ли рациональное число целым
            elif token == 'INT':
                operand = stack.pop()
                # INT_Q_B возвращает строку "да"/"нет"
                is_integer = operand.INT_Q_B()
                # Для дальнейших вычислений кладём в стек 1 или 0,
                # чтобы при желании можно было продолжать считать.
                stack.append(1 if is_integer == 'да' else 0)

        # В стеке должен остаться единственный элемент — результат
        return str(stack[0]) if stack else None
