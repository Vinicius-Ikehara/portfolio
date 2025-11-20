# Quick Start - Deploy no EasyPanel

Guia rápido para fazer deploy na Hostinger VPS com EasyPanel em 5 minutos.

## Opção Mais Rápida: UI do EasyPanel

### 1. Preparar Código
```bash
git add .
git commit -m "Preparar para deploy"
git push origin main
```

### 2. No EasyPanel

**Acesse:** `http://seu-ip-vps:3000`

**Backend API:**
1. Create Project → Nome: `portfolio`
2. Add Service → Docker
   - **Name:** `backend`
   - **Source:** GitHub → `seu-usuario/portfolio`
   - **Branch:** `main`
   - **Context:** `./backend`
   - **Port:** `8000`
   - **Env Vars:**
     ```
     DATABASE_URL=sqlite:///./data/portfolio.db
     SECRET_KEY=cole-resultado-do-comando-abaixo
     CORS_ORIGINS=["https://seu-dominio.com"]
     DEBUG=False
     ```
   - **Volume:** `/app/data` → `/easypanel/projects/portfolio/data`
   - **Domain:** `api.seu-dominio.com`
   - Deploy ✅

**Frontend:**
1. Add Service → Docker
   - **Name:** `frontend`
   - **Source:** GitHub → `seu-usuario/portfolio`
   - **Branch:** `main`
   - **Context:** `./frontend`
   - **Port:** `80`
   - **Build Args:**
     ```
     VITE_API_URL=https://api.seu-dominio.com
     ```
   - **Domain:** `seu-dominio.com`
   - Deploy ✅

### 3. Gerar SECRET_KEY
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Acessar
- Frontend: `https://seu-dominio.com`
- API Docs: `https://api.seu-dominio.com/docs`
- Admin: `https://seu-dominio.com/admin`

---

## Troubleshooting Rápido

**CORS Error?**
→ Adicione domínio do frontend no `CORS_ORIGINS` do backend

**API não responde?**
→ Verifique logs no EasyPanel → Backend → Logs

**Build falhou?**
→ Verifique se Dockerfile está na pasta correta

**SSL não funciona?**
→ Aguarde DNS propagar (até 24h) e habilite "Force HTTPS"

---

## Comando Úteis

```bash
# Ver logs
docker logs portfolio-backend -f

# Reiniciar
docker restart portfolio-backend

# Entrar no container
docker exec -it portfolio-backend bash
```

---

Pronto! Seu portfólio está no ar 🚀
