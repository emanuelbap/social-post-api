from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Float, Integer, DateTime
from app.db import Base


class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    codigo = Column(String)
    valor_total = Column(Float)
    tipo = Column(String)
    parcelas = Column(Integer)
    valor_parcela = Column(Float)
    data = Column(DateTime, default=datetime.utcnow)
    cliente_id = Column(String)
    cliente_email = Column(String)