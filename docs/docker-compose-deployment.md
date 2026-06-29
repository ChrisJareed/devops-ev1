# Guia de despliegue con Docker Compose

Esta guia describe el procedimiento de ejecucion del ambiente de observabilidad con Docker Compose. Aplica para una maquina local o para una instancia AWS con Docker y Docker Compose instalados.

## Alcance

El ambiente se compone del microservicio Flask y los servicios de observabilidad definidos en `docker-compose.yml`: Prometheus, Grafana, Loki, Promtail, cAdvisor y Pushgateway.

## Requisitos

- Git
- Docker
- Docker Compose
- Puertos disponibles: `3000`, `5000`, `8080`, `9090`, `9091`, `3100`

## Clonar repositorio

```bash
git clone https://github.com/ChrisJareed/devops-ev1.git
cd devops-ev1
git checkout develop
```

## Iniciar ambiente

```bash
docker compose up -d --build
```

## Validar servicios

```bash
docker compose ps
curl http://localhost:5000/health
curl http://localhost:5000/metrics
curl http://localhost:9090/-/ready
curl http://localhost:3000/api/health
curl http://localhost:3100/ready
```

## Acceso a Grafana

| URL | Usuario | Password |
|---|---|---|
| `http://localhost:3000` | `admin` | `admin` |

El dashboard se aprovisiona automaticamente desde:

```text
monitoring/grafana/dashboards/devops-ev1-observability.json
```

## Ejecucion en AWS sobre una instancia

En una instancia AWS, habilitar los puertos necesarios en el Security Group y ejecutar:

```bash
sudo apt-get update
sudo apt-get install -y git docker.io docker-compose-plugin
sudo usermod -aG docker $USER
```

Cerrar sesion y volver a entrar para aplicar el grupo `docker`. Luego:

```bash
git clone https://github.com/ChrisJareed/devops-ev1.git
cd devops-ev1
git checkout develop
docker compose up -d --build
```

Para acceder desde el navegador, utilizar la IP publica o el DNS de la instancia:

```text
http://<IP_PUBLICA>:3000
http://<IP_PUBLICA>:5000/health
http://<IP_PUBLICA>:9090
```

## Detener ambiente

```bash
docker compose down
```

## Evidencia

La validacion del ambiente se documenta con capturas y descripciones tecnicas en `docs/evidencias/`. La guia permite reproducir el entorno sin mantener una instancia AWS encendida de forma permanente.
