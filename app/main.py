from time import sleep
from typing import Dict, Optional

from fastapi import Depends, FastAPI, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app.models import Course
from app.schemas import CourseCreate, CourseRead

app = FastAPI(title="API de Cursos")

# CORS habilitado para localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock auth - aceita qualquer token
def get_mock_user(authorization: Optional[str] = Header(None)) -> Dict:
    return {"email": "user@example.com", "sub": "user123", "roles": ["admin"]}

@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def startup():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")


@app.get("/courses", response_model=list[CourseRead])
def listar_cursos(
    user: Dict = Depends(get_mock_user),
    db: Session = Depends(get_db)
):
    """
    Listar cursos. Disponível para ADMIN e USER.
    """
    return db.query(Course).order_by(Course.created_at.desc()).all()


@app.post("/courses", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def cadastrar_curso(
    payload: CourseCreate,
    user: Dict = Depends(get_mock_user),
    db: Session = Depends(get_db)
):
    """
    Cadastrar novo curso. Apenas ADMIN pode criar.
    """
    admin_email = user.get("email", "admin@example.com")
    
    # Verificar se o código do curso já existe
    existing_course = db.query(Course).filter(
        Course.course_code == payload.course_code
    ).first()
    
    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Código do curso já existe"
        )

    course = Course(
        course_code=payload.course_code,
        course_name=payload.course_name,
        instructor_name=payload.instructor_name,
        admin_email=admin_email,
    )

    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@app.delete("/courses/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_curso(
    id: str,
    user: Dict = Depends(get_mock_user),
    db: Session = Depends(get_db)
):
    """
    Deletar curso. Apenas ADMIN pode deletar.
    """
    course = db.query(Course).filter(Course.id == id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )

    db.delete(course)
    db.commit()
