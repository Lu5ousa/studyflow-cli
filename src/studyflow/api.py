"""Integração com a API pública ZenQuotes para citações motivacionais."""

from __future__ import annotations

import requests

ZENQUOTES_URL = "https://zenquotes.io/api/random"


def fetch_motivational_quote() -> dict[str, str]:
    response = requests.get(ZENQUOTES_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    return {"quote": data[0]["q"], "author": data[0]["a"]}