from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class PagamentoCreate(BaseModel):
    cliente_id: str = Field(min_length=1)
    codigo_pagamento: str = Field(min_length=1)
    valor_total: float = Field(gt=0)
    tipo_pagamento: str = Field(min_length=1)
    numero_parcelas: int = Field(ge=1)
    data_pagamento: datetime


class PagamentoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    cliente_id: str
    cliente_email: str
    codigo_pagamento: str
    valor_total: float
    tipo_pagamento: str
    numero_parcelas: int
    valor_parcela: float
    data_pagamento: datetime