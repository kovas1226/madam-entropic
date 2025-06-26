"""Pydantic models for request and response."""

from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from typing import Optional


class PredictionRequest(BaseModel):
    question: str
    include_details: Optional[bool] = False

    model_config = ConfigDict(extra="forbid")


class Symbol(BaseModel):
    label: str
    category: str
    tone: str
    meaning: str


class Details(BaseModel):
    bitstring: str
    entropy: float
    num_qubits: int


class PredictionResponse(BaseModel):
    symbol: Symbol
    details: Optional[Details] = None
