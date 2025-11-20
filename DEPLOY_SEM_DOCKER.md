# Deploy no EasyPanel SEM usar Docker manualmente

Este guia é para você que tem EasyPanel mas não quer/precisa usar comandos Docker.

## Método 1: Interface Gráfica do EasyPanel (RECOMENDADO)

### Pré-requisitos
- Código no GitHub (já está ✅)
- Acesso ao painel EasyPanel
- Domínio apontado para VPS (opcional)

### Passo 1: Acessar EasyPanel

Acesse: `http://seu-ip-vps:3000` ou o domínio que você configurou

### Passo 2: Conectar GitHub

1. Vá em **Settings** → **GitHub**
2. Conecte sua conta GitHub
3. Autorize acesso ao repositório `portfolio`

### Passo 3: Criar Projeto

1. **Projects** → **Create New Project**
2. Nome: `portfolio`
3. Criar

### Passo 4: Adicionar Serviço Backend

1. Dentro do projeto → **Add Service**
2. Escolha: **App**
3. Configure:

**Source:**
- Type: GitHub
- Repository: `Vinicius-Ikehara/portfolio`
- Branch: `main`

**Build:**
- Build Type: `Dockerfile`
- Dockerfile Path: `backend/Dockerfile`
- Docker Context: `backend`

**Environment:**
Adicione estas variáveis (clique em "Add Variable"):
```
DATABASE_URL = sqlite:///./data/portfolio.db
DEBUG = False
SECRET_KEY = cole-aqui-resultado-do-comando
CORS_ORIGINS = ["*"]
```

**Gerar SECRET_KEY:**
Rode no seu computador:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Ports:**
- Container Port: `8000`
- Expose Port: `8000`

**Volumes (Persistência):**
- Mount Path: `/app/data`
- (EasyPanel cria automaticamente)

**Domains:**
- Adicione: `api.seu-dominio.com` (ou deixe em branco para usar IP)

4. Clique em **Deploy**

### Passo 5: Adicionar Serviço Frontend

1. **Add Service** novamente
2. Escolha: **App**
3. Configure:

**Source:**
- Type: GitHub
- Repository: `Vinicius-Ikehara/portfolio`
- Branch: `main`

**Build:**
- Build Type: `Dockerfile`
- Dockerfile Path: `frontend/Dockerfile`
- Docker Context: `frontend`
- Build Arguments:
  ```
  VITE_API_URL = https://api.seu-dominio.com
  ```
  (ou `http://seu-ip-vps:8000` se não tiver domínio)

**Ports:**
- Container Port: `80`
- Expose Port: `80` ou `3000`

**Domains:**
- Adicione: `seu-dominio.com` ou `portfolio.seu-dominio.com`

4. Clique em **Deploy**

### Passo 6: Aguardar Build

- O EasyPanel vai fazer download do código
- Fazer build das imagens Docker
- Iniciar os containers
- Isso pode levar 3-10 minutos

Você pode ver o progresso em:
- **Logs** (ícone de documento)
- **Status** (deve ficar verde quando pronto)

### Passo 7: Acessar

Após deploy concluído:
- **Frontend:** `http://seu-dominio.com` ou `http://seu-ip-vps:3000`
- **Backend:** `http://api.seu-dominio.com` ou `http://seu-ip-vps:8000`
- **API Docs:** `http://seu-ip-vps:8000/docs`
- **Admin:** `http://seu-dominio.com/admin`

---

## Método 2: Se EasyPanel tem "Import Docker Compose"

Alguns EasyPanel têm opção de importar `docker-compose.yml`:

1. No EasyPanel → **Import**
2. Selecione: **Docker Compose**
3. Cole o conteúdo de `easypanel-template.yml`
4. Ajuste variáveis de ambiente
5. Deploy

---

## Método 3: Deploy Manual (Sem Docker, Sem EasyPanel UI)

Se você preferir rodar diretamente na VPS sem Docker:

