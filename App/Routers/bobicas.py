from fastapi import APIRouter
from App.Database import bobicas as bdb
from App.schemas import bobicas as bsc
router = APIRouter(
    prefix="/bobicas",
    tags=["bobicas"]
)
@router.get("/")
def listar_bobicas(nome: str="") -> dict:
    return {
        "nomes" : bdb.listar_bobicas(nome)
    }

@router.get("/{nome}")
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

@router.patch('/')
def atualizar_valor_bobica(valores:dict, nome_bobica:str="", id_bobica:int=0, ):
    print("NO ROUTER:", valores)
    if not id_bobica:
        return {
            "status": bdb.atualizar_bobica_por_nome_valores(nome_bobica, valores_mudados=valores),
            "nome" : nome_bobica
            }
    else:
        return {
            "stauts" : bdb.atualizar_bobica_por_id_valores(id_bobica, valores_mudados=valores),
            "id_bobica":id_bobica
            }

@router.delete("/{bobica_nome}")
def excluir_bobica_por_nome(bobica_nome, senha:str):
    import dotenv, os
    dotenv.load_dotenv()
    if senha == os.getenv("DESTRUCTION_PASSWORD"):
        bdb.destruir_bobica_por_nome(bobica_nome)

@router.delete("/{bobica_id}")
def excluir_bobica_por_id(bobica_id, senha:str):
    import dotenv, os
    dotenv.load_dotenv()
    if senha == os.getenv("DESTRUCTION_PASSWORD"):
        bdb.destruir_bobica_por_id(bobica_id)