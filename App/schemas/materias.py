from pydantic import BaseModel

class Materia(BaseModel):
    nome: str
    id: int

class MateriaResponse:
    nome: str