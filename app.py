"""
Microservicio REST - Evaluación Parcial 1
Asignatura: Ingeniería DevOps (DOY0101) - Duoc UC
"""

from flask import Flask, jsonify, request

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

SERVICE_NAME = "devops-ev1"
SERVICE_VERSION = "1.0.0"


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
