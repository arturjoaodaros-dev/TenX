from pydantic import BaseModel


class Usuario(BaseModel):
    usuario_nome:str
    usuario_email:str
    usuario_senha:str


class UsuarioResponse(BaseModel):
    usuario_id:int
    usuario_nome:str
    usuario_email:str