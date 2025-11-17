from my_math.rational_module import RationalModule
from my_math.integer_module import IntegerModule
from my_math.natural_module import NaturalModule
from my_math.real_module import RealModule
from .math_expression_parser import MathExpressionParser
import re


class PolExpressionParser(MathExpressionParser):
    def __init__(self):
        """
        Парсер полиномиальных выражений с рациональными коэффициентами.

        Поддерживаемые элементы:
        - переменная: x
        - числа и дроби: 2, -3, 4/5, -7/10
        - операции над многочленами: +, -, *, /, %, ^
        - функции над многочленами:
            LED(P)  – старший коэффициент многочлена P (RationalModule)
            DEG(P)  – степень многочлена P (int)
            FAC(P)  – числовой множитель (НОК знаменателей / НОД числителей) (RationalModule)
            GCF(P,Q) – полиномиальный НОД двух многочленов (RealModule)
            DER(P) – производная многочлена (RealModule)
            NMR(P) – преобразование многочлена — кратные корни в простые (RealModule)
        - неявное умножение: 2x, x(x+1), 2GCF(...), (x+1)x и т.п.
        """

        # Таблица приоритетов операторов:
        # чем больше число — тем выше приоритет в алгоритме сортировочной станции.
        self.priority = {
            '+': 1,   # сложение многочленов
            '-': 1,   # вычитание многочленов
            '*': 2,   # умножение
            '/': 2,   # деление
            '%': 2,   # остаток от деления
            '~': 3,   # унарный минус (отрицание многочлена)
            '^': 4,   # возведение многочлена в степень
        }

        # Правоассоциативные операторы: '^' и '~'
        # (для '^' это стандартно, '~' удобно считать унарным и правоассоциативным).
        self.right_assoc = {'^', '~'}

        # Набор имён функций над многочленами.
        self.functions = {'LED', 'DEG', 'FAC', 'GCF', 'DER', 'NMR'}

    def make_rational_from_str(self, s: str) -> RationalModule:
        """
        Преобразование строкового коэффициента в RationalModule.

        Форматы:
        - '3'
        - '-5'
        - '2/3'
        - '-7/10'

        Внутри:
        - числитель -> IntegerModule
        - знаменатель -> NaturalModule
        """
        neg = s.startswith('-')
        if neg:
            s = s[1:]

        if '/' in s:
            num_str, den_str = s.split('/')
        else:
            num_str, den_str = s, '1'

        # Цифры храним в обратном порядке (как в IntegerModule/NaturalModule)
        num_digits = [int(d) for d in num_str][::-1]
        den_digits = [int(d) for d in den_str][::-1]

        up = IntegerModule(1 if neg else 0, len(num_digits) - 1, num_digits)
        down = NaturalModule(len(den_digits) - 1, den_digits)

        return RationalModule(up, down)

    def _token_type(self, tok: str) -> str:
        """
        Классификация токена.

        Нужна для вставки неявного умножения (2x, x(x+1), 2LED(x), ...).

        Возвращает:
        - 'var'    – переменная x
        - 'lparen' – '('
        - 'rparen' – ')'
        - 'op'     – оператор (+ - * / % ^ ~)
        - 'number' – число или дробь (коэффициент)
        - 'func'   – имя функции (LED, DEG, FAC, GCF)
        - 'other'  – всё остальное
        """
        if tok == 'x':
            return 'var'
        if tok == '(':
            return 'lparen'
        if tok == ')':
            return 'rparen'
        if tok in ['+', '-', '*', '/', '%', '^', '~']:
            return 'op'
        if re.fullmatch(r'-?\d+(/\d+)?', tok):
            return 'number'
        if tok in self.functions:
            return 'func'
        return 'other'

    def tokenize(self, expression: str) -> list:
        """
        Токенизация + поддержка неявного умножения.

        Этапы:
        1) Черновое разбиение регулярным выражением:
           - идентификаторы (функции, переменная x)
           - числа
           - одиночные символы операторов и скобок.
        2) Склейка дробей вида a/b.
        3) Склейка отрицательных чисел/dробей как одного токена (унарный минус).
        4) Вставка '*' там, где умножение подразумевается:
           {number, var, ')'} перед {number, var, '(', func}.
        """
        expr = expression.replace(' ', '')

        # 1. Базовое разбиение:
        #    - идентификатор: буква/подчерк + буквы/цифры
        #    - число: \d+
        #    - оператор/скобка: один из + - * / % ^ ( ) , >
        pattern = r'([А-Яа-яA-Za-z_][А-Яа-яA-Za-z0-9_]*|\d+|[+\-*/%^(),>])'
        raw = re.findall(pattern, expr)

        # 2. Склейка дробей a/b → 'a/b'
        tmp = []
        i = 0
        while i < len(raw):
            tok = raw[i]
            # число '/' число -> дробь
            if (tok.isdigit() and i + 2 < len(raw) and
                    raw[i + 1] == '/' and raw[i + 2].isdigit()):
                frac = tok + '/' + raw[i + 2]
                tmp.append(frac)
                i += 3
                continue
            tmp.append(tok)
            i += 1

        # 3. Склейка отрицательных чисел/дробей: -2, -3/5.
        #    Унарный минус: в начале или после оператора/скобки/запятой.
        raw2 = []
        i = 0
        while i < len(tmp):
            tok = tmp[i]
            if tok == '-':
                prev = raw2[-1] if raw2 else None
                # если до '-' ничего не было ИЛИ там оператор/скобка/запятая,
                # пробуем приклеить '-' к числу/дроби справа
                if prev is None or prev in ['+', '-', '*', '/', '%', '^', '(', ',', '>']:
                    if i + 1 < len(tmp) and re.fullmatch(r'\d+(/\d+)?', tmp[i + 1]):
                        raw2.append('-' + tmp[i + 1])
                        i += 2
                        continue
                # иначе это бинарный минус
                raw2.append('-')
                i += 1
                continue
            raw2.append(tok)
            i += 1

        # 4. Вставка '*' для неявного умножения
        tokens = []
        for tok in raw2:
            if tokens:
                prev = tokens[-1]
                t_prev = self._token_type(prev)
                t_cur = self._token_type(tok)

                # {number, var, rparen} перед {number, var, lparen, func} -> '*'
                if (t_prev in ['number', 'var', 'rparen'] and
                        t_cur in ['number', 'var', 'lparen', 'func']):
                    tokens.append('*')
            tokens.append(tok)

        return tokens

    def to_postfix(self, expression: str) -> list:
        """
        Преобразование инфиксного выражения в постфиксную запись (ОПЗ).

        Учитывается:
        - приоритет операторов;
        - правоассоциативность '^' и '~';
        - функции с аргументами (LED, DEG, FAC, GCF) и запятыми как разделителями.
        """
        tokens = self.tokenize(expression)
        output = []
        stack = []

        for i, token in enumerate(tokens):
            # ----- ОПЕРАНДЫ -----

            # число или дробь
            if re.fullmatch(r'-?\d+(/\d+)?', token):
                output.append(token)

            # имя функции
            elif token in self.functions:
                # функции кладём в стек (обработаются при ')')
                stack.append(token)

            # переменная x
            elif token == 'x':
                output.append(token)

            # ----- СКОБКИ И ЗАПЯТАЯ -----

            elif token == '(':
                stack.append(token)

            elif token == ',':
                # запятая разделяет аргументы функции:
                # выталкиваем операторов до ближайшей '('
                while stack and stack[-1] != '(':
                    output.append(stack.pop())

            elif token == ')':
                # выталкиваем всё до '('
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()
                # если после '(' была функция, переносим её имя в выход
                if stack and stack[-1] in self.functions:
                    output.append(stack.pop())

            # ----- МИНУС: УНАРНЫЙ vs БИНАРНЫЙ -----

            elif token == '-':
                prev = tokens[i - 1] if i > 0 else None
                # унарный минус: в начале или после оператора/скобки/запятой/степени
                is_unary = (
                    i == 0 or
                    prev in self.priority or
                    prev in ('(', ',', '^')
                )
                tok = '~' if is_unary else '-'

                while (stack and stack[-1] != '(' and
                       stack[-1] in self.priority and
                       (
                           self.priority[stack[-1]] > self.priority[tok] or
                           (self.priority[stack[-1]] == self.priority[tok] and
                            tok not in self.right_assoc)
                )):
                    output.append(stack.pop())
                stack.append(tok)

            # ----- ОСТАЛЬНЫЕ ОПЕРАТОРЫ -----

            elif token in ['+', '*', '/', '%', '^']:
                tok = token
                while (stack and stack[-1] != '(' and
                       stack[-1] in self.priority and
                       (
                           self.priority[stack[-1]] > self.priority[tok] or
                           (self.priority[stack[-1]] == self.priority[tok] and
                            tok not in self.right_assoc)
                )):
                    output.append(stack.pop())
                stack.append(tok)

        # Выталкиваем оставшиеся операторы/функции
        while stack:
            if stack[-1] != '(':
                output.append(stack.pop())
            else:
                stack.pop()

        return output

    def const_poly(self, q: RationalModule) -> RealModule:
        """
        Создать многочлен P(x) = q (степень 0).
        """
        return RealModule(0, [q])

    def x_poly(self) -> RealModule:
        """
        Создать многочлен P(x) = x.

        C[0] = 0, C[1] = 1.
        """
        zero = RationalModule(IntegerModule(0, 0, [0]), NaturalModule(0, [1]))
        one = RationalModule(IntegerModule(0, 0, [1]), NaturalModule(0, [1]))
        return RealModule(1, [zero, one])

    def evaluate(self, expression: str):
        """
        Вычисление полиномиального выражения.

        - Числа/дроби → многочлены степени 0.
        - x → многочлен x.
        - +, -, *, /, %, ^ → операции над многочленами.
        - LED(P) → RationalModule (старший коэффициент).
        - DEG(P) → int (степень).
        - FAC(P) → RationalModule (общий числовой множитель).
        - GCF(P, Q) → RealModule (полиномиальный НОД).
        """
        postfix = self.to_postfix(expression)
        # print("POSTFIX:", postfix)  # можно включать для отладки
        stack = []

        for token in postfix:
            # ---- ОПЕРАНД: ЧИСЛО / ДРОБЬ ----
            if re.fullmatch(r'-?\d+(/\d+)?', token):
                q = self.make_rational_from_str(token)
                stack.append(self.const_poly(q))

            # ---- ОПЕРАНД: ПЕРЕМЕННАЯ x ----
            elif token == 'x':
                stack.append(self.x_poly())

            # ---- УНАРНЫЙ МИНУС '~' ----
            elif token == '~':
                p = stack.pop()
                new_C = []
                minus_one = RationalModule(
                    IntegerModule(1, 0, [1]),
                    NaturalModule(0, [1])
                )
                for coef in p.C:
                    coef_copy = RationalModule(
                        IntegerModule(coef.up.b, coef.up.n, coef.up.A.copy()),
                        NaturalModule(coef.down.n, coef.down.A.copy())
                    )
                    new_C.append(coef_copy.MUL_QQ_Q(minus_one))
                stack.append(RealModule(len(new_C) - 1, new_C))

            # ---- БИНАРНЫЕ ОПЕРАТОРЫ ----
            elif token in ['+', '-', '*', '/', '%', '^']:
                # Возведение в степень — отдельный случай
                if token == '^':
                    exponent_poly = stack.pop()
                    base_poly = stack.pop()

                    # exponent_poly — полином степени 0, берём его коэффициент
                    exp_coef = exponent_poly.C[0]
                    sign = -1 if exp_coef.up.b == 1 else 1
                    val = 0
                    for i, d in enumerate(exp_coef.up.A):
                        val += d * (10 ** i)
                    k = sign * val
                    if k < 0:
                        raise ValueError("Степень должна быть неотрицательной")

                    one = RationalModule(
                        IntegerModule(0, 0, [1]),
                        NaturalModule(0, [1])
                    )
                    result = self.const_poly(one)
                    for _ in range(k):
                        result = result.MUL_PP_P(base_poly)

                    stack.append(result)
                    continue

                # Обычные бинарные операторы
                right = stack.pop()
                left = stack.pop()

                if token == '+':
                    res = left.ADD_PP_P(right)
                elif token == '-':
                    res = left.SUB_PP_P(right)
                elif token == '*':
                    res = left.MUL_PP_P(right)
                elif token == '/':
                    res = left.DIV_PP_P(right)
                elif token == '%':
                    res = left.MOD_PP_P(right)

                stack.append(res)

            # ---- ФУНКЦИЯ LED(P) ----
            elif token == 'LED':
                poly = stack.pop()          # RealModule
                led = poly.LED_P_Q()        # RationalModule
                stack.append(led)

            # ---- ФУНКЦИЯ DEG(P) ----
            elif token == 'DEG':
                poly = stack.pop()
                deg = poly.DEG_P_N()        # int
                stack.append(deg)

            # ---- ФУНКЦИЯ FAC(P) ----
            elif token == 'FAC':
                poly = stack.pop()
                fac = poly.FAC_P_Q()        # RationalModule
                stack.append(fac)

            # ---- ФУНКЦИЯ GCF(P, Q) ----
            elif token == 'GCF':
                right = stack.pop()         # второй аргумент
                left = stack.pop()          # первый аргумент

                gcf = left.GCF_PP_P(right)  # RealModule
                stack.append(gcf)

            # ---- ФУНКЦИЯ DER(P) ----
            elif token == 'DER':
                poly = stack.pop()
                der = poly.DER_P_P()  # RealModule
                stack.append(der)

            # ---- ФУНКЦИЯ NMR(P) ----
            elif token == 'NMR':
                poly = stack.pop()
                print(str(poly))
                nmr = poly.NMR_P_P()  # RealModule
                stack.append(nmr)

        # В стеке может лежать:
        # - многочлен (RealModule),
        # - рациональное (RationalModule),
        # - int (для DEG), если продолжишь считать.
        result = stack[0] if stack else None
        return str(result) if result is not None else None
