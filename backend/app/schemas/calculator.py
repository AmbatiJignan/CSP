from typing import Optional
from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    cultivated_area: float = Field(..., gt=0, description="Cultivated land area")
    area_unit: str = Field(default="Acres", description="Unit of area: Acres, Hectares, Gunthas, Square Meters")
    application_rate: float = Field(..., gt=0, description="Application rate per area unit supplied by user")
    rate_unit: str = Field(default="kg/acre", description="Unit of application rate (e.g. kg/acre, tonnes/acre, quintals/acre, litres/acre)")
    input_type_name: Optional[str] = Field("Compost / FYM / Biofertiliser", description="Name of the organic input being estimated")


class CalculatorResult(BaseModel):
    cultivated_area: float
    area_unit: str
    application_rate: float
    rate_unit: str
    input_type_name: str
    estimated_quantity: float
    quantity_unit: str
    formula: str
    explanation: str
    disclaimer: str
