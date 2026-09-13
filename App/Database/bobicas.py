from connector import Query

def criar_bobica(nome, preco):
    return Query(
        """
INSERT INTO bobicas(bobica_nome, preco_medio) VALUES(%s, %s)
        """, (nome, preco))

def listar_bobicas(nome: str = ""):
    bobicas = []

    if nome:
        for bobica in Query(
            "SELECT * FROM bobicas WHERE bobica_nome = %s",
            (nome,)
        )[0]:
            bobicas.append(bobica[1])
    else:
        for bobica in Query("SELECT * FROM bobicas")[0]:
            bobicas.append(bobica[1])

    return bobicas