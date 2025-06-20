# Fit API

## 1. Présentation du projet

Fit API est une application Python basée sur FastAPI permettant de manipuler, filtrer et exposer des données d’utilisateurs GitHub via une API REST sécurisée. Elle inclut un script d’extraction et de filtrage des utilisateurs, ainsi qu’une API pour la gestion et la recherche d’utilisateurs.

## 2. Arborescence du projet

```
fit_api/
│
├── api/                  # Code source de l’API FastAPI
│   ├── __init__.py
│   ├── main.py           # Point d’entrée de l’API
│   ├── models.py         # Modèles de données (Pydantic)
│   ├── routes.py         # Définition des routes/endpoints
│   └── security.py       # Gestion de l’authentification
│
├── data/                 # Données utilisateurs (JSON)
│   ├── users.json
│   └── filtered_users.json
│
├── extract_users.py      # Script d’extraction et de filtrage des utilisateurs GitHub
├── main.py               # Classe utilitaire pour l’API GitHub
├── requirements.txt      # Dépendances Python
└── README.md             # Documentation
```

## 3. Prérequis

- Python 3.8 ou supérieur
- Un accès à internet pour l’extraction des utilisateurs GitHub
- Un token GitHub personnel (pour éviter les limitations d’API)

## 4. Installation des dépendances

Dans le dossier du projet, exécutez :

```bash
python -m venv .venv
source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configuration de l’environnement

Créez un fichier `.env` à la racine du projet avec votre token GitHub :

```
GITHUB_TOKEN=VOTRE_TOKEN_GITHUB
```

## 6. Préparation des données

Pour extraire et filtrer les utilisateurs GitHub :

```bash
python extract_users.py
```

- `data/users.json` : contient les utilisateurs extraits de GitHub
- `data/filtered_users.json` : contient les utilisateurs filtrés (bios, avatars, date de création)

## 7. Lancement de l’API

Dans le dossier du projet, lancez l’API avec Uvicorn :

```bash
uvicorn api.main:app --reload
```

L’API sera accessible sur `http://127.0.0.1:8000`.

## 8. Utilisation de l’API

L’API est sécurisée par authentification HTTP Basic (voir section Sécurité).

### Endpoints principaux :

- `GET /total_user` : Nombre total d’utilisateurs
- `GET /users` : Liste de tous les utilisateurs
- `GET /users/search?q=mot` : Recherche d’utilisateurs par login
- `GET /users/{user_id}` : Détails d’un utilisateur par ID
- `POST /users` : Création d’un utilisateur (JSON User)
- `PUT /users/{user_id}` : Mise à jour d’un utilisateur
- `DELETE /users/{user_id}` : Suppression d’un utilisateur
- `GET /users/login/{login}` : Recherche par login exact

La documentation interactive est disponible sur `/docs` (Swagger UI).

## 9. Sécurité et authentification

L’accès à l’API nécessite une authentification HTTP Basic. Les identifiants sont définis dans `api/security.py` :

- Utilisateur : `elvis` / Mot de passe : `elvis_mot_de_passe`
- Utilisateur : `admin` / Mot de passe : `admin123`

Vous pouvez modifier ou ajouter des utilisateurs dans le dictionnaire `USERS`.

## 10. Extraction et filtrage des utilisateurs GitHub

Le script `extract_users.py` permet :
- d’extraire des utilisateurs via l’API GitHub (pagination, enrichissement des données)
- de filtrer les utilisateurs (bio, avatar, date de création)
- de sauvegarder les résultats dans `data/`

**Attention :** Respectez les limitations de l’API GitHub (erreurs 403/429 gérées automatiquement).

## 11. Tests et vérification

- Vérifiez que le serveur démarre sans erreur.
- Testez les endpoints via `/docs` ou un outil comme Postman.
- Vérifiez la présence des fichiers JSON dans `data/` après extraction.

## 12. FAQ / Problèmes courants

- **Erreur 403/429 lors de l’extraction** : Vérifiez votre token GitHub et attendez avant de relancer.
- **Problème d’authentification API** : Vérifiez les identifiants dans `api/security.py`.
- **Dépendances manquantes** : Relancez `pip install -r requirements.txt` dans l’environnement virtuel.

## 13. Auteurs et contact

- Projet réalisé par [Votre Nom / Équipe]
- Contact : [votre.email@exemple.com]

---

Ce projet est compatible Windows, macOS et Linux. Toutes les commandes sont à exécuter dans un terminal adapté à votre système d’exploitation.
