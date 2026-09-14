from pydantic import BaseModel


class Prova(BaseModel):
    nome_materia: str
    nome_bobica: str


class ProvaResponse(BaseModel):
    nome_materia: str
    nome_bobica: str