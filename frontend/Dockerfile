# Dockerfile para Frontend Vue.js

# Etapa 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar package files
COPY package*.json ./

# Instalar dependências
RUN npm install --frozen-lockfile || npm install

# Copiar código fonte
COPY . .

# Accept build arguments
ARG VITE_API_URL
ARG VITE_REBUILD_TIMESTAMP

# Set as environment variables for build
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_REBUILD_TIMESTAMP=$VITE_REBUILD_TIMESTAMP

# Build da aplicação com variáveis de ambiente
RUN npm run build

# Etapa 2: Servir com Nginx
FROM nginx:alpine

# Instalar gettext para envsubst
RUN apk add --no-cache gettext

# Copiar build do Vue
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuração do nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar script de entrypoint
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Expor porta
EXPOSE 80

# Script que substitui variáveis e inicia nginx
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
