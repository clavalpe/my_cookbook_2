# Tests

## Cómo se mide todo

```bash
make linting    # ruff check + ruff format --check + mypy
make test       # pytest dentro del contenedor
```

Los dos corren dentro de los contenedores (`make env-start` antes). Un `pytest` con el intérprete de tu
máquina pasa o falla según lo que tengas instalado, y eso no es una vara.

## Forma de un test

- **Dentro de una clase**, agrupados por el comportamiento que fijan. Nunca funciones sueltas.
- **Cero prosa**: ni comentarios ni docstrings. El nombre del test es la frase.
- El nombre dice **qué se garantiza y por qué**, no qué método se llama:
  `test_does_not_allow_to_create_a_recipe_with_a_short_name`.
- Los helpers de un test son `@staticmethod` de su clase de test o viven en un módulo compartido, nunca
  sueltos a nivel de módulo. Los fixtures van dentro de la clase.
- Estructura arrange / act / assert, separadas por una línea en blanco.

## Qué se testea y qué no

- **Outside-in**, en este orden: primero los casos de uso con los puertos doblados, luego la
  infraestructura. Lo de dentro del dominio se cubre **por ese camino**.
- **No hay tests unitarios de dominio**, ni siquiera cuando el dominio tiene comportamiento: se comprueba
  por el camino real por el que llega. La única excepción es un value object con validación propia que no
  se pueda alcanzar de otra forma. Un test que solo comprueba que un dataclass guarda lo que le pasas mide
  el lenguaje.
- **Aplicación**: puertos doblados por constructor, y el assert sobre el **efecto observable** (qué recibió
  el puerto, qué devolvió el caso de uso).
- **Adaptador de base de datos**: se prueba contra el Postgres real del entorno, no contra una sesión
  doblada. Un doble de `Session` solo comprobaría que llamamos a nuestro propio mapeo. Cada test deja la
  base como la encontró.
- **Endpoint**: con el cliente de pruebas de FastAPI, el caso de uso real y el repositorio doblado. El
  assert es el **código de estado y el cuerpo literal** de la respuesta, no un modelo de ella reescrito en
  el test.
- **Antes de añadir un test, comprobar si el comportamiento ya está cubierto.** Solo entra si aporta una
  dimensión distinta.

## Object Mothers

Los objetos de un test los construye un mother, no el propio test:
`tests/mothers/{cosa}_mother.py`. Da defaults sensatos y deja que cada test nombre **solo lo que su caso
cambia**. Los métodos son escenarios con nombre, no un `create(...)` con todo por defecto.

## Dobles

- **`create_autospec(X, spec_set=True, instance=True)`** para puertos sin estado.
- **Dobles con estado, a mano**, cuando el test necesita preguntar por lo que se le pasó.
- **Un doble dobla lo que su nombre dice y nada más.**
- **Nada de mockear value objects**: se usan instancias reales.
- El arrange **no se construye con la pieza bajo prueba**.

## Asserts

- El assert compara el **valor entero**. Una subcadena suelta da por bueno cualquier texto que la
  contenga.
- Un test que espera una excepción comprueba su tipo y, cuando el mensaje es parte del contrato, el mensaje
  entero.

## Antipatrones

- Un test como función suelta.
- Un comentario o un docstring en un test.
- Un test de dominio que solo ejercita un dataclass.
- Construir un objeto de dominio a mano en el test cuando hay mother.
- Un helper de test suelto a nivel de módulo, o repetido en dos ficheros.
- Un test del adaptador de base de datos contra una `Session` doblada.
- Un test que deja filas en la base para el siguiente.
- Un assert contra un modelo del formato reimplementado en el test, en vez de contra la carga literal.
