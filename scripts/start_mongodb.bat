@echo off
title Web Scrapper - MongoDB Local
echo.
echo ========================================
echo  INICIANDO MONGODB LOCAL
echo ========================================
echo.

REM Verificar se MongoDB esta instalado
mongod --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: MongoDB nao encontrado!
    echo.
    echo Opcoes:
    echo   1. Instale MongoDB Community Server
    echo      https://www.mongodb.com/try/download/community
    echo   2. OU use MongoDB Atlas ^(cloud gratuito^)
    echo      https://www.mongodb.com/cloud/atlas
    echo.
    pause
    exit /b 1
)

REM Criar pasta de dados se nao existir
if not exist "mongodb_data" (
    echo Criando pasta para dados do MongoDB...
    mkdir "mongodb_data"
)

echo.
echo Iniciando MongoDB na porta 27017...
echo Pasta de dados: %cd%\mongodb_data
echo Pressione Ctrl+C para parar o servidor
echo.
mongod --dbpath "mongodb_data"
