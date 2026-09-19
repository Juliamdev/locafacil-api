# ADR 001 — FastAPI em vez de Django

## Status
Aceito

## Contexto
Precisávamos de um framework Python para a API REST do backend, com baixo tempo de setup (projeto desenvolvido solo) e boa documentação automática.

## Decisão
Usar **FastAPI**.

## Justificativa
- Gera documentação OpenAPI/Swagger automaticamente a partir do próprio código, reduzindo o esforço de documentar a API manualmente.
- Menos boilerplate que Django para um projeto que é "API-only" (sem necessidade de admin panel, templates ou ORM próprio).
- Tipagem nativa com Pydantic, o que ajuda a validar entrada/saída sem código extra.
- Alinhado ao domínio Python já conhecido.

## Alternativas consideradas
- **Django + Django REST Framework**: mais robusto para projetos grandes com múltiplos apps, mas com mais boilerplate para um MVP de porte pequeno.
- **ASP.NET Core Web API**: também gera Swagger nativamente e seria uma opção igualmente válida; não escolhida por preferência de manter o projeto em Python.

## Consequências
- Sem admin panel pronto — telas de gestão precisam ser construídas no app mobile.
- Ecossistema de bibliotecas Python (SQLAlchemy, Alembic, APScheduler) continua totalmente compatível.
