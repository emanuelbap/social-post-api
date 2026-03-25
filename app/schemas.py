from pydantic import BaseModel
from datetime import datetime


class PagamentoCreate(BaseModel):
    codigo: str
    valor_total: float
    tipo: str
    parcelas: int
    cliente_id: str


class PagamentoRead(BaseModel):
    id: str
    codigo: str
    valor_total: float
    tipo: str
    parcelas: int
    valor_parcela: float
    data: datetime
    cliente_id: str
    cliente_email: str