# Guia de Deploy - Hostinger VPS com EasyPanel

Este guia explica como fazer deploy do portfólio na sua VPS Hostinger usando EasyPanel.

## Pré-requisitos

- VPS na Hostinger com EasyPanel instalado
- Domínio configurado (ou usar IP da VPS)
- Acesso SSH à VPS
- Git instalado na VPS

## Método 1: Deploy via EasyPanel UI (Recomendado)

### 1. Preparar o Repositório

Certifique-se de que o código está no GitHub e com os arquivos Docker:
- ✅ `backend/Dockerfile`
- ✅ `frontend/Dockerfile`
- ✅ `docker-compose.yml`

### 2. Acessar EasyPanel

1. Acesse seu EasyPanel: `http://seu-ip-vps:3000` ou `https://easypanel.seu-dominio.com`
2. Faça login com suas credenciais

### 3. Criar Projeto

1. Clique em **"Create Project"**
2. Nome do projeto: `portfolio`

### 4. Adicionar Serviço Backend

1. Dentro do projeto, clique em **"Add Service"**
2. Selecione **"App (Docker)"**
3. Configure:
   - **Name**: `backend`
   - **Source**: GitHub Repository
   - **Repository**: `seu-usuario/portfolio`
   - **Branch**: `main`
   - **Docker Context**: `./backend`
   - **Dockerfile Path**: `./backend/Dockerfile`
   - **Port**: `8000`

4. **Environment Variables** (variáveis de ambiente):
   ```
   DATABASE_URL=sqlite:///./data/portfolio.db
   DEBUG=False
   SECRET_KEY=gere-uma-chave-secreta-forte-aqui
   CORS_ORIGINS=["https://seu-dominio.com"]
   ```

5. **Domains** (domínios):
   - Adicione: `api.seu-dominio.com` (ou use subdomínio)
   - Habilite HTTPS/SSL

6. **Volumes** (persistência de dados):
   - Mount Path: `/app/data`
   - Host Path: `/var/lib/easypanel/projects/portfolio/backend-data`

7. Clique em **"Deploy"**

### 5. Adicionar Serviço Frontend

1. No mesmo projeto, clique em **"Add Service"** novamente
2. Selecione **"App (Docker)"**
3. Configure:
   - **Name**: `frontend`
   - **Source**: GitHub Repository
   - **Repository**: `seu-usuario/portfolio`
   - **Branch**: `main`
   - **Docker Context**: `./frontend`
   - **Dockerfile Path**: `./frontend/Dockerfile`
   - **Port**: `80`

4. **Build Args** (argumentos de build):
   ```
   VITE_API_URL=https://api.seu-dominio.com
   ```

5. **Domains**:
   - Adicione: `seu-dominio.com` ou `portfolio.seu-dominio.com`
   - Habilite HTTPS/SSL

6. Clique em **"Deploy"**

### 6. Verificar Deploy

1. Aguarde o build completar (pode levar alguns minutos)
2. Acesse `https://seu-dominio.com` - deve mostrar o portfólio
3. Acesse `https://api.seu-dominio.com/docs` - deve mostrar a documentação da API

---

## Método 2: Deploy via SSH + Docker Compose

Se preferir fazer via linha de comando:

### 1. Conectar via SSH

```bash
ssh root@seu-ip-vps
# ou
ssh seu-usuario@seu-ip-vps
```

### 2. Clonar Repositório

```bash
cd /var/www
git clone https://github.com/seu-usuario/portfolio.git
cd portfolio
```

### 3. Configurar Variáveis de Ambiente

```bash
# Criar arquivo .env na raiz
cat > .env << 'EOF'
# Backend
DATABASE_URL=sqlite:///./data/portfolio.db
DEBUG=False
SECRET_KEY=sua-chave-secreta-super-forte-aqui
CORS_ORIGINS=["https://seu-dominio.com"]

# Frontend
VITE_API_URL=https://api.seu-dominio.com
EOF
```

### 4. Ajustar docker-compose.yml

Edite `docker-compose.yml` e atualize:
- Portas (se necessário)
- Variáveis de ambiente
- Domínios

### 5. Fazer Build e Deploy

```bash
# Build das imagens
docker-compose build

# Iniciar containers
docker-compose up -d

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f
```

### 6. Configurar Nginx Reverse Proxy (Opcional)

Se quiser usar nginx na VPS como proxy:

```bash
# Instalar nginx
apt update && apt install nginx -y

# Criar configuração
nano /etc/nginx/sites-available/portfolio
```

Adicione:
```nginx
# Backend API
server {
    listen 80;
    server_name api.seu-dominio.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}

# Frontend
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# Ativar site
ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/

# Testar configuração
nginx -t

# Reiniciar nginx
systemctl restart nginx
```

### 7. Configurar SSL com Certbot

