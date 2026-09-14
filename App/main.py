#Run using uvicorn: uvicorn main:app --reload (ou a partir da raiz: uvicorn App.main:app --reload)
import sys
from pathlib import Path

# Garante que a raiz do projeto esteja no sys.path para resolver 'App'
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from App.Routers import materias, bobicas, provas

app = FastAPI()

app.include_router(materias.router)
app.include_router(bobicas.router)
app.include_router(provas.router)

@app.get("/")
def mensagem_inicial():
    return {
        "content" : "Bem-vindo ao TenX!"
    }