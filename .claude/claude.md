# Portfolio - AI Developer

Portfólio profissional para desenvolvedores de IA, construído com FastAPI (backend) e Vue.js 3 (frontend).

**Branch Atual**: `feature/dialogflow-assistant-and-logo`
**Branch Principal**: `claude/ai-portfolio-app-01Kij1A8uWTMbnHKtFE5s1Eh`

---

## Visão Geral do Projeto

Aplicação full-stack que apresenta o portfólio de um desenvolvedor de IA, incluindo perfil profissional, experiências e projetos interativos de IA. Integra múltiplas tecnologias: n8n webhooks, Dialogflow CX, Last.fm API via Supabase, e chatbots RAG com vector search.

---

## Estrutura do Projeto

```
portfolio/
├── .claude/
│   ├── CLAUDE.md                      # Documentação completa do projeto
│   └── commands/                      # Comandos slash personalizados
│       ├── architecture-review.md     # Review de arquitetura
│       ├── code-review.md             # Review geral de código
│       ├── frontend-review.md         # Review especializado Vue.js
│       └── security-review.md         # Análise de segurança
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app principal
│   │   ├── config.py                  # Configurações (Pydantic)
│   │   ├── database.py                # SQLAlchemy setup
│   │   ├── models.py                  # Modelos SQLAlchemy
│   │   ├── schemas.py                 # Schemas Pydantic
│   │   ├── schemas_lastfm.py          # Schemas Last.fm
│   │   ├── middleware.py              # Rate limiting
│   │   ├── supabase_client.py         # Cliente Supabase
│   │   └── routers/
│   │       ├── projects.py            # CRUD de projetos
│   │       ├── experiences.py         # CRUD de experiências
│   │       ├── profile.py             # Gestão de perfil
│   │       ├── webhook_proxy.py       # Proxy para n8n
│   │       └── lastfm.py              # Endpoints Last.fm
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   │   ├── config.js                  # Runtime config (API URL)
│   │   ├── profile-placeholder.svg    # Avatar fallback
│   │   └── images/
│   │       ├── dialogflow.jpg         # Capa projeto Dialogflow
│   │       ├── lastfm-insights.jpg    # Capa antiga Last.fm
│   │       └── music-project-cover.jpg # Nova capa Last.fm
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── Navbar.vue             # Navegação principal
│   │   │   ├── Logo.vue               # Logo customizado
│   │   │   ├── ProjectCard.vue        # Card de projeto
│   │   │   ├── ExperienceCard.vue     # Card de experiência
│   │   │   ├── DialogflowChat.vue     # Assistente Dialogflow
│   │   │   └── PokedexChat.vue        # Chat Pokédex
│   │   ├── views/
│   │   │   ├── Home.vue               # Página principal
│   │   │   ├── ProjectDetail.vue      # Detalhe projeto Pokédex
│   │   │   └── LastfmInsightsProject.vue # Analytics Last.fm
│   │   ├── services/
│   │   │   └── api.js                 # Cliente Axios
│   │   ├── data/
│   │   │   └── portfolio.js           # Dados hardcoded
│   │   ├── router/
│   │   │   └── index.js               # Vue Router config
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── Dockerfile                     # Produção (multi-stage)
│   ├── Dockerfile.dev                 # Desenvolvimento
│   ├── nginx.conf                     # Config nginx produção
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
├── docker-compose.yml                 # Orquestração produção
├── docker-compose.dev.yml             # Orquestração dev
└── [outros arquivos de deploy]
```

---

## Tecnologias Utilizadas

### Backend
- **FastAPI 0.104.1**: Framework web assíncrono
- **SQLAlchemy 2.0.23**: ORM para banco de dados
- **SQLite**: Banco padrão (suporta PostgreSQL)
- **Pydantic 2.5.0**: Validação de dados
- **Pydantic-Settings 2.1.0**: Gerenciamento de configuração
- **Uvicorn**: Servidor ASGI
- **SlowAPI**: Rate limiting (60 req/min)
- **HTTPX**: Cliente HTTP assíncrono
- **Supabase 2.10.0**: Cliente PostgreSQL/REST

