"""FastAPI application exposing the /predictlife endpoint."""

from __future__ import annotations

from fastapi import FastAPI

from . import pipeline, schemas

app = FastAPI(title="Entropic API", version="0.1.0")


@app.post("/predictlife", response_model=schemas.PredictionResponse)
async def predict_life(request: schemas.PredictionRequest) -> schemas.PredictionResponse:
    """Endpoint returning an archetypal life prediction."""
    result = pipeline.generate_reading(
        question=request.question,
        seed=request.seed,
        num_qubits=request.num_qubits,
        include_details=request.include_details,
    )
    details = result.get("details")
    if details is not None:
        details = schemas.Details(**details)
    return schemas.PredictionResponse(
        prediction=result["prediction"],
        symbol=result["symbol"],
        details=details,
    )