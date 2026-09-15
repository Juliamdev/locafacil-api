from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import casa, inquilino, contrato, pagamento, jobs
from app.jobs.scheduler import iniciar_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    iniciar_scheduler()  # agenda o job diário de notificação (08:00)
    yield


app = FastAPI(
    title="LocaFácil API",
    description="Controle financeiro de aluguel — casas, inquilinos, contratos e pagamentos.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(casa.router)
app.include_router(inquilino.router)
app.include_router(contrato.router)
app.include_router(pagamento.router)
app.include_router(jobs.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
