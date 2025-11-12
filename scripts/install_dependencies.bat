@echo off
echo.
echo ========================================
echo  INSTALANDO DEPENDENCIAS
echo ========================================
echo.

REM Verificar se estamos no diretorio correto
if not exist "main.py" (
    echo ERRO: Execute este script a partir da raiz do projeto!
    pause
    exit /b 1
)

echo [1/2] Instalando dependencias Python...
echo.
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ERRO: Falha ao atualizar pip
    pause
    exit /b 1
)

echo.
echo Instalando lxml ^(pre-compilado^)...
pip install lxml --only-binary :all:
if %errorlevel% neq 0 (
    echo AVISO: Falha ao instalar lxml, sera instalado com o resto
)

echo.
echo Instalando dependencias do projeto...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ERRO: Falha ao instalar algumas dependencias
    echo.
    echo Solucoes possiveis:
    echo 1. Execute este script como Administrador
    echo 2. Verifique sua conexao com internet
    echo 3. Use Python 3.10, 3.11 ou 3.12
    echo 4. Atualize Python: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Dependencias Python instaladas com sucesso!

echo.
echo [2/2] Instalando dependencias Node.js...
echo.
cd frontend
if not exist "package.json" (
    echo ERRO: Arquivo package.json nao encontrado!
    cd ..
    pause
    exit /b 1
)

call npm install
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias Node.js
    cd ..
    pause
    exit /b 1
)
cd ..
echo [OK] Dependencias Node.js instaladas com sucesso!

echo.
echo ========================================
echo  INSTALACAO CONCLUIDA!
echo ========================================
echo.
exit /b 0
