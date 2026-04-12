"""
Tests unitarios para el endpoint GET /api/info.
"""

import pytest
from app import app


@pytest.fixture
def client():
    """Cliente de prueba Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestInfoSistemaEndpoint:
    """Tests para el endpoint GET /api/info"""

    def test_info_retorna_200(self, client):
        response = client.get("/api/info")
        assert response.status_code == 200

    def test_info_retorna_json(self, client):
        response = client.get("/api/info")
        assert response.content_type == "application/json"

    def test_info_contiene_nombre_servicio(self, client):
        response = client.get("/api/info")
        data = response.get_json()
        assert data["servicio"] == "devops-ev1"

    def test_info_contiene_version(self, client):
        response = client.get("/api/info")
        data = response.get_json()
        assert "version" in data
        assert data["version"] is not None

    def test_info_contiene_sistema_operativo(self, client):
        response = client.get("/api/info")
        data = response.get_json()
        assert "sistema_operativo" in data
        assert len(data["sistema_operativo"]) > 0

    def test_info_contiene_version_python(self, client):
        response = client.get("/api/info")
        data = response.get_json()
        assert "version_python" in data
        # Debe tener formato X.Y.Z
        partes = data["version_python"].split(".")
        assert len(partes) >= 2

    def test_info_contiene_hostname(self, client):
        response = client.get("/api/info")
        data = response.get_json()
        assert "hostname" in data
        assert len(data["hostname"]) > 0

    def test_info_contiene_timestamp_utc(self, client):
        response = client.get("/api/info")
        data = response.get_json()
        assert "timestamp_utc" in data
        # Debe contener indicador UTC (+00:00 o Z)
        assert "+" in data["timestamp_utc"] or "Z" in data["timestamp_utc"]

    def test_info_contiene_todos_los_campos(self, client):
        response = client.get("/api/info")
        data = response.get_json()
        campos_requeridos = [
            "servicio", "version", "sistema_operativo",
            "version_so", "version_python", "hostname", "timestamp_utc"
        ]
        for campo in campos_requeridos:
            assert campo in data, f"Campo '{campo}' ausente en la respuesta"
