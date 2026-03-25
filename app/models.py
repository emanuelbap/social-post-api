from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Text

from app.db import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    titulo = Column(String(200), nullable=False)
    mensagem = Column(Text, nullable=False)
    data = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    usuario = Column(String(100), nullable=False, index=True)