# Deploy usando GitHub Desktop + EasyPanel

Guia completo para quem usa GitHub Desktop (sem linha de comando).

## Parte 1: Enviar Código para GitHub

### Opção A: Se ainda NÃO tem repositório criado

1. **Abra GitHub Desktop**

2. **Adicione seu projeto:**
   - `File` → `Add Local Repository`
   - Navegue até a pasta `portfolio`
   - Clique em `Add Repository`

3. **Se aparecer "This directory does not appear to be a Git repository":**
   - Clique em `Create a repository here instead`
   - Preencha:
     - Name: `portfolio`
     - Description: `Portfólio Profissional - Desenvolvedor IA`
     - ✅ Initialize this repository with a README
   - Clique em `Create Repository`

4. **Fazer primeiro commit (se necessário):**
   - Veja os arquivos na aba `Changes`
   - No campo "Summary", escreva: `Projeto inicial`
   - Clique em `Commit to main`

5. **Publicar no GitHub:**
   - Clique no botão azul `Publish repository`
   - Configurações:
     - Name: `portfolio`
     - Description: `Portfólio - FastAPI + Vue.js`
     - Organization: (sua conta pessoal)
     - ⚠️ **Desmarque** "Keep this code private" (se quiser público)
   - Clique em `Publish Repository`

6. **Verificar:**
   - Clique em `Repository` → `View on GitHub`
   - Seu código está online! 🎉
   - Copie a URL: `https://github.com/seu-usuario/portfolio`

### Opção B: Se JÁ tem repositório no GitHub

1. **Clone do GitHub:**
   - `File` → `Clone Repository`
   - Aba `GitHub.com`
   - Selecione `seu-usuario/portfolio`
   - Choose... → Selecione onde salvar
   - Clone

2. **Ou adicione repositório existente:**
   - `File` → `Add Local Repository`
   - Selecione pasta do projeto
   - Add Repository

### Fazer Push de Novas Mudanças

Sempre que fizer alterações:

1. **Ver mudanças:**
   - GitHub Desktop mostra alterações automaticamente
   - Aba `Changes` lista todos os arquivos modificados

2. **Commit:**
   - Marque os arquivos que quer enviar (ou deixe todos)
   - Campo "Summary": Escreva mensagem (ex: "Adicionar deploy configs")
   - Clique em `Commit to main`

3. **Push (enviar para GitHub):**
   - Clique no botão `Push origin` (topo da tela)
   - Aguarde upload completar

4. **Verificar:**
   - `Repository` → `View on GitHub`
   - Veja se mudanças apareceram

---

## Parte 2: Deploy no EasyPanel

### Método 1: Via Interface (COM conexão GitHub)

#### 1. Conectar GitHub ao EasyPanel

1. **Acesse seu EasyPanel:** `http://seu-ip-vps:3000`

2. **Login** com suas credenciais

3. **Conectar GitHub:**
   - Vá em `Settings` (ou ícone de engrenagem)
   - Procure por `GitHub` ou `Integrations`
   - Clique em `Connect GitHub`
   - Autorize o EasyPanel a acessar seus repositórios
   - Selecione o repositório `portfolio`

#### 2. Criar Projeto

1. **Clique em `Projects`**
2. **`+ Create Project`** ou `New Project`
3. Nome: `portfolio`
4. `Create`

#### 3. Adicionar Backend (API)

1. **Dentro do projeto → `Add Service`**

2. **Selecione tipo:**
   - `App` ou `Application`
   - Source: `GitHub`

3. **Configurações do Source:**
   - Repository: Selecione `seu-usuario/portfolio`
   - Branch: `main`
   - Auto Deploy: ✅ (para rebuild automático)

4. **Build Configuration:**
   - Build Type: `Dockerfile`
   - Dockerfile Path: `backend/Dockerfile`
   - Docker Context: `backend` (pasta raiz do backend)

5. **Port Configuration:**
   - Container Port: `8000`
   - Expose Port: `8000`

6. **Environment Variables:**

   Clique em `Add Variable` para cada uma:

   | Name | Value |
   |------|-------|
   | `DATABASE_URL` | `sqlite:///./data/portfolio.db` |
   | `SECRET_KEY` | (gerar abaixo) |
   | `CORS_ORIGINS` | `["*"]` |
   | `DEBUG` | `False` |

   **Gerar SECRET_KEY:**
   - Windows PowerShell: `python -c "import secrets; print(secrets.token_hex(32))"`
   - Ou use: https://generate-secret.vercel.app/32

7. **Volumes (Persistência de Dados):**
   - Add Volume
   - Mount Path: `/app/data`
   - (EasyPanel cria automaticamente o volume)

8. **Domain (Opcional):**
   - Se tiver domínio: `api.seu-dominio.com`
   - Senão, acesse via: `http://seu-ip-vps:8000`

9. **`Deploy`** ou `Create`

10. **Aguardar build:**
    - Clique em `Logs` para ver progresso
    - Pode levar 3-10 minutos na primeira vez

#### 4. Adicionar Frontend (Site)

1. **`Add Service`** novamente (no mesmo projeto)

2. **Configurações:**
   - Type: `App`
   - Source: `GitHub`
   - Repository: `seu-usuario/portfolio`
   - Branch: `main`

3. **Build:**
   - Build Type: `Dockerfile`
   - Dockerfile Path: `frontend/Dockerfile`
   - Docker Context: `frontend`

