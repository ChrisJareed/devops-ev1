# Politicas de branch protection

Para reforzar la trazabilidad y el cumplimiento, se recomienda aplicar reglas de proteccion sobre `develop` y `main`.

## Reglas para `develop`

- Requerir Pull Request antes de hacer merge.
- Requerir al menos una aprobacion.
- Bloquear push directo.
- Requerir que la rama este actualizada antes del merge.
- Requerir que pasen los siguientes checks:
  - `Lint, pruebas, cobertura y seguridad`
  - `Auditoria automatizada de cumplimiento`
  - `Construccion de imagen Docker`
  - `Despliegue simulado observable con Docker Compose`

## Reglas para `main`

- Requerir Pull Request desde `develop` o `release/*`.
- Requerir al menos una aprobacion.
- Bloquear force push.
- Bloquear eliminacion de rama.
- Requerir que pasen los checks de calidad, seguridad, auditoria y despliegue simulado observable.

## Evidencia de control

La evidencia asociada corresponde a capturas de pantalla de:

- reglas de proteccion configuradas en GitHub;
- checks obligatorios en el Pull Request;
- bloqueo de merge cuando un check falla;
- historial de GitHub Actions.

## Relacion con indicadores

Estas reglas apoyan el IE5 porque convierten la calidad, seguridad y trazabilidad en politicas obligatorias antes de integrar codigo a ramas principales.
