# Estilo de código

Rige para **todo `.py` nuevo**.

## Reglas críticas

- **Cero prosa: ni comentarios ni docstrings.** Nada de `#`, y tampoco docstring de módulo, de clase, de
  función ni de atributo. La única excepción es el shebang.
- **El código va en inglés.** Nombres de fichero y de módulo, clases, funciones, métodos, variables,
  constantes, miembros de enum, excepciones, nombres de test y los mensajes de error que ve una persona.
- **Sin imports relativos.** Todo import parte del paquete: `from my_cookbook.recipes.domain.recipe import Recipe`.
- **Imports al inicio del fichero**, nunca dentro de una función, un método o una clase. Agrupados:
  stdlib, terceros, proyecto, separados por una línea en blanco.
- **Todo está tipado**: parámetros, retornos y atributos.
- **Formato lo decide `ruff format`**, y `ruff check` no puede dar avisos.

## Por qué cero prosa

Si un trozo de código no se entiende sin un párrafo al lado, el arreglo es el código y no el párrafo:
nombres que digan lo que hacen, funciones pequeñas con una responsabilidad, tipos que hagan imposible el
mal uso, constantes con nombre en vez de literales. Un `if` que necesitaba tres líneas de explicación es
casi siempre un método con nombre esperando a nacer.

El *por qué* va al registro duradero: el cuerpo de la pull request y `docs/`.

## Antipatrones

- Un comentario o un docstring explicando código que se podría renombrar. Hay que reescribir el código.
- Un import dentro de una función o de un método.
- Un identificador en castellano que no sea dato de un contrato.
- Una condición redundante: si `len(value) < 5` ya cubre la cadena vacía, `value == ""` sobra.
