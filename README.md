# 🚀 devops-ev1 — Microservicio API REST

> **Asignatura:** Ingeniería DevOps (DOY0101) — Duoc UC  
> **Evaluación:** Parcial 1  
> **Stack:** Python · Flask · GitHub Actions · GitFlow

---

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Estrategia de Branching: GitFlow](#-estrategia-de-branching-gitflow)
- [Naming de Ramas](#-naming-de-ramas)
- [Convenciones de Commits (Conventional Commits)](#-convenciones-de-commits-conventional-commits)
- [Estrategia de Revisión de Código](#-estrategia-de-revisión-de-código)
- [Pipeline CI/CD](#-pipeline-cicd)
- [Cómo ejecutar el proyecto](#-cómo-ejecutar-el-proyecto)

---

## 📦 Descripción del Proyecto

Microservicio REST desarrollado en **Python + Flask** que expone endpoints de salud y operaciones básicas. Sirve como base para demostrar flujos DevOps profesionales: integración continua, revisión de código mediante Pull Requests y trazabilidad completa del desarrollo.

---

## 🌿 Estrategia de Branching: GitFlow

Se adoptó **GitFlow** como estrategia de branching por las siguientes razones:

| Criterio | Justificación |
|---|---|
| **Ambientes diferenciados** | Permite tener `main` (producción) y `develop` (integración) claramente separados |
| **Flujo colaborativo** | Cada feature se desarrolla en su propia rama, minimizando conflictos |
| **Trazabilidad** | Cada cambio queda registrado mediante un Pull Request revisado |
| **Hotfixes controlados** | Los hotfixes se pueden aplicar a producción sin afectar el desarrollo en curso |

### Diagrama de flujo GitFlow

```
main ──────────────────────────────────────────▶
  │                                      ▲  ▲
  └──▶ develop ────────────────────────▶ │  │
           │          ▲            ▲     │  │
           └─▶ feature/... ──────▶ │    │  │
                       └─▶ feature/... ─ │  │
                                         │  │
  hotfix/... ─────────────────────────────── │
```

### Ramas principales

| Rama | Descripción |
|---|---|
| `main` | Código en producción. Solo recibe merges de `develop` o `hotfix/*` |
| `develop` | Rama de integración. Todas las features se fusionan aquí |

### Ramas de soporte

| Tipo | Origen | Destino |
|---|---|---|
| `feature/*` | `develop` | `develop` |
| `hotfix/*` | `main` | `main` + `develop` |
| `release/*` | `develop` | `main` + `develop` |

---

## 🏷️ Naming de Ramas

```
feature/<nombre-descriptivo>
hotfix/<descripcion-del-bug>
release/<version>
```

**Ejemplos válidos:**
```bash
feature/endpoint-health-check
feature/endpoint-calculadora
hotfix/fix-status-code-500
release/v1.0.0
```

**Reglas:**
- Solo minúsculas y guiones medios (`-`)
- Nombres descriptivos en español o inglés (consistente por proyecto)
- Máximo 50 caracteres

---

## 📝 Convenciones de Commits (Conventional Commits)

Se utiliza el estándar **[Conventional Commits v1.0.0](https://www.conventionalcommits.org/)**.

### Formato

```
<tipo>(<alcance>): <descripción>

[cuerpo opcional]

[footer(s) opcionales]
```

### Tipos permitidos

| Tipo | Cuándo usarlo |
|---|---|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de un bug |
| `docs` | Cambios en documentación |
| `style` | Formato, espacios, comas (sin cambio de lógica) |
| `refactor` | Refactorización sin nueva funcionalidad ni fix |
| `test` | Agregar o mejorar tests |
| `chore` | Tareas de mantenimiento, CI, dependencias |
| `ci` | Cambios en pipelines de CI/CD |

### Ejemplos

```bash
feat(api): agregar endpoint GET /health
fix(calculadora): corregir división por cero
docs(readme): agregar sección de convenciones de commits
ci(workflow): configurar pipeline para pull_request a main
chore: agregar .gitignore y dependencias base
```

---

## 👥 Estrategia de Revisión de Código

Todo cambio de código debe seguir el siguiente proceso:

1. **Crear rama** desde `develop` (o `main` para hotfixes) con nombre descriptivo
2. **Desarrollar** haciendo commits atómicos con Conventional Commits
3. **Abrir Pull Request** hacia la rama destino con:
   - Título descriptivo con el tipo de cambio
   - Descripción explicando **qué** y **por qué**
   - Checklist de revisión completada
4. **Code Review**: al menos 1 aprobación requerida antes del merge
5. **Merge**: usar **Squash and Merge** para mantener historial limpio en `develop`/`main`

### Checklist de PR (template)

```markdown
## ¿Qué cambia este PR?
[Descripción breve]

## ¿Por qué?
[Motivación del cambio]

## Checklist
- [ ] El código sigue las convenciones del proyecto
- [ ] Los commits usan Conventional Commits
- [ ] El pipeline de CI pasa correctamente
- [ ] Se actualizó documentación si corresponde
```

---

## ⚙️ Pipeline CI/CD

El archivo `.github/workflows/main.yml` define el pipeline que se ejecuta en:

- **`push` a `develop`**: corre tests y valida el código
- **`pull_request` a `main`**: verifica que el código está listo para producción

### Etapas del pipeline

```
Trigger → Checkout → Setup Python → Install deps → Run tests → Lint
```

---

## 🛠️ Cómo ejecutar el proyecto

### Requisitos

- Python 3.11+
- pip

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/ChrisJareed/devops-ev1.git
cd devops-ev1

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
python app.py
```

### Endpoints disponibles

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Mensaje de bienvenida |
| `GET` | `/health` | Estado del servicio |
| `GET` | `/api/calcular?a=5&b=3&op=suma` | Calculadora básica |

---

## 📁 Estructura del Proyecto

```
devops-ev1/
├── .github/
│   └── workflows/
│       └── main.yml        # Pipeline CI/CD
├── tests/
│   └── test_app.py         # Tests unitarios
├── app.py                  # Aplicación Flask principal
├── requirements.txt        # Dependencias Python
├── .gitignore
└── README.md
```

---

*Desarrollado para la Evaluación Parcial 1 — DOY0101 Ingeniería DevOps — Duoc UC*
