from fastapi import APIRouter
from app.services.engine.tokenizer import tokenize
from app.services.engine.shunting_yard import shunting_yard

router = APIRouter(prefix="/test", tags=["Engine Test"])


@router.get("/tokenize")
def test_tokenizer(expression: str):
    tokens = tokenize(expression)
    return [repr(token) for token in tokens]


@router.get("/postfix")
def test_postfix(expression: str):
    tokens = tokenize(expression)
    postfix = shunting_yard(tokens)
    return [repr(token) for token in postfix]