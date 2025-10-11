# Makefile para Web Scraper UniSER
# Facilita comandos Docker comuns

.PHONY: help setup up down logs restart build clean backup

# Comando padrão
help:
	@echo "🔬 Web Scraper UniSER - Comandos Disponíveis:"
	@echo ""
	@echo "  🚀 Inicialização:"
	@echo "    make setup     - Configurar ambiente inicial"
	@echo "    make up        - Iniciar aplicação"
	@echo "    make build     - Construir containers"
	@echo ""
	@echo "  📊 Gerenciamento:"
	@echo "    make down      - Parar aplicação"
	@echo "    make restart   - Reiniciar aplicação"
	@echo "    make logs      - Ver logs em tempo real"
	@echo "    make status    - Ver status dos containers"
	@echo ""
	@echo "  🛠️ Desenvolvimento:"
	@echo "    make dev       - Iniciar em modo desenvolvimento"
	@echo "    make shell     - Acessar terminal do backend"
	@echo "    make mongo     - Acessar MongoDB shell"
	@echo ""
	@echo "  🔧 Manutenção:"
	@echo "    make clean     - Limpar containers e volumes"
	@echo "    make backup    - Fazer backup do MongoDB"
	@echo "    make health    - Verificar saúde da aplicação"

# Configuração inicial
setup:
	@echo "📝 Configurando ambiente..."
	@cd docker && chmod +x setup.sh && ./setup.sh

# Iniciar aplicação
up:
	@echo "🚀 Iniciando Web Scraper UniSER..."
	@cd docker && docker-compose up -d
	@echo "✅ Aplicação iniciada!"
	@echo "🌐 Frontend: http://localhost:3000"
	@echo "🔧 Backend: http://localhost:8000"

# Construir containers
build:
	@echo "🔨 Construindo containers..."
	@cd docker && docker-compose build --no-cache

# Parar aplicação
down:
	@echo "⏹️ Parando aplicação..."
	@cd docker && docker-compose down

# Ver logs
logs:
	@echo "📋 Mostrando logs em tempo real..."
	@cd docker && docker-compose logs -f

# Reiniciar aplicação
restart:
	@echo "🔄 Reiniciando aplicação..."
	@cd docker && docker-compose restart

# Ver status
status:
	@echo "📊 Status dos containers:"
	@cd docker && docker-compose ps

# Modo desenvolvimento
dev:
	@echo "🛠️ Iniciando em modo desenvolvimento..."
	@cd docker && docker-compose up

# Acessar shell do backend
shell:
	@echo "💻 Acessando terminal do backend..."
	@cd docker && docker-compose exec backend bash

# Acessar MongoDB
mongo:
	@echo "💾 Acessando MongoDB shell..."
	@cd docker && docker-compose exec mongodb mongosh web-scraper-uniser

# Verificar saúde
health:
	@echo "🔍 Verificando saúde da aplicação..."
	@cd docker && python healthcheck.py

# Backup do MongoDB
backup:
	@echo "💾 Fazendo backup do MongoDB..."
	@mkdir -p backup
	@cd docker && docker-compose exec mongodb mongodump --db web-scraper-uniser --out /backup
	@echo "✅ Backup concluído em ./backup/"

# Limpeza completa
clean:
	@echo "🧹 Limpando containers e volumes..."
	@cd docker && docker-compose down -v
	@docker system prune -f
	@echo "✅ Limpeza concluída!"

# Comandos para diferentes sistemas operacionais
ifeq ($(OS),Windows_NT)
    # Comandos específicos para Windows
    setup-win:
		@cd docker && setup.bat
else
    # Comandos para Unix/Linux/Mac
    setup-unix:
		@cd docker && chmod +x setup.sh && ./setup.sh
endif