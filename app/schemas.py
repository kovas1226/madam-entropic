"""Pydantic models for request and response."""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


class PredictionRequest(BaseModel):
    question: str = Field(..., description="Your burning question")
    seed: Optional[int] = Field(None, description="Optional seed for reproducibility")
    num_qubits: Optional[int] = Field(3, ge=2, le=6, description="Number of qubits")
    include_details: Optional[bool] = Field(False, description="Include technical details")


class Details(BaseModel):
    bitstring: str
    entropy: float
    num_qubits: int


class PredictionResponse(BaseModel):
    prediction: str
    symbol: str
    details: Optional[Details] = None