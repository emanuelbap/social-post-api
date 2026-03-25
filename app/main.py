from time import sleep

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app.models import Pagamento
from app.schemas import PagamentoCreate, PagamentoRead
from app.settings import get_settings
from app.user_client import UserClient, UserServiceError

settings = get_settings()
app = FastAPI(title="API de pagamentos")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def startup():
    for _ in range(20):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            Base.metadata.create_all(bind=engine)
            return
        except Exception:
            sleep(2)

    raise RuntimeError("Banco indisponível")


def get_user_client() -> UserClient:
    return UserClient(
        base_url=settings.users_api_url,
        timeout=settings.users_api_timeout,
    )


@app.get("/pagamento", response_model=list[PagamentoRead])
def listar_pagamentos(cliente_id: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Pagamento)

    if cliente_id:
        query = query.filter(Pagamento.cliente_id == cliente_id)

    return query.order_by(Pagamento.data_pagamento.desc()).all()


@app.post("/pagamento", response_model=PagamentoRead, status_code=status.HTTP_201_CREATED)
def criar_pagamento(
    payload: PagamentoCreate,
    db: Session = Depends(get_db),
    user_client: UserClient = Depends(get_user_client),
):
    try:
        user = user_client.get_user(payload.cliente_id)
    except UserServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    tipo = payload.tipo_pagamento.strip().lower()
    if tipo not in {"pix", "crédito", "credito"}:
        raise HTTPException(status_code=400, detail="Tipo de pagamento inválido")

    tipo_normalizado = "PIX" if tipo == "pix" else "Crédito"
    valor_parcela = round(payload.valor_total / payload.numero_parcelas, 2)

    pagamento = Pagamento(
        cliente_id=payload.cliente_id,
        cliente_email=user["email"],
        codigo_pagamento=payload.codigo_pagamento,
        valor_total=payload.valor_total,
        tipo_pagamento=tipo_normalizado,
        numero_parcelas=payload.numero_parcelas,
        valor_parcela=valor_parcela,
        data_pagamento=payload.data_pagamento,
    )

    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)
    return pagamento


@app.delete("/pagamento/{id}")
def deletar_pagamento(id: str, db: Session = Depends(get_db)):
    pagamento = db.query(Pagamento).filter(Pagamento.id == id).first()

    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")

    db.delete(pagamento)
    db.commit()
    return {"msg": "Deletado com sucesso"}