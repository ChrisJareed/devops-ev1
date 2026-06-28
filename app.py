"""
Microservicio REST - Evaluación Parcial 1
Asignatura: Ingeniería DevOps (DOY0101) - Duoc UC
"""

import logging
from time import perf_counter

from flask import Flask, Response, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

logging.basicConfig(level=logging.INFO)

SERVICE_NAME = "devops-ev1"
SERVICE_VERSION = "1.0.0"

OPERACIONES_VALIDAS = ["suma", "resta", "multiplicacion", "division"]

REQUEST_COUNT = Counter(
    "devops_ev1_http_requests_total",
    "Total de solicitudes HTTP recibidas por el microservicio.",
    ["method", "endpoint", "http_status"],
)

ERROR_COUNT = Counter(
    "devops_ev1_http_errors_total",
    "Total de respuestas HTTP con error generadas por el microservicio.",
    ["method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "devops_ev1_http_request_duration_seconds",
    "Duracion de las solicitudes HTTP procesadas por el microservicio.",
    ["method", "endpoint"],
)

SERVICE_AVAILABLE = Gauge(
    "devops_ev1_service_available",
    "Disponibilidad del microservicio reportada por el endpoint de healthcheck.",
)


@app.before_request
def start_request_timer():
    request.start_time = perf_counter()


@app.after_request
def record_request_metrics(response):
    endpoint = request.endpoint or request.path
    method = request.method
    status = str(response.status_code)

    REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status).inc()

    if hasattr(request, "start_time"):
        duration = perf_counter() - request.start_time
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)

    if response.status_code >= 400:
        ERROR_COUNT.labels(method=method, endpoint=endpoint, http_status=status).inc()

    return response


# ── Error handlers ────────────────────────────────────────────────────────────
# BUG FIX: Flask retornaba respuestas de error en HTML por defecto.
# Una API REST debe responder siempre con JSON, incluso en errores.

@app.errorhandler(404)
def not_found(error):
    """Manejador de error 404 — retorna JSON en lugar de HTML."""
    app.logger.warning("Recurso no encontrado: %s", request.path)
    return jsonify({
        "error": "Recurso no encontrado",
        "status": 404,
        "path": request.path
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Manejador de error 405 — método HTTP no permitido."""
    app.logger.warning("Metodo no permitido: %s %s", request.method, request.path)
    return jsonify({
        "error": "Método HTTP no permitido",
        "status": 405,
        "method": request.method,
        "path": request.path
    }), 405


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    """Endpoint raíz con información del servicio."""
    return jsonify({
        "servicio": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "mensaje": "Microservicio DevOps activo",
        "estado": "ok"
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check del servicio."""
    SERVICE_AVAILABLE.set(1)
    return jsonify({
        "status": "healthy",
        "servicio": SERVICE_NAME,
        "version": SERVICE_VERSION
    }), 200


@app.route("/metrics", methods=["GET"])
def metrics():
    """Endpoint de metricas Prometheus."""
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)


@app.route("/api/calcular", methods=["GET"])
def calcular():
    """
    Endpoint calculadora básica.

    Query params:
        a   (float): Primer operando
        b   (float): Segundo operando
        op  (str):   Operación: suma | resta | multiplicacion | division

    Returns:
        JSON con resultado o mensaje de error.
    """
    try:
        a = float(request.args.get("a"))
        b = float(request.args.get("b"))
    except (TypeError, ValueError):
        app.logger.warning("Parametros invalidos en /api/calcular")
        return jsonify({
            "error": "Los parámetros 'a' y 'b' deben ser números válidos"
        }), 400

    op = request.args.get("op", "").lower()

    if op not in OPERACIONES_VALIDAS:
        app.logger.warning("Operacion invalida en /api/calcular: %s", op)
        return jsonify({
            "error": f"Operación '{op}' no válida. Use: {', '.join(OPERACIONES_VALIDAS)}"
        }), 400

    if op == "suma":
        resultado = a + b
    elif op == "resta":
        resultado = a - b
    elif op == "multiplicacion":
        resultado = a * b
    elif op == "division":
        if b == 0:
            app.logger.warning("Intento de division por cero en /api/calcular")
            return jsonify({"error": "División por cero no permitida"}), 400
        resultado = a / b

    return jsonify({
        "operacion": op,
        "a": a,
        "b": b,
        "resultado": resultado
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
