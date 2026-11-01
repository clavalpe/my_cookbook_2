# Rama, pull request, merge

## Nada se commitea directamente en `main`

Ni siquiera un typo.

```bash
git switch -c <type>/<slug>          # feat/create-recipe-endpoint, docs/conventions
git push -u origin <type>/<slug>
gh pr create                          # cuerpo con la intención: qué estaba mal y deja de estarlo
gh pr merge <N> --squash --delete-branch
git switch main && git pull --ff-only
```

## Las reglas y su motivo

- **`--squash`**: a `main` llega un solo commit por pull request, con el título de la pull request como
  mensaje.
- **El título de la pull request es un commit convencional** (`feat(recipes): ...`, `fix(...)`,
  `docs(...)`, `refactor(...)`, `test(...)`, `chore(...)`).
- **El cuerpo de la pull request cuenta el porqué**, no el diff: si borras el cambio, ¿qué queda roto o
  imposible? El código no lleva prosa, así que este es el registro duradero de las decisiones.
- **`make linting` y `make test` en verde antes de abrir la pull request.**
- **Una pull request lleva los commits que hagan falta, y cada ronda de corrección va en el suyo.** Los
  ciclos de TDD pueden ir como commits `Red` y `Green` dentro de la rama: el squash los funde.
- **`git add` con rutas explícitas**, nunca `-A` ni `.`, para no arrastrar al commit lo que nadie declaró.
  Antes de dar un commit por hecho, `git status` tiene que salir limpio.

## Antipatrones

- Un commit en `main`.
- `--merge` o `--rebase` al mergear.
- Un título de pull request que no es un commit convencional.
- Un cuerpo de pull request que resume el diff.
- `git add -A`.
