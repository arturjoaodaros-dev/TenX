from fastapi import APIRouter
from App.Database import materias as mdb
from App.schemas import materias as msc
router = APIRouter(
    prefix="/materias",
    tags=["materias"]
)

@router.get("/", response_model=msc.MateriaResponse)
def listar_todas_materias():
    return {
        "nomes" : mdb.listar_materias()
    }

@router.get("/", response_model=msc.MateriaResponse)
def listar_materias_por_query(nome: str):
    return {
        "nomes" : mdb.listar_materias(nome)
    }

@router.get("/{nome}", response_model=msc.MateriaResponse)
def listar_materias_por_nome(nome: str):
    return {
        "nomes" : mdb.listar_materias(nome)
    }

@router.post('/')
def criar_materia(materia:msc.Materia):
    try:
        mdb.criar_materia(materia.nome)
        return{
            "status": "criado com sucesso",
            "nome": materia.nome,
        }
    except:
        return{
            "status": "erro na criacao",
            "nome": materia.nome,
        }

@router.put('/')
def atualizar_bobica(nova_materia:msc.Materia, nome_materia:str="", id_materia:int=0):
    if not id_materia:
        return mdb.atualizar_materia_por_nome_completa(nome_materia, nova_materia)
    else:
        return mdb.atualizar_materia_por_nome_completa(id_materia, nova_materia)