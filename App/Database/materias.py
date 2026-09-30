# COMUNICAÇÃO COM O DATABASE DAS MATERIAS
# NOME DOS IMPORTS DEVE SER mdb
# imports
from App.Database.connector import Query
from App.schemas import materias as msc

# funções POST 
def criar_materia(materia:msc.Materia) -> str:
    try:
        Query(
            """
    INSERT INTO materias(materia_nome) VALUES(%s)
            """, (materia.nome, ))
        return "materia criada com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

# funções GET
def listar_materias(nome: str = "") -> list:
    if nome:
        return [d[1] for d in Query( "SELECT * FROM materias WHERE materia_nome = %s",(nome,),"data")]
    else:
        return [d[1] for d in Query("SELECT * FROM materias", return_info="data")]

# funções para auxiliar no código
def obter_id_por_materia(nome_materia:str):
    try:
        m = ""
        for d in Query( "SELECT * FROM materias WHERE materia_nome = %s",(nome_materia, ),"data"):
            if d[1] == nome_materia:
                m = d[0]
        return str(m)
    except:
        return "Not found"

def obter_materia_por_id(id_materia):
    m = ""
    for d in Query("SELECT * FROM materias", return_info="data"):
        if d[0] == id_materia:
            m = d[1]
    return str(m)


# funções PATCH
def atualizar_materia_por_id_valores(materia_id, valores_mudados:dict) -> str:
    try:
        for k, v in valores_mudados.items():
            Query(
                f"""
        UPDATE materias
        SET {k} = %s
        WHERE materia_id = %s; 
                """, (v, materia_id)
            )
        return "Valores atualizados com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

def atualizar_materia_por_nome_valores(materia_nome, **valores_mudados) -> str:
    try:
        for k, v in valores_mudados.items():
            Query(
                f"""
        UPDATE materias
        SET {k} = %s
        WHERE materia_nome = %s;
                """, (v, materia_nome)
            )
        return "Valores atualizados com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

# fuunções PUT
def atualizar_materia_por_id_completa(materia_id, nova_materia:msc.Materia) -> str:
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
        return "Materia atualizada com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

def atualizar_materia_por_nome_completa(materia_nome, nova_materia:msc.Materia) -> str:
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
        return "Materia atualizada com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

#funções DELETE

def destruir_materia_por_id(id_materia):
    try:
        Query("DELETE FROM materias WHERE materia_id = %s", (id_materia, ))
        return "materia deletada com sucesso"
    except:
        return "Erro no processo"

def destruir_materia_por_nome(nome_materia):
    try:
        Query("DELETE FROM materias WHERE materia_nome = %s", (nome_materia, ))
        return "materia deletada com sucesso"
    except:
        return "Erro no processo"
if __name__ == "__main__":
    print(obter_id_por_materia("ciencias"))