```bash
# Instalar certbot
apt install certbot python3-certbot-nginx -y

# Obter certificado
certbot --nginx -d seu-dominio.com -d www.seu-dominio.com -d api.seu-dominio.com

# Renovação automática já está configurada
```

---

## Método 3: Deploy Manual com EasyPanel Docker Compose

### 1. No EasyPanel

1. Vá em **"Docker Compose"**
2. Clique em **"Create"**
3. Cole o conteúdo do `docker-compose.yml`
4. Ajuste as variáveis de ambiente
5. Clique em **"Deploy"**

---

## Configurações Importantes

### Banco de Dados

**SQLite (Desenvolvimento/Pequeno Porte)**
- Já configurado
- Arquivo salvo em `/app/data/portfolio.db`
- Volume persistente necessário

**PostgreSQL (Produção/Maior Escala)**

1. No EasyPanel, adicione serviço PostgreSQL:
   - **Service**: PostgreSQL
   - **Name**: `portfolio-db`
   - **Database**: `portfolio`
   - **User**: `portfolio_user`
   - **Password**: (gere uma senha forte)

2. Atualize variável de ambiente do backend:
   ```
   DATABASE_URL=postgresql://portfolio_user:senha@portfolio-db:5432/portfolio
   ```

3. Instale psycopg2 no backend:
   ```bash
   # Adicione ao requirements.txt
   psycopg2-binary==2.9.9
   ```

### Variáveis de Ambiente Obrigatórias

**Backend:**
- `DATABASE_URL` - URL do banco de dados
- `SECRET_KEY` - Chave secreta (gere com: `openssl rand -hex 32`)
- `CORS_ORIGINS` - Lista de domínios permitidos
- `DEBUG=False` - Desabilitar modo debug em produção

**Frontend:**
- `VITE_API_URL` - URL da API backend

### Gerar SECRET_KEY Segura

```bash
# Opção 1: OpenSSL
openssl rand -hex 32

# Opção 2: Python
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Troubleshooting

### Backend não conecta ao banco

```bash
# Verificar permissões do volume
docker exec -it portfolio-backend ls -la /app/data

# Criar diretório se não existir
docker exec -it portfolio-backend mkdir -p /app/data
```

### CORS Error no frontend

Verifique se a variável `CORS_ORIGINS` no backend inclui o domínio do frontend:
```python
CORS_ORIGINS=["https://seu-dominio.com", "http://localhost:3000"]
```

### SSL não funciona

1. Verifique DNS apontando para VPS
2. Aguarde propagação DNS (pode levar até 24h)
3. Use certbot para gerar certificado
4. No EasyPanel, habilite "Force HTTPS"

### Logs de Debug

```bash
# Ver logs do backend
docker logs portfolio-backend -f

# Ver logs do frontend
docker logs portfolio-frontend -f

# Logs do docker-compose
docker-compose logs -f

# Entrar no container
docker exec -it portfolio-backend /bin/bash
```

### Rebuild após mudanças

```bash
# Via docker-compose
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Via EasyPanel
# Clique em "Rebuild" no serviço específico
```

---

## Manutenção

### Backup do Banco de Dados

```bash
# SQLite
docker exec portfolio-backend cp /app/data/portfolio.db /app/data/backup-$(date +%Y%m%d).db

# PostgreSQL
docker exec portfolio-db pg_dump -U portfolio_user portfolio > backup-$(date +%Y%m%d).sql
```

### Atualizar Aplicação

```bash
# Método 1: Git pull + rebuild
cd /var/www/portfolio
git pull origin main
docker-compose build
docker-compose up -d

# Método 2: Via EasyPanel
# Clique em "Rebuild" no serviço
```

### Monitoramento

- Use o dashboard do EasyPanel para ver:
  - Status dos containers
  - Uso de CPU/RAM
  - Logs em tempo real
  - Reiniciar serviços

---

## Checklist Final

- [ ] Código commitado e enviado ao GitHub
- [ ] Variáveis de ambiente configuradas
- [ ] Domínio apontando para VPS
- [ ] Backend deployado e acessível
- [ ] Frontend deployado e acessível
- [ ] SSL/HTTPS configurado
- [ ] CORS configurado corretamente
- [ ] Banco de dados persistente (volume)
- [ ] Backup configurado
- [ ] Logs sendo monitorados

---

## Links Úteis

- [Documentação EasyPanel](https://easypanel.io/docs)
- [FastAPI Deploy](https://fastapi.tiangolo.com/deployment/)
- [Vue.js Production Deployment](https://vuejs.org/guide/best-practices/production-deployment.html)
- [Docker Documentation](https://docs.docker.com/)

## Suporte

Se tiver problemas:
1. Verifique os logs
2. Consulte a documentação do EasyPanel
3. Verifique configurações de firewall/portas na VPS
4. Teste localmente com docker-compose primeiro
