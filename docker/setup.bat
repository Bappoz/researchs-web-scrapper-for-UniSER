@echo off
REM Script de configuração do ambiente Docker para Web Scraper UniSER (Windows)
echo 🐳 Configurando ambiente Docker para Web Scraper UniSER...

REM Verificar se Docker está instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker não está instalado. Por favor, instale o Docker primeiro.
    echo Visite: https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

REM Verificar se Docker Compose está instalado
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro.
    echo Visite: https://docs.docker.com/compose/install/
    pause
    exit /b 1
)

echo ✅ Docker e Docker Compose estão instalados

REM Criar arquivo .env se não existir
if not exist "..\.env" (
    echo 📝 Criando arquivo .env...
    (
        echo # Configurações do MongoDB
        echo MONGODB_URL=mongodb://admin:senha123@localhost:27017/web-scraper-uniser?authSource=admin
        echo.
        echo # Configurações da API
        echo API_HOST=0.0.0.0
        echo API_PORT=8000
        echo.
        echo # Configurações do Frontend
        echo REACT_APP_API_URL=http://localhost:8000
        echo.
        echo # Configurações de Debug
        echo DEBUG=true
        echo PYTHONUNBUFFERED=1
    ) > ..\.env
    echo ✅ Arquivo .env criado
) else (
    echo ✅ Arquivo .env já existe
)

REM Criar diretórios necessários
echo 📁 Criando diretórios necessários...
if not exist "..\exports" mkdir "..\exports"
if not exist "..\lattes_cache" mkdir "..\lattes_cache"
if not exist "..\logs" mkdir "..\logs"
if not exist "..\db" mkdir "..\db"

echo ✅ Configuração concluída!
echo.
echo 🚀 Para iniciar a aplicação, execute:
echo    cd docker
echo    docker-compose up -d
echo.
echo 📱 Acesse a aplicação em:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    MongoDB: localhost:27017
pause