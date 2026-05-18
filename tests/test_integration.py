"""Testes de integração para a API ZenQuotes."""

from __future__ import annotations
from unittest.mock import MagicMock, patch
import pytest
import requests as req
from studyflow.api import fetch_motivational_quote


def _mock(quote, author):
    m = MagicMock()
    m.json.return_value = [{"q": quote, "a": author}]
    m.raise_for_status.return_value = None
    return m


def test_fetch_quote_retorna_campos_corretos():
    with patch("studyflow.api.requests.get") as mock_get:
        mock_get.return_value = _mock("Estude sempre.", "Sócrates")
        result = fetch_motivational_quote()
    assert "quote" in result and "author" in result


def test_fetch_quote_retorna_valores_da_api():
    with patch("studyflow.api.requests.get") as mock_get:
        mock_get.return_value = _mock("A educação é a arma mais poderosa.", "Mandela")
        result = fetch_motivational_quote()
    assert result["quote"] == "A educação é a arma mais poderosa."
    assert result["author"] == "Mandela"


def test_fetch_quote_propaga_excecao_de_rede():
    with patch("studyflow.api.requests.get") as mock_get:
        mock_get.side_effect = req.RequestException("Sem conexão")
        with pytest.raises(req.RequestException):
            fetch_motivational_quote()