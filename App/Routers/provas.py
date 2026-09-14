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
def criar_prova(prova:psc.Prova):
    
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