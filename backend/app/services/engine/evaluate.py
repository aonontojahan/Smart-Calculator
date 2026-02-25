from app.services.engine.tokenizer import tokenize
from app.services.engine.shunting_yard import shunting_yard
from app.services.engine.evaluator import evaluate_postfix


def evaluate_expression(expression: str) -> float:
    tokens = tokenize(expression)
    postfix = shunting_yard(tokens)
    result = evaluate_postfix(postfix)
    return result