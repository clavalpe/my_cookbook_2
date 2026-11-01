# my_cookbook — instrucciones del repo

API interna de un recetario: FastAPI + PostgreSQL, con dominio, aplicación e infraestructura separados.
El código va en inglés; la documentación, en castellano.

## Regla crítica: convenciones primero

**ANTES de proponer cualquier cambio de código, incluidos los tests:**

1. **IDENTIFICAR** la capa afectada en la tabla de abajo.
2. **LEER** con la herramienta Read el fichero de `docs/conventions/` que le corresponde, en esta sesión.
   No vale recordarlo de otra.
3. **APLICAR** lo que dice, literalmente.
4. **NO** asumir, no improvisar, no traer patrones de otros proyectos.

### Convenciones por capa

**Siempre**, antes de cualquier cambio de código: `docs/conventions/code-style.md`.

| Si vas a tocar... | Leer |
|---|---|
| Estructura de carpetas, dependencias, herramientas | `docs/conventions/architecture.md` |
| Entidades, value objects, puertos, excepciones | `docs/conventions/domain.md` |
| Casos de uso | `docs/conventions/application.md` |
| Adaptadores, endpoints, base de datos, migraciones | `docs/conventions/infrastructure.md` |
| Tests, mothers, dobles | `docs/conventions/testing.md` |
| Ramas, commits, pull requests, merge | `docs/conventions/git-workflow.md` |

### Quién lee cada cosa

| Qué es | Dónde vive | Quién lo lee |
|---|---|---|
| **La vara del código** | `code-style`, `architecture`, `domain`, `application`, `infrastructure`, `testing` | Quien implementa antes de escribir y quien revisa antes de bloquear |
| **Cómo se trabaja aquí** | `git-workflow.md`, este `CLAUDE.md` | Tú y yo en sesión |

## Código que NO es referencia

Preceden a las convenciones. No los imites al escribir código nuevo:

- `main.py` en la raíz: resto del "Hello World" inicial, duplica `src/app.py`.
- `Recipe` y `CreateRecipe`: todavía no cumplen del todo `docs/conventions/domain.md` (la receta no tiene
  id) ni `docs/conventions/application.md` (el nombre del parámetro de `execute`). Se migran al tocarlos.

## Cómo se trabaja

- **TDD**: primero el test en rojo, luego el código mínimo en verde, luego el refactor.
- **Outside-in**: primero el caso de uso con los puertos doblados, luego el adaptador y el endpoint.
- **Una regla de negocio se escribe una vez**, en el dominio.

## Cómo se mide un cambio

```bash
make env-start   # levanta app y db
make linting     # ruff check + ruff format --check + mypy
make test        # pytest dentro del contenedor
```

Todo verde antes de dar nada por terminado. Los comandos corren dentro del contenedor `app`; el `Makefile` es
la interfaz.

## Base de datos

PostgreSQL 17 (servicio `db` de `docker/docker-compose.yml`), SQLAlchemy 2 y alembic. El esquema lo crean las
migraciones (`make migrations`, `make migrate`), nunca `create_all`.
