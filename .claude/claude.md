# Portfolio - AI Developer

Portfólio profissional de IA construído com FastAPI + Vue.js 3.

## Stack

| Camada | Tecnologias |
|--------|-------------|
| **Backend** | FastAPI, SQLAlchemy, Pydantic, Supabase, Agno |
| **Frontend** | Vue.js 3, Vue Router, PrimeVue, Tailwind CSS |
| **AI/ML** | GPT-5.2, OpenAI Embeddings (text-embedding-3-small), pgvector RAG |
| **DevOps** | Docker, Docker Compose, Nginx |

---

## Estrutura do Projeto

```
portfolio/
├── .claude/
│   ├── CLAUDE.md              # Este arquivo
│   ├── agents/                # Subagentes especializados
│   │   ├── planner/           # Planeja implementações
│   │   ├── executor/          # Executa código
│   │   ├── frontend-reviewer/ # Review Vue.js/UX
│   │   ├── security-reviewer/ # Análise OWASP
│   │   ├── build-tester/      # Testes e build
│   │   └── langfuse-specialist/ # Observabilidade LLM
│   ├── skills/
│   │   └── pipeline/          # Orquestra agents
│   ├── commands/              # Slash commands
│   └── docs/
│       └── workflows/
│           └── pokedex.md     # Docs técnicos Pokédex
├── backend/
│   ├── app/                   # FastAPI app
│   │   ├── main.py            # Entry point
│   │   ├── config.py          # Settings centralizadas
│   │   ├── routers/           # Endpoints
│   │   └── ...
│   └── workflows/             # AI Workflows
│       └── pokedex/           # Chatbot Pokédex (Agno + RAG)
├── frontend/
│   └── src/
│       ├── components/        # Vue components
│       ├── views/             # Pages
│       └── data/portfolio.js  # Dados hardcoded
└── docker-compose.yml
```

---

## Agents e Pipeline

### Pipeline de Implementação

Use `/pipeline` para executar o fluxo completo:

```
Plan → Execute → Frontend Review → Security Review → Build/Test
```

### Agents Disponíveis

| Agent | Quando Usar | O Que Faz |
|-------|-------------|-----------|
| **planner** | Iniciar nova feature | Cria plano de implementação detalhado |
| **executor** | Implementar código | Executa o plano, escreve código |
| **frontend-reviewer** | Mudanças Vue.js | Valida UX, a11y, PrimeVue |
| **security-reviewer** | Qualquer mudança | Checa OWASP, vulnerabilidades |
| **build-tester** | Final da pipeline | Roda testes, build, verifica tudo |
| **langfuse-specialist** | Observabilidade LLM | Langfuse, tracing, custos, troubleshooting |

### Regras dos Agents

**Anti-Alucinação**: Todos os agents seguem:
- Se encontrar problema → **PARA e reporta**
- **NUNCA** auto-corrige sem plano
- Volta ao **Planner** para criar plano de correção

### Como Invocar

```
# Pipeline completa
/pipeline Adicionar feature X

# Agent individual
Use the planner agent to design: [feature]
Use the executor agent to implement: [plan]
Use the frontend-reviewer agent to review: [files]
Use the security-reviewer agent to audit: [files]
Use the build-tester agent to test
```

---

## Projetos/Features

### 1. Pokédex AI Chatbot

**Rota**: `/projects/pokedex`
**Componente**: `PokedexChat.vue`
**Backend**: `backend/workflows/pokedex/`

Chatbot RAG nativo em Python que responde sobre Pokémon Gen 1:
- **Guardrails**: Bloqueia jailbreak e off-topic via keywords + LLM
- **Memory**: Histórico por sessão (Supabase `n8n_chat_histories`)
- **VectorStore**: RAG com pgvector + embeddings OpenAI
- **Agent**: Agno framework + GPT-5.2
- **Observability**: Langfuse (self-hosted) + OpenLIT auto-instrumentation

**Endpoint**: `POST /api/webhook/pokedex`
```json
{
  "pergunta": "Me fale sobre o Pikachu",
  "sessionId": "sess_123"
}
```

📄 Docs detalhados: `.claude/docs/workflows/pokedex.md`

### 2. AI Newsletter

**Rota**: `/projects/lastfm-insights`
**Componente**: `LastfmInsightsProject.vue`

Dashboard interativo com integração Supabase:
- Seletor de data
- Top 10 ranking de músicas
- Dados via Supabase REST

**Endpoint**: `GET /lastfm/ranking/{date}`

### 3. Dialogflow Assistant

**Componente**: `DialogflowChat.vue`
**Agent ID**: `7bf77edb-587b-4b28-8f40-67b544d24e95`

Widget de chat integrado direto com Google Cloud Dialogflow CX.

---

## Endpoints Principais

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/health` | GET | Health check |
| `/api/profile` | GET/POST/PUT | Perfil |
| `/api/projects` | CRUD | Projetos |
| `/api/experiences` | CRUD | Experiências |
| `/api/webhook/pokedex` | POST | Chatbot Pokédex |
| `/lastfm/ranking/{date}` | GET | Top músicas |

---

## Variáveis de Ambiente

```env
# Database
DATABASE_URL=sqlite:///./portfolio.db