### Frontend
- **Vue.js 3.3.8**: Framework JavaScript (Composition API)
- **Vue Router 4.2.5**: Roteamento SPA
- **Pinia 2.1.7**: State management
- **PrimeVue 4.4.1**: Biblioteca de componentes UI
- **PrimeIcons 7.0.0**: Ícones
- **Tailwind CSS 3.3.6**: Framework CSS utilitário
- **Axios 1.6.2**: Cliente HTTP
- **Vite 5.0.4**: Build tool e dev server

### DevOps
- **Docker**: Containerização
- **Docker Compose**: Orquestração
- **Nginx Alpine**: Servidor web produção

---

## Arquitetura Backend

### FastAPI Application (main.py)

**Routers Registrados:**
1. `/api/projects` - CRUD de projetos
2. `/api/experiences` - CRUD de experiências
3. `/api/profile` - Gerenciamento de perfil
4. `/api/webhook` - Proxy para n8n (CORS bypass)
5. `/lastfm` - Endpoints analytics Last.fm

**Middlewares:**
- Security Headers (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, HSTS)
- CORS (origens configuráveis via env)
- GZip Compression (>1KB)
- Rate Limiting (60 req/min por IP)

**Endpoints Principais:**
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - Swagger UI (desabilitado em produção)

### Modelos de Dados (models.py)

#### Profile
```python
id: Integer (PK)
name: String(100)
title: String(100)
bio: Text
email: String(100)
phone: String(20)
location: String(100)
avatar_url: String(500)
social_links: JSON  # {"GitHub": "url", "LinkedIn": "url"}
skills: JSON        # ["skill1", "skill2", ...]
```

#### Project
```python
id: Integer (PK)
title: String(100)
description: Text
technologies: JSON      # ["tech1", "tech2", ...]
image_url: String(500)
project_url: String(500)
github_url: String(500)
order: Integer
created_at: DateTime
```

#### Experience
```python
id: Integer (PK)
company: String(100)
position: String(100)
description: Text
technologies: JSON  # ["tech1", "tech2", ...]
start_date: Date
end_date: Date (nullable)
current: Boolean
order: Integer
```

### Routers Detalhados

#### 1. projects.py (`/api/projects`)
- `GET /` - Lista projetos (skip, limit)
- `GET /{id}` - Busca por ID
- `POST /` - Cria projeto
- `PUT /{id}` - Atualiza projeto
- `DELETE /{id}` - Remove projeto

#### 2. experiences.py (`/api/experiences`)
- `GET /` - Lista experiências (skip, limit)
- `GET /{id}` - Busca por ID
- `POST /` - Cria experiência
- `PUT /{id}` - Atualiza experiência
- `DELETE /{id}` - Remove experiência

#### 3. profile.py (`/api/profile`)
- `GET /` - Retorna perfil único
- `POST /` - Cria perfil (apenas se não existir)
- `PUT /` - Atualiza perfil

#### 4. webhook_proxy.py (`/api/webhook`)
- `POST /pokedex` - Proxy para n8n
  - URL destino: `https://n8n.ikehara.dev.br/webhook/pokedex`
  - Timeout: 60 segundos
  - Payload: `{"pergunta": str, "sessionId": str}`
  - Tratamento de erros: ConnectionError, Timeout

#### 5. lastfm.py (`/lastfm`)
- `GET /ranking/{data}` - Top 10 músicas por data (YYYY-MM-DD)
  - Consulta Supabase: tabelas `rankings_diarios` + `musicas`
  - Retorna: posição, play_count, track details
  - Schemas: `RankingComMusica`, `TopMusicasResponse`

### Configuração (config.py)

