"""FastAPI application exposing the /predictlife endpoint."""

from __future__ import annotations

from fastapi import FastAPI

from . import pipeline, schemas

app = FastAPI(title="Entropic API", version="0.1.0")


@app.get("/")
async def root() -> dict:
    """Friendly greeting shown at the API root."""
    return {"message": "Welcome to the Entropic API"}


@app.post(
    "/predictlife",
    response_model=schemas.PredictionResponse,
    response_model_exclude_none=True,
)
async def predict_life(request: schemas.PredictionRequest) -> schemas.PredictionResponse:
    """Endpoint returning an archetypal life prediction."""
    result = pipeline.generate_reading(
        question=request.question,
        seed=request.seed,
        num_qubits=request.num_qubits,
        include_details=request.include_details,
    )
   
    symbol = schemas.Symbol(**result["symbol"])
    details_data = result.get("details")
    details = schemas.Details(**details_data) if details_data is not None else None

    return schemas.PredictionResponse(
        prediction=result["prediction"],
        symbol=symbol,
        details=details,
    )