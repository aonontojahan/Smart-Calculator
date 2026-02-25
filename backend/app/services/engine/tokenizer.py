import re
from typing import List


OPERATORS = {"+", "-", "*", "/", "^", "%"}
FUNCTIONS = {
    "sin", "cos", "tan",
    "sqrt", "log", "log10",
    "ln", "factorial"
}
CONSTANTS = {
    "pi": 3.141592653589793,
    "e": 2.718281828459045
}


TOKEN_REGEX = re.compile(
    r"""
    (?P<NUMBER>\d+(\.\d+)?) |
    (?P<FUNCTION>sin|cos|tan|sqrt|log10|log|ln|factorial) |
    (?P<CONSTANT>pi|e) |
    (?P<OPERATOR>[\+\-\*/\^%]) |
    (?P<LPAREN>\() |
    (?P<RPAREN>\))
    """,
    re.VERBOSE
)


class Token:
    def __init__(self, type_: str, value: str):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})"


def tokenize(expression: str) -> List[Token]:
    tokens = []
    position = 0

    while position < len(expression):
        match = TOKEN_REGEX.match(expression, position)

        if not match:
            if expression[position].isspace():
                position += 1
                continue
            raise ValueError(f"Invalid character at position {position}")

        type_ = match.lastgroup
        value = match.group(type_)

        tokens.append(Token(type_, value))
        position = match.end()

    return tokens