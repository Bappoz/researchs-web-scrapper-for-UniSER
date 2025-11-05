@echo off
echo ========================================
echo  Web Scraper UniSER - Instalacao e Inicializacao
echo ========================================
echo.
echo Este script ira instalar as dependencias e iniciar o projeto.
echo Certifique-se de ter Python 3.12+, Node.js 18+ e MongoDB instalados.
echo.
echo Pressione qualquer tecla para continuar...
pause >nul

echo.
echo 1. Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado. Instale Python 3.12+ primeiro.
    echo Baixe em: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo Python OK.

echo.
echo 2. Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Node.js nao encontrado. Instale Node.js 18+ primeiro.
    echo Baixe em: https://nodejs.org/
    pause
    exit /b 1
)
echo Node.js OK.

echo.
echo 3. Verificando MongoDB...
mongod --version >nul 2>&1
if %errorlevel% neq 0 (
    echo AVISO: MongoDB nao encontrado. Use MongoDB Atlas (cloud) ou instale localmente.
    echo MongoDB Atlas: https://www.mongodb.com/cloud/atlas
    echo Instalacao local: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
    echo.
    echo Pressione qualquer tecla para continuar sem MongoDB local...
    pause >nul
) else (
    echo MongoDB OK.
)

echo.
echo 4. Instalando dependencias Python...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias Python.
    pause
    exit /b 1
)
echo Dependencias Python instaladas.

echo.
echo 5. Instalando dependencias Node.js...
cd frontend
npm install
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias Node.js.
    cd ..
    pause
    exit /b 1
)
cd ..
echo Dependencias Node.js instaladas.

echo.
echo 6. Verificando arquivo .env...
if not exist .env (
    echo AVISO: Arquivo .env nao encontrado.
    echo Copie .env.example para .env e configure suas chaves.
    echo Exemplo: SERPAPI_KEY=sua_chave_aqui
    echo.
    echo Pressione qualquer tecla para continuar...
    pause >nul
) else (
    echo Arquivo .env encontrado.
)

echo.
echo ========================================
echo  INSTALACAO CONCLUIDA!
echo ========================================
echo.
echo Para iniciar o projeto:
echo 1. Configure o arquivo .env com suas chaves API
echo 2. Inicie o MongoDB (se usando local)
echo 3. Execute: start_backend.bat
echo 4. Em outro terminal: start_frontend.bat
echo.
echo Ou use o Docker (mais facil):
echo cd docker
echo docker-compose up -d
echo.
pause