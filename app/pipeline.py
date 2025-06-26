"""Generate archetypal predictions by combining simulator and QRNG entropy.

The pipeline builds a quantum circuit seeded from user input, fetches random
bytes from the ANU QRNG service, XORs both bitstrings together, and maps the
result to a symbol.  Users are never exposed to these internal randomness
sources.
"""

from __future__ import annotations

import os
from typing import Optional

import numpy as np

try:  # httpx is optional at runtime
    import httpx  # type: ignore
except Exception:  # pragma: no cover - dependency may be missing
    httpx = None

from . import quantum, symbolic, utils


def get_quantum_random_bytes(num_bytes: int) -> bytes:
    """Return ``num_bytes`` of entropy from the ANU QRNG API or os.urandom."""
    if httpx is None:
        return os.urandom(num_bytes)
    url = f"https://qrng.anu.edu.au/API/jsonI.php?length={num_bytes}&type=uint8"
    try:
        resp = httpx.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        values = data.get("data")
        if isinstance(values, list) and len(values) >= num_bytes:
            return bytes(int(v) & 0xFF for v in values[:num_bytes])
    except Exception:
        pass
    return os.urandom(num_bytes)


def _bytes_to_bitstring(data: bytes) -> str:
    """Convert ``data`` to a binary string."""
    return "".join(f"{b:08b}" for b in data)


def _detect_cluster(bitstring: str) -> Optional[str]:
    """Return a note about synchronicity if repeating patterns are found."""
    run = max_run = 1
    for i in range(1, len(bitstring)):
        if bitstring[i] == bitstring[i - 1]:
            run += 1
            max_run = max(max_run, run)
        else:
            run = 1
    if max_run >= 4:
        return (
            "A repeating pattern echoes through the bits—an omen of synchronicity."
        )
    return None


def _format(symbol: dict, mode: str) -> str:
    """Format the prediction text according to ``mode``."""
    label = symbol["label"]
    category = symbol["category"]
    tone = symbol["tone"]
    meaning = symbol["meaning"]

    if mode == "direct":
        return f"{label}: {meaning}"
    if mode == "narrative":
        return f"As {label} emerges on your path, {meaning}"
    if mode == "riddle":
        return f"Within {label} lies a riddle: {meaning}"
    # default 'poetic'
    return f"You drew: {label} ({category}, {tone}). {meaning}"


def generate_reading(
    question: str,
    seed: Optional[int] = None,
    num_qubits: int = 3,
    include_details: bool = False,
    mode: str = "poetic",
) -> dict:
    """Run the quantum pipeline and return a symbolic prediction."""

    seed_val = utils.deterministic_seed(question, seed)

    rng = np.random.default_rng(seed_val)
    state = quantum.QState(num_qubits)
    quantum.random_circuit(state, rng)
    entropy_value = state.entropy()
    sim_bits = state.measure()

    qrng_bytes = get_quantum_random_bytes(max(1, (num_qubits + 7) // 8))
    qrng_bits = _bytes_to_bitstring(qrng_bytes)[:num_qubits]

    bitstring = "".join(
        "1" if a != b else "0" for a, b in zip(sim_bits, qrng_bits)
    )

    symbol = symbolic.map_bitstring(bitstring)
    reading = _format(symbol, mode)
    note = _detect_cluster(bitstring)
    if note:
        reading += f"\n{note}"

    response = {"prediction": reading, "symbol": symbol}
    if include_details:
        response["details"] = {
            "bitstring": bitstring,
            "entropy": entropy_value,
            "num_qubits": num_qubits,
        }
    return response
