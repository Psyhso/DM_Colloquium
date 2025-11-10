from my_math.integer_module import IntegerModule
import sys
from pathlib import Path
from .math_expression_parser import MathExpressionParser
sys.path.append(str(Path(__file__).parent.parent.parent))


class IntExpressionParser(MathExpressionParser):
    def __init__(self):
        self.priority = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '%': 2,
            '>': 0,
            '~': 3  # Унарный минус
        }
        self.functions = {'ABS', 'POZ'}

    def to_postfix(self, expression: str) -> list:
        """
        Переопределенная версия с поддержкой унарного минуса
        """
        tokens = self.tokenize(expression)
        output = []
        stack = []

        for i, token in enumerate(tokens):
            if token.isdigit():
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

            # Специальная обработка минуса (унарный vs бинарный)
            elif token == '-':
                # Проверяем, является ли минус унарным
                is_unary = (i == 0 or
                            tokens[i-1] in self.priority or
                            tokens[i-1] == '(' or
                            tokens[i-1] == ',')

                if is_unary:
                    # Унарный минус - используем специальный символ
                    while (stack and
                           stack[-1] != '(' and
                           stack[-1] in self.priority and
                           self.priority[stack[-1]] >= self.priority['~']):
                        output.append(stack.pop())
                    stack.append('~')
                else:
                    # Бинарный минус
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

    def evaluate(self, expression: str, module_class: IntegerModule):
        stack = []
        postfix = self.to_postfix(expression)
        for token in postfix:
            if token.isdigit():
                digits = [int(d) for d in token][::-1]
                n = len(digits) - 1
                num = module_class(0, n, digits)
                stack.append(num)

            elif token == '~':  # Унарный минус
                operand = stack.pop()
                # Создаем НОВЫЙ объект с противоположным знаком
                result = module_class(
                    1 - operand.b, operand.n, operand.A.copy())
                stack.append(result)

            elif token in ['+', '-', '*', '/', '%']:
                right = stack.pop()
                left = stack.pop()

                # Создаем копию для безопасности
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

                stack.append(result)

            elif token == 'ABS':
                operand = stack.pop()
                result = operand.ABS_Z_Z()
                stack.append(result)

            elif token == 'POZ':
                operand = stack.pop()
                result = operand.POZ_Z_D()
                digits = [int(d) for d in str(result) if d != '-'][::-1]
                n = len(str(result)) - \
                    2 if result < 0 else len(str(result)) - 1
                num = module_class(0 if result > 0 else 1, n, digits)
                stack.append(num)

        return str(stack[0]) if stack else None
