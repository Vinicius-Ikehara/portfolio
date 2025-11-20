# Portfolio - AI Developer

Este é um projeto de portfólio profissional para desenvolvedores de IA, construído com FastAPI (backend) e Vue.js (frontend).

## Estrutura do Projeto

```
portfolio/
├── backend/          # API FastAPI
│   ├── app/
│   │   ├── main.py           # Aplicação principal
│   │   ├── models.py         # Modelos do banco de dados
│   │   ├── schemas.py        # Schemas Pydantic
│   │   ├── database.py       # Configuração do banco
│   │   └── routers/          # Endpoints da API
│   └── requirements.txt
└── frontend/         # Aplicação Vue.js
    ├── src/
    │   ├── components/       # Componentes reutilizáveis
    │   ├── views/            # Páginas
    │   ├── services/         # Serviços de API
    │   └── router/           # Configuração de rotas
    └── package.json
```

## Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para banco de dados
- **SQLite**: Banco de dados (pode ser migrado para PostgreSQL)
- **Pydantic**: Validação de dados

### Frontend
- **Vue.js 3**: Framework JavaScript progressivo
- **Vue Router**: Roteamento
- **Pinia**: Gerenciamento de estado
- **Tailwind CSS**: Framework CSS utilitário
- **Axios**: Cliente HTTP

## Funcionalidades

1. **Gestão de Perfil**: Informações pessoais, bio, contatos
2. **Gestão de Projetos**: CRUD completo para projetos
3. **Gestão de Experiências**: Timeline de experiências profissionais
4. **Painel Administrativo**: Interface para gerenciar todo o conteúdo
5. **Página Pública**: Portfólio responsivo e profissional

## Subagentes Especializados

Este projeto utiliza subagentes Claude especializados para diferentes aspectos:

- **/security-review**: Análise de segurança do código
- **/frontend-review**: Revisão de código frontend (Vue.js, CSS, UX)
- **/architecture-review**: Análise da arquitetura do sistema
- **/code-review**: Revisão geral de código

## Comandos Úteis

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Boas Práticas

1. **Segurança**: Sempre validar inputs, usar HTTPS em produção
2. **Performance**: Otimizar queries do banco, lazy loading de imagens
3. **Manutenibilidade**: Código limpo, comentários quando necessário
4. **Responsividade**: Design mobile-first
5. **Acessibilidade**: Seguir padrões WCAG
