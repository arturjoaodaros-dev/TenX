from App.Database.connector import Query
from App.schemas import materias as msc
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

def atualizar_materia_por_id_valores(materia_id, **valores_mudados):
    try:
        for k, v in valores_mudados.items():
            Query(
                """
        UPDATE materias
        SET %s = %s
        WHERE materia_id = %s 
                """, (k, v, materia_id)
            )
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

def atualizar_materia_por_nome_valores(materia_nome, **valores_mudados):
    try:
        for k, v in valores_mudados.items():
            Query(
                """
        UPDATE materias
        SET %s = %s
        WHERE materia_nome = %s 
                """, (k, v, materia_nome)
            )
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

def atualizar_materia_por_id_completa(materia_id, nova_materia:msc.Materia):
    try:
        Query(
            """
DELETE FROM materias
WHERE materia_id = %s 
            """, (materia_id, )
            )
        
        Query(
            """
INSERT INTO materias(materia_nome) VALUES (%s)
            """, (nova_materia.nome,)
        )
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

def atualizar_materia_por_nome_completa(materia_nome, nova_materia:msc.Materia):
    try:
        Query(
            """
    DELETE FROM materias
    WHERE bobica_nome = %s 
            """, (materia_nome, )
        )

        Query(
            """
INSERT INTO bobicas(materia_nome) VALUES (%s)
            """, (nova_materia.nome,)
        )
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)