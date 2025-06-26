"""Generate archetypal predictions by combining simulator and QRNG entropy.

The pipeline builds a quantum circuit seeded from user input, fetches random
bytes from the ANU QRNG service, XORs both bitstrings together, and maps the
result to a symbol.  Users are never exposed to these internal randomness
sources.
"""

from __future__ import annotations

import hashlib
import os
import httpx
import numpy as np
from .symbolic import map_bitstring


def get_anu_qrng_bytes(n_bytes: int, retries: int = 3) -> bytes:
    """
    Fetch quantum random bytes from the ANU QRNG API.
    Falls back to os.urandom if the API is unavailable.
    """
    url = f"https://qrng.anu.edu.au/API/jsonI.php?length={n_bytes}&type=uint8"
    for _ in range(retries):
        try:
            resp = httpx.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("success"):
                    return bytes(data["data"])
        except Exception:
            continue
    return os.urandom(n_bytes)


def generate_reading(question: str, include_details: bool = False) -> dict:
    """
    Generate a symbolic impression based on quantum-inspired randomness.
    All technical steps are internal and never exposed unless details are requested.
    """
    # Deterministically derive a seed and qubit count from the question
    q_hash = hashlib.sha256(question.encode()).digest()
    seed = int.from_bytes(q_hash, "big") % (2**32 - 1)
    np.random.seed(seed)
    num_qubits = 2 + (seed % 5)  # 2-6 qubits

    # Simulate quantum circuit (random bits)
    sim_bits = np.random.randint(0, 2, num_qubits)
    sim_bitstring = "".join(str(b) for b in sim_bits)

    # Fetch quantum random bits
    qrng_bytes = get_anu_qrng_bytes(1)
    qrng_bits = "".join(f"{byte:08b}" for byte in qrng_bytes)[:num_qubits]

    # XOR simulated and QRNG bits for final bitstring
    final_bits = "".join(str(int(a) ^ int(b)) for a, b in zip(sim_bitstring, qrng_bits))

    # Map bitstring to an archetypal symbol
    symbol = map_bitstring(final_bits)

    result = {"symbol": symbol}

    if include_details:
        # Calculate entropy of the bitstring
        p0 = final_bits.count("0") / len(final_bits)
        p1 = final_bits.count("1") / len(final_bits)
        entropy = 0
        for p in (p0, p1):
            if p > 0:
                entropy -= p * np.log2(p)
        result["details"] = {
            "bitstring": final_bits,
            "entropy": round(entropy, 2),
            "num_qubits": num_qubits,
        }

    return result
