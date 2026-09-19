# Requisitos — LocaFácil

## 1. Contexto

Sistema para controle financeiro de aluguel de um proprietário com aproximadamente 10 casas alugadas. Hoje esse controle não existe: não há registro de quem pagou, quando pagou nem quanto pagou.

## 2. Personas

- **Cliente (proprietário)** — usuário único do sistema no MVP. Cadastra casas, inquilinos e contratos, lança pagamentos e recebe alertas.
- **Inquilino** — não tem acesso ao sistema no MVP (fora de escopo). Existe apenas como registro de dados.

## 3. Requisitos funcionais

| ID | Descrição |
|---|---|
| RF01 | Cadastrar casas (endereço, valor de referência do aluguel) |
| RF02 | Cadastrar inquilinos (nome, contato) |
| RF03 | Cadastrar contrato de locação vinculando casa + inquilino (data de início, prazo de 1 ano, valor do aluguel, dia de vencimento) |
| RF04 | Encerrar contrato antes do prazo (saída do inquilino ou solicitação do proprietário) |
| RF05 | Registrar pagamento (valor, data, forma = Pix), podendo ser parcial |
| RF06 | Alocar automaticamente o valor pago às parcelas em aberto, da mais antiga para a mais recente |
| RF07 | Calcular e exibir o saldo devedor acumulado por contrato |
| RF08 | Listar contratos com status (em dia / parcial / atrasado) |
| RF09 | Enviar e-mail diário com resumo de vencimentos próximos e inadimplências |
| RF10 | Alertar quando um contrato está próximo do fim do prazo de 1 ano |
| RF11 (opcional) | Notificação push complementar ao e-mail |

## 4. Regras de negócio

- **Parcela mensal**: cada contrato ativo gera uma parcela por mês de referência, com `valor_esperado` = valor do aluguel do contrato.
- **Saldo devedor**: soma acumulada, ao longo de todas as parcelas do contrato, de `valor_esperado − valor_pago`. Não zera a cada mês — dívidas anteriores se somam às seguintes.
- **Status "atrasado"**: uma parcela é considerada atrasada a partir do dia seguinte ao seu vencimento, sem tolerância, caso ainda tenha saldo em aberto.
- **Alocação de pagamento parcial**: ao registrar um pagamento, o valor é distribuído automaticamente começando pela parcela em aberto mais antiga, depois a próxima, e assim por diante (não é vinculado obrigatoriamente ao mês corrente). Justificativa: pagamentos são via Pix, sem boleto por parcela.
- **Fim de contrato**: ao atingir a data prevista de término (1 ano), o sistema não renova automaticamente — fica pendente de ação manual do cliente (renovar, encerrar ou negociar novo contrato).
- **Encerramento antecipado**: o cliente pode encerrar um contrato antes do prazo previsto (saída do inquilino ou pedido do proprietário), registrando a data real de encerramento.

## 5. Requisitos não funcionais

| ID | Descrição |
|---|---|
| RNF01 | Custo de infraestrutura zero ou próximo de zero |
| RNF02 | Notificação primária por e-mail (evitar custo de API de WhatsApp) |
| RNF03 | Backend como API REST, consumível por qualquer cliente (mobile hoje, web no futuro) |
| RNF04 | Deploy inicial em camadas gratuitas (Render/Railway + Supabase/Neon + Vercel) |
| RNF05 | Distribuição do app mobile via build direto (sideload), sem custo de loja |

## 6. Fora de escopo (MVP)

- Login/acesso do inquilino ao sistema
- Emissão de boleto ou integração com meio de pagamento
- Múltiplos usuários/proprietários (multi-tenant)
- Publicação em loja de aplicativos