# Supabase - Last.fm / Newsletter
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...

# Supabase - Pokédex (RAG + Memory)
SUPABASE_POKEDEX_URL=https://xxx.supabase.co
SUPABASE_POKEDEX_KEY=eyJ...

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-5.2

# Langfuse (opcional - observabilidade LLM)
LANGFUSE_ENABLED=false
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_BASE_URL=https://langfuse.seu-dominio.com
```

---

## Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `/pipeline` | Executa pipeline completa de implementação |
| `/security-review` | Análise de segurança OWASP |
| `/frontend-review` | Review Vue.js/UX/a11y |
| `/architecture-review` | Análise de arquitetura |
| `/code-review` | Review geral de código |

---

## Desenvolvimento

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev  # porta 3000
```

### Docker
```bash
# Produção
docker-compose up --build

# Dev (backend apenas)
docker-compose -f docker-compose.dev.yml up backend
```

---

## Padrões de Código

### Backend (Python)
- Use async/await para I/O
- Pydantic para validação
- SQLAlchemy 2.0 syntax
- Type hints sempre

### Frontend (Vue.js)
- Composition API (`<script setup>`)
- PrimeVue components
- Tailwind CSS utilities
- Dados em `portfolio.js`

---

## Produção e CDN

> ⚠️ **O site fica atrás do Cloudflare.** Nada no código revela isso — nem o
> `docker-compose`, nem o `nginx.conf`, nem os docs de deploy. É a primeira
> coisa a considerar quando "a mudança não aparece em produção".

| | |
|---|---|
| **URL de produção** | https://portfolio.ikehara.dev.br |
| **Hospedagem** | EasyPanel (Docker Swarm) em VPS Hostinger |
| **CDN** | Cloudflare, na frente de tudo |

### Regra: trocar arquivo de `public/` exige purge

Arquivos em `frontend/public/` (`favicon.svg`, `images/*`) mantêm o **mesmo nome**
entre deploys. A saída do Vite em `dist/assets/` tem hash no nome e se resolve
sozinha; esses não.

Se você **substituir** um arquivo de `public/` mantendo o nome, o Cloudflare
continua servindo a versão antiga da borda até o TTL expirar. Deploy correto,
container correto, e mesmo assim o mundo inteiro vê o arquivo velho.

**Depois do deploy:** Cloudflare → domínio `ikehara.dev.br` → **Caching** →
**Configuration** → **Purge Cache** → *Custom Purge* com a URL do arquivo.

Arquivo **novo** (nome inédito) aparece na hora e não precisa de purge.

### Diagnóstico: é cache de CDN?

Compare a URL normal com uma que tenha query string. A query cria outra chave de
cache no Cloudflare, então força a ida até a origem:

```bash
curl -sI https://portfolio.ikehara.dev.br/favicon.svg            | grep -iE 'cf-cache-status|age:|content-length'
curl -sI "https://portfolio.ikehara.dev.br/favicon.svg?bust=123" | grep -iE 'cf-cache-status|age:|content-length'
```

`HIT` na primeira e `MISS` na segunda, com tamanhos diferentes, significa
Cloudflare servindo cópia velha. Se as duas forem idênticas, o problema está no
container ou no build — aí vale inspecionar o que está servido de fato:

```bash
C=$(docker ps --format '{{.Names}}' | grep -i front)
docker exec "$C" cat /usr/share/nginx/html/favicon.svg
```

> Histórico: em ago/2026 o `nginx.conf` mandava `Cache-Control: immutable` com
> TTL de 1 ano para todo SVG. O Cloudflare obedeceu e fixou o favicon por um ano.
> O `nginx.conf` foi corrigido — `immutable` agora só vale para `/assets/`, que
> tem hash no nome —, mas objetos já fixados na borda só saem com purge manual.

---

## Notas Importantes

1. **Dados hardcoded**: `frontend/src/data/portfolio.js` contém projetos/experiências
2. **Imagens**: `frontend/public/images/`
3. **Portas**: Backend 8000, Frontend 3000 (dev) / 80 (prod)
4. **Git**: Nunca commitar `.env`, já está no `.gitignore`
5. **Embedding model**: Usa `text-embedding-3-small` (compatível com vectorstore Supabase)
6. **Cloudflare**: trocar arquivo de `public/` mantendo o nome exige purge manual — ver "Produção e CDN"
7. **Favicon/Logo**: o "V" é um `<path>`, não `<text>`. Favicon SVG é rasterizado num contexto isolado, sem garantia de fonte, e `<text>` sai em branco. Manter `favicon.svg` e `Logo.vue` com o mesmo `d`.
8. **Design tokens**: `style.css` define tokens semânticos (`--bg-card`, `--text-heading`…) trocados por `data-theme`. `Home.vue`, `Navbar.vue` e `ProjectCarousel.vue` usam; as 5 telas de projeto ainda têm hex fixo e **não acompanham o modo claro**.
