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

## Names speak the business

Every name -variables, parameters, attributes, methods, constants and tests- is written in the terms of
the recipe book, not in the terms of how the code works. A reader who knows the business and has never seen
the code must understand it.

- Name a thing for **what it is for the business**: `requested_name`, `saved_recipe`, `short_name`; not for
  its mechanism: `dto_name`, `call_args`, `data`, `tmp`, `obj`.
- Name an action for **what happens to the recipe**: `save`, `reject`, `keep`; not for how: `hand`, `pass`,
  `forward`, `invoke`.
- Names that the architecture already fixes for a layer stay as they are (`RecipeRepository`,
  `CreateRecipeDTO`, `execute`). The rule applies to everything the author chooses.
- **A test double is named as a double**, so the reader sees which collaborators are not real: the `mock_`
  prefix for an autospec double (`mock_recipe_repository`) and `fake_` for a hand-written one. The rest of the
  name stays in business terms. This is the only place where a mechanism word belongs in a name.
- A generic container name (`data`, `result`, `item`, `value`, `info`) is allowed only when the business has
  no better word for it.


- A comment or docstring explaining code that could be renamed. Rewrite the code.
- An import inside a function or method.
- An identifier in Spanish that is not contract data.
- A name that describes the mechanism instead of the business: `dto_name`, `call_args`, `tmp`.
- A test double whose name hides that it is a double: `recipe_repository` for an autospec double.
- A redundant condition: if `len(value) < 5` already covers the empty string, `value == ""` is superfluous.
