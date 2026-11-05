from App.Database import usuarios as udb
from App.schemas import usuarios as usc
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

@router.post("/")
def autorizar_usuario(usuario: usc.UsuarioLogin):
    if udb.autorizar_usuario_por_email_senha(usuario.email, usuario.senha):
        return {
            "Authorization":True
        }
    raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")

@router.post("/criar")
def criar_usuario(nome, email, senha):
    udb.criar_usuario(nome, email, senha)