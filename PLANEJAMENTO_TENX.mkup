# Planejamento Arquitetural — Projeto TenX

> Documento de referência para a evolução da arquitetura do projeto. Não descreve o código atual como está, mas define o papel que cada pasta e arquivo deve desempenhar daqui para frente.

---

## 1. Visão geral do projeto

### 1.1 Propósito da aplicação

TenX é uma aplicação de apoio a estudos, construída como uma API backend (FastAPI) com um frontend ainda a ser desenvolvido. O domínio identificado a partir do código existente gira em torno de três entidades centrais:

- **Matérias** (`materias`): disciplinas ou áreas de estudo (ex.: "ciências", "matemática").
- **Bobicas** (`bobicas`): um recurso de estudo com nome e preço médio associado — pelo vocabulário e pela modelagem (nome + preço médio), trata-se provavelmente de materiais de apoio, itens de papelaria/insumos de estudo, ou um recurso similar consumido no processo de estudar. O planejamento tratará "bobica" como um conceito de domínio próprio da aplicação, sem tentar renomeá-lo ou reinterpretá-lo — apenas organizando sua persistência e exposição de forma consistente com as demais entidades.
- **Provas** (`provas`): o registro de associação entre uma matéria e uma bobica, contabilizando ocorrências (quantas vezes uma bobica foi usada em provas de determinada matéria).

O problema que a aplicação pretende resolver é o de **rastrear e relacionar recursos de estudo (bobicas) com o desempenho ou uso em avaliações (provas) organizadas por matéria**, permitindo consultas agregadas (ex.: quantas provas de uma matéria usaram determinado recurso).

### 1.2 Problema que pretende resolver

De forma mais ampla, o projeto resolve a necessidade de **centralizar e estruturar dados de estudo** que hoje provavelmente são controlados de forma manual ou dispersa (planilhas, anotações). Ele oferece:

- Um cadastro estruturado de matérias e recursos de estudo (bobicas).
- Um mecanismo de registro de uso desses recursos em contexto de avaliação (provas).
- Uma camada de API que permitirá, no futuro, que uma interface (Frontend) e/ou outros clientes consumam esses dados.

### 1.3 Relação entre as partes principais

```
Frontend (interface do usuário)
        │
        ▼  HTTP/JSON
App (API FastAPI)
   ├── Routers      → recebem requisições HTTP e validam formato de entrada/saída
   ├── schemas      → definem os contratos de dados (Pydantic) trafegados pela API
   ├── services     → (papel futuro) concentrarão as regras de negócio
   ├── models       → (papel futuro) representarão entidades de domínio/ORM
   └── Database     → acesso direto ao PostgreSQL (queries e persistência)
        │
        ▼
   PostgreSQL (armazenamento relacional)

tests → validam o comportamento de App de forma independente
```

Hoje, a maior parte da lógica está concentrada diretamente em `Database` e `Routers`, com `services` e `models` ainda vazios — o que indica que a arquitetura pretendida é mais estratificada do que a implementação atual, e este documento assume essa estratificação como o alvo a ser perseguido.

---

## 2. Arquitetura e organização

A aplicação segue (ou deve seguir, à medida que evolui) uma arquitetura em camadas inspirada no padrão usado por APIs FastAPI de médio porte:

1. **Camada de apresentação/API** (`Routers`) — ponto de entrada HTTP.
2. **Camada de contrato de dados** (`schemas`) — validação e serialização.
3. **Camada de regra de negócio** (`services`) — orquestração e regras.
4. **Camada de domínio** (`models`) — representação das entidades.
5. **Camada de persistência** (`Database`) — acesso a dados.

Essa separação existe para que cada camada tenha uma única razão para mudar: um Router muda quando a forma de expor a API muda; um schema muda quando o contrato externo muda; um service muda quando a regra de negócio muda; um model muda quando a estrutura de domínio muda; e o Database muda quando a forma de persistir os dados muda (ex.: trocar de driver, otimizar uma query).

A seguir, o papel de cada pasta hoje existente, e o tipo de conteúdo que deve pertencer a cada uma.

### 2.1 Raiz do projeto

