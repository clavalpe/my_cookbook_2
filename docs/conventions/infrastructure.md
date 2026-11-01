# Capa de infraestructura

Adaptadores de los puertos, modelos de frontera y entrypoints. Es la única capa que sabe que hay una base
de datos o un servidor HTTP.

## Lo que llega de fuera se valida al entrar

El cuerpo de una petición se valida con un modelo **Pydantic** por concepto, en `infrastructure/`. Un
campo que no conocemos es un rechazo (`extra="forbid"`), no un campo ignorado. Pydantic no sale de esta
capa: el endpoint convierte el modelo en el DTO del caso de uso y llama a `execute`.

## Contrato HTTP

La API es interna: no hay códigos de estado a medida.

- **Éxito**: el código estándar del verbo (`201` al crear) y el cuerpo que declara el contrato del
  endpoint.
- **Error de negocio o de validación**: siempre **`400`**, con un cuerpo único para toda la API:

```json
{"code": "<ErrorCode>", "detail": "<explicación para una persona>"}
```

- `code` es un `StrEnum` cerrado, con un miembro por excepción del dominio que el entrypoint sabe mapear
  (`InvalidRecipeName` → `INVALID_RECIPE_NAME`). Vive en `infrastructure/`: es vocabulario del contrato,
  no del dominio.
- `detail` es texto legible, en inglés.
- **Una excepción del dominio sin mapeo no se convierte en `400`**: es un fallo del programa y sale como
  `500`. Añadir una excepción al dominio obliga a decidir su `code`.
- El mapeo excepción → `code` se declara en **un solo sitio** (un manejador de excepciones registrado en
  `src/app.py`), no en cada endpoint.
- Un cuerpo de petición mal formado (JSON inválido, campo que falta) también sale como `400` con este
  mismo cuerpo, no con el `422` por defecto de FastAPI.

## Adaptadores

- Implementan un puerto y nada más. **El módulo se llama como la implementación**, no como el puerto:
  `postgres_recipe_repository.py` implementa `RecipeRepository`.
- **La sesión de SQLAlchemy entra por constructor.** El adaptador no la crea ni la cierra; lo hace quien
  monta el grafo de dependencias.
- **El modelo de tabla de SQLAlchemy es de infraestructura** y no se parece necesariamente a la entidad.
  La conversión vive en el adaptador (o en el modelo), nunca en el caso de uso.
- **Una excepción de la librería no sale del adaptador**: se traduce a una excepción propia.

## Base de datos y migraciones

- **El esquema lo crea alembic**, no `create_all`. Cada cambio de tabla es una migración revisable en
  `migrations/`.
- **La configuración sale del entorno** (`PG_*`), leída en un único sitio. Ninguna URL de conexión
  escrita en el código.
- Las migraciones se aplican con `make migrate` y se generan con `make migrations`.

## Entrypoints

- `src/app.py` es el único sitio donde se monta el grafo de dependencias: sesión, adaptador, caso de uso.
  Los endpoints reciben el caso de uso ya construido (por `Depends`).
- Un endpoint hace tres cosas: valida la entrada, llama a `execute`, devuelve el resultado en el formato del
  contrato. Cualquier otra cosa es de otra capa.
- Rutas con barra final, como `/health/`.

## Antipatrones

- Una regla de negocio en un endpoint o en un adaptador.
- Un `try/except` por endpoint para producir el `400`, en vez de un manejador único.
- Un código de estado distinto de `400` para un error de negocio.
- Un modelo Pydantic en `domain/` o `application/`.
- Un adaptador que abre su propia conexión.
- `create_all` en lugar de una migración.
- Una URL o una contraseña de base de datos escrita en el código.
