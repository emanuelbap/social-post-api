# Sistema de Gerenciamento de Cursos - Backend

API FastAPI para o sistema de gerenciamento de cursos da universidade com autenticação Auth0.

## Recursos

- ✅ Autenticação e autorização via Auth0
- ✅ CRUD de cursos
- ✅ Controle de acesso por papel (ADMIN/USER)
- ✅ Banco de dados PostgreSQL
- ✅ Containerização Docker
- ✅ CI/CD com GitHub Actions

## Endpoints

### Autenticação
Todos os endpoints requerem token JWT válido no header `Authorization: Bearer <token>`

### GET /courses
Lista todos os cursos. Disponível para ADMIN e USER.

**Resposta:**
```json
[
  {
    "id": "uuid",
    "course_code": "CS101",
    "course_name": "Introdução à Computação",
    "instructor_name": "Dr. Silva",
    "admin_email": "admin@university.edu",
    "status": "DISPONIVEL",
    "created_at": "2024-05-13T10:30:00"
  }
]
```

### POST /courses
Cadastra um novo curso. Apenas ADMIN.

**Request:**
```json
{
  "course_code": "CS101",
  "course_name": "Introdução à Computação",
  "instructor_name": "Dr. Silva"
}
```

### DELETE /courses/{id}
Deleta um curso. Apenas ADMIN.

## Pré-requisitos

- Python 3.12+
- PostgreSQL 16+
- Docker e Docker Compose
- Conta Auth0

## Configuração Local

1. Clone o repositório
2. Configure as variáveis de ambiente:

```bash
cp .env.example .env
```

3. Preencha os valores:
   - `DATABASE_URL`: URL do PostgreSQL
   - `AUTH0_DOMAIN`: Seu domínio Auth0
   - `AUTH0_CLIENT_ID`: Seu Client ID Auth0

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

5. Inicie o bando de dados:

```bash
docker-compose up db
```

6. Execute a aplicação:

```bash
uvicorn app.main:app --reload
```

A API estará disponível em http://localhost:8000

## Docker Compose

```bash
docker-compose up
```

## Estrutura de Papéis Auth0

Configure os seguintes papéis no Auth0:

- `admin`: Pode criar e deletar cursos
- `user`: Pode apenas visualizar cursos

Adicione a seguinte custom claim ao ID Token:
```json
{
  "https://courses-api/roles": "array"
}
```

## Deploy

### GitHub Actions + EC2

1. Configure os secrets no GitHub:
   - `DOCKERHUB_USERNAME`: Seu usuário Docker Hub
   - `DOCKERHUB_TOKEN`: Seu token Docker Hub
   - `EC2_HOST`: IP da sua instância EC2
   - `EC2_SSH_KEY`: Chave SSH privada para EC2

2. Faça push para main e a aplicação fará deploy automaticamente

## Documentação API

Acesse http://localhost:8000/docs para visualizar a documentação interativa (Swagger UI)
