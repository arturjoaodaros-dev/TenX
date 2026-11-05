from App.Database import usuarios as us

from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_senha(senha: str) -> str:
    """Gera um hash seguro para armazenar no banco."""
    return ph.hash(senha)

for i in range(201, 250):
    resultado = us.obter_usuario(id=i)
    if not resultado or resultado[0] is False:
        print(f"Usuário {i} não encontrado; ignorando.")
        continue

    usuario = resultado[0]
    email = usuario[2]
    senha_atual = usuario[3]
    if senha_atual is None:
        print(f"Usuário {i} não tem senha; ignorando.")
        continue
    if not isinstance(senha_atual, str):
        raise TypeError(f"A senha do usuário {i} não é texto.")
    if senha_atual.startswith("$argon2"):
        print(f"Senha do usuário {i} já está em Argon2; ignorando.")
        continue

    senha_nova = hash_senha(senha_atual)
    us.Query("UPDATE usuarios SET usuario_senha = %s WHERE usuario_email = %s", (senha_nova, email))
    print(f"Senha do usuário {i} atualizada.")
