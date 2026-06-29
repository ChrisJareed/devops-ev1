# devops-ev1 - Microservicio API REST

> **Asignatura:** Ingenieria DevOps (DOY0101) - Duoc UC  
> **Evaluacion actual:** Parcial 3 - Observabilidad y entornos reales en DevOps
> **Base del proyecto:** Parcial 2 - Pipeline CI/CD, Docker y Docker Compose
> **Stack tecnico:** Python, Flask, Docker, Docker Compose, GitHub Actions, Snyk, Dependabot, Prometheus, Grafana, Loki, Promtail, cAdvisor y Pushgateway

---

## Evaluacion Parcial 3

El proyecto incorpora observabilidad, metricas, dashboards, logging centralizado y validaciones automatizadas de cumplimiento sobre el microservicio Flask, utilizando Docker Compose como entorno de ejecucion y validacion.

### Alcance de implementacion

La solucion utiliza Docker Compose como entorno orquestado para desarrollo, validacion y despliegue simulado. La configuracion permite ejecutar el microservicio junto con los componentes de observabilidad en un ambiente reproducible, local o replicable en AWS sobre una instancia con Docker.

### Evidencia de validacion

La validacion se respalda mediante evidencia documental versionada en el repositorio: capturas, descripciones tecnicas, matriz de cumplimiento, configuracion del pipeline y guias de ejecucion.

El ambiente es reproducible mediante los archivos de configuracion incluidos en el proyecto, sin depender de recursos externos permanentes.

### Documentacion y evidencias principales

- [Evidencias de observabilidad](docs/evidencias/README.md)
- [Matriz de cumplimiento](docs/matriz-cumplimiento.md)
- [Guia de despliegue con Docker Compose](docs/docker-compose-deployment.md)
- [Politicas de branch protection](docs/branch-protection.md)
- [Validacion de fallas criticas](docs/failure-validation.md)

### Accesos para validacion

| Servicio | URL local | Usuario | Password | Nota |
|---|---|---|---|---|
| API Flask | `http://localhost:5000` | No aplica | No aplica | Microservicio principal |
| Healthcheck | `http://localhost:5000/health` | No aplica | No aplica | Estado del servicio |
| Metricas API | `http://localhost:5000/metrics` | No aplica | No aplica | Metricas Prometheus |
| Prometheus | `http://localhost:9090` | No aplica | No aplica | Recoleccion de metricas |
| Grafana | `http://localhost:3000` | `admin` | `admin` | Dashboard aprovisionado automaticamente |
| Loki | `http://localhost:3100` | No aplica | No aplica | Backend de logs |
| cAdvisor | `http://localhost:8080` | No aplica | No aplica | Metricas de contenedores |
| Pushgateway | `http://localhost:9091` | No aplica | No aplica | Metricas CI/CD |

### Plataformas externas

| Plataforma | Uso | Acceso / evidencia |
|---|---|---|
| GitHub Actions | Pipeline CI/CD, lint, pruebas, cobertura, Snyk, auditoria y despliegue simulado observable | Visible desde la pestana Actions del repositorio |
| Snyk | Analisis de vulnerabilidades con `--severity-threshold=high` | Evidenciado por el job `Analisis de seguridad con Snyk` en GitHub Actions |
| Dependabot | Revision automatica de dependencias `pip` y GitHub Actions | Configurado en `.github/dependabot.yml` |

---

## Descripcion

Este proyecto corresponde a un microservicio REST desarrollado con Python y Flask. La aplicacion expone endpoints de salud, operaciones basicas de calculadora, metricas Prometheus y respuestas JSON para errores controlados.

Para la Evaluacion Parcial 3, el microservicio se complementa con metricas, logs, dashboards, validaciones de seguridad, auditoria automatizada y despliegue simulado con Docker Compose.

---

## Endpoints

| Metodo | Ruta | Descripcion |
|---|---|---|
| `GET` | `/` | Informacion general del servicio |
| `GET` | `/health` | Estado del microservicio |
| `GET` | `/metrics` | Metricas Prometheus del microservicio |
| `GET` | `/api/calcular?a=5&b=3&op=suma` | Calculadora basica |

Operaciones disponibles en `/api/calcular`:

- `suma`
- `resta`
- `multiplicacion`
- `division`

---

## Estrategia de ramas

El proyecto mantiene una estrategia basada en GitFlow:

| Rama | Uso |
|---|---|
| `main` | Version estable o productiva |
| `develop` | Integracion de cambios antes de produccion |
| `feature/*` | Desarrollo de nuevas funcionalidades |
| `hotfix/*` | Correcciones urgentes |
| `release/*` | Preparacion de versiones |

