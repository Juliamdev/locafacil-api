# LocaFácil API

API REST para controle financeiro de aluguel de imóveis — cadastro de casas, inquilinos e contratos, lançamento de pagamentos (com suporte a pagamento parcial), cálculo de saldo devedor e notificação automática por e-mail.

## Stack

- **Linguagem**: Python 3.12+
- **Framework**: FastAPI
- **Banco**: PostgreSQL (Supabase/Neon)
- **ORM**: SQLAlchemy + Alembic (migrations)
- **Agendamento**: APScheduler (job diário de notificação)
- **E-mail**: Resend

## Documentação

- [`docs/requisitos.md`](docs/requisitos.md) — requisitos funcionais, não funcionais e regras de negócio
- [`docs/der.md`](docs/der.md) — diagrama entidade-relacionamento
- [`docs/arquitetura.md`](docs/arquitetura.md) — arquitetura em camadas e diagrama de contexto
- [`docs/adr/`](docs/adr) — registros de decisões de arquitetura

## Estrutura de pastas

```
app/
├── api/            # routers (rotas HTTP)
├── services/        # regras de negócio
├── repositories/     # acesso a dados
├── models/           # entidades SQLAlchemy
├── schemas/          # validação Pydantic
└── jobs/              # tarefas agendadas
alembic/              # migrations do banco
tests/
```

## Como rodar localmente

```bash
# 1. Clonar o repositório
git clone <url-do-repo>
cd locafacil-api

# 2. Criar ambiente virtual e instalar dependências
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente
cp .env.example .env
# preencher DATABASE_URL e RESEND_API_KEY

# 4. Rodar as migrations
alembic upgrade head

# 5. Subir o servidor
uvicorn app.main:app --reload
```

A documentação interativa da API fica disponível em `http://localhost:8000/docs`.

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `DATABASE_URL` | String de conexão do PostgreSQL |
| `RESEND_API_KEY` | Chave de API do Resend para envio de e-mail |
| `NOTIFICATION_EMAIL_TO` | E-mail do cliente que recebe os alertas |

## Deploy

Backend hospedado no Render/Railway (camada gratuita), banco no Supabase/Neon (camada gratuita).
