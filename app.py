"""
Microservicio REST - Evaluación Parcial 1
Asignatura: Ingeniería DevOps (DOY0101) - Duoc UC
"""

from flask import Flask, jsonify, request

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

SERVICE_NAME = "devops-ev1"
SERVICE_VERSION = "1.0.0"

OPERACIONES_VALIDAS = ["suma", "resta", "multiplicacion", "division"]


# ── Error handlers ────────────────────────────────────────────────────────────
# BUG FIX: Flask retornaba respuestas de error en HTML por defecto.
# Una API REST debe responder siempre con JSON, incluso en errores.

@app.errorhandler(404)
def not_found(error):
    """Manejador de error 404 — retorna JSON en lugar de HTML."""
    return jsonify({
        "error": "Recurso no encontrado",
        "status": 404,
        "path": request.path
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Manejador de error 405 — método HTTP no permitido."""
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
    return jsonify({
        "status": "healthy",
        "servicio": SERVICE_NAME,
        "version": SERVICE_VERSION
    }), 200


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
        return jsonify({
            "error": "Los parámetros 'a' y 'b' deben ser números válidos"
        }), 400

    op = request.args.get("op", "").lower()

    if op not in OPERACIONES_VALIDAS:
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
