import resend

from app.database import SessionLocal, settings
from app.services.notificacao_service import NotificacaoService


def enviar_notificacao_diaria() -> dict:
    """Executado 1x/dia pelo scheduler (ou manualmente via endpoint de teste).
    Abre sua própria sessão de banco, já que não roda dentro de um request HTTP.
    """
    db = SessionLocal()
    try:
        service = NotificacaoService(db)
        itens = service.gerar_resumo()
        corpo_html = service.montar_corpo_email(itens)

        resend.api_key = settings.resend_api_key
        resposta = resend.Emails.send(
            {
                "from": settings.email_from,
                "to": settings.notification_email_to,
                "subject": f"LocaFácil — resumo do dia ({len(itens)} contrato(s) para atenção)",
                "html": corpo_html,
            }
        )
        return {"enviado": True, "itens": len(itens), "resend_id": resposta.get("id")}
    finally:
        db.close()