Ramas de trabajo:

| Evaluacion | Rama |
|---|---|
| Parcial 2 | `feature/pipeline-contenedores` |
| Parcial 3 | `feature/observabilidad-compose` |

Rama de integracion:

```bash
develop
```

---

## Ejecucion local con Python

### Requisitos

- Python 3.11+
- pip

### Instalacion

```bash
git clone https://github.com/ChrisJareed/devops-ev1.git
cd devops-ev1
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

En Windows, la activacion del entorno virtual puede realizarse con:

```powershell
venv\Scripts\activate
```

### Ejecutar pruebas locales

```bash
pytest tests/ -v
flake8 app.py tests/ --max-line-length=100 --statistics
```

---

## Orquestacion con Docker Compose

El archivo `docker-compose.yml` levanta el ambiente completo de observabilidad:

| Servicio | Puerto | Proposito |
|---|---:|---|
| API Flask | 5000 | Microservicio principal |
| Prometheus | 9090 | Recoleccion de metricas |
| Grafana | 3000 | Dashboard de observabilidad |
| Loki | 3100 | Centralizacion de logs |
| Promtail | 9080 | Envio de logs de contenedores a Loki |
| cAdvisor | 8080 | Metricas de CPU y memoria de contenedores |
| Pushgateway | 9091 | Recepcion de metricas generadas por CI/CD |

### Levantar ambiente

```bash
docker compose up -d --build
```

### Validar servicios

```bash
curl http://localhost:5000/health
curl http://localhost:5000/metrics
curl http://localhost:9090/-/ready
curl http://localhost:3000/api/health
curl http://localhost:3100/ready
```

### Detener ambiente

```bash
docker compose down
```

---

## Evidencias

Las evidencias principales se encuentran documentadas en [docs/evidencias/README.md](docs/evidencias/README.md).

| Archivo | Que demuestra | Indicadores |
|---|---|---|
| [01-health.png](docs/evidencias/01-health.png) | Endpoint `/health` respondiendo correctamente | IE1, IE6 |
| [02-metrics.png](docs/evidencias/02-metrics.png) | Endpoint `/metrics` exponiendo metricas Prometheus | IE1, IE3 |
| [03-prometheus-targets.png](docs/evidencias/03-prometheus-targets.png) | Prometheus recolectando metricas de API, cAdvisor y Pushgateway | IE1, IE3 |
| [04-grafana-dashboard.png](docs/evidencias/04-grafana-dashboard.png) | Dashboard Grafana con disponibilidad, errores, latencia, CPU, memoria, cobertura y tiempo de despliegue | IE3, IE4 |
| [05-loki-logs.png](docs/evidencias/05-loki-logs.png) | Logs centralizados consultables desde Loki/Grafana | IE1, IE4 |

---

## Pipeline CI/CD

El pipeline se encuentra en:

```text
.github/workflows/main.yml
```

Se ejecuta en:

- `push` a `main`;
- `push` a `develop`;
- `push` a ramas `feature/**`;
- `pull_request` hacia `main` o `develop`;
- ejecucion manual con `workflow_dispatch`.

### Etapas del pipeline

```text
Checkout del codigo
Configurar Python 3.11
Instalar dependencias
Lint con flake8
Pruebas unitarias con pytest y cobertura
Analisis de seguridad con Snyk
Auditoria automatizada de cumplimiento
Construccion de imagen Docker
Despliegue simulado observable con Docker Compose
Validacion de /health, /metrics, Prometheus, Grafana y Loki
Publicacion de metricas CI/CD en Pushgateway
Apagado del entorno simulado
```

Si una etapa falla, GitHub Actions marca el workflow como fallido y detiene las etapas dependientes.

---

## Seguridad y cumplimiento

El proyecto incorpora:

| Herramienta | Funcion |
|---|---|
| Dependabot | Revisa actualizaciones de dependencias Python y GitHub Actions |
| Snyk | Analiza vulnerabilidades en dependencias dentro del pipeline |
| Auditoria propia | Valida configuraciones minimas de seguridad, observabilidad y CI/CD |
| Branch protection | Politicas recomendadas para `develop` y `main` |

Dependabot se configura en:

```text
.github/dependabot.yml
```

Snyk requiere el secreto de GitHub Actions:

```text
SNYK_TOKEN
```

El pipeline ejecuta Snyk con:

```bash
--severity-threshold=high
```

La auditoria automatizada se ejecuta con:

```bash
python scripts/audit_compliance.py
```

---

## Matriz de cumplimiento

La matriz de cumplimiento esta disponible en:

```text
docs/matriz-cumplimiento.md
```

Resumen:

| Indicador | Cumplimiento |
|---|---|
| IE1 | Prometheus, Loki, Promtail, `/health`, `/metrics` y evidencias de disponibilidad/logs |
| IE2 | Ambiente orquestado con Docker Compose, replicable localmente o en AWS sobre una instancia con Docker |
| IE3 | Dashboard Grafana con metricas clave de desempeno y calidad |
| IE4 | Integracion CI/CD con metricas, evidencias y decisiones tecnicas documentadas |
| IE5 | Snyk, Dependabot, auditoria automatizada y branch protection documentado |
| IE6 | Pipeline bloquea fallas de calidad, seguridad, auditoria, build y observabilidad |

---

## Estructura del proyecto

```text
devops-ev1/
|-- .github/
|   |-- dependabot.yml
|   `-- workflows/
|       `-- main.yml
|-- docs/
|   |-- branch-protection.md
|   |-- docker-compose-deployment.md
|   |-- evidencias/
|   |-- failure-validation.md
|   `-- matriz-cumplimiento.md
|-- monitoring/
|   |-- grafana/
|   |-- loki/
|   |-- prometheus/
|   `-- promtail/
|-- scripts/
|   |-- audit_compliance.py
|   `-- export_ci_metrics.py
|-- tests/
|   |-- test_app.py
|   |-- test_calculadora.py
|   `-- test_error_handlers.py
|-- .dockerignore
|-- .gitignore
|-- app.py
|-- docker-compose.yml
|-- Dockerfile
|-- README.md
`-- requirements.txt
```

---

## Reflexion personal - Christopher Villa (ChrisJareed)

En esta Evaluacion Parcial 3 aprendi que DevOps no finaliza con la construccion o el despliegue de una aplicacion. Tambien requiere observar el comportamiento del servicio, medir disponibilidad, analizar logs y generar evidencia tecnica para apoyar decisiones. La integracion de Prometheus, Grafana, Loki y metricas propias del microservicio permitio comprender de forma practica el valor de la observabilidad para detectar errores, analizar latencia y validar continuidad operativa.

Mi aporte se centro en extender el pipeline, la documentacion tecnica y la validacion del ambiente. Se incorporaron metricas en `/metrics`, validaciones de observabilidad en GitHub Actions, despliegue simulado con Docker Compose, evidencias de ejecucion y documentacion asociada a seguridad, cumplimiento y auditoria automatizada.

Una de las principales dificultades fue integrar de manera coherente el pipeline, Docker, observabilidad, seguridad y evidencia. El desafio no estuvo solo en ejecutar cada herramienta, sino en demostrar su relacion dentro de un flujo CI/CD trazable.

La validacion se realizo mediante jobs de GitHub Actions, pruebas locales, auditorias automatizadas, verificacion de los endpoints `/health` y `/metrics`, revision del dashboard en Grafana, consulta de logs en Loki y evidencia del ambiente Docker Compose. Esta evaluacion permitio abordar el proyecto como una solucion que debe operar de forma confiable, medible y auditable.

## Reflexion personal - Pablo Diaz (pvbloww)

Durante esta evaluacion aprendi la importancia de incorporar observabilidad dentro de un flujo DevOps real, no solo como herramienta complementaria, sino como mecanismo para tomar decisiones tecnicas basadas en evidencia. El uso de Prometheus, Grafana, logs y metricas del microservicio permitio comprender como detectar fallas, validar disponibilidad y observar el comportamiento de una aplicacion despues del despliegue.

Mi aporte estuvo enfocado en revisar la documentacion, la matriz de cumplimiento y la evidencia generada, verificando la relacion entre los elementos implementados y los indicadores de logro. La revision considero la ejecucion del microservicio, la exposicion de metricas, el uso del dashboard y la trazabilidad del pipeline.

Una dificultad relevante fue conectar la evidencia tecnica con los requerimientos de la pauta. Ademas de comprobar que el sistema funcionaba, fue necesario demostrar monitoreo, validacion de cumplimiento y trazabilidad dentro del pipeline CI/CD.

Esta evaluacion permitio comprender que DevOps requiere continuidad operacional despues del despliegue. La observabilidad, la seguridad y la auditoria automatizada son elementos clave para operar un sistema de forma confiable y controlada.

Desarrollado para la Evaluacion Parcial 3 - DOY0101 Ingenieria DevOps - Duoc UC.
