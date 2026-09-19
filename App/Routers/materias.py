from fastapi import APIRouter
from App.Database import materias as mdb
from App.schemas import materias as msc
router = APIRouter(
    prefix="/materias",
    tags=["materias"]
)

@router.get("/", response_model=msc.MateriaResponse)
def listar_todas_materias() -> dict:
    return {
        "nomes" : mdb.listar_materias()
    }

@router.get("/", response_model=msc.MateriaResponse)
def listar_materias_por_query(nome: str) -> dict:
    return {
        "nomes" : mdb.listar_materias(nome)
    }

@router.get("/{nome}", response_model=msc.MateriaResponse)
def listar_materias_por_nome(nome: str) -> dict:
    return {
        "nomes" : mdb.listar_materias(nome)
    }

@router.post('/')
def criar_materia(materia:msc.Materia) -> dict:
    try:
        return{
            "status": mdb.criar_materia(materia.nome),
            "nome": materia.nome,
        }
    except:
        return{
            "status": "erro na criacao",
            "nome": materia.nome,
        }

@router.put('/')
def atualizar_bobica(nova_materia:msc.Materia, nome_materia:str="", id_materia:int=0) -> dict:
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