# Validacion de fallas criticas

Este documento describe como demostrar que el pipeline se interrumpe automaticamente ante fallas criticas de seguridad, calidad, cumplimiento u observabilidad.

## Caso 1: falla de calidad

Cambio controlado en una rama temporal:

```python
assert response.status_code == 500
```

Resultado esperado:

- falla el job `Lint, pruebas, cobertura y seguridad`;
- no se ejecutan los jobs dependientes;
- el Pull Request se bloquea.

## Caso 2: falla de seguridad Snyk

Agregar temporalmente una dependencia vulnerable conocida en `requirements.txt`.

Resultado esperado:

- Snyk detecta vulnerabilidad de severidad alta o critica;
- el pipeline falla por `--severity-threshold=high`;
- no se ejecutan los jobs dependientes.

## Caso 3: falla de cumplimiento

Eliminar temporalmente `USER appuser` del `Dockerfile`.

Resultado esperado:

- falla `scripts/audit_compliance.py`;
- el job `Auditoria automatizada de cumplimiento` finaliza con error;
- se bloquean `docker-build` y `deploy-simulado`.

## Caso 4: falla de observabilidad

Eliminar temporalmente el endpoint `/metrics` o cambiar su ruta.

Resultado esperado:

- fallan los tests de `/metrics`;
- si pasara a deploy simulado, fallaria `curl --fail http://localhost:5000/metrics`;
- el pipeline se detiene.

## Caso 5: falla de Docker Compose

Cambiar temporalmente el nombre del servicio `grafana` o eliminar el puerto `3000` en `docker-compose.yml`.

Resultado esperado:

- el ambiente observable no levanta correctamente;
- falla `curl --fail http://localhost:3000/api/health`;
- el pipeline se detiene antes de considerar la entrega validada.

## Relacion con indicadores

Estos casos cubren el IE6 porque demuestran que las validaciones automatizadas detienen el pipeline antes de aceptar una version que no cumple calidad, seguridad, cumplimiento u observabilidad.
