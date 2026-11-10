from fastapi import APIRouter
from app.schemas.calculator import CalculatorInput, CalculatorResult
from app.services.calculator_service import calculate_organic_input

router = APIRouter(prefix="/calculator", tags=["Input Estimation Calculator"])


@router.post("/estimate", response_model=CalculatorResult)
def estimate_input(data: CalculatorInput):
    """
    Computes estimated organic input requirements based strictly on user-supplied
    cultivated area and application rate.
    """
    return calculate_organic_input(data)
