@echo off
title Web Scrapper - Instalacao e Configuracao
color 0A

:MENU
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║        WEB SCRAPPER - SISTEMA DE PESQUISA ACADEMICA           ║
echo ║              Google Scholar + Plataforma Lattes                ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo  Escolha uma opcao:
echo.
echo  [1] Verificar pre-requisitos ^(Python, Node.js, MongoDB^)
echo  [2] Instalar dependencias do projeto
echo  [3] Iniciar MongoDB local ^(se instalado^)
echo  [4] Iniciar Backend ^(servidor API^)
echo  [5] Iniciar Frontend ^(interface web^)
echo  [6] Iniciar TUDO ^(Backend + Frontend^)
echo  [7] Ver guia de uso rapido
echo  [0] Sair
echo.
set /p opcao="Digite o numero da opcao: "

if "%opcao%"=="1" goto CHECK
if "%opcao%"=="2" goto INSTALL
if "%opcao%"=="3" goto MONGODB
if "%opcao%"=="4" goto BACKEND
if "%opcao%"=="5" goto FRONTEND
if "%opcao%"=="6" goto ALL
if "%opcao%"=="7" goto HELP
if "%opcao%"=="0" goto EXIT
goto MENU

:CHECK
cls
echo.
call scripts\check_requirements.bat
echo.
pause
goto MENU

:INSTALL
cls
echo.
echo Primeiro, vamos verificar os pre-requisitos...
call scripts\check_requirements.bat
if %errorlevel% neq 0 (
    echo.
    echo Corrija os problemas acima antes de instalar dependencias.
    pause
    goto MENU
)
echo.
echo Pre-requisitos OK! Instalando dependencias...
echo.
call scripts\install_dependencies.bat
echo.
pause
goto MENU

:MONGODB
cls
echo.
echo IMPORTANTE: Se voce usa MongoDB Atlas ^(cloud^), nao precisa deste passo.
echo Configure o MONGODB_URI no arquivo .env e pule esta opcao.
echo.
pause
start "MongoDB Local" cmd /k scripts\start_mongodb.bat
echo.
echo MongoDB iniciado em uma nova janela!
timeout /t 3 >nul
goto MENU

:BACKEND
cls
echo.
start "Backend - API" cmd /k scripts\start_backend.bat
echo.
echo Backend iniciado em uma nova janela!
echo Aguarde alguns segundos para o servidor iniciar...
timeout /t 3 >nul
goto MENU

:FRONTEND
cls
echo.
start "Frontend - Interface Web" cmd /k scripts\start_frontend.bat
echo.
echo Frontend iniciado em uma nova janela!
echo O navegador abrira automaticamente em http://localhost:5173
timeout /t 3 >nul
goto MENU

:ALL
cls
echo.
echo ========================================
echo  INICIANDO SISTEMA COMPLETO
echo ========================================
echo.
echo [1/2] Iniciando Backend...
start "Backend - API" cmd /k scripts\start_backend.bat
timeout /t 5 >nul
echo [OK] Backend iniciado!
echo.
echo [2/2] Iniciando Frontend...
start "Frontend - Interface Web" cmd /k scripts\start_frontend.bat
echo [OK] Frontend iniciado!
echo.
echo ========================================
echo  SISTEMA PRONTO!
echo ========================================
echo.
echo O sistema esta rodando em:
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo.
echo O navegador abrira automaticamente.
echo.
pause
goto MENU

:HELP
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    GUIA DE USO RAPIDO                          ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo  PRIMEIRA VEZ USANDO O SISTEMA:
echo  ────────────────────────────────────────────────────────────────
echo  1. Execute opcao [1] para verificar pre-requisitos
echo  2. Se faltar algo, instale e execute opcao [1] novamente
echo  3. Execute opcao [2] para instalar dependencias do projeto
echo  4. Configure o MongoDB:
echo     - MongoDB Atlas ^(cloud^): Configure MONGODB_URI no .env
echo     - MongoDB local: Execute opcao [3] para iniciar
echo  5. Execute opcao [6] para iniciar Backend + Frontend
echo.
echo  USO DIARIO ^(apos configuracao inicial^):
echo  ────────────────────────────────────────────────────────────────
echo  1. Se usar MongoDB local, execute opcao [3] primeiro
echo  2. Execute opcao [6] para iniciar tudo de uma vez
echo  3. Acesse http://localhost:5173 no navegador
echo.
echo  COMO USAR O SISTEMA WEB:
echo  ────────────────────────────────────────────────────────────────
echo  1. Pesquisar por nome: Busca manual no Google Academico
echo  2. Pesquisar por link: Cole o link do perfil do Google Scholar
echo  3. Ver resultados: Metricas, publicacoes e dados Lattes
echo  4. Exportar Excel: Gera arquivo com todos os dados
echo  5. Historico: Ver todos os pesquisadores ja consultados
echo  6. Dark Mode: Clique no icone sol/lua no topo
echo  7. Ajuda: Clique no botao "Ajuda" para tutoriais completos
echo.
echo  SOLUCAO DE PROBLEMAS:
echo  ────────────────────────────────────────────────────────────────
echo  - Backend nao inicia: Verifique se MongoDB esta rodando
echo  - Frontend nao abre: Verifique se Backend esta rodando
echo  - Erro de dependencias: Execute opcao [2] novamente
echo  - Excel vazio: Certifique-se de fazer uma busca primeiro
echo.
echo  REQUISITOS MINIMOS:
echo  ────────────────────────────────────────────────────────────────
echo  - Python 3.9 ou superior
echo  - Node.js 18 ou superior
echo  - MongoDB ^(local ou Atlas cloud^)
echo  - 4GB RAM minimo
echo  - Conexao com internet ^(para acessar Google Scholar e Lattes^)
echo.
pause
goto MENU

:EXIT
cls
echo.
echo Encerrando...
echo Obrigado por usar o Web Scrapper!
timeout /t 2 >nul
exit

