from fastapi import APIRouter
from App.Database import provas as pdb
from App.schemas import provas as psc

router = APIRouter(
    prefix="/provas",
    tags=["provas"]
)

@router.get("/")
def listar_todas_provas():
    return pdb.listar_provas()

@router.get("/")
def listar_provas_por_query(nome_materia: str):
    return pdb.listar_provas(nome_materia)

@router.get("/{nome_materia}")
def listar_provas_por_nome(nome_materia: str):
    return pdb.listar_provas(nome_materia)

@router.post("/")
def criar_prova(prova:psc.Prova) -> dict:
    
    try:
        pdb.criar_prova(prova.nome_materia, prova.nome_bobica)
        return{
            "status": "criado com sucesso",
            "nome_materia": prova.nome_materia,
            "nome_bobica": prova.nome_bobica
        }
    except Exception as e:
        return{
            "status": f"erro na criação, ERR: {e}",
            "nome_materia": prova.nome_materia,
            "nome_bobica": prova.nome_bobica
        }

@router.put('/')
def atualizar_prova(nova_prova:psc.Prova, nome_bobica:str="", id_prova:int=0, nome_materia:str="") -> dict:
    if id_prova:
        return {
            "status": pdb.atualizar_prova_por_id_completa(id_prova, nova_prova),
            "id_prova": id_prova
        }
    elif nome_materia:
        return {
            "status": pdb.atualizar_prova_por_materia_completa(nome_materia, nova_prova),
            "nome_materia": nome_materia
        } 
    elif nome_bobica:
        return {
            "status": pdb.atualizar_prova_por_bobica_completa(nome_bobica, nova_prova),
            "nome_bobica": nome_bobica
        }
    else:
        return{
            "error":"you must inform id_prova, nome_materia or nome_bobica"
        }