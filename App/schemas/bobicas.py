from pydantic import BaseModel

class Bobica(BaseModel):
    nome: str 
    id: int

class BobicaResponse(BaseModel):
    nome: str