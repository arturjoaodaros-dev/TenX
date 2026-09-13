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