@echo off
echo.
echo ========================================
echo  VERIFICANDO PRE-REQUISITOS
echo ========================================
echo.

set MISSING=0

REM Verificar Python
echo [1/3] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] PYTHON NAO INSTALADO
    echo     Baixe e instale Python 3.9 ou superior em:
    echo     https://www.python.org/downloads/
    echo     IMPORTANTE: Marque "Add Python to PATH" durante instalacao
    echo.
    set MISSING=1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [OK] Python instalado: %PYTHON_VERSION%
)

REM Verificar Node.js
echo.
echo [2/3] Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] NODE.JS NAO INSTALADO
    echo     Baixe e instale Node.js 18 ou superior em:
    echo     https://nodejs.org/
    echo.
    set MISSING=1
) else (
    for /f "tokens=1" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
    echo [OK] Node.js instalado: %NODE_VERSION%
)

REM Verificar MongoDB
echo.
echo [3/3] Verificando MongoDB...
mongod --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] MONGODB NAO ENCONTRADO ^(opcional se usar MongoDB Atlas^)
    echo     Opcao 1 ^(Recomendado^): Use MongoDB Atlas ^(gratis, cloud^)
    echo                             https://www.mongodb.com/cloud/atlas
    echo     Opcao 2: Instale MongoDB localmente
    echo                             https://www.mongodb.com/try/download/community
    echo.
) else (
    for /f "tokens=3" %%i in ('mongod --version 2^>^&1 ^| findstr "version"') do set MONGO_VERSION=%%i
    echo [OK] MongoDB instalado: %MONGO_VERSION%
)

echo.
echo ========================================
if %MISSING%==1 (
    echo  RESULTADO: FALTAM REQUISITOS OBRIGATORIOS
    echo ========================================
    echo.
    echo Por favor, instale os itens marcados com [X] antes de continuar.
    echo.
    exit /b 1
) else (
    echo  RESULTADO: TODOS REQUISITOS OK
    echo ========================================
    echo.
    exit /b 0
)
