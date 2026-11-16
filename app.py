# app.py : une interface Streamlit qui parle à notre API Bottle.
# Lancer avec : uv run streamlit run app.py (l'API doit déjà tourner).

# requests sert à envoyer des requêtes HTTP à l'API.
import requests
# streamlit sert à construire l'interface web.
import streamlit as st

# L'adresse de notre API.
API = "http://localhost:8000"

# Important : Streamlit relance TOUT ce script, de haut en bas,
# à chaque fois qu'on clique sur quelque chose.

# Le titre de la page.
st.title("Mes tâches")

# Un formulaire pour ajouter une tâche ; il se vide après l'envoi.
with st.form("nouvelle", clear_on_submit=True):
    # Un champ texte pour écrire le titre.
    titre = st.text_input("Nouvelle tâche")
    # Si on clique sur « Ajouter » et que le titre n'est pas vide...
    if st.form_submit_button("Ajouter") and titre:
        # ... on envoie un POST à l'API avec le titre en JSON.
        requests.post(f"{API}/taches", json={"titre": titre})

# Cette fonction est appelée quand on clique sur une case,
# AVANT que Streamlit relance le script.
def cocher(tache_id, faite):
    # On prévient l'API avec un PATCH.
    requests.patch(f"{API}/taches/{tache_id}", json={"faite": faite})


# On envoie un GET à l'API pour avoir les tâches.
reponse = requests.get(f"{API}/taches")
# .json() transforme le JSON reçu en dict Python : {"taches": [...]}
donnees = reponse.json()
# On sort la liste des tâches, rangée sous la clé "taches".
liste = donnees["taches"]

# Pour chaque tâche reçue...
for tache in liste:
    # ... on affiche une case à cocher, cochée si la tâche est faite.
    st.checkbox(
        tache["titre"],
        value=tache["faite"],
        # Une clé unique, pour que Streamlit ne confonde pas deux cases.
        key=tache["id"],
        # La fonction à appeler quand la case change...
        on_change=cocher,
        # ... avec l'id de la tâche et sa nouvelle valeur.
        # Un clic inverse toujours la case : la nouvelle valeur est donc l'inverse.
        args=(tache["id"], not tache["faite"]),
    )
