from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db import Base, engine, get_db
from app.models import Pagamento
from app.schemas import PagamentoCreate, PagamentoRead
from app.user_client import UserClient

app = FastAPI()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


# GET com filtro opcional
@app.get("/pagamento", response_model=list[PagamentoRead])
def listar_pagamentos(cliente_id: str = None, db: Session = Depends(get_db)):
    if cliente_id:
        return db.query(Pagamento).filter(Pagamento.cliente_id == cliente_id).all()

    return db.query(Pagamento).all()


# POST pagamento
@app.post("/pagamento", response_model=PagamentoRead)
def criar_pagamento(payload: PagamentoCreate, db: Session = Depends(get_db)):
    user_client = UserClient()

    user = user_client.get_user(payload.cliente_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    valor_parcela = payload.valor_total / payload.parcelas

    pagamento = Pagamento(
        codigo=payload.codigo,
        valor_total=payload.valor_total,
        tipo=payload.tipo,
        parcelas=payload.parcelas,
        valor_parcela=valor_parcela,
        cliente_id=payload.cliente_id,
        cliente_email=user["email"],
    )

    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)

    return pagamento


# DELETE
@app.delete("/pagamento/{id}")
def deletar_pagamento(id: str, db: Session = Depends(get_db)):
    pagamento = db.query(Pagamento).filter(Pagamento.id == id).first()

    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")

    db.delete(pagamento)
    db.commit()

    return {"msg": "Deletado com sucesso"}