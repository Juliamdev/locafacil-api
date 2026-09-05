# Diagrama Entidade-Relacionamento — LocaFácil

> Este diagrama é escrito em Mermaid e renderiza automaticamente na visualização do GitHub.

```mermaid
erDiagram
    CASA ||--o{ CONTRATO : possui
    INQUILINO ||--o{ CONTRATO : assina
    CONTRATO ||--o{ PARCELA : gera
    CONTRATO ||--o{ PAGAMENTO : recebe
    PAGAMENTO ||--o{ PAGAMENTO_PARCELA : aloca
    PARCELA ||--o{ PAGAMENTO_PARCELA : recebe

    CASA {
        uuid id PK
        string endereco
        decimal valor_referencia
    }

    INQUILINO {
        uuid id PK
        string nome
        string email
        string telefone
    }

    CONTRATO {
        uuid id PK
        uuid casa_id FK
        uuid inquilino_id FK
        decimal valor_aluguel
        int dia_vencimento
        date data_inicio
        date data_fim_prevista
        date data_fim_real
        string status
    }

    PARCELA {
        uuid id PK
        uuid contrato_id FK
        string mes_referencia
        date data_vencimento
        decimal valor_esperado
        decimal valor_pago
        string status
    }

    PAGAMENTO {
        uuid id PK
        uuid contrato_id FK
        date data_pagamento
        decimal valor
        string forma_pagamento
    }

    PAGAMENTO_PARCELA {
        uuid id PK
        uuid pagamento_id FK
        uuid parcela_id FK
        decimal valor_alocado
    }
```

## Notas de modelagem

- **Parcela** é gerada automaticamente todo mês para cada contrato ativo (`valor_esperado` = `valor_aluguel` do contrato no momento da geração).
- **Pagamento** representa o valor recebido de fato (evento financeiro real, ex: um Pix).
- **PagamentoParcela** é a tabela de alocação: registra como cada pagamento foi distribuído entre parcelas, sempre da mais antiga em aberto para a mais recente. Isso mantém o histórico auditável (dá pra ver exatamente qual pagamento cobriu qual mês).
- O **saldo devedor** de um contrato é calculado (não armazenado diretamente) como: soma de `valor_esperado` de todas as parcelas do contrato menos soma de `valor_pago`.
- `status` da parcela (pago / parcial / atrasado / pendente) pode ser calculado em tempo real pela regra de negócio, sem precisar ser persistido — evita inconsistência.
