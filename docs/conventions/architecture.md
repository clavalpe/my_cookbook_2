# Arquitectura y herramientas

## Estructura

```
src/
  app.py                              entrypoint de FastAPI: monta las dependencias y registra los routers
  my_cookbook/
    {contexto}/                       un contexto por área de negocio (hoy, `recipes`)
      domain/
        {value_object}.py             un value object por módulo
        {entity}.py                   una entidad por módulo
        {puerto}.py                   un puerto por fichero
        exceptions.py                 las excepciones del dominio, juntas
      application/
        {caso_de_uso}.py              un caso de uso por módulo, con su DTO
      infrastructure/
        {impl}_{puerto}.py            el adaptador se llama como su implementación
        {contrato}.py                 un modelo de frontera por concepto
      tests/                          co-localizados, espejando las capas de arriba
        mothers/                      Object Mothers
migrations/                           alembic
```

- **Un concepto por módulo**, y con él lo que no existe sin él. La vara: si borras el concepto principal,
  ¿el otro tipo se queda sin consumidor y sin sentido propio? Solo entonces comparten fichero. Un tipo que
  construye otro sitio o consume otra capa es un concepto y va a su módulo.
- Las excepciones del dominio son la excepción a la regla: viven juntas en `domain/exceptions.py`.
- **El flujo de dependencias va hacia dentro**: `infrastructure` conoce `application` y `domain`,
  `application` conoce `domain`, y `domain` no conoce a nadie.
- **Los tests viven dentro del contexto**, no en una carpeta aparte, y espejan las capas que se testean.
  No hay un árbol de tests de dominio (ver `docs/conventions/testing.md`).

## Una regla de negocio se escribe una vez

La regla de tres gobierna el parecido del código: trozos que se repiten se extraen cuando extraerlos deja
el sitio mejor. **No gobierna dónde vive una decisión.** Una regla de negocio -qué nombre es válido, qué
cuenta como receta duplicada- se escribe una vez, en el dominio, y quien la necesita pregunta.

**La vara: si esta decisión cambiara, ¿cuántos ficheros hay que tocar para que el programa siga siendo
coherente?** Uno, o está repartida. Dos sitios que hoy dicen lo mismo con palabras distintas ya están
repartidos.

## Herramientas

Python 3.14, FastAPI, SQLAlchemy 2, alembic, psycopg 3, PostgreSQL 17, `pytest`, `mypy`, `ruff`. Todo se
ejecuta dentro de los contenedores de `docker/`; el `Makefile` es la interfaz.

- **`dataclasses` frozen para value objects y DTOs.** Pydantic solo aparece en los modelos que cruzan la
  frontera HTTP (ver `docs/conventions/infrastructure.md`).
- **`abc.ABC` para puertos**, `StrEnum` para vocabularios cerrados, `unittest.mock` para dobles.

## Antipatrones

- Pydantic en `domain/` o en el DTO de un caso de uso.
- `domain/` importando de `application/` o de `infrastructure/`.
- Una regla de negocio escrita en dos sitios, aunque las dos redacciones sean distintas.
- Un helper que las dos copias llaman desde donde estaban: la decisión sigue repartida, con una
  indirección delante.
