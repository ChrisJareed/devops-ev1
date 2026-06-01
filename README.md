# devops-ev1 - Microservicio API REST

> **Asignatura:** Ingenieria DevOps (DOY0101) - Duoc UC  
> **Evaluacion:** Parcial 2  
> **Stack:** Python, Flask, Docker, Docker Compose, GitHub Actions, Snyk y Dependabot

---

## Descripcion

Este proyecto corresponde a un microservicio REST desarrollado con Python y Flask. La aplicacion expone endpoints de salud, operaciones basicas de calculadora y respuestas JSON para errores controlados.

En esta evaluacion se agrega una estrategia DevOps completa sobre el microservicio base: contenerizacion, orquestacion local, integracion continua, analisis de seguridad, despliegue simulado y trazabilidad mediante GitHub.

---

## Endpoints

| Metodo | Ruta | Descripcion |
|---|---|---|
| `GET` | `/` | Informacion general del servicio |
| `GET` | `/health` | Estado del microservicio |
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



 Uso de inteligencia artificial

Durante el desarrollo se utilizo IA como apoyo para interpretar requisitos, resolver dudas de configuracion y revisar errores del flujo DevOps. Las decisiones tecnicas, pruebas, validaciones y conclusiones fueron revisadas por el equipo responsable del proyecto.



## Reflexiones de este proyecto Christopher Villa (ChrisJareed):

Christopher Villa (ChrisJareed):
Durante esta evaluación aprendí que DevOps no se trata solo de escribir código, sino de preparar un proyecto para que pueda construirse, probarse, ejecutarse y mantenerse de forma ordenada. Al trabajar con GitFlow, Docker, Docker Compose y GitHub Actions, comprendí mejor cómo se organiza un flujo de trabajo más profesional, donde cada cambio pasa por validaciones antes de integrarse a una rama principal.

También me di cuenta de la importancia de automatizar procesos. Antes podía ver las pruebas, el lint o la construcción de una imagen Docker como pasos separados, pero ahora entiendo que al integrarlos en un pipeline se reduce el riesgo de errores y se mejora la confianza en el proyecto. Además, herramientas como Dependabot y Snyk me ayudaron a ver que la seguridad y el mantenimiento de dependencias también forman parte del desarrollo responsable.

Esta actividad me permitió reforzar habilidades técnicas, pero también mejorar mi forma de trabajar: hacer commits más claros, documentar mejor, usar Pull Requests y validar los cambios antes de hacer merge. En general, siento que aprendí a mirar un proyecto no solo como una aplicación que funciona, sino como una solución que debe poder desplegarse, revisarse, protegerse y mantenerse en el tiempo.


## Reflexiones de este proyecto Pablo Díaz (pvbloww):
¿Qué aprendí?
Aprendí a orquestar servicios con Docker Compose, entendiendo cómo configurar la construcción desde un Dockerfile, la exposición de puertos y cómo agregar un healthcheck para validar que el contenedor responde correctamente. También aprendí a documentar un proyecto DevOps de forma estructurada, separando claramente las secciones de ejecución local, contenedores, pipeline y seguridad.

¿Qué aporté?
Me encargué de dos contribuciones concretas dentro del PR:

docker-compose.yml: Configuré la orquestación local del microservicio con construcción desde el Dockerfile, exposición del puerto 5000, política restart: unless-stopped y un healthcheck usando urllib.request de Python para validar el endpoint /health.
README.md: Actualicé la documentación para la Evaluación Parcial 2, agregando la descripción del proyecto, instrucciones de ejecución local con Python, sección de contenerización con Docker, uso de Docker Compose, descripción del pipeline CI/CD, seguridad con Snyk y Dependabot, y la estructura del proyecto actualizada.
¿Qué dificultad tuve?
La principal dificultad fue el healthcheck en Docker Compose. La imagen python:3.11-slim no incluye curl, por lo que no podía usarlo directamente. Tuve que implementar el chequeo usando urllib.request de Python para que funcionara sin instalar dependencias adicionales en la imagen.

¿Cómo validé mi trabajo?
Validé el docker-compose.yml ejecutando docker compose up --build localmente y verificando con docker ps que el contenedor aparecía como healthy. El README lo revisé sección por sección comprobando que los comandos y rutas descritos coincidieran con la estructura real del repositorio.

Desarrollado para la Evaluacion Parcial 2 - DOY0101 Ingenieria DevOps - Duoc UC.
