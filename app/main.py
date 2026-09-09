from fastapi import FastAPI

from app.api import casa, inquilino, contrato, pagamento

app = FastAPI(
    title="LocaFácil API",
    description="Controle financeiro de aluguel — casas, inquilinos, contratos e pagamentos.",
    version="0.1.0",
)

app.include_router(casa.router)
app.include_router(inquilino.router)
app.include_router(contrato.router)
app.include_router(pagamento.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
