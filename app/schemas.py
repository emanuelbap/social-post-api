from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class CourseStatus(str, Enum):
    DISPONIVEL = "DISPONIVEL"
    CANCELADO = "CANCELADO"


class CourseCreate(BaseModel):
    course_code: str = Field(min_length=1)
    course_name: str = Field(min_length=1)
    instructor_name: str = Field(min_length=1)


class CourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    course_code: str
    course_name: str
    instructor_name: str
    admin_email: str
    status: CourseStatus
    created_at: datetime