Contém os artefatos de configuração e orquestração do projeto como um todo: variáveis de ambiente (`.env`), dependências Python (`requirements.txt`), controle de versão (`.git`, `.gitignore`) e ambiente virtual (`.venv`). É também onde, futuramente, devem residir arquivos de configuração de nível de projeto (ex.: `README.md`, `pyproject.toml`, `docker-compose.yml`, `alembic.ini` caso se adote migrations).

### 2.2 `App/`

É o pacote Python que constitui o backend da aplicação. Tudo que for código-fonte da API deve estar aqui dentro, nunca na raiz do projeto. `App/main.py` é o ponto de entrada: cria a instância do FastAPI e registra os routers. Ele deve permanecer o mais enxuto possível — sua responsabilidade é exclusivamente montar a aplicação, não conter lógica de negócio ou de acesso a dados.

### 2.3 `App/Routers/`

Responsável por expor os endpoints HTTP. Cada arquivo representa um recurso da API (materias, bobicas, provas) e deve conter apenas: declaração de rotas, extração/validação de parâmetros de entrada (delegada aos schemas) e chamada para a camada de serviço (não diretamente para o banco, no estado futuro desejado). Não deve conter regras de negócio nem SQL.

### 2.4 `App/schemas/`

Contém os contratos de dados da API, escritos com Pydantic. Definem o formato de entrada (payloads de criação) e saída (respostas) de cada recurso. Um arquivo por entidade, espelhando a organização de `Routers` e `Database`. Não deve conter lógica de negócio, acesso a dados, nem ser usado como modelo de banco de dados (isso é papel de `models`).

### 2.5 `App/services/`

Atualmente vazio (apenas `__init__.py`), reservado para a camada de regras de negócio. É aqui que devem residir as funções que hoje estão soltas em `Database/*.py` misturando SQL com lógica (por exemplo, a agregação de contagem de provas por matéria em `provas.py`). Um service orquestra uma ou mais chamadas a `Database`/`models`, aplica regras (validações de negócio, cálculos, agregações) e devolve dados prontos para os Routers formatarem como resposta.

### 2.6 `App/models/`

Atualmente vazio (apenas `__init__.py`), reservado para a representação de domínio das entidades — hoje ausente, já que os dados trafegam como tuplas cruas vindas do `psycopg`. O papel futuro desta pasta é abrigar classes que representem `Materia`, `Bobica` e `Prova` como objetos de domínio (podendo evoluir para modelos ORM SQLAlchemy, já presente em `requirements.txt` mas ainda não utilizado). Isso eliminará o acesso a dados por índice de tupla (`d[0]`, `d[1]`) presente na camada de banco atual, substituindo-o por atributos nomeados.

### 2.7 `App/Database/`

Responsável pelo acesso físico ao banco de dados PostgreSQL. `connector.py` centraliza a conexão e a execução de queries (função `Query`); os demais arquivos (`materias.py`, `bobicas.py`, `provas.py`) contêm as operações específicas de cada entidade. Esta camada deve conter apenas SQL e mapeamento de resultado bruto — nenhuma regra de negócio (a agregação de contagem em `provas.py`, por exemplo, é uma regra de negócio que pertence conceitualmente a `services`, não a `Database`).

### 2.8 `Frontend/`

Atualmente vazia — reservada para a interface de usuário da aplicação (web, mobile ou desktop). Ainda não há indicação tecnológica (React, Vue, Flutter etc.); a decisão de stack deve ser tomada antes do início do desenvolvimento desta camada, mas o papel dela já está definido: consumir a API exposta por `App` via HTTP.

### 2.9 `tests/`

Atualmente vazia — reservada para os testes automatizados do projeto (unitários e de integração). Deve espelhar a estrutura de `App` para facilitar a localização dos testes correspondentes a cada módulo.

---

## 3. Planejamento por pasta

### 3.1 `App/`

