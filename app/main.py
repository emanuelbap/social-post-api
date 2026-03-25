from fastapi import Depends, FastAPI, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app.models import Post
from app.schemas import PostCreate, PostRead
from app.settings import get_settings
from app.user_client import UserClient, UserServiceError

settings = get_settings()
app = FastAPI(title="social-post-api")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


def get_user_client() -> UserClient:
    return UserClient(
        base_url=settings.users_api_url,
        timeout=settings.users_api_timeout,
        token=settings.users_api_token,
    )


@app.get("/post", response_model=list[PostRead])
def list_posts(db: Session = Depends(get_db)):
    return db.query(Post).order_by(Post.data.desc()).all()


@app.post("/post", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(
    payload: PostCreate,
    usuario: str = Header(..., alias="X-User-Id"),
    db: Session = Depends(get_db),
    user_client: UserClient = Depends(get_user_client),
):
    try:
        exists = user_client.user_exists(usuario)
    except UserServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    if not exists:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    post = Post(
        titulo=payload.titulo,
        mensagem=payload.mensagem,
        usuario=usuario,
    )

    db.add(post)
    db.commit()
    db.refresh(post)
    return post