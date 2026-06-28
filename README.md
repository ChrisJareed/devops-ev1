# devops-ev1 - Microservicio API REST

> **Asignatura:** Ingenieria DevOps (DOY0101) - Duoc UC  
> **Evaluacion actual:** Parcial 3 - Observabilidad y entornos reales en DevOps
> **Base del proyecto:** Parcial 2 - Pipeline CI/CD, Docker y Docker Compose
> **Stack:** Python, Flask, Docker, Docker Compose, GitHub Actions, Snyk, Dependabot, Prometheus, Grafana, Loki, Kubernetes, Amazon EKS y Amazon ECR

---

## Evaluacion Parcial 3

Esta entrega extiende el microservicio y el pipeline DevOps para incorporar observabilidad, metricas, dashboards, despliegue orquestado en AWS EKS y validaciones automatizadas de cumplimiento.

La implementacion considera:

- monitoreo del microservicio con metricas Prometheus expuestas en `/metrics`;
- dashboard Grafana con disponibilidad, errores, latencia, CPU, memoria, cobertura y tiempo de despliegue;
- centralizacion de logs con Loki y Promtail;
- despliegue en Kubernetes sobre Amazon EKS usando imagenes publicadas en Amazon ECR;
- auditoria automatizada de cumplimiento mediante scripts propios dentro del pipeline;
- bloqueo del pipeline ante fallas de calidad, seguridad, manifiestos Kubernetes u observabilidad.

La Evaluacion Parcial 2 queda como base tecnica del proyecto: Docker, Docker Compose, GitHub Actions, Snyk, Dependabot y estrategia GitFlow.

---

## Descripcion

Este proyecto corresponde a un microservicio REST desarrollado con Python y Flask. La aplicacion expone endpoints de salud, operaciones basicas de calculadora y respuestas JSON para errores controlados.

En la Evaluacion Parcial 3, el foco del proyecto es operar el microservicio con observabilidad y cumplimiento: se agregan metricas, logs, dashboards, validaciones de seguridad y despliegue en un entorno orquestado real sobre AWS.

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

Para la Evaluacion Parcial 2 se trabajo sobre la rama:

```bash
feature/pipeline-contenedores
```

Los cambios se registran con commits atomicos siguiendo Conventional Commits.

Ejemplos usados:

