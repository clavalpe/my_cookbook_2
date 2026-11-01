# Code style

Applies to **every new `.py` file**.

## Critical rules

- **Zero prose: no comments and no docstrings.** No `#`, and no module, class, function or attribute
  docstring. The only exception is the shebang.
- **Code is written in English.** File and module names, classes, functions, methods, variables, constants,
  enum members, exceptions, test names and the error messages a person sees.
- **No relative imports.** Every import starts at the package: `from my_cookbook.recipes.domain.recipe import Recipe`.
- **Imports go at the top of the file**, never inside a function, method or class. Grouped as stdlib,
  third party, project, separated by a blank line.
- **Everything is typed**: parameters, return values and attributes.
- **Formatting is decided by `ruff format`**, and `ruff check` must report nothing.

## Why zero prose

If a piece of code cannot be understood without a paragraph next to it, the fix is the code, not the
paragraph: names that say what they do, small functions with one responsibility, types that make misuse
impossible, named constants instead of literals. An `if` that needed three lines of explanation is almost
always a named method waiting to be born.

The *why* goes to the durable record: the pull request body and `docs/`.

## Anti-patterns

- A comment or docstring explaining code that could be renamed. Rewrite the code.
- An import inside a function or method.
- An identifier in Spanish that is not contract data.
- A redundant condition: if `len(value) < 5` already covers the empty string, `value == ""` is superfluous.
