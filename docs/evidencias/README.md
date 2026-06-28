# Evidencias de observabilidad

Esta carpeta contiene capturas generadas desde el entorno local de observabilidad levantado con Docker Compose. Las evidencias respaldan la integracion de monitoreo, metricas, logs, dashboard y validaciones solicitadas en la Evaluacion Parcial 3.

## Capturas incluidas

| Archivo | Evidencia | Indicador relacionado |
|---|---|---|
| `01-health.png` | Valida que el microservicio responde correctamente el endpoint `/health` y reporta estado `healthy`. | IE1, IE6 |
| `02-metrics.png` | Muestra el endpoint `/metrics` exponiendo metricas Prometheus del microservicio, incluyendo requests, errores, latencia y disponibilidad. | IE1, IE3 |
| `03-prometheus-targets.png` | Muestra Prometheus recolectando metricas desde la API, cAdvisor y Pushgateway. | IE1, IE3 |
| `04-grafana-dashboard.png` | Muestra el dashboard Grafana con disponibilidad, solicitudes por segundo, errores, latencia, CPU, memoria, tiempo de despliegue, cobertura y logs. | IE3, IE4 |
| `05-loki-logs.png` | Muestra logs centralizados en Loki, incluyendo eventos reales generados por el microservicio. | IE1, IE4 |

## Relacion con la pauta

Estas capturas respaldan los siguientes puntos de la evaluacion:

- IE1: configuracion de herramientas de monitoreo para visualizar logs, metricas, errores y disponibilidad.
- IE3: creacion de dashboard con metricas clave de desempeno, calidad y operacion.
- IE4: documentacion de como las herramientas permiten tomar decisiones tecnicas informadas.
- IE6: validacion de endpoints criticos como `/health` y `/metrics`, los cuales detienen el pipeline si fallan.

## Nota sobre metricas CI/CD

Las metricas de cobertura de pruebas y tiempo de despliegue se publican en Pushgateway desde el pipeline CI/CD. Para la evidencia local se publicaron valores de prueba usando `scripts/export_ci_metrics.py`, con el objetivo de validar que Grafana puede visualizar esas metricas cuando son generadas por GitHub Actions.
