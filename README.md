# Entropic Psychic API

A conversational API delivering symbolic life predictions backed by an internal quantum simulator.

## Setup

```bash
pip install -e .
uvicorn app.main:app --reload
```

## Usage

Send a `POST` request to `https://entropic-api.onrender.com/predictlife` with JSON:

```json
{
  "question": "Will I find adventure?",
  "include_details": false
}
```

Responses include a friendly prediction and the archetypal `symbol` that inspired it. Include `"include_details": true` to receive technical data as well.

Example response:

```json
{
  "prediction": "I sense The Wanderer I guiding you...",
  "symbol": {
    "label": "The Wanderer I",
    "category": "Journey",
    "tone": "Adventurous",
    "meaning": "A call to roam invites fresh adventures into your life."
  }
}
```

## Plugin Integration

Use `.well-known/ai-plugin.json` and `openapi.yaml` to add this API to Custom GPTs. Only the `/predictlife` endpoint is available.

## Personality Guidance

Responses adopt the voice of a wise, intuitive friend—never referencing quantum mechanics or technical terms. Encourage reflection and curiosity in each reading.

`symbols.json` is used to persist newly generated symbols when write access is available. It includes entries for bitstrings up to six bits so the mapping covers dozens of archetypes out of the box.

This project is for entertainment and creative inspiration only