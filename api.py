# api.py : une mini API qui gère une liste de tâches.
# Lancer avec : uv run api.py

# On importe les outils de Bottle dont on a besoin :
# - Bottle : la classe qui crée l'application web ;
# - request : la requête envoyée par le client (ce qu'il nous demande) ;
# - response : la réponse qu'on lui renvoie (on peut changer son code HTTP) ;
# - abort : arrête tout de suite la fonction et renvoie une erreur HTTP.
from bottle import Bottle, request, response, abort

# On crée notre application web.
app = Bottle()

# Nos données, gardées en mémoire dans un dictionnaire (pas de base de données).
# La clé est l'id de la tâche, la valeur est la tâche elle-même.
# Attention : tout est perdu quand on arrête le serveur.
taches = {1: {"id": 1, "titre": "Découvrir Bottle", "faite": False}}


# GET /taches : renvoie la liste de toutes les tâches.
@app.get("/taches")
def lister():
    # taches.values() donne toutes les tâches ; list() en fait une liste.
    # Si on renvoie un dict, Bottle le transforme tout seul en JSON.
    # Si on renvoie une liste, Bottle plante (erreur 500).
    # On range donc la liste dans un dict, sous la clé "taches".
    # Le client reçoit : {"taches": [{"id": 1, ...}, {"id": 2, ...}]}
    return {"taches": list(taches.values())}


# POST /taches : crée une nouvelle tâche.
@app.post("/taches")
def creer():
    # On calcule un nouvel id : le plus grand id existant + 1.
    nouvel_id = max(taches, default=0) + 1
    # On lit le titre envoyé par le client dans le corps JSON de la requête.
    # request est importé une seule fois en haut du fichier, mais Bottle le
    # remplit à chaque appel avec la requête du client en cours.
    # request.json transforme le corps JSON en dict Python :
    # si le client envoie {"titre": "Faire les courses"},
    # alors request.json["titre"] vaut "Faire les courses".
    # Attention : request.json vaut None si le client n'envoie pas l'en-tête
    # Content-Type: application/json. Dans ce cas, ["titre"] plante (erreur 500).
    titre = request.json["titre"]
    # On construit la nouvelle tâche, pas encore faite.
    tache = {"id": nouvel_id, "titre": titre, "faite": False}
    # On l'ajoute à nos données.
    taches[nouvel_id] = tache
    # Code HTTP 201 : « créé ».
    response.status = 201
    # On renvoie la tâche créée au client.
    return tache


# PATCH /taches/<id> : modifie une partie d'une tâche (ici, cochée ou non).
# <tache_id:int> récupère l'id dans l'URL et le convertit en nombre entier.
@app.patch("/taches/<tache_id:int>")
def modifier(tache_id):
    # Si la tâche n'existe pas, on répond 404 : « introuvable ».
    # abort lève une exception : la fonction s'arrête ici et la suite
    # ne s'exécute pas. Bottle attrape l'exception et envoie l'erreur au client.
    # C'est l'équivalent de response.status = 404 suivi d'un return.
    # Attention : Bottle renvoie cette erreur en page HTML, pas en JSON.
    if tache_id not in taches:
        abort(404, "Tâche introuvable")
    # On met à jour le champ "faite" avec la valeur envoyée par le client.
    # Même principe que dans creer() : request.json est le corps JSON en dict,
    # par exemple {"faite": true} donne request.json["faite"] == True.
    taches[tache_id]["faite"] = request.json["faite"]
    # On renvoie la tâche modifiée.
    return taches[tache_id]


# On démarre le serveur sur http://localhost:8000.
# debug=True affiche des messages d'erreur détaillés.
app.run(port=8000, debug=True)
