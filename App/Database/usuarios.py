from App.Database.connector import Query
from App.schemas.usuarios import Usuario

def criar_usuario(usuario:Usuario):
    return Query("INSERT INTO usuarios(usuario_nome, usuario_email, usuario_senha) VALUES (%s, %s, %s)", (Usuario.usuario_nome, Usuario.usuario_email, Usuario.usuario_senha, ))

def obter_usuario(nome:str="", id:int=0, email:str="", senha:str=""):
    if nome:
        return Query("SELECT * FROM usuarios WHERE usuario_nome = %s", (nome))
    elif id:
        return Query("SELECT * FROM usuarios WHERE usuario_id = %s", (id))
    elif email:
        return Query("SELECT * FROM usuarios WHERE usuario_email = %s", (email))
    elif senha:
        return Query("SELECT * FROM usuarios WHERE usuario_senha = %s", (senha))

def remover_usuario(nome:str="", id:int=0, email:str="", senha:str=""):
    if nome:
        return Query("DELETE FROM usuarios WHERE usuario_nome = %s", (nome))
    elif id:
        return Query("DELETE FROM usuarios WHERE usuario_id = %s", (id))
    elif email:
        return Query("DELETE FROM usuarios WHERE usuario_email = %s", (email))
    elif senha:
        return Query("DELETE FROM usuarios WHERE usuario_senha = %s", (senha))

def atualizar_usuario_valores(nome:str="", id:int=0, email:str="", senha:str=""):
    if nome:
        return Query("UPDATE usuarios set usuario_nome = %s WHERE ", (nome))
    if id:
        return Query("DELETE FROM usuarios WHERE usuario_id = %s", (id))
    if email:
        return Query("DELETE FROM usuarios WHERE usuario_email = %s", (email))
    if senha:
        return Query("DELETE FROM usuarios WHERE usuario_senha = %s", (senha))

def atualizar_usuario_completo():
    ...

def autorizar_usuario_por_email_senha(email:str, senha:str):
    ...