### Backend (FastAPI)

1. **Conectar via SSH:**
```bash
ssh usuario@seu-ip-vps
```

2. **Instalar dependências:**
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e pip
sudo apt install python3 python3-pip python3-venv -y

# Instalar git
sudo apt install git -y
```

3. **Clonar repositório:**
```bash
cd /var/www
git clone https://github.com/Vinicius-Ikehara/portfolio.git
cd portfolio/backend
```

4. **Configurar ambiente:**
```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

5. **Configurar variáveis:**
```bash
# Criar arquivo .env
nano .env
```

Cole:
```env
DATABASE_URL=sqlite:///./data/portfolio.db
DEBUG=False
SECRET_KEY=sua-chave-aqui
CORS_ORIGINS=["http://seu-dominio.com"]
```

6. **Criar diretório de dados:**
```bash
mkdir -p data
```

7. **Rodar aplicação:**
```bash
# Testar
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Para produção, usar supervisor ou systemd
```

### Frontend (Vue.js)

1. **Instalar Node.js:**
```bash
# Usando NVM (recomendado)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18

# Ou direto
sudo apt install nodejs npm -y
```

2. **Build frontend:**
```bash
cd /var/www/portfolio/frontend

# Instalar dependências
npm install

# Build
npm run build
```

3. **Servir com Nginx:**
```bash
# Instalar nginx
sudo apt install nginx -y

# Criar configuração
sudo nano /etc/nginx/sites-available/portfolio
```

Cole:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    root /var/www/portfolio/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Configurar Serviços como Systemd

Para backend rodar automaticamente:

```bash
sudo nano /etc/systemd/system/portfolio-backend.service
```

Cole:
```ini
[Unit]
Description=Portfolio Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/portfolio/backend
Environment="PATH=/var/www/portfolio/backend/venv/bin"
ExecStart=/var/www/portfolio/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Ativar:
```bash
sudo systemctl daemon-reload
sudo systemctl enable portfolio-backend
sudo systemctl start portfolio-backend
sudo systemctl status portfolio-backend
```

---

## Troubleshooting

### "Não consigo acessar o painel"

Verifique se EasyPanel está rodando:
```bash
sudo systemctl status easypanel
# ou
sudo docker ps | grep easypanel
```

### "Build falhou no EasyPanel"

1. Verifique logs no painel
2. Confirme que Dockerfile está no caminho correto
3. Verifique se GitHub tem acesso

### "Serviço não inicia"

1. Veja logs: **Service** → **Logs**
2. Verifique variáveis de ambiente
3. Confirme portas não estão em uso

### "CORS Error"

No backend, ajuste `CORS_ORIGINS`:
```
CORS_ORIGINS=["http://seu-dominio.com", "http://localhost:3000", "*"]
```

---

## Qual método usar?

| Método | Dificuldade | Quando usar |
|--------|-------------|-------------|
| **EasyPanel UI** | ⭐ Fácil | Tem EasyPanel instalado |
| **Docker Compose Import** | ⭐⭐ Médio | EasyPanel suporta import |
| **Deploy Manual** | ⭐⭐⭐ Avançado | Sem Docker/EasyPanel |

**Recomendado:** Use EasyPanel UI (Método 1)

---

## Checklist

- [ ] Código no GitHub
- [ ] EasyPanel instalado e acessível
- [ ] GitHub conectado ao EasyPanel
- [ ] Backend deployado
- [ ] Frontend deployado
- [ ] Variáveis de ambiente configuradas
- [ ] Domínio configurado (opcional)
- [ ] SSL ativo (opcional)
- [ ] Acesso ao /admin funciona

---

## Próximos Passos

1. Acesse `/admin`
2. Configure seu perfil
3. Adicione projetos
4. Adicione experiências
5. Compartilhe seu portfólio!

---

Dúvidas? Veja os logs no EasyPanel ou teste localmente primeiro.
