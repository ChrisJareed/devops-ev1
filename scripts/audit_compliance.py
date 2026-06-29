"""
Auditoria automatizada de cumplimiento para la Evaluacion Parcial 3.

El script falla con codigo distinto de cero si detecta omisiones criticas
en seguridad, observabilidad, Docker Compose o CI/CD.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def file_contains(relative_path, expected, failures):
    path = ROOT / relative_path
    require(path.exists(), f"Falta el archivo {relative_path}", failures)
    if path.exists():
        content = path.read_text(encoding="utf-8")
        require(expected in content, f"{relative_path} debe contener: {expected}", failures)


def audit_requirements(failures):
    content = read_text("requirements.txt")
    for line in content.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            require("==" in line, f"Dependencia sin version fija: {line}", failures)

    file_contains("requirements.txt", "prometheus_client==", failures)
    file_contains("requirements.txt", "pytest-cov==", failures)


def audit_dockerfile(failures):
    content = read_text("Dockerfile")
    require(
        "python:3.11-slim" in content,
        "Dockerfile debe usar una imagen base slim",
        failures,
    )
    require(
        "PYTHONDONTWRITEBYTECODE=1" in content,
        "Dockerfile debe evitar bytecode en runtime",
        failures,
    )
    require(
        "USER appuser" in content,
        "Dockerfile debe ejecutar la aplicacion con usuario no root",
        failures,
    )


def audit_observability(failures):
    file_contains("app.py", "@app.route(\"/metrics\"", failures)
    file_contains("app.py", "devops_ev1_http_requests_total", failures)
    file_contains("docker-compose.yml", "prometheus:", failures)
    file_contains("docker-compose.yml", "grafana:", failures)
    file_contains("docker-compose.yml", "loki:", failures)
    file_contains("docker-compose.yml", "promtail:", failures)
    file_contains("docker-compose.yml", "cadvisor:", failures)
    file_contains("docker-compose.yml", "pushgateway:", failures)
    file_contains("docker-compose.yml", "GF_SECURITY_ADMIN_USER: admin", failures)
    file_contains("docker-compose.yml", "GF_SECURITY_ADMIN_PASSWORD: admin", failures)
    file_contains("monitoring/prometheus/prometheus.yml", "api:5000", failures)
    file_contains(
        "monitoring/grafana/dashboards/devops-ev1-observability.json",
        "DevOps EV1 - Observabilidad y CI/CD",
        failures,
    )


def audit_documentation(failures):
    readme = read_text("README.md")
    require(
        "Alcance de implementacion" in readme and "Docker Compose" in readme,
        "README debe declarar el alcance tecnico con Docker Compose",
        failures,
    )
    require(
        "Evidencia de validacion" in readme,
        "README debe declarar la evidencia de validacion",
        failures,
    )
    require(
        "admin" in readme and "Grafana" in readme,
        "README debe documentar credenciales de Grafana",
        failures,
    )
    require(
        "docs/evidencias/01-health.png" in readme,
        "README debe enlazar evidencias principales",
        failures,
    )
    file_contains("docs/matriz-cumplimiento.md", "Docker Compose", failures)
    file_contains("docs/docker-compose-deployment.md", "docker compose up -d --build", failures)
    file_contains("docs/evidencias/README.md", "Docker Compose", failures)


def audit_pipeline(failures):
    workflow = read_text(".github/workflows/main.yml")
    required_fragments = [
        "pytest tests/ -v --tb=short --cov=app --cov-report=xml --cov-report=term-missing",
        "python scripts/audit_compliance.py",
        "docker compose up -d --build",
        "http://localhost:5000/metrics",
        "http://localhost:3000/api/health",
        "snyk/actions/python@master",
        "docker compose down",
    ]
    for fragment in required_fragments:
        require(fragment in workflow, f"Workflow debe contener {fragment}", failures)

    forbidden_fragments = [
        "Kubernetes",
        "validate_k8s_manifests",
        "kubectl",
        "aws eks",
        "EKS_CLUSTER_NAME",
    ]
    for fragment in forbidden_fragments:
        require(fragment not in workflow, f"Workflow no debe contener {fragment}", failures)


def main():
    failures = []
    audit_requirements(failures)
    audit_dockerfile(failures)
    audit_observability(failures)
    audit_documentation(failures)
    audit_pipeline(failures)

    if failures:
        print("Auditoria de cumplimiento fallida:")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)

    print("Auditoria de cumplimiento aprobada.")


if __name__ == "__main__":
    main()
