from my_math.integer_module import IntegerModule
import sys
from pathlib import Path
from .math_expression_parser import MathExpressionParser
sys.path.append(str(Path(__file__).parent.parent.parent))


class IntExpressionParser(MathExpressionParser):
    def __init__(self):
        # Таблица приоритетов операторов.
        # Чем больше число, тем выше приоритет.
        self.priority = {
            '+': 1,   # сложение
            '-': 1,   # вычитание (бинарное)
            '*': 2,   # умножение
            '/': 2,   # деление
            '%': 2,   # остаток от деления
            # служебный/низкоприоритетный оператор (если используется)
            '>': 0,
            '~': 3    # унарный минус (искусственный оператор)
        }
        # Множество поддерживаемых функций над целыми.
        # ABS  – модуль числа
        # POZ  – знак числа (результат POZ_Z_D)
        self.functions = {'ABS', 'POZ'}

    def to_postfix(self, expression: str) -> list:
        """
        Преобразует выражение из инфиксной формы в постфиксную (ОПЗ),
        используя модифицированный алгоритм сортировочной станции
        с поддержкой унарного минуса.

        На вход подаётся строка, на выход — список токенов в постфиксном виде.
        """
        # Разбиваем исходную строку на токены (цифры, скобки, операторы, функции).
        tokens = self.tokenize(expression)

        # output  – выходной список с постфиксной записью
        # stack   – стек для временного хранения операторов и функций
        output = []
        stack = []

        for i, token in enumerate(tokens):
            # 1. Если токен – число (состоит только из цифр), выводим его сразу.
            if token.isdigit():
                output.append(token)

            # 2. Если токен – функция (ABS, POZ), кладём её в стек.
            elif token in self.functions or token.upper() in self.functions:
                stack.append(token.upper())

            # 3. Разделитель аргументов функции (запятая):
            #    выталкиваем из стека всё до ближайшей '('.
            elif token == ',':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())

            # 4. Открывающая скобка просто помещается в стек.
            elif token == '(':
                stack.append(token)

            # 5. Закрывающая скобка:
            #    выталкиваем операторы до соответствующей '(',
            #    затем убираем '(' и, если на вершине стека стоит функция,
            #    переносим её в выход.
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()
                if stack and stack[-1] in self.functions:
                    output.append(stack.pop())

            # 6. Специальная обработка '-' для различения унарного и бинарного минуса.
            elif token == '-':
                # Минус считается унарным, если:
                #   - он стоит в самом начале выражения,
                #   - перед ним оператор,
                #   - перед ним открывающая скобка,
                #   - перед ним запятая (аргументы функции).
                is_unary = (
                    i == 0 or
                    tokens[i - 1] in self.priority or
                    tokens[i - 1] == '(' or
                    tokens[i - 1] == ','
                )

                if is_unary:
                    # Унарный минус реализуется через искусственный оператор '~'
                    # с собственным приоритетом.
                    while (stack and
                           stack[-1] != '(' and
                           stack[-1] in self.priority and
                           self.priority[stack[-1]] >= self.priority['~']):
                        output.append(stack.pop())
                    stack.append('~')
                else:
                    # Обычный (бинарный) минус:
                    # выталкиваем из стека все операторы с приоритетом
                    # не ниже, чем у '-', затем кладём '-' в стек.
                    while (stack and
                           stack[-1] != '(' and
                           stack[-1] in self.priority and
                           self.priority[stack[-1]] >= self.priority[token]):
                        output.append(stack.pop())
                    stack.append(token)

            # 7. Остальные операторы (+, *, /, %, >):
            #    выталкиваем из стека операторы с приоритетом не ниже текущего.
            elif token in self.priority:
                while (stack and
                       stack[-1] != '(' and
                       stack[-1] in self.priority and
                       self.priority[stack[-1]] >= self.priority[token]):
                    output.append(stack.pop())
                stack.append(token)

        # 8. После обработки всех токенов выталкиваем оставшиеся операторы из стека.
        while stack:
            if stack[-1] != '(':
                output.append(stack.pop())
            else:
                # На случай незакрытых скобок просто удаляем '('.
                stack.pop()

        return output

    def evaluate(self, expression: str, module_class: IntegerModule):
        """
        Вычисляет значение целочисленного выражения.

        expression  – строка с выражением (в инфиксной записи),
        module_class – класс IntegerModule, используется для создания объектов.

        Возвращает строковое представление результата (str(stack[0])).
        """
        stack = []

        # Получаем список токенов в постфиксной записи.
        postfix = self.to_postfix(expression)

        for token in postfix:
            # 1. Если это число – создаём объект IntegerModule и кладём в стек.
            if token.isdigit():
                # массив цифр в обратном порядке
                digits = [int(d) for d in token][::-1]
                n = len(digits) - 1                    # индекс старшей цифры
                num = module_class(0, n, digits)       # знак 0 = положительное
                stack.append(num)

            # 2. Унарный минус '~':
            #    снимаем один операнд со стека, меняем знак и кладём обратно.
            elif token == '~':
                operand = stack.pop()
                # Создаём новый объект с противоположным знаком: 0 -> 1, 1 -> 0.
                result = module_class(
                    1 - operand.b,    # новый знак
                    operand.n,        # степень
                    operand.A.copy()  # копия массива цифр
                )
                stack.append(result)

            # 3. Бинарные арифметические операторы.
            elif token in ['+', '-', '*', '/', '%']:
                # Снимаем два операнда: left (левый), right (правый).
                right = stack.pop()
                left = stack.pop()

                # Выполняем соответствующую операцию методов IntegerModule.
                if token == '+':
                    result = left.ADD_ZZ_Z(right)
                elif token == '-':
                    result = left.SUB_ZZ_Z(right)
                elif token == '*':
                    result = left.MUL_ZZ_Z(right)
                elif token == '/':
                    result = left.DIV_ZZ_Z(right)
                elif token == '%':
                    result = left.MOD_ZZ_Z(right)

                # Результат кладём обратно в стек.
                stack.append(result)

            # 4. Функция ABS: модуль числа.
            elif token == 'ABS':
                operand = stack.pop()
                result = operand.ABS_Z_Z()   # метод возвращает |operand|
                stack.append(result)

            # 5. Функция POZ: признак знака.
            #    POZ_Z_D() возвращает:
            #       0 – если число равно 0,
            #       1 – если число > 0,
            #       2 – если число < 0.
            elif token == 'POZ':
                operand = stack.pop()
                result = operand.POZ_Z_D()

                # Преобразуем результат (целое Python) обратно в IntegerModule.
                # Формируем массив цифр без возможного минуса.
                digits = [int(d) for d in str(result) if d != '-'][::-1]
                # n — индекс старшей цифры: длина строки без знака минус минус 1
                n = len(str(result)) - \
                    2 if result < 0 else len(str(result)) - 1
                # Определяем знак: 0 – неотрицательное, 1 – отрицательное.
                num = module_class(0 if result > 0 else 1, n, digits)
                stack.append(num)

        # В стеке должен остаться единственный элемент – результат вычисления.
        # Возвращаем его строковое представление.
        return str(stack[0]) if stack else None
