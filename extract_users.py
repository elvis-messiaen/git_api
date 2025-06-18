import base64
import json
import os
import time
from dotenv import load_dotenv
from requests import get
from datetime import datetime
from collections import Counter

load_dotenv()
token = os.getenv("GITHUB_TOKEN")


def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def get_users(list_id: list):
    users_data = []

    for id_user in list_id:
        while len(users_data) < 1000:
            url = f"https://api.github.com/users?since={id_user}&per_page=30"
            result = get(url, headers=get_auth_header(token))

            if result.status_code == 200:
                json_result = result.json()
                users_data.extend(json_result)
                if json_result:
                    id_user = json_result[-1]["id"]
                else:
                    break

            elif result.status_code == 403:
                print("Erreur 403: Accès interdit. Vérifie ton token ou tes permissions.")
                return []

            elif result.status_code == 429:
                print("Erreur 429: Trop de requêtes. Pause automatique.")
                time.sleep(60)

            else:
                print(f"Erreur {result.status_code}: {result.reason}")
                return []

    return users_data


def enrich_users(users):
    enriched_data = []
    for user in users:
        user_url = f"https://api.github.com/users/{user['login']}"
        try:
            response = get(user_url, headers=get_auth_header(token))
            if response.status_code == 200:
                user_info = response.json()
                enriched_data.append({
                    "login": user_info.get("login"),
                    "id": user_info.get("id"),
                    "created_at": user_info.get("created_at"),
                    "avatar_url": user_info.get("avatar_url"),
                    "bio": user_info.get("bio") or "Pas de bio disponible"
                })
            elif response.status_code == 403:
                print(f"Erreur 403: Impossible de récupérer {user['login']}.")
            elif response.status_code == 429:
                print("Erreur 429: Trop de requêtes, pause automatique.")
                time.sleep(60)
        except Exception as e:
            print(f"Erreur lors de l'enrichissement des données : {str(e)}")

    return enriched_data


def save_to_json(data, filename="data/users.json"):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Données enregistrées dans {filename}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du fichier JSON: {str(e)}")


def filter_users(input_file="data/users.json", output_file="data/filtered_users.json"):
    try:
        if not os.path.exists(input_file):
            print(f"Le fichier {input_file} n'existe pas.")
            return

        with open(input_file, "r", encoding="utf-8") as file:
            users = json.load(file)

        if not isinstance(users, list):
            print("Erreur : Les données JSON ne sont pas sous forme de liste.")
            return

        unique_users = list({user["id"]: user for user in users}.values())

        bio_removed_count = sum(1 for user in unique_users if not user.get("bio") or user.get("bio") == "Pas de bio disponible")
        avatar_removed_count = sum(1 for user in unique_users if not user.get("avatar_url"))
        created_at_removed_count = sum(1 for user in unique_users if not user.get("created_at") or user.get("created_at") <= "2015-01-01T00:00:00Z")

        print(f"Nombre de bios supprimées : {bio_removed_count}")
        print(f"Nombre d'avatars supprimés : {avatar_removed_count}")
        print(f"Nombre de comptes créés avant 2015 supprimés : {created_at_removed_count}")

        unique_users = [user for user in unique_users if user.get("bio") and user.get("bio") != "Pas de bio disponible" and user.get("avatar_url")]

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(unique_users, file, indent=4, ensure_ascii=False)

        print(f"Données enregistrées dans {output_file}")

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")



def check_duplicate_ids(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        users = json.load(file)

    ids = [user["id"] for user in users]
    duplicates = [id for id, count in Counter(ids).items() if count > 1]

    print(f"IDs en doublon : {duplicates}")
    return duplicates


list_id = [5555]
users = get_users(list_id)
users = enrich_users(users)
#save_to_json(users)
filter_users(input_file="data/users.json", output_file="data/filtered_users.json")
#check_duplicate_ids("data/filtered_users.json")
