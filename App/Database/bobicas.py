# COMUNICAÇÕ COM O DATABASE DAS BOBICAS
# NOME DOS IMPORTS DEVE SER bdb
# imports
from App.Database.connector import Query
from App.schemas import bobicas as bsc

# funções POST
def criar_bobica(nome, preco) -> str:
    Query(
        """
INSERT INTO bobicas(bobica_nome, preco_medio) VALUES(%s, %s)
        """, (nome, preco))
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
def atualizar_bobica_por_id_valores(id_bobica, **valores_mudados) -> str:
    try:
        for k, v in valores_mudados.items():
            Query(
                """
        UPDATE bobicas
        SET %s = %s
        WHERE bobica_id = %s 
                """, (k, v, id_bobica)
            )
        return "valores atualizados com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

def atualizar_bobica_por_nome_valores(nome_bobica, **valores_mudados) -> str:
    try:
        for k, v in valores_mudados.items():
            Query(
                """
        UPDATE bobicas
        SET %s = %s
        WHERE bobica_nome = %s 
                """, (k, v, nome_bobica)
            )
        return "valores atualizados com sucesso"
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

# funções PUT
def atualizar_bobica_por_id_completa(id_bobica, nova_bobica:bsc.Bobica) -> str:
    try:
        Query(
            """
DELETE FROM bobicas
WHERE bobica_id = %s 
            """, (id_bobica, )
            )
        
        Query(
            """
        INSERT INTO bobicas(bobica_nome, preco_medio) VALUES (%s, %s)
            """, (nova_bobica.nome, nova_bobica.preco_medio)
            )
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