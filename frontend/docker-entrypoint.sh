#!/bin/sh

# Script para substituir variáveis de ambiente no runtime

# URL padrão da API (pode ser sobrescrita por variável de ambiente)
API_URL="${VITE_API_URL:-http://localhost:8000}"

echo "Configurando API URL: $API_URL"

# Encontrar todos os arquivos JavaScript no build
find /usr/share/nginx/html/assets -type f -name "*.js" -exec sed -i "s|http://localhost:8000|$API_URL|g" {} \;

echo "Configuração concluída!"

# Executar comando passado (nginx)
exec "$@"
