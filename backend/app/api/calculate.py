from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.calculation import Calculation
from app.models.user import User
from app.schemas.calculation import (
    EvaluateRequest,
    EvaluateResponse,
    CalculationHistoryResponse
)
from app.services.engine.evaluate import evaluate_expression

# Routing for calculation-related endpoints
# This router handles all endpoints related to evaluating expressions and managing calculation history for authenticated users.
router = APIRouter(prefix="/calculate", tags=["Calculation"])


@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate(
    request: EvaluateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        result = evaluate_expression(request.expression)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    calculation = Calculation(
        expression=request.expression,
        result=str(result),
        user_id=current_user.id
    )

    db.add(calculation)
    db.commit()

    return EvaluateResponse(
        expression=request.expression,
        result=result
    )


@router.get("/history", response_model=list[CalculationHistoryResponse])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    history = (
        db.query(Calculation)
        .filter(Calculation.user_id == current_user.id)
        .order_by(Calculation.created_at.desc())
        .all()
    )

    return history


@router.delete("/history/{calculation_id}")
def delete_single_history(
    calculation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    calculation = (
        db.query(Calculation)
        .filter(
            Calculation.id == calculation_id,
            Calculation.user_id == current_user.id
        )
        .first()
    )

    if not calculation:
        raise HTTPException(status_code=404, detail="History item not found")

    db.delete(calculation)
    db.commit()

    return {"message": "Deleted successfully"}


@router.delete("/history")
def delete_all_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db.query(Calculation).filter(
        Calculation.user_id == current_user.id
    ).delete()

    db.commit()
    

    return {"message": "All history cleared"}
# Note: The endpoints in this router are protected by the get_current_user dependency, which ensures that only authenticated users can access their calculation history and perform operations on it.
# The evaluate endpoint allows users to evaluate mathematical expressions, and the history endpoints allow users to view and manage their past calculations.