- **Objetivo:** ser o pacote raiz do backend, agregando todos os módulos da API.
- **Responsabilidade:** inicializar a aplicação FastAPI e servir como namespace para os demais subpacotes.
- **Deve conter:** `main.py`, `__init__.py`, e os subpacotes `Routers`, `schemas`, `services`, `models`, `Database`. Futuramente também um módulo de configuração central (ex.: `config.py` ou `core/settings.py`) e tratadores de exceção globais.
- **Não deve conter:** lógica de negócio direta, SQL, ou arquivos de configuração de infraestrutura (esses pertencem à raiz do projeto).
- **Relação com outras partes:** é consumido pelo `Frontend` via HTTP e testado por `tests`.
- **Possíveis adições futuras:** `App/core/` (configurações, segurança, middlewares), `App/exceptions.py` (exceções customizadas de domínio), `App/dependencies.py` (dependências reutilizáveis do FastAPI, como conexão de banco por requisição e autenticação).

### 3.2 `App/main.py`

- **Objetivo:** ponto de entrada da aplicação.
- **Responsabilidade:** instanciar o FastAPI, registrar routers, middlewares e handlers globais.
- **Deve conter:** criação da instância `app`, `include_router` de cada recurso, configuração de CORS (necessária assim que o Frontend existir), e o endpoint raiz de boas-vindas/healthcheck.
- **Não deve conter:** definição de rotas de negócio, acesso a banco de dados, regras de validação específicas de entidade.
- **Relação com outras partes:** importa de `Routers`; é o arquivo executado pelo `uvicorn`.
- **Possíveis adições futuras:** registro de middlewares de log e tratamento de erros, configuração de CORS, eventos de `startup`/`shutdown` (ex.: abrir/fechar pool de conexões).

### 3.3 `App/Routers/`

- **Objetivo:** expor a API HTTP.
- **Responsabilidade:** roteamento, validação de entrada via schemas, tradução de chamadas de serviço em respostas HTTP (incluindo códigos de status apropriados).
- **Deve conter:** um arquivo por entidade/recurso de domínio (`materias.py`, `bobicas.py`, `provas.py`, e futuros recursos), cada um definindo um `APIRouter` com prefixo e tags próprios.
- **Não deve conter:** SQL, lógica de agregação/negócio, acesso direto ao `Database`.
- **Relação com outras partes:** consome `schemas` (contratos) e `services` (regra de negócio, no estado futuro desejado — hoje consome `Database` diretamente, o que deve ser migrado); é consumido pelo `Frontend`.
- **Possíveis adições futuras:** `App/Routers/__init__.py` agregando todos os routers em um único objeto exportável; roteadores para autenticação/usuários caso o sistema evolua para multiusuário; versionamento de rota (`/v1/...`).

### 3.4 `App/schemas/`

- **Objetivo:** definir os contratos de dados da API.
- **Responsabilidade:** validação de entrada (request models) e formatação de saída (response models) usando Pydantic.
- **Deve conter:** um arquivo por entidade, com classes separadas para criação (`Materia`), resposta (`MateriaResponse`) e, futuramente, atualização parcial (`MateriaUpdate`) e listagem paginada.
- **Não deve conter:** lógica de negócio, chamadas a banco de dados, ou reaproveitamento como modelo de persistência.
- **Relação com outras partes:** usado por `Routers` para tipar entrada/saída; pode futuramente derivar ou se relacionar com `models` (ex.: método `from_orm`).
- **Possíveis adições futuras:** `schemas/common.py` para tipos compartilhados (paginação, respostas de erro padronizadas); schemas de atualização (`Update`) e de listagem (`List`) para cada entidade.

### 3.5 `App/services/`

- **Objetivo:** concentrar as regras de negócio da aplicação.
- **Responsabilidade:** orquestrar chamadas a `Database`/`models`, aplicar validações de domínio, cálculos e agregações, e devolver dados já tratados para os `Routers`.
- **Deve conter:** um arquivo por entidade (`materias_service.py`, `bobicas_service.py`, `provas_service.py`), com funções que representem casos de uso completos (ex.: "listar provas agregadas por matéria").
- **Não deve conter:** SQL cru, definição de rotas HTTP, definição de schemas.
- **Relação com outras partes:** é chamado pelos `Routers`; chama `Database` (e, no futuro, `models`) para obter/persistir dados.
- **Possíveis adições futuras:** regras de validação cruzada entre entidades (ex.: impedir criação de prova para matéria/bobica inexistente antes de tentar o insert), lógica de cache, regras de negócio mais elaboradas conforme o domínio cresça (ex.: cálculo de custo total de bobicas por matéria).

