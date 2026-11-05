from App.Database.connector import Query
from App.schemas.usuarios import Usuario

def criar_usuario(usuario_nome, usuario_email, usuario_senha):
    Query("INSERT INTO usuarios(usuario_nome, usuario_email, usuario_senha) VALUES (%s, %s, %s)", (usuario_nome, usuario_email, usuario_senha, ))
    return True
def obter_usuario(nome:str="", id:int=0, email:str="", senha:str="") -> list:
    if nome:
        return Query("SELECT * FROM usuarios WHERE usuario_nome = %s", (nome, ), "data")
    elif id:
        return Query("SELECT * FROM usuarios WHERE usuario_id = %s", (id, ), "data")        
    elif email:
        return Query("SELECT * FROM usuarios WHERE usuario_email = %s", (email, ), "data")
    elif senha:
        return Query("SELECT * FROM usuarios WHERE usuario_senha = %s", (senha, ), "data")
    else:
        return [False]
def remover_usuario(nome:str="", id:int=0, email:str="", senha:str=""):
    try:
        if nome:
            Query("DELETE FROM usuarios WHERE usuario_nome = %s", (nome, ))
            return True
        elif id:
            Query("DELETE FROM usuarios WHERE usuario_id = %s", (id, ))
            return True
        elif email:
            Query("DELETE FROM usuarios WHERE usuario_email = %s", (email, ))
            return True
        elif senha:
            Query("DELETE FROM usuarios WHERE usuario_senha = %s", (senha, ))
            return True
    except:
        return False

def atualizar_usuario_valores(email:str="", senha:str="", **Valores_mudados):
    collumns = []
    values = []
    for k, v in Valores_mudados.items():
        collumns.append(k)
        values.append(v)

    print(collumns, values)
    for i in range(len(collumns)):
        print(collumns[i], values[i])
        if autorizar_usuario_por_email_senha(email, senha):
            print("chegou aqui")
            Query("UPDATE usuarios SET usuario_senha = %s WHERE usuario_email = %s", (values[i], email))
            
    return True

def atualizar_usuario_completo(novo_usuario:Usuario, email:str="", senha:str=""):
    if autorizar_usuario_por_email_senha(email, senha):
            Query("DELETE FROM usuarios WHERE usuario_senha = %s", (senha, ))

    Query("INSERT INTO usuarios(usuario_nome, usuario_email, usuario_senha) VALUES (%s, %s, %s)", (novo_usuario.usuario_nome, novo_usuario.usuario_email, novo_usuario.usuario_senha))
    return True

def autorizar_usuario_por_email_senha(email:str, senha:str):
    i = obter_usuario(email=email)
    if i[0][3] == senha: # type: ignore
        return True
    else:
        return False

