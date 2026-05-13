from datetime import datetime
from uuid import uuid4
from enum import Enum

from sqlalchemy import Column, DateTime, String, Enum as SQLEnum

from app.db import Base


class CourseStatus(str, Enum):
    DISPONIVEL = "DISPONIVEL"
    CANCELADO = "CANCELADO"


class Course(Base):
    __tablename__ = "courses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    course_code = Column(String(50), nullable=False, unique=True, index=True)
    course_name = Column(String(255), nullable=False)
    instructor_name = Column(String(255), nullable=False)
    admin_email = Column(String(255), nullable=False)
    status = Column(SQLEnum(CourseStatus), nullable=False, default=CourseStatus.DISPONIVEL)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)