### 3.6 `App/models/`

- **Objetivo:** representar as entidades de domínio da aplicação.
- **Responsabilidade:** modelar `Materia`, `Bobica` e `Prova` como estruturas de dados nomeadas (dataclasses, ou modelos ORM SQLAlchemy, já listado em `requirements.txt`).
- **Deve conter:** um arquivo por entidade, definindo campos, tipos e (se adotado ORM) mapeamento de tabela.
- **Não deve conter:** lógica de rota, SQL manual fora do escopo do ORM, regras de negócio complexas (isso pertence a `services`).
- **Relação com outras partes:** usado por `Database` para retornar objetos tipados em vez de tuplas; pode ser referenciado por `schemas` para conversão automática.
- **Possíveis adições futuras:** `models/base.py` (classe base declarativa do SQLAlchemy, caso adotado), relacionamentos entre entidades (`Prova` referenciando `Materia` e `Bobica` via chave estrangeira ORM).

### 3.7 `App/Database/`

- **Objetivo:** isolar o acesso físico ao banco de dados.
- **Responsabilidade:** executar queries SQL, gerenciar conexão, e devolver dados brutos (ou objetos de `models`, no estado futuro).
- **Deve conter:** `connector.py` (conexão e execução genérica de query) e um arquivo por entidade com as operações CRUD específicas.
- **Não deve conter:** regras de negócio (agregações, validações cruzadas), formatação de resposta HTTP, schemas Pydantic.
- **Relação com outras partes:** é consumido por `services` (no estado futuro) ou diretamente por `Routers` (estado atual, a ser migrado); depende da configuração em `.env` (raiz do projeto).
- **Possíveis adições futuras:** pool de conexões (em vez de conexão única global, que não é resiliente a quedas), migrations (pasta `migrations/` com Alembic), arquivo de configuração de sessão SQLAlchemy caso o projeto migre de SQL cru para ORM.

### 3.8 `Frontend/`

- **Objetivo:** fornecer a interface com a qual o usuário final interage.
- **Responsabilidade:** consumir a API do `App`, apresentar os dados de matérias, bobicas e provas, e permitir a criação/edição desses registros.
- **Deve conter:** a aplicação cliente completa, incluindo sua própria estrutura interna de pastas (componentes, páginas, serviços de chamada HTTP, estado global), a ser definida quando a stack for escolhida.
- **Não deve conter:** lógica de negócio de domínio (essa deve viver no backend, para evitar duplicidade de regras entre cliente e servidor) nem acesso direto ao banco de dados.
- **Relação com outras partes:** comunica-se exclusivamente com `App` via chamadas HTTP/JSON.
- **Possíveis adições futuras:** `Frontend/src/pages`, `Frontend/src/components`, `Frontend/src/services` (cliente HTTP), `Frontend/src/hooks` ou `store` (estado), dependendo do framework escolhido.

### 3.9 `tests/`

- **Objetivo:** garantir a corretude e estabilidade do backend (e futuramente do frontend).
- **Responsabilidade:** validar o comportamento de `Routers`, `services`, `models` e `Database` de forma isolada e integrada.
- **Deve conter:** testes espelhando a estrutura de `App` (ex.: `tests/routers/test_materias.py`, `tests/database/test_connector.py`), fixtures de banco de dados de teste, e configuração do runner (`pytest.ini` ou `conftest.py`).
- **Não deve conter:** lógica de produção, dados sensíveis reais (usar dados de teste/fixtures), dependência de banco de produção.
- **Relação com outras partes:** importa e exercita diretamente os módulos de `App`.
- **Possíveis adições futuras:** `tests/conftest.py` (fixtures compartilhadas, como client de teste do FastAPI e banco de dados isolado), `tests/integration/` vs `tests/unit/`, testes de contrato para o Frontend futuramente.

