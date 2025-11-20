# Dockerfile para Frontend Vue.js

# Etapa 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Argumentos de build (URL da API)
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

# Copiar package files
COPY package*.json ./

# Instalar dependências
RUN npm ci

# Copiar código fonte
COPY . .

# Build da aplicação
RUN npm run build

# Etapa 2: Servir com Nginx
FROM nginx:alpine

# Copiar build do Vue
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuração do nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expor porta
EXPOSE 80

# Iniciar nginx
CMD ["nginx", "-g", "daemon off;"]