```python
class Settings(BaseSettings):
    # App
    app_name: str = "Portfolio API"
    app_version: str = "1.0.0"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./portfolio.db"

    # Security
    secret_key: str = "change-this-in-production"
    cors_origins: list = ["http://localhost:3000"]

    # Rate Limiting
    rate_limit_per_minute: int = 60

    # Supabase
    supabase_url: str
    supabase_key: str
```

### Supabase Integration (supabase_client.py)

```python
# Singleton pattern
supabase_client = create_client(settings.supabase_url, settings.supabase_key)

def get_supabase() -> Client:
    return supabase_client
```

**Tabelas Supabase:**
- `rankings_diarios`: id, data, musica_id, posicao, play_count
- `musicas`: id, nome, artista, album, duracao_ms, spotify_id, preview_url, imagem_url, generos

---

## Arquitetura Frontend

### Vue Router (router/index.js)

**Rotas Definidas:**
```javascript
'/' → Home.vue                              // Página principal
'/projects/pokedex' → ProjectDetail.vue     // Pokédex AI Agent
'/projects/lastfm-insights' → LastfmInsightsProject.vue  // Last.fm Analytics
```

**Configurações:**
- History mode
- Scroll behavior: suave em hashes, topo em mudanças de rota

### Componentes

#### 1. Navbar.vue
- Menu sticky com logo customizado
- Links: About, Experience, Projects, Contact
- Menu mobile responsivo (hamburger)
- Scroll suave para seções

