from pydantic import BaseModel

class Materia(BaseModel):
    nome: str

class MateriaResponse(BaseModel):
    nome: str