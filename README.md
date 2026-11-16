# bottlestream

Une mini API de tâches avec Bottle, et une interface Streamlit qui l'utilise.

## Installer

```
uv sync
```

## Lancer

Ouvrir deux terminaux, et lancer l'API en premier.

| | Sans `.venv` activé | Avec `.venv` activé |
|---|---|---|
| Terminal 1 : l'API | `uv run api.py` | `python api.py` |
| Terminal 2 : l'interface | `uv run streamlit run app.py` | `streamlit run app.py` |

Pour activer le `.venv` : `source .venv/bin/activate`, à faire dans chaque terminal.

Ensuite, ouvrir http://localhost:8501.
# bottle-api-streamlit
