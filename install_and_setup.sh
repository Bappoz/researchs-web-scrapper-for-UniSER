#!/bin/bash

echo "========================================"
echo " Web Scraper UniSER - Instalacao e Inicializacao"
echo "========================================"
echo ""
echo "Este script ira instalar as dependencias e preparar o projeto."
echo "Certifique-se de ter Python 3.12+, Node.js 18+ e MongoDB instalados."
echo ""
read -p "Pressione Enter para continuar..."

echo ""
echo "1. Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python3 nao encontrado. Instale Python 3.12+ primeiro."
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "Mac: brew install python3"
    exit 1
fi
echo "Python OK."

echo ""
echo "2. Verificando Node.js..."
if ! command -v node &> /dev/null; then
    echo "ERRO: Node.js nao encontrado. Instale Node.js 18+ primeiro."
    echo "Baixe em: https://nodejs.org/"
    echo "Ou use: curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs"
    exit 1
fi
echo "Node.js OK."

echo ""
echo "3. Verificando MongoDB..."
if ! command -v mongod &> /dev/null; then
    echo "AVISO: MongoDB nao encontrado. Use MongoDB Atlas (cloud) ou instale localmente."
    echo "MongoDB Atlas: https://www.mongodb.com/cloud/atlas"
    echo "Ubuntu: sudo apt install mongodb"
    echo "Mac: brew install mongodb-community"
    echo ""
    read -p "Pressione Enter para continuar sem MongoDB local..."
else
    echo "MongoDB OK."
fi

echo ""
echo "4. Instalando dependencias Python..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao instalar dependencias Python."
    exit 1
fi
echo "Dependencias Python instaladas."

echo ""
echo "5. Instalando dependencias Node.js..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao instalar dependencias Node.js."
    cd ..
    exit 1
fi
cd ..
echo "Dependencias Node.js instaladas."

echo ""
echo "6. Verificando arquivo .env..."
if [ ! -f .env ]; then
    echo "AVISO: Arquivo .env nao encontrado."
    echo "Copie .env.example para .env e configure suas chaves."
    echo "Exemplo: SERPAPI_KEY=sua_chave_aqui"
    echo ""
    read -p "Pressione Enter para continuar..."
else
    echo "Arquivo .env encontrado."
fi

echo ""
echo "========================================"
echo " INSTALACAO CONCLUIDA!"
echo "========================================"
echo ""
echo "Para iniciar o projeto:"
echo "1. Configure o arquivo .env com suas chaves API"
echo "2. Inicie o MongoDB (se usando local): sudo systemctl start mongod"
echo "3. Execute: ./start_backend.sh"
echo "4. Em outro terminal: ./start_frontend.sh"
echo ""
echo "Ou use o Docker (mais facil):"
echo "cd docker"
echo "docker-compose up -d"
echo ""