/**
 * GreenGrow - Organic Input Estimation Calculator
 * Performs client-side calculation with seamless API synchronization.
 */

document.addEventListener("DOMContentLoaded", () => {
  const calcForm = document.getElementById("organicCalculatorForm");
  const resultContainer = document.getElementById("calculatorResultContainer");

  if (!calcForm) return;

  calcForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const areaInput = document.getElementById("calcArea");
    const areaUnitSelect = document.getElementById("calcAreaUnit");
    const rateInput = document.getElementById("calcRate");
    const rateUnitSelect = document.getElementById("calcRateUnit");
    const inputTypeSelect = document.getElementById("calcInputType");

    const area = parseFloat(areaInput.value);
    const areaUnit = areaUnitSelect.value;
    const rate = parseFloat(rateInput.value);
    const rateUnit = rateUnitSelect.value;
    const inputType = inputTypeSelect.value;

    if (isNaN(area) || area <= 0 || isNaN(rate) || rate <= 0) {
      alert("Please enter valid positive numbers for cultivated area and application rate.");
      return;
    }

    // Call FastAPI backend calculation endpoint
    try {
      const response = await fetch("/api/v1/calculator/estimate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cultivated_area: area,
          area_unit: areaUnit,
          application_rate: rate,
          rate_unit: rateUnit,
          input_type_name: inputType,
        }),
      });

      if (!response.ok) {
        throw new Error("Calculator service error");
      }

      const data = await response.json();
      displayResult(data);
    } catch (err) {
      // Fallback local calculation
      const estimated = Math.round(area * rate * 100) / 100;
      const unitName = rateUnit.includes("/") ? rateUnit.split("/")[0].trim() : rateUnit;
      displayResult({
        cultivated_area: area,
        area_unit: areaUnit,
        application_rate: rate,
        rate_unit: rateUnit,
        input_type_name: inputType,
        estimated_quantity: estimated,
        quantity_unit: unitName,
        formula: `Estimated Quantity = Area (${area} ${areaUnit}) × Rate (${rate} ${rateUnit}) = ${estimated} ${unitName}`,
        explanation: `For your ${area} ${areaUnit} field, applying ${inputType} at ${rate} ${rateUnit} requires approximately ${estimated.toLocaleString()} ${unitName}.`,
        disclaimer: "Note: Ensure application rates align with soil test results and local agricultural extension guidance.",
      });
    }
  });

  function displayResult(res) {
    resultContainer.innerHTML = `
      <div class="calculator-result-box shadow-sm animate__animated animate__fadeIn">
        <div class="d-flex align-items-center justify-content-between mb-3 border-bottom pb-2">
          <h5 class="fw-bold mb-0 text-success">
            <i class="bi bi-check-circle-fill me-2"></i>Calculation Result
          </h5>
          <span class="badge bg-success bg-opacity-25 text-success px-3 py-2 fs-6">
            ${res.input_type_name}
          </span>
        </div>

        <div class="row align-items-center mb-3">
          <div class="col-md-5 text-center text-md-start mb-3 mb-md-0">
            <div class="text-muted small text-uppercase fw-bold">Estimated Quantity</div>
            <div class="result-quantity-display">
              ${Number(res.estimated_quantity).toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 2})}
              <span class="fs-4 text-muted fw-normal">${res.quantity_unit}</span>
            </div>
          </div>
          <div class="col-md-7 border-start-md ps-md-4">
            <div class="mb-2">
              <span class="fw-bold text-dark">Formula Applied:</span>
              <div class="p-2 bg-white rounded border font-monospace small mt-1 text-primary">
                ${res.formula}
              </div>
            </div>
            <p class="mb-0 text-muted small">
              ${res.explanation}
            </p>
          </div>
        </div>

        <div class="alert alert-light border-0 mb-0 py-2 px-3 small text-muted rounded-3" style="background: rgba(255,255,255,0.7);">
          <i class="bi bi-info-circle me-1 text-primary"></i> ${res.disclaimer}
        </div>
      </div>
    `;
    resultContainer.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
});
