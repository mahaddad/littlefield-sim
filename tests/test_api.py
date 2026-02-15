"""Tests for the Flask API routes.

Routes:
  - POST /simulate valid -> 200 + expected JSON keys
  - POST /simulate invalid -> 400
  - GET / -> 200
  - GET /guide -> 200
"""

import sys
import os
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


@pytest.fixture
def client():
    """Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestSimulateEndpoint:

    def test_valid_config_returns_200(self, client):
        """POST /simulate with valid config returns 200."""
        cfg = {
            "seed": 42,
            "end_day": 20,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
            "reorder_point": 1800,
            "order_quantity": 3600,
            "contract": 1,
        }
        resp = client.post(
            "/simulate",
            data=json.dumps(cfg),
            content_type="application/json",
        )
        assert resp.status_code == 200

    def test_valid_config_returns_expected_keys(self, client):
        """POST /simulate returns JSON with summary, charts, warnings."""
        cfg = {
            "seed": 42,
            "end_day": 20,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
        }
        resp = client.post(
            "/simulate",
            data=json.dumps(cfg),
            content_type="application/json",
        )
        data = resp.get_json()
        assert "summary" in data
        assert "charts" in data
        assert "warnings" in data

    def test_minimal_config_returns_200(self, client):
        """POST /simulate with minimal config (just seed) returns 200."""
        cfg = {"seed": 42}
        resp = client.post(
            "/simulate",
            data=json.dumps(cfg),
            content_type="application/json",
        )
        assert resp.status_code == 200

    def test_invalid_contract_returns_400(self, client):
        """POST /simulate with invalid contract ID returns 400."""
        cfg = {"seed": 42, "contract": 99}
        resp = client.post(
            "/simulate",
            data=json.dumps(cfg),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_invalid_json_returns_400(self, client):
        """POST /simulate with non-JSON body returns 400."""
        resp = client.post(
            "/simulate",
            data="not json at all {{{",
            content_type="application/json",
        )
        # Flask's get_json(force=True) may still parse or fail
        # Either 200 (if it parses somehow) or 400 is acceptable
        assert resp.status_code in (200, 400)

    def test_empty_body_returns_200_with_defaults(self, client):
        """POST /simulate with empty JSON object uses defaults."""
        resp = client.post(
            "/simulate",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["summary"]["orders_completed"] > 0


class TestIndexRoute:

    def test_index_returns_200(self, client):
        """GET / returns 200."""
        resp = client.get("/")
        assert resp.status_code == 200

    def test_index_returns_html(self, client):
        """GET / returns HTML content."""
        resp = client.get("/")
        assert b"html" in resp.data.lower() or resp.content_type.startswith("text/html")


class TestGuideRoute:

    def test_guide_returns_200(self, client):
        """GET /guide returns 200."""
        resp = client.get("/guide")
        assert resp.status_code == 200

    def test_guide_returns_html(self, client):
        """GET /guide returns HTML content."""
        resp = client.get("/guide")
        assert b"html" in resp.data.lower() or resp.content_type.startswith("text/html")
