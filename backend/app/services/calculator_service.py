from app.schemas.calculator import CalculatorInput, CalculatorResult


def calculate_organic_input(data: CalculatorInput) -> CalculatorResult:
    """
    Calculates estimated quantity of organic input based on:
    Estimated Quantity = Cultivated Area * Application Rate

    Does not impose universal rates; calculates purely on user-provided application rate.
    """
    area = data.cultivated_area
    rate = data.application_rate
    estimated_quantity = round(area * rate, 2)

    # Determine rate quantity unit (e.g. if rate is 'kg/acre', quantity unit is 'kg')
    if "/" in data.rate_unit:
        unit_name = data.rate_unit.split("/")[0].strip()
    elif "per" in data.rate_unit.lower():
        unit_name = data.rate_unit.lower().split("per")[0].strip()
    else:
        unit_name = data.rate_unit

    formula = f"Estimated Quantity = Cultivated Area ({area} {data.area_unit}) × Application Rate ({rate} {data.rate_unit}) = {estimated_quantity} {unit_name}"

    explanation = (
        f"For your cultivated land area of {area} {data.area_unit}, applying {data.input_type_name} "
        f"at your specified recommendation rate of {rate} {data.rate_unit} will require approximately "
        f"{estimated_quantity:,.2f} {unit_name}."
    )

    disclaimer = (
        "Note: Application rates vary based on crop variety, soil test parameters, organic matter status, "
        "and local agro-climatic conditions. Always consult your local agricultural extension officer, "
        "Krishi Vigyan Kendra (KVK), or soil health card before field application."
    )

    return CalculatorResult(
        cultivated_area=area,
        area_unit=data.area_unit,
        application_rate=rate,
        rate_unit=data.rate_unit,
        input_type_name=data.input_type_name,
        estimated_quantity=estimated_quantity,
        quantity_unit=unit_name,
        formula=formula,
        explanation=explanation,
        disclaimer=disclaimer,
    )
