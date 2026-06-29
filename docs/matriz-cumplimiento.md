# Matriz de cumplimiento - Evaluacion Parcial 3

Este documento relaciona los requisitos de la Evaluacion Parcial 3 con las herramientas implementadas, la evidencia generada y la forma en que cada elemento se valida dentro del proyecto. El entorno de ejecucion y observabilidad se implementa con Docker Compose.

| Indicador / requisito | Implementacion en el proyecto | Evidencia / archivo relacionado | Validacion |
|---|---|---|---|
| IE1 - Monitoreo, logging y disponibilidad | Se incorporan Prometheus, Grafana, Loki, Promtail, cAdvisor, Pushgateway y endpoint `/metrics` en el microservicio. | `docs/evidencias/01-health.png`, `02-metrics.png`, `03-prometheus-targets.png`, `05-loki-logs.png` | Validacion de `/health`, `/metrics`, targets Prometheus y logs centralizados. |
| IE2 - Entorno orquestado con Docker Compose | El microservicio y las herramientas observables se levantan con `docker-compose.yml`, replicable localmente o en una instancia AWS con Docker. | `docker-compose.yml`, `docs/docker-compose-deployment.md`, `docs/evidencias/01-health.png`, `03-prometheus-targets.png`, `04-grafana-dashboard.png` | `docker compose up -d --build`, contenedores activos, healthcheck OK y servicios observables disponibles. |
| IE3 - Dashboard con metricas clave | Se configura dashboard en Grafana con disponibilidad, errores, latencia, CPU, memoria, cobertura y metricas CI/CD. | `monitoring/grafana/dashboards/devops-ev1-observability.json`, `docs/evidencias/04-grafana-dashboard.png` | Visualizacion del dashboard y consulta de metricas desde Prometheus. |
| IE4 - Integracion con pipeline CI/CD | GitHub Actions ejecuta lint, pruebas, cobertura, seguridad, auditoria, build Docker y despliegue simulado observable con Docker Compose. | `.github/workflows/main.yml`, `README.md` | Workflow ejecutado correctamente con jobs de calidad, cumplimiento, Docker y observabilidad. |
| IE5 - Cumplimiento y auditoria automatizada | Se agregan Snyk, Dependabot, branch protection documentado y script de auditoria propio. | `scripts/audit_compliance.py`, `docs/branch-protection.md`, `.github/dependabot.yml` | El pipeline se detiene si falla la auditoria o si Snyk detecta vulnerabilidades altas. |
| IE6 - Bloqueo ante fallas criticas | Se documentan casos de falla controlada de calidad, seguridad, cumplimiento, Docker Compose, healthcheck y metricas. | `docs/failure-validation.md` | El pipeline falla cuando no se cumplen los criterios minimos definidos. |

## Conclusion

La solucion implementada cumple con los requisitos principales de la evaluacion porque integra observabilidad, dashboard, auditoria automatizada, seguridad y validaciones dentro del pipeline CI/CD. La evidencia se presenta mediante capturas y documentacion tecnica detallada dentro del repositorio.
