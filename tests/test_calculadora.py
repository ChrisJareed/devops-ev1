"""
Tests unitarios para el endpoint GET /api/calcular.
"""

import pytest
from app import app


@pytest.fixture
def client():
    """Cliente de prueba Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestCalculadoraSuma:
    """Tests para la operación suma."""

    def test_suma_enteros_positivos(self, client):
        response = client.get("/api/calcular?a=5&b=3&op=suma")
        data = response.get_json()
        assert response.status_code == 200
        assert data["resultado"] == 8.0

    def test_suma_con_negativos(self, client):
        response = client.get("/api/calcular?a=-4&b=10&op=suma")
        data = response.get_json()
        assert response.status_code == 200
        assert data["resultado"] == 6.0

    def test_suma_con_decimales(self, client):
        response = client.get("/api/calcular?a=1.5&b=2.5&op=suma")
        data = response.get_json()
        assert response.status_code == 200
        assert data["resultado"] == 4.0


class TestCalculadoraResta:
    """Tests para la operación resta."""

    def test_resta_basica(self, client):
        response = client.get("/api/calcular?a=10&b=4&op=resta")
        data = response.get_json()
        assert response.status_code == 200
        assert data["resultado"] == 6.0

    def test_resta_resultado_negativo(self, client):
        response = client.get("/api/calcular?a=3&b=10&op=resta")
        data = response.get_json()
        assert response.status_code == 200
        assert data["resultado"] == -7.0


class TestCalculadoraMultiplicacion:
    """Tests para la operación multiplicacion."""

    def test_multiplicacion_basica(self, client):
        response = client.get("/api/calcular?a=4&b=3&op=multiplicacion")
        data = response.get_json()
        assert response.status_code == 200
        assert data["resultado"] == 12.0

    def test_multiplicacion_por_cero(self, client):
        response = client.get("/api/calcular?a=999&b=0&op=multiplicacion")
        data = response.get_json()
        assert response.status_code == 200
        assert data["resultado"] == 0.0


class TestCalculadoraDivision:
    """Tests para la operación division."""

    def test_division_basica(self, client):
        response = client.get("/api/calcular?a=10&b=2&op=division")
        data = response.get_json()
        assert response.status_code == 200
        assert data["resultado"] == 5.0

    def test_division_por_cero_retorna_400(self, client):
        response = client.get("/api/calcular?a=10&b=0&op=division")
        assert response.status_code == 400

    def test_division_por_cero_retorna_mensaje_error(self, client):
        response = client.get("/api/calcular?a=10&b=0&op=division")
        data = response.get_json()
        assert "error" in data


class TestCalculadoraErrores:
    """Tests para casos de error y validación."""

    def test_operacion_invalida_retorna_400(self, client):
        response = client.get("/api/calcular?a=5&b=3&op=potencia")
        assert response.status_code == 400

    def test_parametro_a_no_numerico_retorna_400(self, client):
        response = client.get("/api/calcular?a=abc&b=3&op=suma")
        assert response.status_code == 400

    def test_parametro_b_ausente_retorna_400(self, client):
        response = client.get("/api/calcular?a=5&op=suma")
        assert response.status_code == 400

    def test_respuesta_contiene_campos_correctos(self, client):
        response = client.get("/api/calcular?a=6&b=2&op=suma")
        data = response.get_json()
        assert "operacion" in data
        assert "a" in data
        assert "b" in data
        assert "resultado" in data
