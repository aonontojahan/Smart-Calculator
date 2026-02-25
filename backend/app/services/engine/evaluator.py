import math
from typing import List
from app.services.engine.tokenizer import Token, CONSTANTS


def apply_operator(operator: str, a: float, b: float) -> float:
    if operator == "+":
        return a + b
    if operator == "-":
        return a - b
    if operator == "*":
        return a * b
    if operator == "/":
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    if operator == "%":
        return a % b
    if operator == "^":
        return a ** b
    raise ValueError(f"Unknown operator {operator}")


def apply_function(func: str, value: float) -> float:
    if func == "sin":
        return math.sin(math.radians(value))
    if func == "cos":
        return math.cos(math.radians(value))
    if func == "tan":
        return math.tan(math.radians(value))
    if func == "sqrt":
        if value < 0:
            raise ValueError("Square root of negative number")
        return math.sqrt(value)
    if func == "log":
        return math.log(value)
    if func == "log10":
        return math.log10(value)
    if func == "ln":
        return math.log(value)
    if func == "factorial":
        if value < 0 or not value.is_integer():
            raise ValueError("Factorial only defined for non-negative integers")
        return math.factorial(int(value))
    raise ValueError(f"Unknown function {func}")


def evaluate_postfix(tokens: List[Token]) -> float:
    stack = []

    for token in tokens:
        if token.type == "NUMBER":
            stack.append(float(token.value))

        elif token.type == "CONSTANT":
            stack.append(float(CONSTANTS[token.value]))

        elif token.type == "OPERATOR":
            if len(stack) < 2:
                raise ValueError("Invalid expression")

            b = stack.pop()
            a = stack.pop()

            result = apply_operator(token.value, a, b)
            stack.append(result)

        elif token.type == "FUNCTION":
            if len(stack) < 1:
                raise ValueError("Invalid function usage")

            value = stack.pop()
            result = apply_function(token.value, value)
            stack.append(result)

    if len(stack) != 1:
        raise ValueError("Invalid expression")

    return stack[0]