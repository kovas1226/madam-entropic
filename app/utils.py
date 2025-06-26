"""Utility helpers for the Entropic API."""

from __future__ import annotations

import hashlib
from typing import Optional


def deterministic_seed(text: str, seed: Optional[int] = None) -> int:
    """Return a deterministic seed derived from text and optional seed."""
    if seed is not None:
        return seed
    digest = hashlib.sha256(text.encode()).hexdigest()
    return int(digest[:16], 16)