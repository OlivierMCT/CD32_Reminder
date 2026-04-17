# 🐍 Création de l'environnement virtuel
```bash
python -m venv .venv
```
## Activation de l'environnement virtuel
### Sur Windows
```bash
.venv\Scripts\activate
```
### Sur macOS/Linux
```bash
source .venv/bin/activate
```

# 📦 Installation des dépendances
```bash
pip install -r requirements.txt
```
Packages utilisés :
- fastapi : framework web pour créer des API
- uvicorn : serveur ASGI pour exécuter l'application FastAPI
- sqlalchemy : ORM pour interagir avec la base de données
- pytest : framework de test pour Python
- mysql-connector-python : connecteur pour MySQL

# 🚀 Démarrage de l'application
```bash
uvicorn main:app --reload
```
Urls :
- http://localhost:8000/docs : documentation interactive de l'API
- http://localhost:8000/redoc : documentation statique de l'API
- http://localhost:8000/todo : exemple d'appel à l'API
- http://localhost:8000/category : exemple d'appel à l'API

# 🧪 Exécution des tests
```bash
python -m pytest tests/ -v
```