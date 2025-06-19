import json
from pathlib import Path
from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from api.routes import router
from api.models import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    path = Path(__file__).resolve().parent.parent / "data" / "filtered_users.json"
    with open(path, "r", encoding="utf-8") as f:
        users = json.load(f)
    list_users = {user["id"]: user for user in users}
    app.state.list_users = list_users
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)

