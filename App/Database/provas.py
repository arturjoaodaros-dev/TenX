from App.Database.connector import Query
from App.Database import materias as mdb
from App.Database import bobicas as bdb

def criar_prova(nome_materia, nome_bobica):
    return Query(
        """
INSERT INTO provas(materia_id, bobica_id) VALUES(%s, %s)
        """, (mdb.obter_id_por_materia(nome_materia)[0], bdb.obter_id_por_bobica(nome_bobica)[0]))

def listar_provas(nome:str=""):
    provas = {}
    for d in Query("SELECT * FROM provas", return_info="data"):
        try:
            provas[mdb.obter_materia_por_id(d[1])] += 1
        except KeyError:
            provas[mdb.obter_materia_por_id(d[1])] = 1
    if nome:
        return {nome : provas[nome]}
    else:
        return provas

def atualizar_prova_por_id(id_prova, **valores_mudados):
    try:
        for k, v in valores_mudados.items():
            Query(
                """
        UPDATE provas
        SET %s = %s
        WHERE prova_id = %s 
                """, (k, v, id_prova)
            )
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

def atualizar_prova_por_materia(nome_materia, **valores_mudados):
    try:
        for k, v in valores_mudados.items():
            Query(
                """
        UPDATE provas
        SET %s = %s
        WHERE materia_id = %s 
                """, (k, v, mdb.obter_id_por_materia(nome_materia))
            )
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)
    
def atualizar_prova_por_bobica(nome_bobica, **valores_mudados):
    try:
        for k, v in valores_mudados.items():
            Query(
                """
        UPDATE provas
        SET %s = %s
        WHERE bobica_id = %s 
                """, (k, v, bdb.obter_id_por_bobica(nome_bobica))
            )
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)
if __name__ == "__main__":
    print(listar_provas("ciencias"))