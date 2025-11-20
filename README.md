# Portfolio - AI Developer

Um portfólio profissional moderno e completo para desenvolvedores de IA, construído com FastAPI e Vue.js.

## Funcionalidades

- Gestão completa de perfil profissional
- CRUD de projetos com tecnologias, imagens e links
- Timeline de experiências profissionais
- Painel administrativo intuitivo
- Design responsivo e moderno
- API REST documentada com OpenAPI/Swagger
- Segurança implementada (CORS, Rate Limiting, Headers de Segurança)

## Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e de alta performance
- **SQLAlchemy** - ORM Python
- **SQLite** - Banco de dados (fácil migração para PostgreSQL)
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI

### Frontend
- **Vue.js 3** - Framework JavaScript progressivo
- **Vue Router** - Gerenciamento de rotas
- **Pinia** - Gerenciamento de estado
- **Tailwind CSS** - Framework CSS utilitário
- **Axios** - Cliente HTTP
- **Vite** - Build tool

## Estrutura do Projeto

```
portfolio/
├── backend/                    # API FastAPI
│   ├── app/
│   │   ├── main.py            # Aplicação principal
│   │   ├── config.py          # Configurações
│   │   ├── models.py          # Modelos do banco de dados
│   │   ├── schemas.py         # Schemas Pydantic
│   │   ├── database.py        # Configuração do banco
│   │   ├── middleware.py      # Middlewares (rate limiting)
│   │   └── routers/           # Endpoints da API
│   │       ├── projects.py
│   │       ├── experiences.py
│   │       └── profile.py
│   ├── requirements.txt       # Dependências Python
│   └── .env.example          # Exemplo de variáveis de ambiente
│
├── frontend/                  # Aplicação Vue.js
│   ├── src/
│   │   ├── components/       # Componentes reutilizáveis
│   │   │   ├── Navbar.vue
│   │   │   ├── ProjectCard.vue
│   │   │   └── ExperienceCard.vue
│   │   ├── views/            # Páginas
│   │   │   ├── Home.vue      # Página pública
│   │   │   └── Admin.vue     # Painel administrativo
│   │   ├── services/         # Serviços de API
│   │   │   └── api.js
│   │   ├── router/           # Configuração de rotas
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json          # Dependências Node
│   └── vite.config.js        # Configuração do Vite
│
└── .claude/                   # Subagentes especializados Claude
    ├── claude.md
    └── commands/
        ├── security-review.md
        ├── frontend-review.md
        ├── architecture-review.md
        └── code-review.md
```

## Instalação

### Pré-requisitos

- Python 3.8+
- Node.js 16+
- npm ou yarn

### Backend

1. Navegue até o diretório do backend:
```bash
cd backend
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` baseado no `.env.example`:
```bash
cp .env.example .env
```

5. Inicie o servidor:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O backend estará disponível em `http://localhost:8000`
- Documentação Swagger: `http://localhost:8000/docs`
- Documentação ReDoc: `http://localhost:8000/redoc`

### Frontend

1. Navegue até o diretório do frontend:
```bash
cd frontend
```

2. Instale as dependências:
```bash
npm install
```

3. Inicie o servidor de desenvolvimento:
```bash
npm run dev
```

O frontend estará disponível em `http://localhost:3000` (ou outra porta indicada)

## Uso

### Primeira Configuração

1. Acesse `http://localhost:3000/admin`
2. Configure seu perfil na aba "Perfil"
3. Adicione seus projetos na aba "Projetos"
4. Adicione suas experiências na aba "Experiências"
5. Visualize seu portfólio em `http://localhost:3000`

### API Endpoints

**Perfil**
- `GET /api/profile` - Obter perfil
- `POST /api/profile` - Criar perfil
- `PUT /api/profile` - Atualizar perfil

**Projetos**
- `GET /api/projects` - Listar todos os projetos
- `GET /api/projects/{id}` - Obter projeto específico
- `POST /api/projects` - Criar novo projeto
- `PUT /api/projects/{id}` - Atualizar projeto
- `DELETE /api/projects/{id}` - Deletar projeto

**Experiências**
- `GET /api/experiences` - Listar todas as experiências
- `GET /api/experiences/{id}` - Obter experiência específica
- `POST /api/experiences` - Criar nova experiência
- `PUT /api/experiences/{id}` - Atualizar experiência
- `DELETE /api/experiences/{id}` - Deletar experiência

## Desenvolvimento

### Backend

Execute testes (quando implementados):
```bash
pytest
```

Verifique o código com linters:
```bash
flake8 app/
black app/
mypy app/
```

