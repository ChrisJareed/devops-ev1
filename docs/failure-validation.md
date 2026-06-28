# Validacion de fallas criticas

Este documento describe como demostrar que el pipeline se interrumpe automaticamente ante fallas criticas de seguridad, calidad o cumplimiento.

## Caso 1: falla de calidad

Cambio de prueba sugerido en una rama temporal:

```python
assert response.status_code == 500
```

Resultado esperado:

- falla el job `Lint, pruebas, cobertura y seguridad`;
- no se ejecutan los jobs dependientes;
- el Pull Request queda bloqueado.

## Caso 2: falla de seguridad Snyk

Agregar temporalmente una dependencia vulnerable conocida en `requirements.txt`.

Resultado esperado:

- Snyk detecta vulnerabilidad de severidad alta o critica;
- el pipeline falla por `--severity-threshold=high`;
- no se publica imagen ni se despliega.

## Caso 3: falla de cumplimiento

Eliminar temporalmente `USER appuser` del `Dockerfile`.

Resultado esperado:

- falla `scripts/audit_compliance.py`;
- el job `Auditoria automatizada de cumplimiento` queda en rojo;
- se bloquean `docker-build`, `deploy-simulado`, `push-ecr` y `deploy-eks`.

## Caso 4: falla de observabilidad

Eliminar temporalmente el endpoint `/metrics` o cambiar su ruta.

Resultado esperado:

- fallan los tests de `/metrics`;
- si pasara a deploy simulado, fallaria `curl --fail http://localhost:5000/metrics`;
- el pipeline se detiene.

## Caso 5: falla en Kubernetes

Eliminar temporalmente `readinessProbe` o `resources` en `k8s/deployment.yaml`.

Resultado esperado:

- falla la auditoria de cumplimiento;
- si el manifiesto queda incompleto, falla `python scripts/validate_k8s_manifests.py`;
- no se despliega en AWS EKS.

## Relacion con la pauta

Estos casos cubren el IE6 porque demuestran que las validaciones automatizadas detienen el pipeline antes de afectar un entorno productivo o productivo simulado.
