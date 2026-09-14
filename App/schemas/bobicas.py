from pydantic import BaseModel

class Bobica(BaseModel):
    nome: str
    preco_medio: float

class BobicaResponse(BaseModel):
    nome: str
    preco_medio: float