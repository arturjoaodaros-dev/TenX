from fastapi import APIRouter, Query
from App.Database import provas as pdb
from App.schemas import provas as psc

router = APIRouter(
    prefix="/provas",
    tags=["provas"]
)

@router.get("/")
def listar_todas_provas(id_materia:int=Query(ge=0, default=0), id_prova:int=Query(0, ge=0)):
    try:
        print("listar tudo usado", id_materia)
        if id_materia:
            return{
                "materia/provas":pdb.listar_provas()[id_materia - 1],
                }
        elif id_prova:
            return {
                "materia/bobica":pdb.listar_provas_por_id(id_prova),}
    except IndexError:
        return{
            "Error": "index out of range"
        }

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
def atualizar_prova(nova_prova:psc.Prova, id_prova:int=0, nome_bobica:str="", nome_materia:str="") -> dict:
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
            "error":"you must inform id_prova, nome_materia or nome_bobica",
            "id_prova": id_prova,
            "nome_bobica": nome_bobica,
            "nome_materia": nome_materia,
            "prova_bobica": nova_prova.nome_bobica,
            "prova_materia": nova_prova.nome_materia}