from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

app = FastAPI(title="API de Cursos - Mock")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos
class CourseCreate(BaseModel):
    course_code: str
    course_name: str
    instructor_name: str

class CourseRead(BaseModel):
    id: str
    course_code: str
    course_name: str
    instructor_name: str
    admin_email: str
    status: str = "DISPONIVEL"
    created_at: str

# Dados em memória (para teste)
COURSES_DB = []

# Rotas
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/courses", response_model=List[CourseRead])
def listar_cursos():
    """Listar todos os cursos"""
    return COURSES_DB

@app.post("/courses", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def cadastrar_curso(payload: CourseCreate):
    """Criar novo curso"""
    # Verif se code existe
    if any(c["course_code"] == payload.course_code for c in COURSES_DB):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Código do curso já existe"
        )
    
    course = {
        "id": str(uuid.uuid4()),
        "course_code": payload.course_code,
        "course_name": payload.course_name,
        "instructor_name": payload.instructor_name,
        "admin_email": "admin@example.com",
        "status": "DISPONIVEL",
        "created_at": datetime.now().isoformat()
    }
    
    COURSES_DB.append(course)
    return course

@app.delete("/courses/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_curso(id: str):
    """Deletar um curso"""
    global COURSES_DB
    course = next((c for c in COURSES_DB if c["id"] == id), None)
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )
    
    COURSES_DB = [c for c in COURSES_DB if c["id"] != id]
    return None
