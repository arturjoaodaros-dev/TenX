from fastapi import APIRouter, Query
from App.Database import materias as mdb
from App.schemas import materias as msc
router = APIRouter(
    prefix="/materias",
    tags=["materias"]
)

@router.get("/")
def listar_todas_materias(nome_materia:str=Query("", min_length=3)) -> dict:
    return {
        "nomes" : mdb.listar_materias(nome_materia)
    }

@router.get("/{nome}")
def listar_materias_por_nome(nome: str) -> dict:
    return {
        "nomes" : mdb.listar_materias(nome)
    }

@router.post('/')
def criar_materia(materia:msc.Materia) -> dict:
    try:
        return{
            "status": mdb.criar_materia(materia),
            "nome": materia.nome,
        }
    except:
        return{
            "status": "erro na criacao",
            "nome": materia.nome,
        }

@router.put('/')
def atualizar_materia(nova_materia:msc.Materia, nome_materia:str="", id_materia:int=0) -> dict:
    if not id_materia:
        return {
            "status": mdb.atualizar_materia_por_nome_completa(nome_materia, nova_materia),
            "nome_materia": nome_materia
        }
    else:
        return {
            "status": mdb.atualizar_materia_por_nome_completa(id_materia, nova_materia),
            "id_materia": id_materia
        }

@router.patch('/')
def atualizar_valor_materia(valores:dict, nome_materia:str="", id_materia:int=0, ):
    print("NO ROUTER:", valores)
    if not id_materia:
        return {
            "status": mdb.atualizar_materia_por_nome_valores(nome_materia, valores_mudados=valores),
            "nome_materia" : nome_materia
            }
    else:
        return {
            "stauts" : mdb.atualizar_materia_por_id_valores(id_materia, valores_mudados=valores),
            "id_bobica":id_materia
            }

@router.delete("/{materia_nome}")
def excluir_bobica_por_nome(materia_nome, senha:str):
    import dotenv, os
    dotenv.load_dotenv()
    if senha == os.getenv("DESTRUCTION_PASSWORD"):
        mdb.destruir_materia_por_nome(materia_nome)

@router.delete("/{bobica_id}")
def excluir_bobica_por_id(bobica_id, senha:str):
    import dotenv, os
    dotenv.load_dotenv()
    if senha == os.getenv("DESTRUCTION_PASSWORD"):
        mdb.destruir_materia_por_id(bobica_id)