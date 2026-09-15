from fastapi import APIRouter

from app.jobs.notificacao_diaria import enviar_notificacao_diaria

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/notificacao/executar")
def executar_notificacao_manual():
    """Dispara o mesmo job que roda diariamente às 08:00 — útil para testar
    sem esperar o horário agendado."""
    return enviar_notificacao_diaria()
