"""
Validacion offline de manifiestos Kubernetes.

No reemplaza un admission controller, pero permite bloquear el pipeline si faltan
manifiestos o controles minimos antes de intentar desplegar en EKS.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
K8S_DIR = ROOT / "k8s"

EXPECTED_KINDS = {
    "namespace.yaml": "Namespace",
    "serviceaccount.yaml": "ServiceAccount",
    "deployment.yaml": "Deployment",
    "service.yaml": "Service",
    "hpa.yaml": "HorizontalPodAutoscaler",
    "networkpolicy.yaml": "NetworkPolicy",
}


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read_manifest(file_name, failures):
    path = K8S_DIR / file_name
    require(path.exists(), f"Falta k8s/{file_name}", failures)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def validate_common(file_name, expected_kind, content, failures):
    require("apiVersion:" in content, f"k8s/{file_name} no declara apiVersion", failures)
    require(
        f"kind: {expected_kind}" in content,
        f"k8s/{file_name} debe ser {expected_kind}",
        failures,
    )
    require("metadata:" in content, f"k8s/{file_name} no declara metadata", failures)
    require("name:" in content, f"k8s/{file_name} no declara metadata.name", failures)


def validate_specific(failures):
    deployment = read_manifest("deployment.yaml", failures)
    for fragment in [
        "replicas: 2",
        "readinessProbe:",
        "livenessProbe:",
        "resources:",
        "requests:",
        "limits:",
        "runAsNonRoot: true",
        "allowPrivilegeEscalation: false",
        "readOnlyRootFilesystem: true",
        "prometheus.io/scrape: \"true\"",
    ]:
        require(fragment in deployment, f"deployment.yaml debe contener {fragment}", failures)

    service = read_manifest("service.yaml", failures)
    require("type: LoadBalancer" in service, "service.yaml debe exponer LoadBalancer", failures)
    require("targetPort: http" in service, "service.yaml debe usar targetPort http", failures)

    hpa = read_manifest("hpa.yaml", failures)
    require("averageUtilization: 70" in hpa, "hpa.yaml debe definir umbral CPU 70", failures)


def main():
    failures = []
    for file_name, expected_kind in EXPECTED_KINDS.items():
        content = read_manifest(file_name, failures)
        if content:
            validate_common(file_name, expected_kind, content, failures)

    validate_specific(failures)

    if failures:
        print("Validacion Kubernetes fallida:")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)

    print("Validacion Kubernetes aprobada.")


if __name__ == "__main__":
    main()
