from fastapi import APIRouter
from App.Database import bobicas as bdb
from App.schemas import bobicas as bsc
router = APIRouter(
    prefix="/bobicas",
    tags=["bobicas"]
)

@router.get("/", response_model=bsc.BobicaResponse)
def listar_todas_bobicas() -> dict:
    return {
        "bobicas" : bdb.listar_bobicas()
    }

@router.get("/", response_model=bsc.BobicaResponse)
def listar_bobicas_por_query(nome: str) -> dict:
    return {
        "nomes" : bdb.listar_bobicas(nome)
    }

@router.get("/{nome}", response_model=bsc.BobicaResponse)
def listar_bobicas_por_nome(nome: str) -> dict:
    return {
        "nomes" : bdb.listar_bobicas(nome)
    }

@router.post('/')
def criar_bobica(bobica:bsc.Bobica) -> dict:
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

@router.put('/')
def atualizar_bobica(nova_bobica:bsc.Bobica, nome_bobica:str="", id_bobica:int=0) -> dict:
    if not id_bobica:
        return {
            "status": bdb.atualizar_bobica_por_nome_completa(nome_bobica, nova_bobica),
            "nome" : nome_bobica
            }
    else:
        return {
            "stauts" : bdb.atualizar_bobica_por_id_completa(id_bobica, nova_bobica),
            "id_bobica":id_bobica
            }

