from typing import List
from app.services.engine.tokenizer import Token

PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "%": 2,
    "^": 3,
}

RIGHT_ASSOCIATIVE = {"^"}


def shunting_yard(tokens: List[Token]) -> List[Token]:
    output_queue = []
    operator_stack = []

    for token in tokens:
        if token.type == "NUMBER" or token.type == "CONSTANT":
            output_queue.append(token)

        elif token.type == "FUNCTION":
            operator_stack.append(token)

        elif token.type == "OPERATOR":
            while (
                operator_stack
                and operator_stack[-1].type in {"OPERATOR", "FUNCTION"}
                and (
                    (
                        token.value not in RIGHT_ASSOCIATIVE
                        and PRECEDENCE.get(token.value, 0)
                        <= PRECEDENCE.get(operator_stack[-1].value, 0)
                    )
                    or (
                        token.value in RIGHT_ASSOCIATIVE
                        and PRECEDENCE.get(token.value, 0)
                        < PRECEDENCE.get(operator_stack[-1].value, 0)
                    )
                )
            ):
                output_queue.append(operator_stack.pop())

            operator_stack.append(token)

        elif token.type == "LPAREN":
            operator_stack.append(token)

        elif token.type == "RPAREN":
            while operator_stack and operator_stack[-1].type != "LPAREN":
                output_queue.append(operator_stack.pop())

            if not operator_stack:
                raise ValueError("Mismatched parentheses")

            operator_stack.pop()

            if operator_stack and operator_stack[-1].type == "FUNCTION":
                output_queue.append(operator_stack.pop())

    while operator_stack:
        if operator_stack[-1].type in {"LPAREN", "RPAREN"}:
            raise ValueError("Mismatched parentheses")

        output_queue.append(operator_stack.pop())

    return output_queue