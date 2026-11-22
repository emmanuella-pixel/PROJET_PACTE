from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth

app = FastAPI(
    title="API Projet 3pH - Agriculture de Précision",
    description="Backend de supervision IoT pour l'exploitation pilote de Bobo-Dioulasso",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/")
def root():
    return {"status": "online", "projet": "3pH", "site": "Bobo-Dioulasso"}