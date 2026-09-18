from App.Database.connector import Query

def criar_materia(nome):
    return Query(
        """
INSERT INTO materias(materia_nome) VALUES(%s)
        """, (nome, ))

def listar_materias(nome: str = ""):
    if nome:
        return [d[1] for d in Query( "SELECT * FROM materias WHERE materia_nome = %s",(nome,),"data")]
    else:
        return [d[1] for d in Query("SELECT * FROM materias", return_info="data")]

def obter_id_por_materia(nome_materia:str):
    try:
        return [d[0] for d in Query( "SELECT * FROM materias WHERE materia_nome = %s",(nome_materia, ),"data")]
    except:
        return "Not found"

def obter_materia_por_id(id_materia):
    for d in Query("SELECT * FROM materias", return_info="data"):
        if d[0] == id_materia:
            return d[1]
        break

def atualizar_materia_por_id(id_materia, **valores_mudados):
    try:
        for k, v in valores_mudados.items():
            Query(
                """
        UPDATE materias
        SET %s = %s
        WHERE materia_id = %s 
                """, (k, v, id_materia)
            )
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

def atualizar_materia_por_nome(nome_materia, **valores_mudados):
    try:
        for k, v in valores_mudados.items():
            Query(
                """
        UPDATE materias
        SET %s = %s
        WHERE materia_nome = %s 
                """, (k, v, nome_materia)
            )
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)