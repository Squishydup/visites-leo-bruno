# Journal

## TP01

### Questions d'observation
- **Q1 – Délai de changement** : premier commit à 14:04:50, fusion sur main vers 14:50, soit environ 45 minutes.
- **Q2 – Ce qui ne dépend pas de GitHub** : Git lui-même (branches, commits, rebase, conflits), la signature SSH des commits et des tags, pre-commit, Conventional Commits. Tout cela marche tel quel sur GitLab, Gitea ou Forgejo. Ce qui change : la CLI `gh` (remplacée par `glab`, `tea`…), le vocabulaire (Merge Request sur GitLab), l'ajout des clés SSH et les règles de protection de branche.
- **Q3 – Pourquoi signer les commits** : la forge sait qui a poussé, pas qui a écrit le commit (le nom et l'email d'un commit se falsifient facilement). La signature prouve l'auteur et reste vérifiable si le dépôt est cloné, poussé par quelqu'un d'autre ou migré vers une autre forge.

### Réponses aux questions des étapes
- **allowed_signers** : associe un email à une clé publique SSH ; `git log --show-signature` s'en sert pour dire si une signature vient d'une clé autorisée pour cet auteur.
- **Modèle vs fork** : un dépôt créé depuis un modèle est indépendant (un seul commit, sans historique ni lien) ; un fork reste lié à l'original et garde son historique.
- **Branche locale après squash** : le squash crée un nouveau commit sur main, donc Git considère que les commits de la branche locale ne sont pas fusionnés ; `git branch -d` refuse, il faut `-D`.
- **--force-with-lease** : refuse d'écraser la branche distante si elle a changé depuis notre dernier fetch, contrairement à `--force` qui écrase tout.
- **Commit mal formaté / --no-verify** : pre-commit bloque le commit et ruff corrige le fichier, à re-ajouter ; `--no-verify` saute les hooks, d'où l'intérêt de refaire ces contrôles en CI.

### Ce qui a pris le plus de temps
- Installation de l'environnement (Git, gh, Docker absents de la VM) et une première VM perdue en cours de route.
- Connexion de `gh` sans navigateur sur la VM (code d'appareil).
- Pas de dépôt modèle fourni : création du modèle nous-mêmes.
- Deux conflits résolus par rebase : `tests/test_api.py` (ajouts concurrents) et le titre du README.

## TP02

### Secret historique (étape 5)
- Contexte : notre dépôt n'ayant pas été créé depuis le modèle du formateur, nous avons planté nous-mêmes un faux jeton avant de protéger `main`, pour reproduire le scénario.
- Détecté par `gitleaks git --verbose --redact .` : règle `generic-api-key`, entropie 5,27.
- Commit fautif : `c84a70dbd9e8632f6edc6eac6ed1eb1d60cf7294`, auteur Léo Berganton, 13/10/2026 06:47 UTC, fichier `app/old_settings.py` ligne 2.
- Décision sur l'historique : nous ne réécrivons pas l'historique (`git filter-repo` obligerait tout le monde à recloner et ne supprime pas les copies déjà faites : forks, clones, caches).
- Rotation : le secret a été poussé sur une forge publique, il est donc considéré comme compromis. Un vrai jeton aurait été révoqué immédiatement chez le fournisseur et remplacé par un nouveau, stocké hors du dépôt (variable d'environnement ou gestionnaire de secrets). Ici : fichier supprimé du dépôt, empreinte ajoutée à `.gitleaksignore` pour que le rapport historique soit propre (`docs/gitleaks.json`, code retour 0).