### 3.10 Raiz do projeto (arquivos de configuração)

- **Objetivo:** configurar o ambiente de desenvolvimento e execução do projeto como um todo.
- **Responsabilidade:** declarar dependências (`requirements.txt`), variáveis sensíveis (`.env`), e regras de versionamento (`.gitignore`).
- **Deve conter:** arquivos de configuração de projeto, documentação de alto nível (`README.md`, ainda inexistente), e futuramente arquivos de orquestração (`docker-compose.yml`, `Dockerfile`) e de qualidade de código (`.flake8`, `pyproject.toml` com `black`/`ruff`).
- **Não deve conter:** código-fonte da aplicação (isso pertence a `App` e `Frontend`).
- **Relação com outras partes:** é lido por todas as camadas do backend (via `dotenv`) e usado pelo ambiente de execução (`uvicorn`, `pip`).
- **Possíveis adições futuras:** `README.md`, `docker-compose.yml`, `Dockerfile`, `pyproject.toml`, `Makefile` com atalhos de comandos (rodar servidor, rodar testes, aplicar migrations).

---

## 4. Fluxo da aplicação

Conceitualmente, o fluxo de dados na aplicação deve seguir o seguinte percurso, da entrada da requisição até o resultado final entregue ao usuário:

1. **Entrada:** o usuário interage com o `Frontend` (quando existir), que dispara uma requisição HTTP para a API.
2. **Roteamento:** a requisição chega a um `Router` correspondente ao recurso solicitado (`materias`, `bobicas` ou `provas`), que identifica o endpoint e extrai os parâmetros da URL/corpo.
3. **Validação de contrato:** os dados de entrada são validados automaticamente pelo `schema` associado (Pydantic), garantindo tipos e formato corretos antes de qualquer processamento.
4. **Orquestração de negócio:** o `Router` delega o processamento a uma função de `services`, que decide quais operações de dados são necessárias e aplica eventuais regras de negócio (ex.: verificar se a matéria/bobica existe antes de registrar uma prova; agregar contagens).
5. **Acesso a dados:** o `service` invoca funções de `Database`, que executam as queries SQL necessárias contra o PostgreSQL através do `connector`.
6. **Modelagem de domínio:** os dados brutos retornados pelo banco são (no estado futuro) convertidos em instâncias de `models`, evitando o uso de índices de tupla e tornando o dado autoexplicativo.
7. **Resposta:** o `service` devolve ao `Router` um resultado já tratado; o `Router` o encaixa no `schema` de resposta apropriado e o retorna como JSON.
8. **Saída:** o `Frontend` recebe a resposta e a apresenta ao usuário (tabelas, formulários, gráficos de uso de bobicas por matéria, etc.).
9. **Verificação contínua:** em paralelo a esse fluxo, `tests` deve validar cada uma dessas etapas isoladamente (testes unitários de `services`/`Database`) e em conjunto (testes de integração via cliente de teste do FastAPI).

---

## 5. Estrutura futura

