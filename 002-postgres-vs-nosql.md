# ADR 002 — PostgreSQL relacional em vez de banco NoSQL

## Status
Aceito

## Contexto
O domínio do sistema (casas, inquilinos, contratos, parcelas, pagamentos e a alocação entre eles) é fortemente relacional, com múltiplas chaves estrangeiras e a necessidade de somas e agregações consistentes (saldo devedor).

## Decisão
Usar **PostgreSQL**, hospedado gratuitamente em Supabase ou Neon.

## Justificativa
- Relacionamentos claros entre entidades (Contrato → Parcelas → Pagamentos) se beneficiam de chaves estrangeiras e integridade referencial nativas.
- Cálculo de saldo devedor depende de somas agregadas consistentes — mais natural em SQL do que em um modelo de documentos.
- Camada gratuita generosa tanto no Supabase quanto no Neon, suficiente para a escala do projeto (10 casas).
- Migrations versionadas (via Alembic) documentam a evolução do schema ao longo do projeto.

## Alternativas consideradas
- **Firestore (NoSQL)**: mais simples para prototipagem rápida, mas exigiria desnormalizar dados ou fazer múltiplas leituras para calcular saldo devedor de forma consistente.

## Consequências
- Precisa definir migrations a cada mudança de schema (Alembic), mas isso já é parte da documentação técnica desejada para o projeto.