4. **Build Arguments:**

   Clique em `Add Build Arg`:

   | Name | Value |
   |------|-------|
   | `VITE_API_URL` | `http://seu-ip-vps:8000` |

   (ou `https://api.seu-dominio.com` se configurou domínio no backend)

5. **Port:**
   - Container Port: `80`
   - Expose Port: `80` ou `3000`

6. **Domain:**
   - `seu-dominio.com` ou deixe em branco

7. **`Deploy`**

8. **Aguardar build**

#### 5. Verificar Deploy

Após build concluído (status verde):

- **Frontend:** `http://seu-ip-vps` ou `http://seu-dominio.com`
- **Backend API:** `http://seu-ip-vps:8000/docs`
- **Admin:** `http://seu-ip-vps/admin`

---

### Método 2: Via Interface (SEM conexão GitHub)

Se não conseguir conectar GitHub ou preferir upload manual:

#### Opção A: Download ZIP e Upload

1. **No GitHub (navegador):**
   - Vá em `https://github.com/seu-usuario/portfolio`
   - Clique em `Code` → `Download ZIP`
   - Salve e extraia

2. **Upload para VPS via SFTP:**
   - Use FileZilla, WinSCP ou similar
   - Host: `seu-ip-vps`
   - User: `root` (ou seu usuário)
   - Password: sua senha
   - Upload pasta `portfolio` para `/var/www/`

3. **No EasyPanel:**
   - Create Project → `portfolio`
   - Add Service → `Custom` ou `Docker`
   - Build From: `Local Path`
   - Path: `/var/www/portfolio/backend`
   - Dockerfile: `Dockerfile`
   - Configure portas e variáveis como acima
   - Deploy

#### Opção B: Git Clone na VPS (via SSH)

Se tiver acesso SSH:

```bash
# Conectar
ssh usuario@seu-ip-vps

# Clonar repositório
cd /var/www
git clone https://github.com/seu-usuario/portfolio.git

# Voltar ao EasyPanel e usar caminho local
```

---

## Parte 3: Configurar Domínio (Opcional)

### No seu provedor de domínio:

1. Acesse painel do domínio (Registro.br, GoDaddy, etc)
2. Vá em DNS Settings
3. Adicione registros:

**Para o site:**
```
Type: A
Name: @
Value: seu-ip-vps
TTL: 3600
```

**Para a API:**
```
Type: A
Name: api
Value: seu-ip-vps
TTL: 3600
```

### No EasyPanel:

1. Vá no serviço Backend → `Domains`
2. Add Domain: `api.seu-dominio.com`
3. Enable HTTPS ✅

4. Vá no serviço Frontend → `Domains`
5. Add Domain: `seu-dominio.com`
6. Enable HTTPS ✅

Aguarde DNS propagar (5 min a 24h).

---

## Parte 4: Atualizar Aplicação

Quando fizer mudanças no código:

### Via GitHub Desktop:

1. **Edite seus arquivos** (VS Code, etc)
2. **Abra GitHub Desktop**
3. **Veja mudanças** na aba Changes
4. **Commit:**
   - Summary: "Atualizar layout" (ou descrição)
   - `Commit to main`
5. **Push:** Clique em `Push origin`

### No EasyPanel:

Se configurou Auto Deploy:
- ✅ Rebuild automático quando fizer push

Se NÃO tem auto deploy:
1. Vá no serviço
2. Clique em `Rebuild` ou `Redeploy`
3. Aguarde build

---

## Troubleshooting

### GitHub Desktop: "Authentication Failed"

1. File → Options → Accounts
2. Sign out do GitHub
3. Sign in novamente
4. Tente push de novo

### EasyPanel: "Cannot connect to GitHub"

1. Settings → GitHub → Disconnect
2. Connect novamente
3. Autorize todos os escopos
4. Tente de novo

### Build Failed no EasyPanel

1. Clique em `Logs` no serviço
2. Veja erro específico
3. Verifique se:
   - Dockerfile está no caminho correto
   - Context Path está correto
   - Branch está correta

### CORS Error

No Backend:
- Environment Variable: `CORS_ORIGINS`
- Mude de `["*"]` para `["http://seu-dominio.com"]`
- Rebuild

### Não consigo acessar

Verifique:
- Firewall da VPS (liberar portas 80, 8000)
- Status dos serviços (devem estar verdes)
- Logs (se há erros)

---

## Checklist Final

- [ ] Código no GitHub (via GitHub Desktop)
- [ ] EasyPanel acessível
- [ ] GitHub conectado ao EasyPanel (ou upload manual)
- [ ] Projeto criado no EasyPanel
- [ ] Backend deployado (verde)
- [ ] Frontend deployado (verde)
- [ ] Variáveis de ambiente configuradas
- [ ] Acessível via IP (ou domínio)
- [ ] Admin funciona (`/admin`)
- [ ] Pode adicionar projetos/experiências

---

## Comandos Úteis (PowerShell Windows)

```powershell
# Gerar SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Verificar se Python está instalado
python --version

# Testar backend localmente
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Testar frontend localmente
cd frontend
npm install
npm run dev
```

---

## Próximos Passos

1. ✅ Acesse `/admin`
2. ✅ Configure seu perfil
3. ✅ Adicione projetos
4. ✅ Adicione experiências
5. ✅ Compartilhe seu portfólio!

---

**Dica:** Sempre que fizer mudanças:
1. Salve arquivos
2. GitHub Desktop → Commit → Push
3. EasyPanel → Rebuild (se não for automático)

Pronto! Seu portfólio está no ar! 🚀
