#!/bin/bash

# Script de configuração do ambiente Docker para Web Scraper UniSER
echo "🐳 Configurando ambiente Docker para Web Scraper UniSER..."

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    echo "Visite: https://docs.docker.com/get-docker/"
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
    echo "Visite: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker e Docker Compose estão instalados"

# Criar arquivo .env se não existir
if [ ! -f ../.env ]; then
    echo "📝 Criando arquivo .env..."
    cat > ../.env << EOF
# Configurações do MongoDB
MONGODB_URL=mongodb://admin:senha123@localhost:27017/web-scraper-uniser?authSource=admin

# Configurações da API
API_HOST=0.0.0.0
API_PORT=8000

# Configurações do Frontend
REACT_APP_API_URL=http://localhost:8000

# Configurações de Debug
DEBUG=true
PYTHONUNBUFFERED=1
EOF
    echo "✅ Arquivo .env criado"
else
    echo "✅ Arquivo .env já existe"
fi

# Criar diretórios necessários
echo "📁 Criando diretórios necessários..."
mkdir -p ../exports ../lattes_cache ../logs ../db

echo "✅ Configuração concluída!"
echo ""
echo "🚀 Para iniciar a aplicação, execute:"
echo "   cd docker"
echo "   docker-compose up -d"
echo ""
echo "📱 Acesse a aplicação em:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   MongoDB: localhost:27017"