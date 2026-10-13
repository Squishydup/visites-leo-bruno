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

### Étapes 1 à 4
- **Règles (ruleset `main`)** : PR obligatoire avec 1 approbation et « dismiss stale approvals », historique linéaire, commits signés, suppression et force push bloqués. Test : push direct refusé (`GH013 … Changes must be made through a pull request`) ; PR #8 avec commit non signé bloquée (« Commits must have verified signatures »), puis fermée.
- **Pourquoi « dismiss stale approvals »** : une approbation est annulée dès qu'un nouveau commit est poussé ; sinon on pourrait faire approuver une PR saine puis y ajouter du code malveillant avant de fusionner.
- **CODEOWNERS** : valide (`codeowners/errors` vide) ; la PR Dependabot #10 qui touche `.github/` a affiché « Waiting on code owner review from Squishydup ».
- **Propriétaire absent** : si le seul propriétaire d'un dossier est absent, plus rien ne peut être fusionné sur ce dossier. Il faut au moins deux propriétaires (ou une équipe) par zone sensible et un administrateur capable de débloquer en urgence.
- **Dependabot** : pip, github-actions et docker, hebdomadaire, préfixe `chore(deps)` ; 5 PR ouvertes dès l'activation (#11 à #15, limite par défaut de 5 PR simultanées). Alertes de sécurité activées.
- **PR Dependabot ouverte par un robot** : elle doit quand même être approuvée par un humain (et par le propriétaire de code concerné). C'est voulu : une mise à jour peut casser l'application ou introduire un paquet compromis.
- **gitleaks en pre-commit** : commit avec `AWS_SECRET_ACCESS_KEY = "…"` refusé (règle `generic-api-key`, entropie 5,17, `app/config.py` ligne 13). En renommant la variable en `TRUC`, le même secret passe : la détection repose surtout sur le nom (mots-clés key/secret/token) combiné à l'entropie de la valeur.
- Hook gitleaks en `repo: local` (binaire installé sur la VM) : la version officielle compilait Go pendant plus de 15 minutes sur la VM.

### Questions d'observation
- **Q1** : auraient empêché le secret d'arriver sur main : la revue obligatoire (humaine), gitleaks en pre-commit et un contrôle gitleaks requis en CI (automatiques). La plus fiable est le contrôle requis côté serveur (CI) : il ne dépend ni de l'attention du relecteur ni de l'installation locale.
- **Q2** : non, pre-commit ne s'exécute que chez ceux qui l'ont installé, et `git commit --no-verify` le contourne. Il faut ajouter gitleaks au pipeline CI et en faire un contrôle requis dans le ruleset (TP03).
- **Q3** : quasiment aucun délai : des robots scrutent les dépôts publics en continu et récupèrent un secret en quelques minutes, voire secondes. GitHub Secret Scanning (programme partenaires) détecte et fait révoquer automatiquement certains jetons, notamment les jetons GitHub (PAT, OAuth) et des jetons de partenaires comme npm ou PyPI ; AWS met en quarantaine les clés exposées.

### Ce qui a pris le plus de temps
- Attendre l'approbation de l'autre à chaque PR (les règles l'imposent, y compris pour le propriétaire du dépôt).
- La compilation du hook gitleaks officiel (Go) sur la VM.
