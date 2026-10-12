# Contribuer à visites

## Flux de travail (GitHub Flow)

1. Partir de `main` à jour : `git switch main && git pull`
2. Créer une branche courte nommée selon son objet :
   `feat/…`, `fix/…`, `docs/…`, `test/…`, `chore/…`
3. Faire de petits commits signés et conventionnels (voir ci-dessous)
4. Pousser la branche et ouvrir une pull request avec `gh pr create`.
   La description indique : **quoi**, **pourquoi**, **comment tester**.
5. Revue par l'autre membre du binôme : lecture du diff et test en local
   (`gh pr checkout <num>`). Les corrections se font par **nouveaux commits**
   (pas de `--amend` sur une branche en cours de revue).
6. Avant fusion, mettre la branche à jour par **rebase** :
   `git fetch && git rebase origin/main`, puis `git push --force-with-lease` (jamais `--force`).
7. Fusion par **squash** uniquement, après approbation :
   `gh pr merge <num> --squash --delete-branch`
8. L'historique de `main` reste linéaire : aucun commit de fusion.

## Convention de commits

Format Conventional Commits (https://www.conventionalcommits.org/fr/v1.0.0/) :

    <type>(<portée>): <description à l'impératif>

Types : `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`.
Exemple : `feat(api): ajouter POST /reset pour remettre le compteur à zéro`

Tous les commits et tags sont **signés** avec une clé SSH.

## Lancer le projet et les tests

    python3 -m venv .venv && source .venv/bin/activate
    pip install -e ".[dev]"
    docker run -d --name redis -p 6379:6379 redis:8-alpine
    pytest -q                    # tests unitaires (fakeredis)
    pytest -q -m integration     # tests d'intégration (Redis réel)
    uvicorn app.main:app --reload

## pre-commit

    pre-commit install           # une fois après le clone
    pre-commit run --all-files   # lancer tous les contrôles à la main

Les hooks (ruff, ruff-format, contrôles de base) s'exécutent à chaque commit.
Un commit refusé se corrige, il ne se contourne pas avec `--no-verify`.
