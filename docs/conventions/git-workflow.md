# Branch, pull request, merge

## Nothing is committed directly to `main`

Not even a typo.

```bash
git switch -c <type>/<slug>          # feat/create-recipe-endpoint, docs/conventions
git push -u origin <type>/<slug>
gh pr create                          # body with the intent: what was wrong and no longer is
gh pr merge <N> --squash --delete-branch
git switch main && git pull --ff-only
```

## The rules and their reason

- **`--squash`**: one commit per pull request reaches `main`, with the pull request title as its message.
- **The pull request title is a conventional commit** (`feat(recipes): ...`, `fix(...)`, `docs(...)`,
  `refactor(...)`, `test(...)`, `chore(...)`).
- **The pull request body tells the why**, not the diff: if you delete the change, what is left broken or
  impossible? Code carries no prose, so this is the durable record of decisions.
- **`make linting` and `make test` green before opening the pull request.**
- **A pull request carries as many commits as needed, and each correction round goes in its own.** TDD
  cycles can go as `Red` and `Green` commits inside the branch: the squash folds them.
- **`git add` with explicit paths**, never `-A` or `.`, so nothing nobody declared gets dragged into the
  commit. Before taking a commit as done, `git status` must be clean.

## Anti-patterns

- A commit on `main`.
- `--merge` or `--rebase` when merging.
- A pull request title that is not a conventional commit.
- A pull request body that summarizes the diff.
- `git add -A`.
