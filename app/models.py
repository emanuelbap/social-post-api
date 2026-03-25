from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.db import Base


class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    cliente_id = Column(String(50), nullable=False, index=True)
    cliente_email = Column(String(255), nullable=False)

    codigo_pagamento = Column(String(100), nullable=False, unique=True, index=True)
    valor_total = Column(Float, nullable=False)
    tipo_pagamento = Column(String(20), nullable=False)
    numero_parcelas = Column(Integer, nullable=False)
    valor_parcela = Column(Float, nullable=False)

    data_pagamento = Column(DateTime, nullable=False, default=datetime.utcnow)