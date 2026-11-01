# Capa de aplicación

Los casos de uso. Orquestan; la lógica vive en el dominio y la entrada/salida detrás de un puerto.

## Forma de un caso de uso

- Un módulo por caso de uso, en `application/`, con el nombre del caso de uso en snake_case.
- La clase **sin coletilla**: `CreateRecipe`, no `CreateRecipeUseCase` ni `CreateRecipeService`.
- Método principal `execute(dto: <Name>DTO) -> <Result>`.
- `<Name>DTO` -y `<Name>Result` si devuelve datos- son dataclasses frozen **en el mismo módulo**.
- Las dependencias entran por constructor y son puertos, nunca adaptadores.

```python
# ejemplo/application/{hacer_algo}.py
class {HacerAlgo}:
    def __init__(self, {puerto}: {Puerto}) -> None:
        self._{puerto} = {puerto}

    def execute(self, dto: {HacerAlgo}DTO) -> {Resultado}: ...
```

## Lo que hace

- Construye las entidades y los value objects del dominio a partir del DTO, y se los pasa a los puertos.
- **Genera el id** de lo que crea, cuando la entidad lo necesita y el caso de uso es quien la crea.

## Lo que no hace

- **No traduce a formatos externos.** Devuelve objetos del dominio o un `Result`; serializar es de la
  frontera.
- **No captura excepciones para convertirlas en códigos HTTP.** Las propaga tipadas y las mapea el
  entrypoint.
- **No habla con la base de datos ni con FastAPI.** Solo conoce puertos.
- **No contiene reglas de negocio**: preguntan al dominio.

## Antipatrones

- Un caso de uso que importa un adaptador o `sqlalchemy`.
- Un `try/except` que traduce una excepción del dominio a un código de estado.
- Una regla de negocio escrita en `execute` en vez de en el dominio.
- Un DTO con Pydantic.
