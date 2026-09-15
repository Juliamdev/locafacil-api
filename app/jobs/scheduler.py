from apscheduler.schedulers.background import BackgroundScheduler

from app.jobs.notificacao_diaria import enviar_notificacao_diaria

scheduler = BackgroundScheduler()


def iniciar_scheduler():
    # Roda todo dia às 08:00 — horário parametrizável se precisar ajustar depois.
    scheduler.add_job(
        enviar_notificacao_diaria,
        trigger="cron",
        hour=8,
        minute=0,
        id="notificacao_diaria",
        replace_existing=True,
    )
    scheduler.start()
