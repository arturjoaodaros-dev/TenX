from App.Database.connector import Query

def criar_bobica(nome, preco):
    return Query(
        """
INSERT INTO bobicas(bobica_nome, preco_medio) VALUES(%s, %s)
        """, (nome, preco))

def listar_bobicas(nome: str = ""):
    if nome:
        return [d[1] for d in Query( "SELECT * FROM bobicas WHERE bobica_nome = %s",(nome,),"data")]
    else:
        return [d[1] for d in Query("SELECT * FROM bobicas", return_info="data")]

def obter_id_por_bobica(nome_bobica:str):
    try:
        return [d[0] for d in Query( "SELECT * FROM bobicas WHERE bobica_nome = %s",(nome_bobica, ),"data")]
    except:
        return "Not found"

def obter_bobica_por_id(id_bobica):
    try:
        return [d[1] for d in Query( "SELECT * FROM bobicas WHERE bobica_id = %s",(id_bobica, ),"data")]
    except:
        return "Not found"

def atualizar_bobica_por_id(id_bobica, **valores_mudados):
    try:
        for k, v in valores_mudados.items():
            Query(
                """
        UPDATE bobicas
        SET %s = %s
        WHERE bobica_id = %s 
                """, (k, v, id_bobica)
            )
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)

def atualizar_bobica_por_nome(nome_bobica, **valores_mudados):
    try:
        for k, v in valores_mudados.items():
            Query(
                """
        UPDATE bobicas
        SET %s = %s
        WHERE bobica_nome = %s 
                """, (k, v, nome_bobica)
            )
    except Exception as e:
        raise Exception("Algo deu de errado na operação, ERR: ", e)