```bash
feat(container): agregar dockerfile
chore(docker): agregar dockerignore
feat(compose): agregar orquestacion local
ci(workflow): agregar build docker y despliegue simulado
ci(dependabot): configurar actualizaciones de dependencias
ci(security): agregar analisis con snyk
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

## Contenerizacion con Docker

El proyecto incluye un `Dockerfile` para construir una imagen del microservicio.

### Construir imagen

```bash
docker build -t devops-ev1:latest .
```

### Ejecutar contenedor

```bash
docker run --name devops-ev1-test -p 5000:5000 devops-ev1:latest
```

### Validar healthcheck

```bash
curl http://localhost:5000/health
```

Respuesta esperada:

```json
{
  "servicio": "devops-ev1",
  "status": "healthy",
  "version": "1.0.0"
}
```

### Limpiar contenedor

```bash
docker rm devops-ev1-test
```

---

## Orquestacion con Docker Compose

El archivo `docker-compose.yml` permite levantar el microservicio en un entorno simulado.

```bash
docker compose up --build
```

Para detener y limpiar el entorno:

```bash
docker compose down
```

La configuracion incluye:

- construccion desde el `Dockerfile`;
- exposicion del puerto `5000`;
- reinicio controlado con `restart: unless-stopped`;
- `healthcheck` contra el endpoint `/health`.

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
- `pull_request` hacia `main` o `develop`.

### Etapas del pipeline

```text
Checkout del codigo
Configurar Python 3.11
Instalar dependencias
Lint con flake8
Pruebas unitarias con pytest
Analisis de seguridad con Snyk
Construccion de imagen Docker
Despliegue simulado con Docker Compose
Validacion de /health
Apagado del entorno simulado
```

Si una etapa falla, GitHub Actions marca el workflow como fallido y detiene las etapas dependientes.

---

## Seguridad

El proyecto incorpora dos controles principales:

| Herramienta | Funcion |
|---|---|
| Dependabot | Revisa actualizaciones de dependencias Python y GitHub Actions |
| Snyk | Analiza vulnerabilidades en dependencias dentro del pipeline |

Dependabot se configura en:

```text
.github/dependabot.yml
```

Snyk usa el secreto de GitHub Actions:

```text
SNYK_TOKEN
```

El pipeline ejecuta Snyk con:

```bash
--severity-threshold=high
```

Esto permite bloquear el flujo si se detectan vulnerabilidades de severidad alta o superior.

---

## Trazabilidad y calidad

La trazabilidad se garantiza mediante:

- uso de ramas `feature/*` desde `develop`;
- commits atomicos con Conventional Commits;
- Pull Requests para integrar cambios;
- historial de ejecuciones en GitHub Actions;
- validacion automatica de lint, pruebas, seguridad, build y despliegue simulado.

La calidad se controla mediante:

- `flake8` para revision estatica;
- `pytest` para pruebas automatizadas;
- healthcheck `/health` despues del despliegue simulado;
- Snyk y Dependabot para seguridad y gobernanza.

---

## Estructura del proyecto

```text
devops-ev1/
|-- .github/
|   |-- dependabot.yml
|   `-- workflows/
|       `-- main.yml
|-- docs/
|   |-- aws-eks-deployment.md
|   |-- branch-protection.md
|   `-- failure-validation.md
|-- k8s/
|   |-- deployment.yaml
|   |-- hpa.yaml
|   |-- namespace.yaml
|   |-- networkpolicy.yaml
|   |-- service.yaml
|   `-- serviceaccount.yaml
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

## Evaluacion Parcial 3: Observabilidad y entornos reales

La Evaluacion Parcial 3 extiende el pipeline DevOps para incorporar observabilidad, metricas, dashboards, despliegue en Kubernetes sobre AWS y validaciones automatizadas de cumplimiento.

### IE1 - Monitoreo, logs, errores y disponibilidad

El microservicio expone el endpoint `/metrics` usando `prometheus_client`. Este endpoint entrega metricas Prometheus sobre:

- total de solicitudes HTTP;
- errores HTTP por endpoint y codigo de estado;
- latencia de solicitudes;
- disponibilidad reportada por `/health`.

El entorno observable se levanta con Docker Compose:

```bash
docker compose up -d --build
```

Servicios incluidos:

| Servicio | Puerto | Proposito |
|---|---:|---|
| API Flask | 5000 | Microservicio principal |
| Prometheus | 9090 | Recoleccion de metricas |
| Grafana | 3000 | Dashboard de observabilidad |
| Loki | 3100 | Centralizacion de logs |
| Promtail | 9080 | Envio de logs de contenedores a Loki |
| cAdvisor | 8080 | Metricas de CPU y memoria de contenedores |
| Pushgateway | 9091 | Recepcion de metricas generadas por CI/CD |

Validaciones principales:

```bash
curl http://localhost:5000/health
curl http://localhost:5000/metrics
curl http://localhost:9090/-/ready
curl http://localhost:3000/api/health
curl http://localhost:3100/ready
```

La pauta permite usar Prometheus, AWS CloudWatch o una herramienta similar. En este proyecto, la implementacion principal de observabilidad se realiza con Prometheus, Grafana y Loki; CloudWatch queda documentado como alternativa o complemento opcional para entornos AWS.

### IE2 - Despliegue orquestado en AWS EKS

El proyecto incluye manifiestos Kubernetes en `k8s/` para desplegar el microservicio en Amazon EKS.

Los manifiestos incluyen:

- `Namespace` dedicado;
- `ServiceAccount` sin montaje automatico de token;
- `Deployment` con 2 replicas;
- `readinessProbe` y `livenessProbe`;
- anotaciones para scraping de Prometheus;
- limites y requests de CPU/memoria;
- `securityContext` con `runAsNonRoot`, `allowPrivilegeEscalation: false` y `readOnlyRootFilesystem`;
- `Service` tipo `LoadBalancer`;
- `HorizontalPodAutoscaler`;
- `NetworkPolicy`.

El pipeline usa Amazon ECR para publicar la imagen Docker y Amazon EKS para desplegarla.

Variables y secretos requeridos en GitHub:

| Tipo | Nombre | Uso |
|---|---|---|
| Secret | `SNYK_TOKEN` | Analisis de seguridad |
| Secret | `AWS_ROLE_TO_ASSUME` | Autenticacion OIDC contra AWS |
| Variable | `AWS_REGION` | Region AWS |
| Variable | `ECR_REPOSITORY` | Repositorio Amazon ECR |
| Variable | `EKS_CLUSTER_NAME` | Cluster Amazon EKS |

La guia de despliegue esta documentada en `docs/aws-eks-deployment.md`.

### IE3 - Dashboard con metricas clave

Grafana queda aprovisionado automaticamente desde:

```text
monitoring/grafana/dashboards/devops-ev1-observability.json
```

El dashboard incluye:

- disponibilidad del microservicio;
- solicitudes por segundo;
- errores registrados;
- latencia HTTP p95;
- uso de CPU por contenedor;
- uso de memoria por contenedor;
- tiempo de despliegue CI/CD;
- cobertura de pruebas CI/CD;
- logs del microservicio desde Loki.

Las metricas de cobertura y tiempo de despliegue se generan en GitHub Actions y se publican en Pushgateway durante el despliegue simulado.

### IE4 - Integracion en CI/CD y toma de decisiones

El workflow `.github/workflows/main.yml` integra observabilidad, seguridad y cumplimiento mediante los siguientes jobs:

| Job | Funcion |
|---|---|
| `quality` | Ejecuta lint, pruebas, cobertura y Snyk |
| `compliance` | Ejecuta auditoria automatizada de cumplimiento |
| `kubernetes-validate` | Valida manifiestos Kubernetes de forma offline |
| `docker-build` | Construye la imagen Docker |
| `deploy-simulado` | Levanta API, Prometheus, Grafana, Loki y valida `/health` y `/metrics` |
| `push-ecr` | Publica imagen en Amazon ECR |
| `deploy-eks` | Despliega el microservicio en Amazon EKS |

Estas herramientas permiten tomar decisiones tecnicas porque muestran si el servicio esta disponible, si aumentan los errores, si sube la latencia, si baja la cobertura, si el despliegue demora demasiado o si una politica de seguridad se incumple.

### IE5 - Cumplimiento y auditoria automatizada

El proyecto aplica politicas de cumplimiento con:

- Snyk con `--severity-threshold=high`;
- Dependabot para dependencias `pip` y `github-actions`;
- script `scripts/audit_compliance.py`;
- manifiestos Kubernetes con controles de seguridad;
- estrategia GitFlow y Pull Requests;
- reglas de branch protection documentadas en `docs/branch-protection.md`.

La auditoria automatizada valida, entre otros puntos:

- dependencias con version fija;
- endpoint `/metrics`;
- configuracion de Prometheus, Grafana, Loki y Pushgateway;
- Dockerfile con usuario no root;
- Kubernetes con probes, recursos y security context;
- workflow con Snyk, auditoria, cobertura, AWS EKS y validacion de metricas.

### IE6 - Bloqueo del pipeline ante fallas criticas

El pipeline se detiene automaticamente si ocurre alguna de estas situaciones:

- falla el lint;
- fallan las pruebas unitarias;
- baja la calidad o no se genera cobertura;
- Snyk detecta vulnerabilidades altas o criticas;
- falla `scripts/audit_compliance.py`;
- los manifiestos Kubernetes no pasan validacion;
- la imagen Docker no construye;
- `/health` no responde;
- `/metrics` no responde;
- Prometheus, Grafana o Loki no quedan disponibles;
- el despliegue en EKS no completa el rollout.

La forma de demostrar fallas controladas esta documentada en `docs/failure-validation.md`.



 Uso de inteligencia artificial

Durante el desarrollo se utilizo IA como apoyo para interpretar requisitos, resolver dudas de configuracion y revisar errores del flujo DevOps. Las decisiones tecnicas, pruebas, validaciones y conclusiones fueron revisadas por el equipo responsable del proyecto.



## Reflexiones de este proyecto Christopher Villa (ChrisJareed):

Christopher Villa (ChrisJareed):
Durante esta evaluación aprendí que DevOps no se trata solo de escribir código, sino de preparar un proyecto para que pueda construirse, probarse, ejecutarse y mantenerse de forma ordenada. Al trabajar con GitFlow, Docker, Docker Compose y GitHub Actions, comprendí mejor cómo se organiza un flujo de trabajo más profesional, donde cada cambio pasa por validaciones antes de integrarse a una rama principal.

También me di cuenta de la importancia de automatizar procesos. Antes podía ver las pruebas, el lint o la construcción de una imagen Docker como pasos separados, pero ahora entiendo que al integrarlos en un pipeline se reduce el riesgo de errores y se mejora la confianza en el proyecto. Además, herramientas como Dependabot y Snyk me ayudaron a ver que la seguridad y el mantenimiento de dependencias también forman parte del desarrollo responsable.

Esta actividad me permitió reforzar habilidades técnicas, pero también mejorar mi forma de trabajar: hacer commits más claros, documentar mejor, usar Pull Requests y validar los cambios antes de hacer merge. En general, siento que aprendí a mirar un proyecto no solo como una aplicación que funciona, sino como una solución que debe poder desplegarse, revisarse, protegerse y mantenerse en el tiempo.


## Reflexiones de este proyecto Pablo Díaz (pvbloww):
¿Qué aprendí? 
Aprendi a usar docker compose y lo teorico que pasamos.
Entendi como configurar el healthcheck y que no siempre esta el comando curl en la imagen,
eso me pillo de sorpresa y tuve que buscar otra forma.

¿Qué aporté?
Aporte el docker-compose.yml para levantar todo local con puertos y politicas de reinicio.
Tambien actualice el README con los comandos para correr el proyecto con docker y sin docker para que se entienda facil.

¿Qué dificultad tuve?
El healthcheck no me funcionaba porque la imagen slim no viene con curl instalado.
Tuve dificultades para encontrar la sintaxis para usar urllib con python pero despues de buscar me funciono.

¿Cómo validé?
Corri docker compose up --build en mi pc y verifique que el contenedor partiera bien y saliera como healthy cuando tiras el docker ps.
Tambien lei el README completo para ver que no tuviera errores.

Desarrollado para la Evaluacion Parcial 2 - DOY0101 Ingenieria DevOps - Duoc UC.
