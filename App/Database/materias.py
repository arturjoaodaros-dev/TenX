from connector import Query

def criar_materia(nome):
    return Query(
        """
INSERT INTO materias(materia_nome) VALUES(%s)
        """, (nome, ))

def listar_materias(nome: str = ""):
    materias = []

    if nome:
        for materia in Query(
            "SELECT * FROM materias WHERE materia_nome = %s",
            (nome,)
        )[0]:
            materias.append(materia[1])
    else:
        for materia in Query("SELECT * FROM materias")[0]:
            materias.append(materia[1])

    return materias


print(listar_materias())
