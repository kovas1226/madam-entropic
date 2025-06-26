"""Pipeline orchestrating quantum simulation and symbolic mapping."""

from __future__ import annotations

import numpy as np
from typing import Optional

from . import quantum, symbolic, utils


def generate_reading(
    question: str,
    seed: Optional[int] = None,
    num_qubits: int = 3,
    include_details: bool = False,
) -> dict:
    """Run the quantum pipeline and return a symbolic prediction."""

    seed_val = utils.deterministic_seed(question, seed)
    rng = np.random.default_rng(seed_val)

    state = quantum.QState(num_qubits)
    quantum.random_circuit(state, rng)
    entropy_value = state.entropy()
    bitstring = state.measure()
    symbol = symbolic.map_bitstring(bitstring)

    reading = (
        f"I sense {symbol} guiding you. This suggests new pathways unfolding. "
        "Trust your instincts and stay open to unexpected opportunities."
    )

    response = {"prediction": reading, "symbol": symbol}
    if include_details:
        response["details"] = {
            "bitstring": bitstring,
            "entropy": entropy_value,
            "num_qubits": num_qubits,
        }
    return response
