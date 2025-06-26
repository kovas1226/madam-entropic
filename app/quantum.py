"""Simple quantum simulator for internal use."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


class QState:
    """Represent a quantum state with basic gate operations."""

    def __init__(self, num_qubits: int) -> None:
        if not 2 <= num_qubits <= 6:
            raise ValueError("num_qubits must be between 2 and 6")
        self.num_qubits = num_qubits
        self.state: NDArray[np.complex128] = np.zeros(2 ** num_qubits, dtype=np.complex128)
        self.state[0] = 1.0

    def apply_gate(self, gate: NDArray[np.complex128], qubit: int) -> None:
        """Apply a single-qubit gate."""
        full_gate = np.array([[1]], dtype=np.complex128)
        for i in range(self.num_qubits):
            full_gate = np.kron(full_gate, gate if i == qubit else np.eye(2))
        self.state = full_gate @ self.state

    def apply_cnot(self, control: int, target: int) -> None:
        """Apply a CNOT gate."""
        size = 2 ** self.num_qubits
        mat = np.zeros((size, size), dtype=np.complex128)
        for i in range(size):
            b = format(i, f"0{self.num_qubits}b")
            if b[-1 - control] == '1':
                flipped = list(b)
                flipped[-1 - target] = '0' if flipped[-1 - target] == '1' else '1'
                j = int(''.join(flipped), 2)
            else:
                j = i
            mat[j, i] = 1
        self.state = mat @ self.state

    def measure(self) -> str:
        """Measure in the computational basis using the Born rule."""
        probs = np.abs(self.state) ** 2
        outcome = np.random.choice(len(probs), p=probs)
        bitstring = format(outcome, f"0{self.num_qubits}b")
        self.state = np.zeros_like(self.state)
        self.state[outcome] = 1.0
        return bitstring

    def entropy(self) -> float:
        """Return Shannon entropy of the measurement distribution."""
        probs = np.abs(self.state) ** 2
        probs = probs[probs > 0]
        return float(-(probs * np.log2(probs)).sum())


# Common gates
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
H = np.array([[1, 1], [1, -1]], dtype=np.complex128) / np.sqrt(2)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
S = np.array([[1, 0], [0, 1j]], dtype=np.complex128)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=np.complex128)


def random_circuit(state: QState, rng: np.random.Generator) -> None:
    """Apply a random sequence of gates."""
    for q in range(state.num_qubits):
        gate = rng.choice([X, H, Z, S, T])
        state.apply_gate(gate, q)
    if state.num_qubits >= 2:
        state.apply_cnot(0, 1)