```
TenX/
├── .env                        # Variáveis de ambiente (credenciais de banco, etc.) — nunca versionado
├── .gitignore                  # Regras de exclusão do controle de versão
├── requirements.txt            # Dependências Python do backend
├── README.md                   # (futuro) Documentação de alto nível: propósito, setup, execução
├── docker-compose.yml          # (futuro) Orquestração de banco de dados + API para desenvolvimento
├── pyproject.toml              # (futuro) Configuração de lint/formatação (ruff, black) e metadados do projeto
│
├── App/                        # Backend — API FastAPI
│   ├── __init__.py
│   ├── main.py                 # Ponto de entrada: cria app, registra routers, middlewares
│   ├── core/                   # (futuro) Configurações centrais, settings, segurança
│   │   ├── config.py           # (futuro) Leitura tipada de variáveis de ambiente
│   │   └── exceptions.py       # (futuro) Exceções de domínio e handlers globais
│   ├── dependencies.py         # (futuro) Dependências reutilizáveis do FastAPI (ex.: sessão de banco)
│   │
│   ├── Routers/                # Camada de exposição HTTP
│   │   ├── materias.py
│   │   ├── bobicas.py
│   │   └── provas.py
│   │
│   ├── schemas/                # Contratos de entrada/saída (Pydantic)
│   │   ├── materias.py
│   │   ├── bobicas.py
│   │   ├── provas.py
│   │   └── common.py           # (futuro) Tipos compartilhados: paginação, erro padrão
│   │
│   ├── services/                # Regras de negócio (atualmente vazio)
│   │   ├── materias_service.py # (futuro)
│   │   ├── bobicas_service.py  # (futuro)
│   │   └── provas_service.py   # (futuro) — ex.: agregação de contagem por matéria
│   │
│   ├── models/                  # Entidades de domínio / ORM (atualmente vazio)
│   │   ├── base.py             # (futuro) Base declarativa SQLAlchemy, se adotado
│   │   ├── materia.py           # (futuro)
│   │   ├── bobica.py            # (futuro)
│   │   └── prova.py             # (futuro)
│   │
│   └── Database/                # Acesso a dados (PostgreSQL)
│       ├── connector.py         # Conexão e execução de queries
│       ├── materias.py
│       ├── bobicas.py
│       └── provas.py
│
├── Frontend/                    # Interface do usuário (atualmente vazia — stack a definir)
│   └── (estrutura a ser definida conforme o framework escolhido: src/pages,
│         src/components, src/services, etc.)
│
└── tests/                       # Testes automatizados (atualmente vazia)
    ├── conftest.py               # (futuro) Fixtures compartilhadas (client de teste, banco de teste)
    ├── routers/                  # (futuro) Testes de endpoint
    ├── services/                 # (futuro) Testes de regra de negócio
    └── database/                 # (futuro) Testes de acesso a dados
```

---

## 6. Prioridades

O desenvolvimento futuro deve ser organizado em etapas incrementais, do essencial ao avançado, respeitando a separação de camadas definida neste documento.

### Etapa 1 — Consolidação da base atual (essencial)

Formalizar a separação de responsabilidades que já está esboçada na estrutura de pastas, mas ainda não totalmente aplicada no fluxo de dados: garantir que `Routers` deixe de acessar `Database` diretamente e passe a depender de `services`; iniciar o preenchimento de `services` com as regras já existentes de forma implícita (como a agregação de `provas` por matéria); documentar o propósito do projeto e das entidades de domínio (README).

### Etapa 2 — Confiabilidade e persistência (essencial)

Introduzir gerenciamento de conexão mais robusto (pool de conexões em vez de conexão única global), variáveis de ambiente documentadas, e uma primeira camada de testes automatizados cobrindo `Database` e `services`, garantindo uma base segura para evoluir sem regressões.

### Etapa 3 — Modelagem de domínio (intermediário)

Preencher `App/models` com representações tipadas das entidades, avaliando a adoção do SQLAlchemy (já presente nas dependências) como ORM, o que trará ganhos de manutenibilidade e eliminará o acesso por índice de tupla.

### Etapa 4 — Contrato de API mais rico (intermediário)

Expandir `schemas` com modelos de atualização, paginação e respostas de erro padronizadas; revisar os `Routers` para eliminar rotas duplicadas com mesmo path (identificadas na estrutura atual) e adotar convenções RESTful mais consistentes.

### Etapa 5 — Interface de usuário (avançado)

Definir a stack tecnológica do `Frontend`, estruturar suas pastas internas seguindo o mesmo princípio de separação por responsabilidade, e implementar o consumo da API já estabilizada nas etapas anteriores.

### Etapa 6 — Qualidade, observabilidade e operação (avançado)

Adicionar testes de integração ponta a ponta (Frontend + Backend), configurar CI/CD, logging estruturado, tratamento de erros centralizado (`core/exceptions.py`), e containerização (`Docker`/`docker-compose`) para padronizar o ambiente de desenvolvimento e produção.

---

*Documento gerado a partir da análise da estrutura e do código-fonte existente no projeto TenX, com o objetivo de servir como referência arquitetural para as próximas etapas de desenvolvimento.*





- [ ] aaaaaaaaaaaaaaaaaaaaaaaaa