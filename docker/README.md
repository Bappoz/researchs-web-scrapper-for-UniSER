# Docker Setup - Web Scraper UniSER

Este diretório contém a configuração Docker completa para containerizar e executar a aplicação Web Scraper UniSER.

## 🐳 Estrutura Docker

### Containers

- **MongoDB** (mongo:7.0): Banco de dados NoSQL
- **Backend** (Python 3.12 + FastAPI): API de scraping e processamento
- **Frontend** (React + Nginx): Interface web do usuário

### Arquivos Principais

- `docker-compose.yml`: Orquestração dos containers
- `Dockerfile.backend`: Container Python com Chrome/Selenium
- `Dockerfile.frontend`: Container React com build otimizado
- `nginx.conf`: Configuração proxy reverso
- `init-mongo.js`: Inicialização do banco MongoDB

## 🚀 Instalação e Execução

### Pré-requisitos

- Docker Desktop instalado
- Docker Compose disponível
- Portas 3000, 8000 e 27017 livres

### Método 1: Scripts Automatizados

#### Windows

```bash
# Navegar para a pasta docker
cd docker

# Executar script de setup
./setup.bat
```

#### Linux/macOS

```bash
# Navegar para a pasta docker
cd docker

# Executar script de setup
chmod +x setup.sh
./setup.sh
```

### Método 2: Manual

```bash
# 1. Navegar para a pasta docker
cd docker

# 2. Construir e iniciar todos os containers
docker-compose up -d

# 3. Verificar status dos containers
docker-compose ps

# 4. Visualizar logs (opcional)
docker-compose logs -f
```

## 📋 Verificação da Instalação

### Status dos Containers

```bash
docker-compose ps
```

Todos os containers devem mostrar status "Up".

### Testes de Conectividade

```bash
# Teste do Frontend (deve retornar 200)
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000

# Teste do Backend (deve retornar 200)
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health

# Teste do MongoDB
docker-compose exec mongodb mongosh --eval "db.runCommand('ping')"
```

### Acessos da Aplicação

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **MongoDB**: localhost:27017

## 🔧 Comandos Úteis

### Gerenciamento dos Containers

```bash
# Parar todos os containers
docker-compose down

# Reiniciar containers
docker-compose restart

# Visualizar logs específicos
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mongodb

# Reconstruir containers (após mudanças)
docker-compose build
docker-compose up -d
```

### Limpeza e Manutenção

```bash
# Parar e remover containers, redes e volumes
docker-compose down -v

# Limpar imagens e cache do Docker
docker system prune -f

# Rebuild completo (limpo)
docker-compose build --no-cache
docker-compose up -d
```

### Acesso aos Containers

```bash
# Acessar container do backend
docker-compose exec backend bash

# Acessar container do MongoDB
docker-compose exec mongodb mongosh

# Acessar container do frontend
docker-compose exec frontend sh
```

## 📊 Volumes e Persistência

### Volumes Configurados

- `mongodb_data`: Dados persistentes do MongoDB
- `../exports`: Arquivos Excel exportados
- `../lattes_cache`: Cache dos dados Lattes
- `../logs`: Logs da aplicação

### Backup dos Dados

```bash
# Backup do MongoDB
docker-compose exec mongodb mongodump --out /data/backup

# Copiar backup para host
docker cp webscraper-mongodb:/data/backup ./backup
```

## 🌐 Configurações de Rede

### Rede Interna

- Nome: `webscraper-network`
- Tipo: bridge
- Comunicação entre containers via nomes de serviço

### Portas Expostas

- Frontend: `3000:80`
- Backend: `8000:8000`
- MongoDB: `27017:27017`

## 🔐 Configurações de Segurança

### MongoDB

- Usuário: `admin`
- Senha: `senha123` (configurável via .env)
- Banco: `web-scraper-uniser`

### Variáveis de Ambiente

```bash
# Backend
MONGODB_URL=mongodb://admin:senha123@mongodb:27017/web-scraper-uniser?authSource=admin
PYTHONPATH=/app
PYTHONUNBUFFERED=1

# Frontend (construção)
VITE_API_URL=http://localhost:8000
```

## 🛠️ Troubleshooting

### Problemas Comuns

#### Container não inicia

```bash
# Verificar logs detalhados
docker-compose logs [nome-do-container]

# Verificar recursos disponíveis
docker system df
```

#### Porta em uso

```bash
# Verificar processos usando as portas
netstat -tlnp | grep :3000
netstat -tlnp | grep :8000
netstat -tlnp | grep :27017

# Parar processo específico ou alterar porta no docker-compose.yml
```

#### Problemas de build

```bash
# Limpar cache e rebuild
docker-compose down
docker system prune -f
docker-compose build --no-cache
docker-compose up -d
```

#### MongoDB não conecta

```bash
# Verificar status do MongoDB
docker-compose exec mongodb mongosh --eval "db.runCommand('ping')"

# Reiniciar container específico
docker-compose restart mongodb
```

### Performance

#### Otimizações

- Use SSD para melhor performance do MongoDB
- Aloque pelo menos 4GB de RAM para Docker
- Configure `vm.max_map_count` no Linux se necessário

#### Monitoramento

```bash
# Uso de recursos dos containers
docker stats

# Logs em tempo real
docker-compose logs -f --tail=100
```

## 🔄 Atualizações e Desenvolvimento

### Workflow de Desenvolvimento

1. Faça alterações no código
2. Rebuild do container específico:
   ```bash
   docker-compose build backend  # ou frontend
   docker-compose up -d
   ```

### Deploy em Produção

1. Configure variáveis de ambiente apropriadas
2. Use volumes externos para persistência
3. Configure proxy reverso (nginx externo)
4. Implemente backup automatizado do MongoDB

## 📞 Suporte

Para problemas específicos:

1. Verifique os logs: `docker-compose logs`
2. Confirme status: `docker-compose ps`
3. Teste conectividade conforme seção "Verificação"
4. Consulte a documentação do Docker e Docker Compose

---

**Versão**: 1.0  
**Última atualização**: Outubro 2025  
**Compatibilidade**: Docker 20+, Docker Compose 2.0+
