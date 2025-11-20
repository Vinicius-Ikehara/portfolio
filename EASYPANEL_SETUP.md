# Configuração do Portfolio no Easypanel

Este guia explica passo a passo como configurar o projeto no Easypanel para resolver o erro de CORS.

## Problema

```
Access to XMLHttpRequest has been blocked by CORS policy:
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## Solução

O código já foi atualizado no GitHub. Agora você precisa configurar as variáveis de ambiente no Easypanel e fazer o redeploy.

---

## Passo 1: Configurar Variáveis de Ambiente

### Backend (portfolio-backend)

1. **Acesse o Easypanel**
   - URL: https://easypanel.mktdr8.easypanel.host (ou seu domínio)

2. **Navegue até o projeto**
   - Clique no projeto "portfolio" ou similar

3. **Selecione o serviço Backend**
   - Procure por "portfolio-backend" ou "backend"

4. **Vá para a aba Environment**
   - Procure por "Environment", "Environment Variables" ou "Env Vars"

5. **Adicione/Edite as seguintes variáveis**:

   **CORS_ORIGINS** - Aceita dois formatos:

   **Formato 1 - JSON (Recomendado)**:
   ```
   CORS_ORIGINS=["https://portfolio-frontend.mktdr8.easypanel.host"]
   ```

   **Formato 2 - Separado por vírgula (Alternativo)**:
   ```
   CORS_ORIGINS=https://portfolio-frontend.mktdr8.easypanel.host
   ```

   Para múltiplos domínios:
   ```
   CORS_ORIGINS=["https://frontend1.com","https://frontend2.com"]
   ```
   ou
   ```
   CORS_ORIGINS=https://frontend1.com,https://frontend2.com
   ```

   **IMPORTANTE**:
   - Use HTTPS (não HTTP) em produção
   - Não adicione barra final no domínio: ❌ `https://domain.com/`
   - Se usar formato JSON, use aspas duplas `"` (não aspas simples)

   **Outras variáveis recomendadas** (se não existirem):
   ```
   DATABASE_URL=sqlite:///./portfolio.db
   DEBUG=True
   SECRET_KEY=uma-chave-secreta-forte-aleatoria
   ```

   **⚠️ IMPORTANTE sobre DEBUG**:
   - Use `DEBUG=True` para poder acessar o endpoint `/debug/config`
   - Depois de verificar que está tudo funcionando, mude para `DEBUG=False`

6. **Salve as variáveis**
   - Clique em "Save", "Update" ou "Apply"

---

## Passo 2: Atualizar o Código e Reiniciar

Você tem 3 opções:

### **OPÇÃO A: Redeploy Manual (Recomendado)**

Esta é a melhor opção porque garante que você tenha o código mais recente + as variáveis de ambiente.

1. **No serviço Backend, procure por uma opção de Deploy**
   - Pode ser "Deploy", "Deployment", "Redeploy" ou "Rebuild"

2. **Clique em "Redeploy" ou "Deploy"**
   - Isso vai:
     - Puxar o código mais recente do GitHub
     - Reconstruir a imagem Docker
     - Aplicar as variáveis de ambiente
     - Reiniciar o serviço

3. **Aguarde o deploy finalizar**
   - Acompanhe os logs para ver se há erros
   - Deve levar de 1-3 minutos

### **OPÇÃO B: Configurar Auto-Deploy do GitHub**

Configure para fazer deploy automático quando houver push:

1. **No serviço Backend, procure por "Source" ou "Git"**

2. **Configure a conexão com o GitHub**:
   - Repository: `Vinicius-Ikehara/portfolio`
   - Branch: `claude/fix-portfolio-issue-0186451B928g2p2iMbFrVQTJ` (ou `main` após o merge)
   - Path: `backend`

3. **Ative o Auto-Deploy**
   - Marque a opção "Auto Deploy" ou similar
   - Isso fará deploy automático a cada push

4. **Faça o primeiro deploy**
   - Clique em "Deploy" ou "Trigger Deploy"

### **OPÇÃO C: Restart Simples**

⚠️ **Atenção**: Isso só funciona se o código já estiver atualizado no container!

1. **No serviço Backend, clique em "Restart"**
   - Isso apenas reinicia o container
   - Não atualiza o código
   - Aplica as variáveis de ambiente

---

## Passo 3: Verificar se Funcionou

### 3.1. Verificar os Logs

1. **Acesse os logs do backend**
   - Procure por "Logs", "Console" ou "View Logs"

