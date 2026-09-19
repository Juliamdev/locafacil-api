# ADR 003 — App mobile (React Native/Expo) como primeiro frontend

## Status
Aceito

## Contexto
O sistema precisa de uma interface para o cliente (proprietário) gerenciar casas, inquilinos, contratos e pagamentos, além de receber alertas.

## Decisão
Construir primeiro um **app mobile em React Native (Expo)**, distribuído por build direto (sideload) para o cliente, sem publicação em loja.

## Justificativa
- O cliente usa Android; a distribuição fora de loja é gratuita e simples (basta permitir instalação de fontes desconhecidas).
- Um app mobile permite complementar o e-mail com notificação push (Firebase Cloud Messaging, gratuito).
- O backend já nasce como API REST desacoplada — uma versão web pode ser adicionada depois como um novo frontend, sem alterar o backend.

## Alternativas consideradas
- **Web app responsivo**: mais simples de distribuir (sem instalação), mas sem suporte nativo a push notification gratuito equivalente, e o cliente prefere um app instalável no celular.
- **Publicação em loja (Google Play)**: desnecessária para uso de um único cliente; taxa de US$ 25 só se justificaria em uma futura comercialização para múltiplos clientes.

## Consequências
- Distribuição de atualizações do app exige gerar e reenviar um novo build (via EAS Build) para o cliente instalar manualmente, já que não passa pela Play Store.
- iOS não é suportado por esta via de distribuição gratuita — caso o cliente troque para iPhone, será necessário avaliar conta de desenvolvedor Apple.
