from fastapi import APIRouter, Request, HTTPException, Depends
from api.models import User
from api.security import check_credentials
from fastapi.responses import JSONResponse

router = APIRouter(dependencies=[Depends(check_credentials)])

@router.get("/total_user", summary="Retourne le nombre total d'utilisateurs")
def total_user(request: Request) -> dict:
    list_users = request.app.state.list_users
    return {"total": len(list_users)}

@router.get("/users", summary="Récupère tous les utilisateurs")
def get_total_user(request: Request) -> list[User]:
    return list(request.app.state.list_users.values())

@router.get("/users/search", summary="Recherche d'utilisateurs par mot-clé dans le login")
def search_users(q: str, request: Request):
    users = request.app.state.list_users
    keyword = q.strip().lower()
    results = [
        user for user in users.values()
        if keyword in user["login"].strip().lower()
    ]
    return {
        "message": f"{len(results)} utilisateur(s) trouvé(s).",
        "results": results
    }

@router.get("/users/{user_id}", summary="Récupère un utilisateur par son identifiant")
def get_user_by_id(user_id: int, request: Request) -> User:
    users = request.app.state.list_users
    if user_id in users:
        return users[user_id]
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

@router.post("/users", status_code=201, summary="Crée un nouvel utilisateur")
def create_user(user: User, request: Request):
    users = request.app.state.list_users
    next_id = max(users.keys()) + 1 if users else 1
    user.id = next_id
    users[user.id] = user.model_dump()
    return {"message": "Utilisateur enregistré avec succès.", "user_id": user.id}

@router.put("/users/{user_id}", summary="Met à jour un utilisateur existant")
def update_user(user_id: int, updated: User, request: Request):
    users = request.app.state.list_users
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    users[user_id] = updated.model_dump()
    users[user_id]["id"] = user_id
    return {"message": "Utilisateur mis à jour", "user_id": user_id}

@router.delete("/users/{user_id}", summary="Supprime un utilisateur")
def delete_user(user_id: int, request: Request):
    users = request.app.state.list_users
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    del users[user_id]
    return {"message": "Utilisateur supprimé", "user_id": user_id}

@router.get("/users/login/{login}", summary="Récupère un utilisateur par son login")
def get_user_by_login(login: str, request: Request):
    users = request.app.state.list_users
    for user in users.values():
        if user["login"] == login:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Utilisateur trouvé.",
                    "user": user
                }
            )
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
