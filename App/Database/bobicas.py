# COMUNICAÇÕ COM O DATABASE DAS BOBICAS
# NOME DOS IMPORTS DEVE SER bdb
# imports
import os

from App.Database.connector import Query, conn
from App.schemas import bobicas as bsc

# funções POST
def criar_bobica(bobica:bsc.Bobica) -> str:
    Query(
        """
INSERT INTO bobicas(bobica_nome, preco_medio) VALUES(%s, %s)
        """, (bobica.nome, bobica.preco_medio))
    return "bobica criada com sucesso"
# funções GET
def listar_bobicas(nome: str = "") -> list:
    if nome:
        return [d[1] for d in Query( "SELECT * FROM bobicas WHERE bobica_nome = %s",(nome,),"data")]
    else:
        return [d[1] for d in Query("SELECT * FROM bobicas", return_info="data")]

# funções para auxiliar no código
def obter_id_por_bobica(nome_bobica:str) -> str:
    try:
        return [d[0] for d in Query( "SELECT * FROM bobicas WHERE bobica_nome = %s",(nome_bobica, ),"data")][0]
    except:
        return "Not found"

def obter_bobica_por_id(id_bobica) -> str:
    try:
        return [d[1] for d in Query( "SELECT * FROM bobicas WHERE bobica_id = %s",(id_bobica, ),"data")][0]
    except:
        return "Not found"

# funções PATCH
def atualizar_bobica_por_id_valores(id_bobica, valores_mudados:dict) -> str:
    print("NO DATABASE:", valores_mudados)
    try:
        for k, v in valores_mudados.items():
            print(k, v, id_bobica)
            Query(f"UPDATE bobicas SET {k} = %s WHERE bobica_id = %s;", params=(v, id_bobica), return_info="data")
        return "valores atualizados com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

def atualizar_bobica_por_nome_valores(nome_bobica, valores_mudados:dict) -> str:
    print("NO DATABASE:", valores_mudados)
    try:
        for k, v in valores_mudados.items():
            print(k, v, nome_bobica)
            Query(f"UPDATE bobicas SET {k} = %s WHERE bobica_nome = %s;", params=(v, nome_bobica), return_info="data")
        return "valores atualizados com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

# funções PUT
def atualizar_bobica_por_id_completa(id_bobica, nova_bobica:bsc.Bobica) -> str:
    try:
        Query("UPDATE bobicas SET bobica_nome = %s WHERE bobica_id = %s",(nova_bobica.nome, id_bobica))
        Query("UPDATE bobicas SET preco_medio = %s WHERE bobica_id = %s",(nova_bobica.preco_medio, id_bobica))
        return "bobica atualizada com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

def atualizar_bobica_por_nome_completa(nome_bobica, nova_bobica:bsc.Bobica) -> str:
    try:
        Query(
            """
    DELETE FROM bobicas
    WHERE bobica_nome = %s 
            """, (nome_bobica, )
        )

        Query(
            """
INSERT INTO bobicas(bobica_nome, preco_medio) VALUES (%s, %s)
            """, (nova_bobica.nome, nova_bobica.preco_medio)
        )
        return "bobica atualizada com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

# funções DELETE

def Destruir_Tabela(password:str):
    from dotenv import load_dotenv

    load_dotenv()
    destruction_password = os.getenv("DESTRUCTION_PASSWORD")
    if destruction_password is None:
        raise RuntimeError("DESTRUCTION_PASSWORD is not configured")

    if password == destruction_password:
        import time
        Query("DROP TABLE bobicas", autocommit=False)
        time.sleep(1.800)
        conn.commit()

    else:
        from time import time
        file = open("PASSWORD_NOT_MATCH.txt", "w")
        file.write(f"""
password: {password}
time: {time()}
                    """)

def destruir_bobica_por_id(id_bobica):
    Query("DELETE FROM bobicas WHERE bobica_id = %s", (id_bobica))

def destruir_bobica_por_nome(nome_bobica):
    Query("DELETE FROM bobicas WHERE bobica_nome = %s", (nome_bobica))
    

