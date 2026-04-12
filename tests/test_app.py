"""
Tests unitarios para el microservicio devops-ev1.
"""

import pytest
from app import app


@pytest.fixture
def client():
    """Cliente de prueba Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestIndexEndpoint:
    """Tests para el endpoint raíz GET /"""

    def test_index_retorna_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_index_retorna_json(self, client):
        response = client.get("/")
        assert response.content_type == "application/json"

    def test_index_contiene_nombre_servicio(self, client):
        response = client.get("/")
        data = response.get_json()
        assert data["servicio"] == "devops-ev1"

    def test_index_contiene_estado_ok(self, client):
        response = client.get("/")
        data = response.get_json()
        assert data["estado"] == "ok"


class TestHealthEndpoint:
    """Tests para el endpoint GET /health"""

    def test_health_retorna_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_retorna_json(self, client):
        response = client.get("/health")
        assert response.content_type == "application/json"

    def test_health_status_es_healthy(self, client):
        response = client.get("/health")
        data = response.get_json()
        assert data["status"] == "healthy"
