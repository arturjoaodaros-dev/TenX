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