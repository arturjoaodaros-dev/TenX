#Run using uvicorn: uvicorn main:app --reload (ou a partir da raiz: uvicorn App.main:app --reload)
import sys
from pathlib import Path

# Garante que a raiz do projeto esteja no sys.path para resolver 'App'
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from App.Routers import materias, bobicas, provas, usuarios

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(materias.router)
app.include_router(bobicas.router)
app.include_router(provas.router)
app.include_router(usuarios.router)
@app.get("/")
def mensagem_inicial():
    return {
        "content" : "Bem-vindo ao TenX!"
    }