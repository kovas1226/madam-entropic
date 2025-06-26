"""FastAPI application exposing the /predictlife endpoint."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import pipeline, schemas

app = FastAPI(title="Entropic API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to your GPT domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict:
    """Friendly greeting shown at the API root."""
    return {"message": "Welcome to the Entropic API"}


@app.post(
    "/predictlife",
    response_model=schemas.PredictionResponse,
    response_model_exclude_none=True,
)
async def predict_life(
    request: schemas.PredictionRequest,
) -> schemas.PredictionResponse:
    """Endpoint returning an archetypal life prediction."""
    result = pipeline.generate_reading(
        question=request.question,
        include_details=request.include_details,
    )

    symbol = schemas.Symbol(**result["symbol"])
    details = result.get("details")
    details_obj = schemas.Details(**details) if details else None
    return schemas.PredictionResponse(
        symbol=symbol,
        details=details_obj,
    )
