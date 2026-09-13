from fastapi import FastAPI
from App.Routers import materias, bobicas

app = FastAPI()

app.include_router(materias.router)
app.include_router(bobicas.router)