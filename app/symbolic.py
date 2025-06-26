"""Mapping between quantum measurement results and archetypal symbols.

This module maintains a dictionary of bitstrings to rich symbol objects.
Each symbol contains a ``label`` with descriptive fields to craft a unique prediction.
Mappings are persisted to ``symbols.json`` so the same bitstring always yields the same archetype.

New symbols are deterministically generated using a hash of the bitstring for diversity and reproducibility.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict
import hashlib

SYMBOL_FILE = Path(__file__).with_name("symbols.json")

LABELS = [
    "The Wanderer",
    "The Sage",
    "The Seeker",
    "The Gatekeeper",
    "The Phoenix",
    "The Mirror",
    "The Oracle",
    "The Trickster",
    "The Dreamer",
    "The Alchemist",
]

CATEGORIES = [
    "Journey",
    "Wisdom",
    "Quest",
    "Threshold",
    "Rebirth",
    "Reflection",
    "Prophecy",
    "Chaos",
    "Vision",
    "Transformation",
]

TONES = [
    "Adventurous",
    "Reflective",
    "Curious",
    "Mysterious",
    "Transformative",
    "Playful",
    "Insightful",
    "Disruptive",
    "Dreamlike",
    "Alchemical",
]

MEANINGS = [
    "A call to roam invites fresh adventures into your life.",
    "Quiet contemplation brings the guidance you seek.",
    "Your questions lead you toward unexpected horizons.",
    "A new doorway appears, challenging you to step through.",
    "From endings arise new beginnings and transformation.",
    "Look inward to mirror the truths around you.",
    "Visions of the future arrive in subtle whispers.",
    "Embrace chaos; it leads to unexpected growth.",
    "Dreams hold keys to hidden possibilities.",
    "Through transformation, you discover hidden power.",
]

ORDINALS = [
    "I",
    "II",
    "III",
    "IV",
    "V",
    "VI",
    "VII",
    "VIII",
    "IX",
    "X",
    "XI",
    "XII",
    "XIII",
    "XIV",
    "XV",
    "XVI",
]


def load_symbols() -> Dict[str, Dict[str, Any]]:
    """Return stored symbol mappings or built-in defaults."""
    if SYMBOL_FILE.exists():
        with SYMBOL_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    # Fallback: Only the basic 2-bit ones, for safety.
    return {
        "00": {
            "label": "The Wanderer I",
            "category": "Journey",
            "tone": "Adventurous",
            "meaning": "A call to roam invites fresh adventures into your life.",
        },
        "01": {
            "label": "The Sage II",
            "category": "Wisdom",
            "tone": "Reflective",
            "meaning": "Quiet contemplation brings the guidance you seek.",
        },
        "10": {
            "label": "The Seeker III",
            "category": "Quest",
            "tone": "Curious",
            "meaning": "Your questions lead you toward unexpected horizons.",
        },
        "11": {
            "label": "The Gatekeeper IV",
            "category": "Threshold",
            "tone": "Mysterious",
            "meaning": "A new doorway appears, challenging you to step through.",
        },
    }


def save_symbols(symbols: Dict[str, Dict[str, Any]]) -> None:
    """Persist symbol mappings if possible, ignoring write errors."""
    try:
        with SYMBOL_FILE.open("w", encoding="utf-8") as f:
            json.dump(symbols, f, indent=2, ensure_ascii=False)
    except OSError:
        pass


def _generate_symbol(bitstring: str) -> Dict[str, str]:
    """Create a deterministic symbol object for an unseen bitstring."""
    digest = hashlib.sha256(bitstring.encode()).digest()
    label = LABELS[digest[0] % len(LABELS)]
    category = CATEGORIES[digest[1] % len(CATEGORIES)]
    tone = TONES[digest[2] % len(TONES)]
    meaning = MEANINGS[digest[3] % len(MEANINGS)]
    ordinal = ORDINALS[digest[4] % len(ORDINALS)]
    return {
        "label": f"{label} {ordinal}",
        "category": category,
        "tone": tone,
        "meaning": meaning,
    }


def map_bitstring(bitstring: str) -> Dict[str, Any]:
    """Map a measured bitstring to an archetypal symbol object."""
    symbols = load_symbols()
    if bitstring not in symbols:
        symbols[bitstring] = _generate_symbol(bitstring)
        save_symbols(symbols)
    return symbols[bitstring]