### Frontend

Build para produção:
```bash
npm run build
```

Preview da build de produção:
```bash
npm run preview
```

## Subagentes Claude

Este projeto inclui subagentes especializados para revisão e análise:

### Uso dos Subagentes

```bash
# Análise de segurança
/security-review

# Revisão de código frontend
/frontend-review

# Análise de arquitetura
/architecture-review

# Revisão geral de código
/code-review
```

## Deploy

### Backend (Railway/Render/Heroku)

1. Configure as variáveis de ambiente:
   - `DATABASE_URL` - URL do banco PostgreSQL
   - `SECRET_KEY` - Chave secreta forte
   - `CORS_ORIGINS` - Domínios permitidos
   - `DEBUG=False`

2. Para PostgreSQL, atualize `backend/app/config.py`:
```python
DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
```

3. Execute migrations (se usar Alembic)

### Frontend (Vercel/Netlify)

1. Configure a variável de ambiente:
   - `VITE_API_URL` - URL da API em produção

2. Build command: `npm run build`
3. Output directory: `dist`

### Deploy no Easypanel

#### Configuração do Backend

1. **Variáveis de Ambiente no Easypanel**:
   ```
   DATABASE_URL=sqlite:///./portfolio.db
   DEBUG=False
   SECRET_KEY=sua-chave-secreta-forte-aqui
   CORS_ORIGINS=["https://portfolio-frontend.mktdr8.easypanel.host"]
   ```

2. **Importante**: Adicione o domínio do seu frontend no `CORS_ORIGINS`
   - Formato: `["https://seu-frontend-domain.easypanel.host"]`
   - Para múltiplos domínios: `["https://domain1.com","https://domain2.com"]`

#### Configuração do Frontend

1. **Variável de Ambiente no Easypanel**:
   ```
   VITE_API_URL=https://portfolio-backend.mktdr8.easypanel.host
   ```

#### Troubleshooting CORS

Se você receber o erro:
```
Access to XMLHttpRequest has been blocked by CORS policy
```

**Soluções**:

1. **Verifique as variáveis de ambiente do backend**:
   - Acesse o painel do Easypanel
   - Vá em "Environment Variables" do serviço backend
   - Certifique-se que `CORS_ORIGINS` contém o domínio do frontend

2. **Formato correto do CORS_ORIGINS**:
   ```
   CORS_ORIGINS=["https://portfolio-frontend.mktdr8.easypanel.host"]
   ```
   - Use HTTPS (não HTTP) para produção
   - Não inclua barra final no domínio
   - Use aspas duplas dentro dos colchetes

3. **Após alterar variáveis de ambiente**:
   - Reinicie o serviço backend no Easypanel
   - Aguarde alguns segundos para o serviço reiniciar
   - Teste novamente a aplicação

4. **Verifique os logs do backend**:
   - Acesse os logs no Easypanel
   - Procure por erros relacionados a CORS
   - Verifique se as variáveis foram carregadas corretamente

## Segurança

- CORS configurado para origens específicas
- Headers de segurança implementados
- Rate limiting ativo
- Validação de dados com Pydantic
- SQL Injection prevenido via ORM
- XSS prevenido via Vue.js (escape automático)

### Checklist de Produção

- [ ] Alterar `SECRET_KEY` em `.env`
- [ ] Configurar `CORS_ORIGINS` com domínios específicos
- [ ] Definir `DEBUG=False`
- [ ] Usar HTTPS
- [ ] Configurar backup do banco de dados
- [ ] Implementar autenticação (se necessário)
- [ ] Configurar monitoramento e logs
- [ ] Testar rate limiting
- [ ] Revisar permissões de CORS

## Melhorias Futuras

- [ ] Autenticação JWT para painel admin
- [ ] Upload de imagens direto (ao invés de URLs)
- [ ] Testes unitários e de integração
- [ ] CI/CD pipeline
- [ ] Internacionalização (i18n)
- [ ] Dark mode
- [ ] SEO otimizado
- [ ] Blog integrado
- [ ] Analytics
- [ ] Comentários em projetos
- [ ] Migração para PostgreSQL
- [ ] Cache com Redis
- [ ] Busca com Elasticsearch

## Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## Suporte

Para problemas, dúvidas ou sugestões:
- Abra uma issue no GitHub
- Entre em contato via email (configurar no perfil)

## Autor

Desenvolvido por [Seu Nome] - Desenvolvedor IA

---

**Nota**: Este é um projeto de portfólio. Personalize conforme suas necessidades!