2. **Procure por mensagens de inicialização**
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

3. **Verifique se as variáveis foram carregadas**
   - Você pode adicionar um print temporário no `config.py` para ver os valores

### 3.2. Testar a API Diretamente

1. **Abra o navegador**

2. **Acesse a documentação da API**:
   ```
   https://portfolio-backend.mktdr8.easypanel.host/docs
   ```

3. **Teste um endpoint**:
   - Clique em `GET /api/profile`
   - Clique em "Try it out"
   - Clique em "Execute"
   - Deve retornar 404 ou os dados do perfil

### 3.3. Testar o Frontend

1. **Acesse o frontend**:
   ```
   https://portfolio-frontend.mktdr8.easypanel.host
   ```

2. **Abra o Console do navegador** (F12)

3. **Tente salvar dados no perfil**

4. **Verifique se o erro de CORS desapareceu**
   - Se ainda aparecer, volte ao Passo 1 e verifique as variáveis

---

## Troubleshooting

### Erro: CORS ainda não funciona após configurar

**Possíveis causas**:

1. **Variável CORS_ORIGINS com formato incorreto**
   - ❌ ERRADO: `https://portfolio-frontend.mktdr8.easypanel.host`
   - ❌ ERRADO: `['https://portfolio-frontend.mktdr8.easypanel.host']` (aspas simples)
   - ✅ CORRETO: `["https://portfolio-frontend.mktdr8.easypanel.host"]` (aspas duplas)

2. **Backend não foi reiniciado**
   - Faça um restart ou redeploy do backend

3. **Código antigo ainda está rodando**
   - Faça um redeploy para puxar o código novo do GitHub

4. **URL incorreta**
   - Verifique se o domínio está exatamente igual
   - Use HTTPS, não HTTP
   - Não coloque barra final: ❌ `https://domain.com/`

### Erro: Failed to load resource: net::ERR_FAILED

Este erro pode indicar que:

1. **Backend não está rodando**
   - Verifique os logs do backend
   - Reinicie o serviço se necessário

2. **URL do backend está incorreta**
   - Verifique a variável `VITE_API_URL` no frontend
   - Deve ser: `https://portfolio-backend.mktdr8.easypanel.host`

3. **Problema de rede/proxy**
   - Verifique se o domínio do backend está acessível
   - Tente acessar: `https://portfolio-backend.mktdr8.easypanel.host/docs`

### Como verificar se as variáveis de ambiente estão corretas

Você pode adicionar um endpoint temporário para verificar:

1. **Edite `backend/app/main.py`** e adicione:
   ```python
   @app.get("/debug/cors")
   async def debug_cors():
       from .config import settings
       return {"cors_origins": settings.CORS_ORIGINS}
   ```

2. **Faça redeploy**

3. **Acesse**:
   ```
   https://portfolio-backend.mktdr8.easypanel.host/debug/cors
   ```

4. **Verifique a resposta**:
   ```json
   {
     "cors_origins": ["https://portfolio-frontend.mktdr8.easypanel.host"]
   }
   ```

5. **IMPORTANTE**: Remova este endpoint depois de verificar!

---

## Resumo dos Comandos

Se você estiver fazendo deploy local e depois fazendo push:

```bash
# 1. Fazer pull das últimas mudanças
git pull origin claude/fix-portfolio-issue-0186451B928g2p2iMbFrVQTJ

# 2. Testar localmente (opcional)
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload

# 3. Fazer push
git push origin claude/fix-portfolio-issue-0186451B928g2p2iMbFrVQTJ
```

---

## Checklist Final

Use este checklist para garantir que tudo está configurado:

- [ ] Variável `CORS_ORIGINS` configurada no backend do Easypanel
- [ ] Formato da variável está correto (com colchetes e aspas duplas)
- [ ] Backend foi reiniciado ou redeployado
- [ ] Código mais recente está no GitHub
- [ ] Frontend tem a variável `VITE_API_URL` correta
- [ ] Consegue acessar `https://portfolio-backend.mktdr8.easypanel.host/docs`
- [ ] Teste salvar dados no frontend e verifique se o erro de CORS sumiu

---

## Precisa de Ajuda?

Se ainda estiver com problemas:

1. **Verifique os logs do backend** no Easypanel
2. **Tire um print das variáveis de ambiente** configuradas
3. **Compartilhe o erro completo** do console do navegador
4. **Verifique se consegue acessar** `https://portfolio-backend.mktdr8.easypanel.host/docs`

---

**Última atualização**: 2025-11-20
