# Problema: Backend em Loop de Restart no Easypanel

## Descrição do Problema

O backend FastAPI está iniciando corretamente mas sendo desligado automaticamente pelo Easypanel após alguns segundos, resultando em erro 502 para os usuários.

## Evidências

### Logs do Backend (mostrando que funciona):
```
[CONFIG] Settings initialized successfully!
[CONFIG] CORS_ORIGINS final value: ['https://portfolio-frontend.mktdr8.easypanel.host']
[CONFIG] DEBUG: True
INFO: Started server process [1]
INFO: Waiting for application startup.
INFO: Application startup complete.
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Shutting down    <-- Easypanel está matando o processo
INFO: Waiting for application shutdown.
INFO: Application shutdown complete.
INFO: Finished server process [1]
```

### Erro no navegador:
```
GET https://portfolio-backend.mktdr8.easypanel.host/health
502 (Bad Gateway)
```

## Configuração Atual

**Dockerfile**: Correto, usa `uvicorn app.main:app --host 0.0.0.0 --port 8000`

**Porta exposta**: 8000

**Health check endpoint**: `/health` (retorna `{"status": "healthy"}`)

**Variáveis de ambiente configuradas**:
- `CORS_ORIGINS=["https://portfolio-frontend.mktdr8.easypanel.host"]`
- `DEBUG=True`
- `DATABASE_URL=sqlite:///./portfolio.db`
- `SECRET_KEY=lminha-chave-super-secreta-12345`

## O que já foi tentado

1. ✅ Adicionado curl ao Dockerfile
2. ✅ Removido health check do docker-compose.yml
3. ✅ Configurado CORS corretamente
4. ✅ Verificado que o código inicia sem erros
5. ✅ Adicionado endpoint `/health` para health checks

## Possíveis Causas

1. **Health Check configurado no Easypanel** que está falhando
2. **Liveness/Readiness Probe** com configuração incorreta
3. **Limite de recursos** (CPU/memória) muito baixo
4. **Configuração de porta** incorreta no Easypanel
5. **Política de restart** que está causando loop

## Solução Necessária

Preciso **desabilitar ou configurar corretamente** o health check / liveness probe no Easypanel.

### Configuração correta do Health Check:
- **Path**: `/health`
- **Port**: `8000`
- **Initial Delay**: `10s` (dar tempo para o app iniciar)
- **Period**: `30s`
- **Timeout**: `5s`
- **Success Threshold**: `1`
- **Failure Threshold**: `3`

### Ou simplesmente:
**Desabilitar completamente** o health check por enquanto para testar.

## Pedido de Ajuda

Como posso:
1. Desabilitar o health check no Easypanel?
2. Ou configurar o health check corretamente?
3. Ou identificar o que está causando o shutdown do container?

## Informações Adicionais

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **Python**: 3.11-slim
- **Repositório**: https://github.com/Vinicius-Ikehara/portfolio
- **Branch**: claude/fix-portfolio-issue-0186451B928g2p2iMbFrVQTJ

## Teste Rápido

Para verificar que o backend funciona, você pode executar localmente:

```bash
docker build -t portfolio-backend ./backend
docker run -p 8000:8000 -e CORS_ORIGINS='["http://localhost:3000"]' -e DEBUG=True portfolio-backend
```

E acessar: http://localhost:8000/health

Isso comprovará que o problema é especificamente a configuração do Easypanel.
