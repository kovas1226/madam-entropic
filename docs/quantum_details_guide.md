# Quantum Details Guide

This document describes the contents of the optional `details` object returned by the `/predictlife` endpoint. It is intended for developers and AI system understanding only.

- `bitstring`: Resulting measurement bitstring from the quantum simulation.
- `entropy`: Shannon entropy of the state prior to measurement.
- `num_qubits`: Number of qubits used in the simulation.

These values are never referenced in user-facing text unless explicitly requested via `include_details`.