from fastapi import APIRouter
from App.Database import bobicas as bdb
from App.schemas import bobicas as bsc
router = APIRouter(
    prefix="/bobicas",
    tags=["bobicas"]
)

@router.get("/", response_model=bsc.BobicaResponse)
def listar_todas_bobicas():
    return {
        "bobicas" : bdb.listar_bobicas()
    }

@router.get("/", response_model=bsc.BobicaResponse)
def listar_bobicas_por_query(nome: str):
    return {
        "nomes" : bdb.listar_bobicas(nome)
    }

@router.get("/{nome}", response_model=bsc.BobicaResponse)
def listar_bobicas_por_nome(nome: str):
    return {
        "nomes" : bdb.listar_bobicas(nome)
    }

@router.post('/')
def criar_bobica(bobica:bsc.Bobica):
    try:
        bdb.criar_bobica(bobica.nome, bobica.preco_medio)
        return{
            "status": "criado com sucesso",
            "nome": bobica.nome,
            "preco_medio": bobica.preco_medio
        }
    except:
        return{
            "status": "erro na criacao",
            "nome": bobica.nome,
            "preco_medio": bobica.preco_medio
        }