# COMUNICAÇÃO COM O DATABASE DAS PROVAS
# NOME DOS IMPORTS DEVE SER pdb
# imports
from App.Database.connector import Query
from App.Database import materias as mdb
from App.Database import bobicas as bdb
from App.schemas import provas as psc
# funções POST
def criar_prova(prova:psc.Prova) -> str:
    try:
        Query(
            """
    INSERT INTO provas(materia_id, bobica_id) VALUES(%s, %s)
            """, (mdb.obter_id_por_materia(prova.nome_materia), bdb.obter_id_por_bobica(prova.nome_bobica)))
        return "prova criada com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

# funções GET
def listar_provas(nome:str="") -> list:
    provas = {}
    lista_provas = []
    for d in Query("SELECT * FROM provas", return_info="data"):
        try:
            provas[mdb.obter_materia_por_id(d[1])] += 1
        except KeyError:
            provas[mdb.obter_materia_por_id(d[1])] = 1
    
    for k, v in provas.items():
        if not nome:
            lista_provas.append((k, v))
        else:
            if k == nome:
                lista_provas.append((k, v))
                break

    return lista_provas

def listar_provas_por_id(id_prova):
    data = Query("SELECT materia_id, bobica_id FROM provas WHERE prova_id = %s",(id_prova, ), "data")[0]
    processed_data = [mdb.obter_materia_por_id(data[0]), bdb.obter_bobica_por_id(data[1])]
    return processed_data

# funções PATCH
def atualizar_prova_por_id_valores(id_prova, valores_mudados:dict) -> str:
    try:
        for k, v in valores_mudados.items():
            Query(
                f"""
        UPDATE provas
        SET {k} = %s
        WHERE prova_id = %s 
                """, (v, id_prova)
            )
        return "Valores atualizados com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

def atualizar_prova_por_materia_valores(nome_materia, valores_mudados:dict) -> str:
    try:
        for k, v in valores_mudados.items():
            Query(
                f"""
        UPDATE provas
        SET {k} = %s
        WHERE materia_id = %s 
                """, (v, mdb.obter_id_por_materia(nome_materia))
            )
        return "Valores atualizados com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)
    
def atualizar_prova_por_bobica_valores(nome_bobica, valores_mudados:dict) -> str:
    try:
        for k, v in valores_mudados.items():
            Query(
                f"""
        UPDATE provas
        SET {k} = %s
        WHERE bobica_id = %s 
                """, (v, bdb.obter_id_por_bobica(nome_bobica))
            )
        return "Valores atualizados com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

# funções PUT
def atualizar_prova_por_id_completa(prova_id, nova_prova:psc.Prova) -> str:
    try:
        Query(
            """
DELETE FROM provas
WHERE prova_id = %s 
            """, (prova_id, )
            )
        
        Query(
            """
        INSERT INTO provas(materia_id, bobica_id) VALUES (%s, %s)
            """, (mdb.obter_id_por_materia(nova_prova.nome_materia), bdb.obter_id_por_bobica(nova_prova.nome_bobica))
            )
        return "prova atualizada com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

def atualizar_prova_por_materia_completa(nome_materia, nova_prova:psc.Prova) -> str:
    try:
        Query(
            """
    DELETE FROM provas
    WHERE materia_id = %s 
            """, (mdb.obter_id_por_materia(nome_materia), )
        )

        Query(
            """
INSERT INTO provas(materia_id, bobica_id) VALUES (%s, %s)
            """, (mdb.obter_id_por_materia(nova_prova.nome_materia), bdb.obter_id_por_bobica(nova_prova.nome_bobica))
        )
        return "prova atualizada com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

def atualizar_prova_por_bobica_completa(nome_bobica, nova_prova:psc.Prova) -> str:
    try:
        Query(
            """
    DELETE FROM provas
    WHERE bobica_id = %s 
            """, (bdb.obter_id_por_bobica(nome_bobica), )
        )

        Query(
            """
INSERT INTO provas(materia_id, bobica_id) VALUES (%s, %s)
            """, (mdb.obter_id_por_materia(nova_prova.nome_materia), bdb.obter_id_por_bobica(nova_prova.nome_bobica))
        )
        return "prova atualizada com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

def destruir_prova_por_id(id_prova):
    Query("DELETE FROM provas WHERE prova_id = %s", (id_prova))

def destruir_prova_por_bobica(nome_bobica):
    Query("DELETE FROM provas WHERE bobica_id = %s", (bdb.obter_id_por_bobica(nome_bobica)))

def destruir_prova_por_materia(nome_materia):
    Query("DELETE FROM provas WHERE materia_id = %s", (mdb.obter_id_por_materia(nome_materia)))