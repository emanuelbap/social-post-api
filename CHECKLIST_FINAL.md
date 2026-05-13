# ✅ CHECKLIST FINAL - SISTEMA DE CURSOS

## 🎯 STATUS ATUAL
- ✅ Backend API criado (FastAPI)
- ✅ Frontend criado (Next.js)
- ✅ Sistema de autenticação mock funcionando
- ⏳ Faltam: configurar Auth0, conectar ao backend, fazer deploy

---

## 📋 PASSO A PASSO (Ordem Correta)

### FASE 1: TESTANDO LOCALMENTE (Hoje)

#### 1️⃣ Testar Backend Localmente
```bash
cd /home/emanuel/Documentos/social-post-api/social-post-api

# Ver requisitos
cat requirements.txt

# Instalar dependências Python
pip install -r requirements.txt
# OU se tiver venv:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Rodar backend
python -m uvicorn app.main:app --reload
# Acessa: http://localhost:8000
# Swagger docs: http://localhost:8000/docs
```

#### 2️⃣ Conectar Frontend ao Backend Localmente
Edite `.env.local` no frontend:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Reinicie:
```bash
cd /home/emanuel/Documentos/social-post-api/social-post-api/PF-zambao
npm run dev
```

#### 3️⃣ Testar Fluxo Completo (SEM Auth0)
1. Abra `http://localhost:3000`
2. Login com "admin@example.com" e role "admin"
3. Crie um curso
4. Veja se aparece na lista
5. Delete um curso

**Observação:** Se der erro de conexão, é porque o backend não está rodando.

---

### FASE 2: CONFIGURAR AUTH0 (Opcional, mas recomendado)

#### 1️⃣ Criar Conta Auth0
- Acesse https://auth0.com
- Clique em "Sign Up"
- Crie uma conta (email + senha)

#### 2️⃣ Criar Tenant
- Um será criado automaticamente
- Pode pular ou customizar

#### 3️⃣ Criar Aplicação
- Dashboard → Applications → Create Application
- Nome: "Sistema de Cursos"
- Tipo: **Regular Web Application**
- Clique "Create"

#### 4️⃣ Copiar Credenciais
Na aba "Settings":
- **Domain** (ex: `seu-dominio.auth0.com`)
- **Client ID** (ex: `abc123xyz`)
- **Client Secret** (ex: `super_secret_key`)

#### 5️⃣ Configurar URLs no Auth0
Ainda em Settings, procure por:

**Allowed Callback URLs:**
```
http://localhost:3000/api/auth/callback
```

**Allowed Logout URLs:**
```
http://localhost:3000
```

**Allowed Web Origins:**
```
http://localhost:3000
```

Clique "Save Changes"

#### 6️⃣ Configurar Roles
- Vá para: User Management → Roles
- Clique "Create"
- Crie role "admin"
- Clique "Create" novamente
- Crie role "user"

#### 7️⃣ Criar Custom Claim (IMPORTANTE!)
- Vá para: Actions → Library
- Clique "New Action"
- Trigger: "Login / Post Login"
- Nome: "Add Roles to Token"

Cole este código:
```javascript
exports.onExecutePostLogin = async (event, api) => {
  const namespace = 'https://courses-api/roles';
  const roles = event.authorization?.roles || [];
  api.idToken.setCustomClaim(namespace, roles);
  api.accessToken.setCustomClaim(namespace, roles);
};
```

Clique "Save"
Clique "Deploy"

#### 8️⃣ Adicionar Action ao Flow
- Na aba "Flows" da action
- Clique em "Login"
- Arraste a action para o fluxo
- Salve

#### 9️⃣ Editar `.env.local` do Frontend
```env
AUTH0_SECRET='96631e82caa0ca71a4dbb0bd6247046e0414ad199c268f0f6de5d52756a89053'
AUTH0_BASE_URL='http://localhost:3000'
AUTH0_ISSUER_BASE_URL='https://seu-dominio.auth0.com'
AUTH0_CLIENT_ID='seu_client_id_aqui'
AUTH0_CLIENT_SECRET='seu_client_secret_aqui'

NEXT_PUBLIC_AUTH0_DOMAIN=seu-dominio.auth0.com
NEXT_PUBLIC_AUTH0_CLIENT_ID=seu_client_id_aqui
NEXT_PUBLIC_AUTH0_REDIRECT_URI=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### 🔟 Testar Auth0
- Reinicie o frontend: `npm run dev`
- Acesse `http://localhost:3000`
- Deve mostrar tela de login Auth0

---

### FASE 3: GIT & GITHUB (Enviar código)

#### 1️⃣ Backend
```bash
cd /home/emanuel/Documentos/social-post-api/social-post-api

# Verificar remoto existente
git remote -v

# Se não tiver, adicionar
git remote add origin https://github.com/seu-user/seu-repo-backend.git

# Enviar
git add .
git commit -m "Projeto inicial: API de cursos com FastAPI e Auth0"
git push -u origin main
```

