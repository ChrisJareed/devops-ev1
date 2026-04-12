"""
Tests para el hotfix de error handlers JSON (404 y 405).
Bug: Flask retornaba HTML en errores, API debe responder siempre JSON.
"""

import pytest
from app import app


@pytest.fixture
def client():
    """Cliente de prueba Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestErrorHandler404:
    """Tests para el manejador de error 404."""

    def test_ruta_inexistente_retorna_404(self, client):
        response = client.get("/ruta/que/no/existe")
        assert response.status_code == 404

    def test_error_404_retorna_json_no_html(self, client):
        response = client.get("/ruta-inexistente")
        assert response.content_type == "application/json"

    def test_error_404_contiene_campo_error(self, client):
        response = client.get("/ruta-inexistente")
        data = response.get_json()
        assert "error" in data

    def test_error_404_contiene_status_404(self, client):
        response = client.get("/ruta-inexistente")
        data = response.get_json()
        assert data["status"] == 404

    def test_error_404_contiene_path(self, client):
        response = client.get("/ruta-inexistente")
        data = response.get_json()
        assert "path" in data
        assert data["path"] == "/ruta-inexistente"


class TestErrorHandler405:
    """Tests para el manejador de error 405."""

    def test_metodo_no_permitido_retorna_405(self, client):
        # GET /health solo acepta GET, POST debe dar 405
        response = client.post("/health")
        assert response.status_code == 405

    def test_error_405_retorna_json_no_html(self, client):
        response = client.post("/health")
        assert response.content_type == "application/json"

    def test_error_405_contiene_campo_error(self, client):
        response = client.post("/health")
        data = response.get_json()
        assert "error" in data

    def test_error_405_contiene_status_405(self, client):
        response = client.post("/health")
        data = response.get_json()
        assert data["status"] == 405