#### 2. Logo.vue
- SVG customizado (letra "V")
- Gradiente azul (#0284c7 → #38bdf8)
- Tema tech: linhas de acento, pontos de circuito
- Prop: `size` (padrão: 40)

#### 3. ProjectCard.vue
**Capas Condicionais:**
- **Pokedex**: Gradiente vermelho com pokéball
- **Last.fm**: Gradiente azul com barras de música + waveform
- **FAQ Bot**: Gradiente verde com ícones de chat
- **Default**: Gradiente azul com ícone de código

**Recursos:**
- Badges de tecnologias
- Botões "Try it Now" para projetos interativos
- Links externos e GitHub
- Manipulação shadow DOM para abrir Dialogflow

#### 4. ExperienceCard.vue
- Layout: empresa (esquerda) + detalhes (direita)
- Badge "Current" para posições ativas
- Formatação de datas (MMM YYYY)
- Descrições expansíveis (>200 chars)
- Tags de tecnologias

#### 5. DialogflowChat.vue
- Web Component: `<df-messenger>`
- Agent ID: `7bf77edb-587b-4b28-8f40-67b544d24e95`
- Título: "Assistente Virtual"
- Script: https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js
- Custom chat bubble icon (SVG)

#### 6. PokedexChat.vue
- Interface estilo Pokédex físico
- Elementos: câmera, LEDs (red/yellow/green), tela, controles
- Chat funcional com histórico
- Session tracking para webhook n8n
- Mensagens de boas-vindas com exemplos
- Loading spinner
- Endpoint: `${API_URL}/api/webhook/pokedex`
- Auto-scroll para última mensagem

### Views

#### 1. Home.vue
**Seções:**
1. **Hero**: Avatar, nome, título, bio, badge "Available for Projects"
2. **Skills**: Badges interativos
3. **Social Links**: GitHub, LinkedIn
4. **Experience**: Timeline com ExperienceCard
5. **Projects**: Grid com ProjectCard
6. **Contact**: (seção de contato)
7. **Footer**

#### 2. ProjectDetail.vue (Pokédex)
**Estrutura:**
- Header com botão voltar
- Título + descrição + tecnologias
- Seção "Live Demo" com PokedexChat
- Seção "How it Works" (3 passos):
  1. Pergunta do usuário
  2. RAG Search (PostgreSQL vector database)
  3. AI Response (GPT-4o mini)

#### 3. LastfmInsightsProject.vue
**Recursos:**
- Header com botão voltar
- Seletor de data (calendar)
- Cards de resumo (data, total tracks, unique artists)
- Top 10 ranking:
  - Badges de posição (color-coded)
  - Nome da música + artista
  - Play count
- Estados: loading, error, data
- Endpoint: `/lastfm/ranking/{date}`
- Formatação de data

### Serviços

#### api.js
```javascript
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000'
});

export const profileApi = {
  get: () => api.get('/api/profile'),
  create: (data) => api.post('/api/profile', data),
  update: (data) => api.put('/api/profile', data)
};

export const projectsApi = {
  getAll: () => api.get('/api/projects'),
  getById: (id) => api.get(`/api/projects/${id}`),
  create: (data) => api.post('/api/projects', data),
  update: (id, data) => api.put(`/api/projects/${id}`, data),
  delete: (id) => api.delete(`/api/projects/${id}`)
};

export const experiencesApi = {
  // mesma estrutura
};
```

### Dados Hardcoded (data/portfolio.js)

**Profile:**
- Nome: Vinicius Ikehara
- Título: AI Developer
- Email: vhikehara@gmail.com
- Skills: n8n, AI, LLM, Prompt Engineering, RAG, SQL, Vector Search
- Social: GitHub, LinkedIn

**Experiences (3):**
1. AI Developer @ domy (2025-08 - presente)
2. Data Analyst & AI @ HSystem (2024-05 - 2025-08)
3. Junior Data Analyst @ Banco Daycoval (2023-01 - 2024-05)

**Projects (3):**
1. **Pokédex AI Agent** (slug: `pokedex`, interactive: true)
2. **Dialogflow Virtual Assistant** (slug: `dialogflow-assistant`, interactive: true, special: "open-chat")
3. **Last.fm Music Insights** (slug: `lastfm-insights`, interactive: true, image: `/images/music-project-cover.jpg`)

---

## Fluxo de Dados

### 1. Home Page Load
- Vue renderiza dados hardcoded de `portfolio.js`
- (Opcional) Pode chamar `/api/profile` para dados dinâmicos

### 2. Pokédex Chat
1. Usuário digita pergunta em `PokedexChat.vue`
2. Frontend → `POST /api/webhook/pokedex` (backend)
3. Backend → `POST https://n8n.ikehara.dev.br/webhook/pokedex`
4. n8n → RAG + GPT-4o mini → resposta
5. Backend → Frontend → Exibição no chat

### 3. Dialogflow Assistant
1. Web Component `<df-messenger>` carrega script Google
2. Comunicação direta Google Cloud ↔ Dialogflow CX
3. Não usa backend deste projeto

### 4. Last.fm Rankings
1. Usuário seleciona data em `LastfmInsightsProject.vue`
2. Frontend → `GET /lastfm/ranking/{date}` (backend)
3. Backend → Supabase query em `rankings_diarios` + `musicas`
4. Backend → Frontend (JSON com top 10)
5. Frontend renderiza cards de ranking

---

## Integrações de Terceiros

### 1. Dialogflow CX (Google Cloud)
- **Agent ID**: `7bf77edb-587b-4b28-8f40-67b544d24e95`
- **Tipo**: Web Component
- **Propósito**: Assistente virtual para responder sobre o portfólio

### 2. n8n Webhook
- **URL**: https://n8n.ikehara.dev.br/webhook/pokedex
- **Propósito**: Chatbot Pokédex com RAG (vector search PostgreSQL + GPT-4o mini)
- **Proxy Backend**: Resolve problemas de CORS

### 3. Supabase (PostgreSQL)
- **Tabelas**: `rankings_diarios`, `musicas`
- **Propósito**: Armazenamento de dados Last.fm
- **Auth**: `SUPABASE_URL` + `SUPABASE_KEY`

### 4. Last.fm API
- **Implementação**: Dados coletados previamente no Supabase
- **Acesso**: Via endpoint `/lastfm/ranking/{date}`

### 5. PrimeVue
- **Componentes usados**: Avatar, Badge, Button, Card, Chip, Image, InlineMessage, MenuBar, ProgressSpinner, Tag, Timeline
- **Ícones**: PrimeIcons (`pi pi-*`)

---

## Docker & Deployment

### Produção (docker-compose.yml)

```yaml
services:
  backend:
    image: python:3.11-slim
    ports: ["8000:8000"]
    volumes: ["./backend/portfolio.db:/app/portfolio.db"]
    environment:
      DEBUG: "False"
    healthcheck: CMD curl --fail http://localhost:8000/health

  frontend:
    build: multi-stage (node:18-alpine → nginx:alpine)
    ports: ["80:80"]
    depends_on: backend
```

### Desenvolvimento (docker-compose.dev.yml)

```yaml
services:
  backend:
    environment:
      DEBUG: "True"
    env_file: .env

  frontend:
    image: node:18-alpine
    ports: ["3000:3000"]
    command: npm run dev
    stdin_open: true
    tty: true
```

### Dockerfiles

**backend/Dockerfile:**
- Base: `python:3.11-slim`
- Instala requirements.txt
- Comando: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

**frontend/Dockerfile (produção):**
- Stage 1: `node:18-alpine` (build)
- Stage 2: `nginx:alpine` (serve)
- Copia dist/ para nginx
- Configuração nginx customizada

**frontend/Dockerfile.dev:**
- Base: `node:18-alpine`
- Comando: `npm run dev -- --host 0.0.0.0`

---

## Configuração de Ambiente

### Backend (.env)

```env
# Database
DATABASE_URL=sqlite:///./portfolio.db

# Debug
DEBUG=False

# Security
SECRET_KEY=your-secret-key-change-in-production
CORS_ORIGINS=["http://localhost:3000","https://seu-dominio.com"]

# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-publica-anon
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

**Nota**: Em produção, usar `docker-entrypoint.sh` para substituir variáveis em runtime via `window.APP_CONFIG`.

---

## Comandos de Desenvolvimento

### Backend
```bash
cd backend
pip install -r requirements.txt

# Desenvolvimento local (requer Python no PATH)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Ou via Docker
docker-compose -f docker-compose.dev.yml up backend
```

### Frontend
```bash
cd frontend
npm install

# Desenvolvimento
npm run dev        # http://localhost:3000

# Build
npm run build      # Output: dist/

# Preview do build
npm run preview
```

### Docker Compose
```bash
# Produção
docker-compose up --build

# Desenvolvimento
docker-compose -f docker-compose.dev.yml up --build

# Apenas backend
docker-compose up backend

# Apenas frontend
docker-compose up frontend
```

---

## Segurança

### Headers HTTP (Backend)
```python
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### CORS
- Configurável via `CORS_ORIGINS` no `.env`
- Suporta múltiplas origens

### Rate Limiting
- **Limite**: 60 requisições/minuto por IP
- **Biblioteca**: SlowAPI

### Validação de Dados
- **Pydantic Schemas**: Validação automática de inputs
- **SQLAlchemy**: Proteção contra SQL injection

---

## Mudanças Recentes (Branch Atual)

### Arquivos Novos (Untracked)
- `backend/app/routers/lastfm.py` - Integração Last.fm
- `backend/app/schemas_lastfm.py` - Schemas música
- `backend/app/supabase_client.py` - Cliente Supabase
- `docker-compose.dev.yml` - Ambiente dev
- `frontend/Dockerfile.dev` - Container dev frontend
- `frontend/public/images/music-project-cover.jpg` - Capa Last.fm (ATUAL)
- `frontend/public/images/lastfm-insights.jpg` - Capa antiga
- `frontend/src/views/LastfmInsightsProject.vue` - Página analytics

### Arquivos Modificados
- `backend/.env.example` - Adicionado Supabase
- `backend/app/config.py` - Config Supabase
- `backend/app/main.py` - Router lastfm registrado
- `backend/requirements.txt` - Dependência supabase
- `frontend/src/components/ProjectCard.vue` - Estilo Last.fm
- `frontend/src/data/portfolio.js` - Projetos Last.fm + Dialogflow
- `frontend/src/router/index.js` - Rota LastfmInsightsProject

### Commits Recentes
1. `6c35b3e` - Add Dialogflow Virtual Assistant project
2. `ddbab7c` - Update chat title to 'Assistente Virtual'
3. `85c866b` - Add Dialogflow assistant widget and new brand logo
4. `7e871f2` - Use correct n8n webhook domain

---

## Comandos Slash Disponíveis

- `/security-review` - Análise OWASP (XSS, SQL Injection, CORS, etc.)
- `/frontend-review` - Review Vue.js, CSS, UX, acessibilidade
- `/architecture-review` - Análise de arquitetura e design patterns
- `/code-review` - Review geral Python + JavaScript

---

## Considerações de Deploy

### Variáveis Obrigatórias em Produção
```env
# Backend
SECRET_KEY=produção-secret-alterar
CORS_ORIGINS=["https://seu-dominio.com"]
SUPABASE_URL=https://projeto.supabase.co
SUPABASE_KEY=chave-publica

# Frontend
VITE_API_URL=https://api.seu-dominio.com
```

### Database
- **SQLite**: OK para portfolio single-user
- **PostgreSQL**: Recomendado para escala
- **Connection String**: `DATABASE_URL`

### Frontend Build
- `npm run build` → `dist/`
- Nginx serve arquivos estáticos
- SPA routing configurado

### HTTPS
- **Obrigatório** em produção para HSTS
- Configure certificado SSL no proxy reverso

---

## Notas Importantes para Claude

### 1. Estrutura de Dados
- **Portfolio data** está HARDCODED em `frontend/src/data/portfolio.js`
- API REST serve dados SQLite (não usado atualmente no frontend)
- Para atualizar projetos/experiências: editar `portfolio.js`

### 2. Imagens de Projetos
- **Diretório**: `frontend/public/images/`
- **Referência**: `/images/nome-do-arquivo.jpg` (no portfolio.js)
- **Capa Last.fm Atual**: `music-project-cover.jpg`

### 3. Ambientes
- **Dev Frontend**: Porta 3000 (Vite)
- **Dev Backend**: Porta 8000 (Uvicorn)
- **Produção**: Frontend porta 80 (Nginx), Backend porta 8000

### 4. Python no Git Bash
- Python **NÃO** está disponível no Git Bash Windows
- Para rodar backend localmente: usar PowerShell/CMD com Python instalado
- Ou usar Docker Compose

### 5. Projetos Interativos
- **Pokédex**: Rota `/projects/pokedex`, componente PokedexChat
- **Dialogflow**: Especial handling "open-chat", shadow DOM manipulation
- **Last.fm**: Rota `/projects/lastfm-insights`, componente LastfmInsightsProject

### 6. Integrações Externas
- **n8n**: Webhook proxy via backend (CORS bypass)
- **Dialogflow**: Direct Google Cloud (sem backend)
- **Supabase**: Backend consulta para Last.fm data

### 7. Build Process
- **Frontend**: Multi-stage Dockerfile (build → serve)
- **Backend**: Single-stage Dockerfile (Python slim)
- **Dev**: Hot reload habilitado (Vite + Uvicorn --reload)

---

## Próximos Passos Sugeridos

1. Migrar dados hardcoded para API dinâmica
2. Adicionar autenticação no painel admin
3. Implementar upload de imagens
4. Adicionar testes automatizados
5. Configurar CI/CD pipeline
6. Monitoramento e logs centralizados
7. Otimização de performance (CDN para imagens)
8. SEO e meta tags dinâmicos
