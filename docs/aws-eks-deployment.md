# Guia de despliegue en AWS EKS

Este documento describe la configuracion necesaria para desplegar el microservicio en Amazon EKS desde GitHub Actions.

## Servicios AWS utilizados

| Servicio | Uso |
|---|---|
| Amazon EKS | Cluster Kubernetes administrado |
| Amazon ECR | Registro de imagenes Docker |
| IAM OIDC | Autenticacion segura desde GitHub Actions |
| Amazon CloudWatch | Logs y observabilidad del cluster |

## Requisitos previos

- Tener un cluster EKS creado.
- Tener habilitado el proveedor OIDC de GitHub para AWS IAM.
- Crear un rol IAM que pueda publicar imagenes en ECR y desplegar en EKS.
- Instalar el add-on de observabilidad de AWS para enviar logs a CloudWatch.

Ejemplo de instalacion del add-on de observabilidad:

```bash
aws eks create-addon \
  --cluster-name devops-ev1-cluster \
  --addon-name amazon-cloudwatch-observability
```

## Secrets y variables de GitHub

| Tipo | Nombre | Ejemplo |
|---|---|---|
| Secret | `AWS_ROLE_TO_ASSUME` | `arn:aws:iam::123456789012:role/github-actions-devops-ev1` |
| Secret | `SNYK_TOKEN` | Token de Snyk |
| Variable | `AWS_REGION` | `us-east-1` |
| Variable | `ECR_REPOSITORY` | `devops-ev1` |
| Variable | `EKS_CLUSTER_NAME` | `devops-ev1-cluster` |

## Flujo automatizado

1. GitHub Actions ejecuta lint, pruebas, cobertura, Snyk y auditoria.
2. El workflow valida los manifiestos Kubernetes.
3. Se construye la imagen Docker.
4. En `develop` o `main`, la imagen se publica en Amazon ECR.
5. El workflow actualiza el contexto de Kubernetes con `aws eks update-kubeconfig`.
6. Se aplican los manifiestos de `k8s/`.
7. Se reemplaza la imagen del deployment con el SHA del commit.
8. Se valida el rollout.
9. Se validan `/health` y `/metrics` mediante port-forward temporal.

## Validacion manual opcional

```bash
aws eks update-kubeconfig --name devops-ev1-cluster --region us-east-1
kubectl get pods -n devops-ev1
kubectl get svc -n devops-ev1
kubectl rollout status deployment/devops-ev1-api -n devops-ev1
```

## Relacion con la pauta

Este despliegue cubre el IE2 porque ejecuta el microservicio en un entorno Kubernetes real en la nube e integra configuraciones de observabilidad mediante probes, anotaciones Prometheus, logs hacia CloudWatch y validaciones automatizadas en CI/CD.
