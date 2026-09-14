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
    for d in Query("SELECT * FROM bobica", return_info="data"):
        if d[0] == id_bobica:
            return d[1]
        break