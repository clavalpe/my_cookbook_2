# Capa de dominio

Entidades, value objects, puertos y excepciones. Python puro: no importa FastAPI, SQLAlchemy ni Pydantic.

## Value objects

- **Dataclasses `frozen=True`.** Se validan al construirse: un value object que existe es válido.
- Un dato con una regla (`RecipeName` no puede ser corto) es un value object, no un `str` suelto con la
  validación en el caso de uso.
- **Un value object que tiene el dato posee la pregunta.** Si cada consumidor deriva a mano una condición a
  partir de un campo, la regla está repartida aunque el campo viva en un sitio.
- Se compara por valor, y en los tests se usan instancias reales: nada de mockear value objects.

## Entidades

- Una entidad tiene identidad. **El id nace en el dominio o en la aplicación, nunca en la base de datos**:
  la receta existe con su `RecipeId` (un UUID) antes de guardarse, y `save` no devuelve nada.
- Lo que construye una entidad válida es su constructor; no hay estados a medio construir.

## Vocabulario cerrado

- Un conjunto cerrado de valores es un `StrEnum` en su propio módulo.
- **Un estado ausente es un miembro del vocabulario**, no un `| None`.
- **Un puerto contesta con el vocabulario, no con un `bool`** derivado de él.

## Puertos

- Un puerto abstracto (`abc.ABC`) por fichero, en `domain/`, con el vocabulario del negocio y sin rastro de
  la tecnología: `RecipeRepository.save(recipe)`, no `insert_row`.
- Es lo que el caso de uso conoce. Su adaptador vive en `infrastructure/`.

## Excepciones

- Las del dominio viven juntas en `domain/exceptions.py` y se leen como un catálogo.
- Cada una nombra **una razón de negocio** (`InvalidRecipeName`), no una capa técnica.
- **El mensaje describe el motivo**, no repite el nombre de la clase.

## Nada de `dict` crudo como valor de retorno

Lo que devuelve la lógica del dominio es un value object o una entidad, no un `dict` ni una tupla de
posiciones con significado.

## Antipatrones

- Pydantic, SQLAlchemy o FastAPI importados en `domain/`.
- Un id que solo existe tras guardar.
- Un `bool` o un `| None` donde el dominio tiene un vocabulario.
- Validar un nombre en el caso de uso o en el endpoint en vez de en su value object.
- Una excepción de infraestructura (`IntegrityError`) que se escapa de su adaptador.
