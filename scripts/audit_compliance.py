"""
Auditoria automatizada de cumplimiento para la Evaluacion Parcial 3.

El script falla con codigo distinto de cero si detecta omisiones criticas
en seguridad, observabilidad, Kubernetes o CI/CD.
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
    file_contains("docker-compose.yml", "pushgateway:", failures)
    file_contains("monitoring/prometheus/prometheus.yml", "api:5000", failures)
    file_contains(
        "monitoring/grafana/dashboards/devops-ev1-observability.json",
        "DevOps EV1 - Observabilidad y CI/CD",
        failures,
    )


def audit_kubernetes(failures):
    deployment = read_text("k8s/deployment.yaml")
    required_fragments = [
        "readinessProbe:",
        "livenessProbe:",
        "resources:",
        "runAsNonRoot: true",
        "allowPrivilegeEscalation: false",
        "readOnlyRootFilesystem: true",
        "prometheus.io/scrape: \"true\"",
    ]
    for fragment in required_fragments:
        require(fragment in deployment, f"k8s/deployment.yaml debe contener {fragment}", failures)

    file_contains("k8s/service.yaml", "type: LoadBalancer", failures)
    file_contains("k8s/hpa.yaml", "HorizontalPodAutoscaler", failures)
    file_contains("k8s/networkpolicy.yaml", "NetworkPolicy", failures)


def audit_pipeline(failures):
    workflow = read_text(".github/workflows/main.yml")
    required_fragments = [
        "pytest tests/ -v --tb=short --cov=app --cov-report=xml --cov-report=term-missing",
        "python scripts/audit_compliance.py",
        "python scripts/validate_k8s_manifests.py",
        "curl --fail http://localhost:5000/metrics",
        "aws-actions/configure-aws-credentials@v4",
        "aws eks update-kubeconfig",
        "kubectl rollout status deployment/devops-ev1-api",
        "snyk/actions/python@master",
    ]
    for fragment in required_fragments:
        require(fragment in workflow, f"Workflow debe contener {fragment}", failures)


def main():
    failures = []
    audit_requirements(failures)
    audit_dockerfile(failures)
    audit_observability(failures)
    audit_kubernetes(failures)
    audit_pipeline(failures)

    if failures:
        print("Auditoria de cumplimiento fallida:")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)

    print("Auditoria de cumplimiento aprobada.")


if __name__ == "__main__":
    main()
