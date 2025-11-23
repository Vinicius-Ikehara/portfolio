# Portfolio - AI Developer

Portfólio profissional para desenvolvedores de IA, construído com FastAPI (backend) e Vue.js 3 (frontend).

## Estrutura do Projeto

```
portfolio/
├── .claude/
│   ├── claude.md                 # Este arquivo (documentação do projeto)
│   └── commands/                 # Comandos slash personalizados
│       ├── architecture-review.md
│       ├── code-review.md
│       ├── frontend-review.md
│       └── security-review.md
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Aplicação FastAPI principal
│   │   ├── config.py            # Configurações (pydantic-settings)
│   │   ├── database.py          # Configuração SQLAlchemy
│   │   ├── models.py            # Modelos do banco (Project, Experience, Profile)
│   │   ├── schemas.py           # Schemas Pydantic para validação
│   │   ├── middleware.py        # Middlewares customizados
│   │   └── routers/
│   │       ├── projects.py      # CRUD de projetos
│   │       ├── experiences.py   # CRUD de experiências
│   │       └── profile.py       # Gestão de perfil
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   ├── config.js            # Configuração runtime (API URL)
│   │   └── profile-placeholder.svg  # Imagem fallback do avatar
│   ├── src/
│   │   ├── assets/              # Assets estáticos
│   │   ├── components/
│   │   │   ├── Navbar.vue       # Navegação principal
│   │   │   ├── ProjectCard.vue  # Card de projeto
│   │   │   └── ExperienceCard.vue  # Card de experiência
│   │   ├── views/
│   │   │   ├── Home.vue         # Página pública do portfólio
│   │   │   └── Admin.vue        # Painel administrativo
│   │   ├── services/
│   │   │   └── api.js           # Cliente Axios para API
│   │   ├── router/
│   │   │   └── index.js         # Configuração Vue Router
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css            # Estilos globais
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
├── docker-compose.yml           # Orquestração de containers
├── easypanel-template.yml       # Template para Easypanel
├── README.md
├── QUICK_START.md
├── DEPLOY_EASYPANEL.md
├── DEPLOY_GITHUB_DESKTOP.md
└── DEPLOY_SEM_DOCKER.md
```

## Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e rápido para APIs
- **SQLAlchemy**: ORM para banco de dados
- **SQLite**: Banco de dados padrão (pode migrar para PostgreSQL)
- **Pydantic**: Validação de dados com pydantic-settings
- **Uvicorn**: Servidor ASGI para produção

### Frontend
- **Vue.js 3**: Framework JavaScript com Composition API
- **Vue Router 4**: Roteamento SPA
- **Pinia**: Gerenciamento de estado
- **Tailwind CSS 3**: Framework CSS utilitário
- **Axios**: Cliente HTTP
- **Vite 5**: Build tool e dev server

### DevOps
- **Docker**: Containerização
- **Docker Compose**: Orquestração local
- **Easypanel**: Deploy em produção (opcional)
- **Nginx**: Servidor web para frontend em produção

## Funcionalidades

1. **Página Pública (Home.vue)**
   - Seção Hero com avatar (fallback automático se imagem não carregar)
   - Lista de skills como badges
   - Links sociais (GitHub, LinkedIn, etc.)
   - Timeline de experiências profissionais
   - Grid de projetos
   - Seção de contato
   - Footer

2. **Painel Administrativo (Admin.vue)**
   - CRUD completo de perfil
   - CRUD de projetos (título, descrição, tecnologias, URLs)
   - CRUD de experiências (empresa, cargo, datas, descrição)
   - Interface responsiva

3. **API REST (Backend)**
   - Endpoints: `/profile`, `/projects`, `/experiences`
   - Validação de dados com Pydantic
   - CORS configurável
   - Headers de segurança (X-Content-Type-Options, X-Frame-Options, etc.)
   - Compressão GZip
   - Health check em `/health`

## Modelos de Dados

### Profile
- name, title, bio
- email, phone, location
- avatar_url (URL da imagem de perfil)
- social_links (JSON: github, linkedin, etc.)
- skills (JSON array)

### Project
- title, description
- technologies (JSON array)
- image_url, project_url, github_url
- order (para ordenação)

### Experience
- company, position, description
- technologies (JSON array)
- start_date, end_date
- current (boolean)
- order (para ordenação)

## Comandos de Desenvolvimento

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev      # Desenvolvimento
npm run build    # Build para produção
npm run preview  # Preview do build
```

### Docker
```bash
# Build e run completo
docker-compose up --build

# Apenas backend
docker-compose up backend

# Apenas frontend
docker-compose up frontend
```

## Subagentes Especializados

Use os comandos slash para análises especializadas:

- `/security-review`: Análise de segurança OWASP (XSS, SQL Injection, CORS, etc.)
- `/frontend-review`: Revisão de código Vue.js, CSS, UX, acessibilidade
- `/architecture-review`: Análise da arquitetura e design patterns
- `/code-review`: Revisão geral de código Python e JavaScript

## Configuração de Ambiente

### Variáveis de Ambiente (Backend)
```env
DATABASE_URL=sqlite:///./portfolio.db
DEBUG=False
CORS_ORIGINS=["http://localhost:3000","https://seu-dominio.com"]
SECRET_KEY=your-secret-key-change-this
```

### Configuração Runtime (Frontend)
Edite `frontend/public/config.js`:
```javascript
window.APP_CONFIG = {
  API_URL: 'http://localhost:8000'
}
```

## Boas Práticas

1. **Segurança**: Validar inputs, HTTPS em produção, headers de segurança
2. **Performance**: Lazy loading, compressão GZip, otimização de imagens
3. **UX**: Design responsivo mobile-first, feedback visual, estados de loading
4. **Manutenibilidade**: Componentes reutilizáveis, separação de responsabilidades
5. **Acessibilidade**: Semântica HTML, contraste de cores, navegação por teclado