#### 2️⃣ Frontend
```bash
cd /home/emanuel/Documentos/social-post-api/social-post-api/PF-zambao

# Verificar remoto
git remote -v
# Deve estar apontando para PF-zambao repo

# Enviar
git add .
git commit -m "UI completa: Sistema de cursos com Next.js, Auth0 e mock auth"
git push -u origin main
```

---

### FASE 4: DEPLOY (Para produção)

#### BACKEND - Deploy no EC2

**4.1. Preparar Repo**
- Adicione arquivo `deployment.md` no backend com:
  - Como deploy (Docker)
  - Variáveis de ambiente necessárias
  - Como acessar

**4.2. GitHub Actions (CI/CD)**
- Arquivo já existe: `.github/workflows/deploy.yml`
- Você precisa configurar:
  - GitHub Secrets com dados de acesso EC2
  - IP da máquina EC2
  - Chave SSH privada

**4.3. EC2 Setup (Manual ou automático)**
```bash
# Na máquina EC2:
sudo apt update
sudo apt install docker.io
sudo apt install docker-compose

# Ou use GitHub Actions para automatizar
```

#### FRONTEND - Deploy na Vercel

**4.1. Conectar Vercel ao GitHub**
- Acesse https://vercel.com
- Faça login com GitHub
- Clique "New Project"
- Selecione repo do frontend (PF-zambao)
- Clique "Import"

**4.2. Configurar Variáveis**
Na aba "Settings" do projeto na Vercel:
- Environment Variables
- Adicione:
  ```
  NEXT_PUBLIC_AUTH0_DOMAIN=seu-dominio.auth0.com
  NEXT_PUBLIC_AUTH0_CLIENT_ID=seu_client_id
  NEXT_PUBLIC_AUTH0_REDIRECT_URI=https://seu-dominio.vercel.app
  NEXT_PUBLIC_API_URL=https://seu-backend-url
  AUTH0_SECRET=sua_chave_secreta
  AUTH0_BASE_URL=https://seu-dominio.vercel.app
  AUTH0_ISSUER_BASE_URL=https://seu-dominio.auth0.com
  AUTH0_CLIENT_ID=seu_client_id
  AUTH0_CLIENT_SECRET=seu_client_secret
  ```

**4.3. Deploy Automático**
- Vercel vai fazer deploy automático quando fizer push no GitHub

**4.4. Configurar Auth0 para Produção**
- Volta no Auth0
- Settings da aplicação
- Adicione as URLs de produção (Vercel):
  ```
  Allowed Callback URLs:
  https://seu-dominio.vercel.app/api/auth/callback
  
  Allowed Logout URLs:
  https://seu-dominio.vercel.app
  
  Allowed Web Origins:
  https://seu-dominio.vercel.app
  ```

---

## 🎯 ORDEM RECOMENDADA (Comece por isso):

1. **ÜJ HOJE:**
   - [ ] Testar backend localmente
   - [ ] Testar frontend localmente conectado ao backend
   - [ ] Testar login (mock ou Auth0)
   - [ ] Testar criar/listar/deletar cursos

2. **AMANHÃ (Opcional):**
   - [ ] Configurar Auth0
   - [ ] Enviar código pro GitHub
   - [ ] Deploy (EC2 + Vercel)

---

## 🔗 LINKS ÚTEIS

- Backend Swagger: http://localhost:8000/docs
- Frontend: http://localhost:3000
- Auth0: https://auth0.com/docs
- Vercel: https://vercel.com/docs
- FastAPI: https://fastapi.tiangolo.com

---

## ⚠️ CHECKLIST DE SEGURANÇA

- [ ] `.env.local` está em `.gitignore` (NÃO commitar)
- [ ] `AUTH0_SECRET` é único por máquina
- [ ] `AUTH0_CLIENT_SECRET` nunca em código (usar variáveis)
- [ ] Database password está em variável de ambiente
- [ ] URLs de callback estão corretas no Auth0

---

## 📞 PRÓXIMOS ERROS COMUNS

1. **"Invalid Callback URL"** → Verifique a URL exata no Auth0
2. **"Token inválido"** → Generate novo `AUTH0_SECRET` com `openssl rand -hex 32`
3. **"API não responde"** → Backend não está rodando ou `NEXT_PUBLIC_API_URL` errada
4. **"Roles não aparecem"** → Custom claim não foi deployada no Auth0

---

## ✅ PRONTO!

Sistema está **95% pronto**. O que fazer:

**OPÇÃO 1 (Rápido - Teste local):**
1. Rodar backend: `python -m uvicorn app.main:app --reload`
2. Testar frontend: `npm run dev`
3. Testar criação de cursos

**OPÇÃO 2 (Completo - Com Auth0):**
1. Seguir todos os passos de Auth0 acima
2. Enviar pro GitHub
3. Deploy na Vercel + EC2

Qual quer fazer primeiro?
