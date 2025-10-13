# 🔬 Web Scraper UniSER - Busca de Pesquisadores Acadêmicos

<div align="center">

**Sistema completo para encontrar informações de pesquisadores e trabalhos científicos**

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![React](https://img.shields.io/badge/React-18+-61DAFB.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)
![Status](https://img.shields.io/badge/Status-Funcionando-green.svg)

_Solução completa para pesquisa acadêmica com Google Scholar e SerpAPI_

</div>

---

## 🚀 Instalação e Configuração

### Pré-requisitos

- **Python 3.12+**
- **Node.js 18+** e **npm**
- **MongoDB** (local ou remoto)
- **Google Chrome** (para Selenium)
- **Conta SerpAPI** (para Google Scholar)

### � Instalação Passo a Passo

#### 1️⃣ Clone o Repositório

```bash
git clone https://github.com/Bappoz/web-scrapper.git
cd web-scrapper
```

#### 2️⃣ Configuração do Backend (Python)

**Instale as dependências:**

```bash
# Crie um ambiente virtual (recomendado)
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

**Configure as variáveis de ambiente:**

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas configurações
```

#### 3️⃣ Configuração da API SerpAPI

**🔑 Obtenha sua chave da SerpAPI:**

1. **Cadastre-se gratuitamente** em: https://serpapi.com/users/sign_up
2. **Confirme seu email** e faça login
3. **Acesse seu dashboard**: https://serpapi.com/dashboard
4. **Copie sua API Key** (encontrada na seção "Your Private API Key")

**📝 Configure no arquivo .env:**

```bash
# Abra o arquivo .env e encontre a linha:
SERPAPI_KEY=your_serpapi_key_here

# Substitua por sua chave real:
SERPAPI_KEY=sua_chave_serpapi_aqui_1234567890abcdef

# Outras configurações importantes da SerpAPI:
REQUEST_DELAY=2.0        # Intervalo entre requisições (evita rate limit)
MAX_RETRIES=3           # Tentativas em caso de erro
TIMEOUT=30              # Timeout das requisições
```

**💡 Dicas sobre SerpAPI:**

- **Plano gratuito**: 100 buscas/mês (suficiente para testes)
- **Rate limit**: Respeite o intervalo entre requisições
- **Precisão**: SerpAPI oferece dados mais estáveis que scraping direto
- **Custo**: Planos pagos começam em $50/mês para uso intensivo

#### 4️⃣ Configuração do Frontend (React)

```bash
# Entre na pasta do frontend
cd frontend

# Instale as dependências
npm install

# Configure as variáveis de ambiente
echo "VITE_API_URL=http://localhost:8000" > .env.local
```

#### 5️⃣ Configuração do MongoDB

**Opção A - MongoDB Local:**


## Instale o MongoDB Community Edition
Windows: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
Linux: https://docs.mongodb.com/manual/administration/install-on-linux/
Mac: brew install mongodb-community

# Inicie o serviço
# Windows: net start MongoDB
# Linux/Mac: sudo systemctl start mongod

# Configure no .env:
MONGODB_URI=mongodb://localhost:27017/web-scraper-uniser
```

**Opção B - MongoDB Atlas (Cloud):**

```bash
# 1. Crie uma conta gratuita em: https://www.mongodb.com/cloud/atlas
# 2. Crie um cluster gratuito
# 3. Configure um usuário de banco de dados
# 4. Obtenha a string de conexão
# 5. Configure no .env:
MONGODB_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/web-scraper-uniser
```

### 🏃‍♂️ Executando a Aplicação

#### 1️⃣ Inicie o Backend

```bash
# Na pasta raiz do projeto, com o ambiente virtual ativo
# Ou usando o script python:
python -m src.api
```

#### 2️⃣ Inicie o Frontend

```bash
# Em outro terminal, na pasta frontend
cd frontend
npm run dev

# Ou para build de produção:
npm run build
npm run preview
```

### 📱 Acesso à Aplicação

- **🌐 Interface Web**: http://localhost:5173 (dev) ou http://localhost:4173 (prod)
- **🔧 API Backend**: http://localhost:8000
- **📊 Documentação API**: http://localhost:8000/docs

---

## 🐳 Instalação Alternativa com Docker

Se preferir uma instalação simplificada sem configurar dependências manualmente:

### Pré-requisitos Docker

- **Docker** (versão 20.10+)
- **Docker Compose** (versão 2.0+)

### Instalação Docker

```bash
# 1. Clone o repositório (se ainda não fez)
git clone https://github.com/Bappoz/web-scrapper.git
cd web-scrapper

# 2. Configure a chave SerpAPI no .env
cp .env.example .env
# Edite o .env e adicione sua SERPAPI_KEY

# 3. Inicie com Docker
cd docker
docker-compose up -d

# Acesse em: http://localhost:3000
```

**📋 Mais detalhes**: Consulte `/docker/README.md` para documentação completa do Docker.

---

## 🎯 Como Usar (Busca no Google Acadêmico)

### 1. Acesse a Interface

- Abra seu navegador em `http://localhost:3000`
- Você verá a interface moderna do Web Scraper UniSER

### 2. Realize uma Busca

- **Digite um nome**: Ex: "Maria Silva", "João Santos", "aging research"
- **Selecione "Google Scholar"** na opção de plataforma
- **Configure parâmetros**:
  - Número de publicações: 20 (recomendado)
  - Busca por autor: Ativada
- **Clique em "� Buscar"**

### 3. Visualize os Resultados

A interface mostrará:

- **👤 Perfil do Pesquisador**: Nome, instituição, áreas de pesquisa
- **� Métricas Acadêmicas**: H-index, i10-index, total de citações
- **📚 Lista de Publicações**: Títulos, autores, anos, citações
- **🎯 Filtros por Palavras-chave**: Pesquisas relacionadas ao envelhecimento

### 4. Exporte os Dados

- **Clique em "📊 Exportar Excel"**
- **Escolha o formato**: Individual ou Consolidado
- **Download automático** do arquivo Excel profissional

---

## 📊 Formatos de Exportação

### 📄 Excel Individual

- **Aba "Publicações"**: Uma linha por publicação
- **Aba "Pesquisador"**: Dados completos do autor
- **Colunas incluem**: H-index, i10-index, citações, links

### � Excel Consolidado

- **Aba "Resumo"**: Estatísticas gerais
- **Aba "Pesquisadores"**: Lista de todos os autores encontrados
- **Aba "Publicações"**: Todas as publicações consolidadas
- **Aba "Métricas"**: Análises e indicadores de impacto

---

## 🔧 Comandos de Desenvolvimento

### Gerenciar a Aplicação

```bash
# Iniciar backend (pasta raiz)
uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload

# Iniciar frontend (pasta frontend)
cd frontend
npm run dev

# Verificar status da API
curl http://localhost:8000/health

# Ver logs do backend
tail -f logs/app.log

# Verificar MongoDB
mongosh --eval "db.runCommand('ping')"
```

# Verificar status dos containers

docker-compose ps

````

### Desenvolvimento e Debug

```bash
# Modo desenvolvimento com debug
DEBUG=true uvicorn src.api:app --reload

# Instalar novas dependências Python
pip install nova-dependencia
pip freeze > requirements.txt

# Instalar novas dependências React
cd frontend
npm install nova-dependencia
````

### Backup e Limpeza

```bash
# Backup do MongoDB
mongodump --db web-scraper-uniser --out backup/

# Limpar cache do Lattes
rm -rf lattes_cache/*

# Limpar logs
rm -rf logs/*

# Atualizar dependências
pip install --upgrade -r requirements.txt
cd frontend && npm update
```

---

## 🔍 Estrutura do Sistema

### 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Frontend     │────│     Backend     │────│    MongoDB      │
│   React + TS    │    │  FastAPI + Py   │    │   Database      │
│  localhost:5173 │    │ localhost:8000  │    │ localhost:27017 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 📁 Estrutura de Pastas

```
web-scrapper/
├── 🎨 frontend/               # Interface React
│   ├── src/                   # Código fonte React
│   ├── public/                # Arquivos estáticos
│   ├── package.json           # Dependências Node.js
│   └── vite.config.ts         # Configuração Vite
├── ⚙️ src/                    # Backend Python (FastAPI)
│   ├── api.py                 # Servidor FastAPI principal
│   ├── scraper/               # Módulos de scraping
│   ├── models/                # Modelos de dados
│   ├── export/                # Geração de Excel
│   └── services/              # Serviços e business logic
├── 🐳 docker/                 # Configurações Docker (opcional)
│   ├── docker-compose.yml     # Orquestração dos containers
│   ├── README.md              # Documentação Docker
│   └── setup scripts         # Scripts de configuração
├── 📊 exports/                # Arquivos Excel gerados
├── 💾 lattes_cache/           # Cache dos dados Lattes
├── � logs/                   # Logs da aplicação
├── 📋 requirements.txt        # Dependências Python
├── 🔧 .env.example            # Exemplo de configurações
└── � README.md               # Esta documentação
```

---

## ⚙️ Configurações Detalhadas (.env)

### 🔑 Configurações Essenciais

```bash
# Copie o arquivo de exemplo
cp .env.example .env
```

**Principais configurações do arquivo `.env`:**

```bash
# 1. SerpAPI (OBRIGATÓRIO para Google Scholar)
SERPAPI_KEY=sua_chave_serpapi_aqui_1234567890abcdef

# 2. MongoDB (local ou remoto)
MONGODB_URI=mongodb://localhost:27017/web-scraper-uniser

# 3. API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# 4. Rate Limiting (importante para SerpAPI)
REQUEST_DELAY=2.0        # Segundos entre requisições
MAX_RETRIES=3           # Tentativas em caso de erro
TIMEOUT=30              # Timeout das requisições
```

### 🔧 Configurações Avançadas

```bash
# Cache e Performance
CACHE_ENABLED=true
CACHE_EXPIRE_HOURS=24

# Logs e Debug
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Selenium (se necessário)
HEADLESS_BROWSER=true
BROWSER_TIMEOUT=30

# Exportação
EXPORT_DIR=exports/
TEMP_DIR=temp/
```

### 🌐 URLs das Plataformas

```bash
GOOGLE_SCHOLAR_URL=https://scholar.google.com
LATTES_URL=http://lattes.cnpq.br
PUBMED_URL=https://pubmed.ncbi.nlm.nih.gov
```

---

## � Funcionalidades Detalhadas

### 🎯 Busca Inteligente

- **Google Scholar**: Maior base de dados acadêmicos mundial
- **Busca por nome**: Encontra múltiplos pesquisadores
- **Perfis completos**: Dados institucionais e acadêmicos
- **Filtros avançados**: Palavras-chave relacionadas ao envelhecimento

### 📊 Métricas Acadêmicas

- **H-index**: Índice de produtividade e impacto
- **i10-index**: Publicações com 10+ citações
- **Total de citações**: Impacto geral do pesquisador
- **Áreas de pesquisa**: Especialidades identificadas

### 📋 Sistema de Filtros

36 palavras-chave em 3 idiomas (PT/EN/ES):

- **População**: idoso, elderly, anciano
- **Processo**: envelhecimento, aging, envejecimiento
- **Áreas**: gerontologia, geriatria, qualidade de vida
- **Educação**: universidade aberta, lifelong learning

### 💾 Persistência de Dados

- **MongoDB integrado**: Armazenamento local seguro
- **Cache inteligente**: Evita buscas desnecessárias
- **Histórico**: Todas as pesquisas são salvas
- **Backup automático**: Dados protegidos em containers

---

## 🛠️ Solução de Problemas

### ❌ Backend não inicia

```bash
# Verificar se o ambiente virtual está ativo
which python  # Deve apontar para venv/bin/python

# Verificar se as dependências estão instaladas
pip list | grep fastapi

# Verificar se a porta está livre
netstat -tulpn | grep :8000

# Executar com debug
DEBUG=true uvicorn src.api:app --reload
```

### 🔌 Erro de conexão com SerpAPI

```bash
# Verificar se a chave está configurada
grep SERPAPI_KEY .env

# Testar a chave diretamente
curl "https://serpapi.com/search.json?engine=google_scholar&q=coffee&api_key=SUA_CHAVE"

# Verificar rate limit
# SerpAPI: máximo 1 request/segundo no plano gratuito
```

### 💾 Problemas com MongoDB

```bash
# Verificar se MongoDB está rodando
sudo systemctl status mongod  # Linux
brew services list | grep mongodb  # Mac

# Conectar diretamente
mongosh --eval "db.runCommand('ping')"

# Verificar conexão no Python
python -c "from pymongo import MongoClient; print(MongoClient().admin.command('ping'))"
```

### 🌐 Frontend não carrega

```bash
# Verificar se Node.js está instalado
node --version  # Deve ser 18+
npm --version

# Reinstalar dependências
cd frontend
rm -rf node_modules package-lock.json
npm install

# Verificar se a porta está livre
netstat -tulpn | grep :5173
```

### 🐍 Problemas com Python/Selenium

```bash
# Verificar versão do Python
python --version  # Deve ser 3.12+

# Instalar Chrome/Chromium
# Ubuntu: sudo apt install chromium-browser
# Mac: brew install --cask google-chrome

# Verificar ChromeDriver
which chromedriver
chromedriver --version
```

---

## 📈 Roadmap e Funcionalidades Futuras

### 🔄 Em Desenvolvimento

- [ ] **Integração com Lattes**: Busca na Plataforma Lattes
- [ ] **ORCID Support**: Integração com ORCID API
- [ ] **Análises Avançadas**: Grafos de colaboração
- [ ] **Relatórios Customizados**: Templates personalizáveis

### 🎯 Funcionalidades Planejadas

- [ ] **API Authentication**: Sistema de usuários
- [ ] **Scheduled Searches**: Buscas agendadas
- [ ] **Email Notifications**: Alertas de novas publicações
- [ ] **Advanced Filters**: Filtros por período, tipo de publicação
- [ ] **Data Visualization**: Dashboards interativos

---

## 🤝 Contribuição

### Para Desenvolvedores

1. **Fork** o repositório
2. **Clone** localmente
3. **Configure** ambiente Docker
4. **Desenvolva** suas features
5. **Teste** thoroughly
6. **Submit** pull request

### Reportar Bugs

- Use as **Issues** do GitHub
- Inclua **logs completos**
- Descreva **passos para reproduzir**
- Informe **versão do Docker**

---

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo `LICENSE` para detalhes.

---

## 🆘 Suporte

### � Contato

- **Email**: [suporte@uniser.edu.br](mailto:suporte@uniser.edu.br)
- **GitHub Issues**: [Reportar problema](https://github.com/Bappoz/web-scrapper/issues)

### 📚 Documentação

- **API Docs**: http://localhost:8000/docs (após inicialização)
- **Swagger UI**: Interface interativa da API
- **MongoDB Compass**: Ferramenta visual para MongoDB

### � Tecnologias Utilizadas

- [ ] **Performance**: Otimizações de velocidade
- [ ] **Multilingual**: Interface em múltiplos idiomas

---

## 🤝 Contribuindo

### 📝 Como Contribuir

1. **Fork o projeto**
2. **Crie uma branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit suas mudanças** (`git commit -m 'Add some AmazingFeature'`)
4. **Push para a branch** (`git push origin feature/AmazingFeature`)
5. **Abra um Pull Request**

### 🐛 Reportar Bugs

Encontrou um bug? [Abra uma issue](https://github.com/Bappoz/web-scrapper/issues) com:

- **Descrição** do problema
- **Passos** para reproduzir
- **Screenshots** (se aplicável)
- **Informações do sistema** (OS, Python version, etc.)

### � Sugerir Features

Tem uma ideia? [Abra uma issue](https://github.com/Bappoz/web-scrapper/issues) com a tag `enhancement`.

---

## � Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🎓 Tecnologias Utilizadas

### Backend

- **Python 3.12+** - Linguagem principal
- **FastAPI** - Framework web moderno
- **Selenium** - Automação web
- **BeautifulSoup** - Parser HTML/XML
- **Pymongo** - Driver MongoDB
- **Pandas** - Manipulação de dados
- **OpenPyXL** - Geração de Excel

### Frontend

- **React 18** - Library UI
- **TypeScript** - Tipagem estática
- **Vite** - Build tool
- **Tailwind CSS** - Framework CSS
- **Axios** - Cliente HTTP

### Database

- **MongoDB** - Banco NoSQL

### APIs

- **SerpAPI** - Google Scholar data
- **Google Scholar** - Dados acadêmicos

---

<div align="center">

**🎓 Desenvolvido com ❤️ pelo time UniSER**

_Facilitando pesquisa acadêmica através da tecnologia_

[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/Bappoz/web-scrapper)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![SerpAPI](https://img.shields.io/badge/Powered%20by-SerpAPI-orange)](https://serpapi.com)

**📞 Suporte**: [Abrir Issue](https://github.com/Bappoz/web-scrapper/issues) • **📧 Contato**: via GitHub

</div>
# IMPORTANTE: Execute este comando da pasta RAIZ do projeto (não da pasta src)
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

**Se deu certo**, você verá algo como:

```
INFO: Uvicorn running on http://0.0.0.0:8000
```

---

## 🎮 Como usar?

### Método 1: Interface Visual (Mais Fácil)

```bash
# Em outro terminal, vá para a pasta frontend
cd frontend

# Instale as dependências do site
npm install

# Rode a interface
npm run dev
```

Agora abra seu navegador em: **http://localhost:3000**
(Se a porta 3000 estiver ocupada, o Vite usará automaticamente a porta 3001 ou outra disponível)

### Método 2: Usando comandos diretos

Você pode fazer buscas direto pelo navegador visitando essas URLs:

#### 🔍 Buscar pesquisadores:

```
http://localhost:8000/search/authors/scholar?name=Silva&max_results=10
```

#### 📚 Buscar publicações de um pesquisador específico:

```
http://localhost:8000/search/author/publications/AUTHOR_ID?max_results=50&export_excel=true
```

#### 🌐 Verificar status da API:

```
http://localhost:8000/health
```

---

## 💡 Exemplos práticos

### 🎯 Exemplo 1: Encontrar pesquisadores chamados "Silva"

**O que você quer**: Ver todos os pesquisadores com sobrenome "Silva"

**Como fazer**:

1. Abra: http://localhost:3000
2. Digite: "Silva"
3. Clique em "Buscar Pesquisadores"
4. **Veja a lista** de pesquisadores encontrados
5. **Selecione um pesquisador** para ver detalhes
6. **Clique em "Exportar para Excel"** para baixar todas as publicações

**O que você vai ver**: Lista de pesquisadores, suas instituições, áreas de pesquisa, índices acadêmicos

### 🎯 Exemplo 2: Analisar um pesquisador específico

**O que você quer**: Dados completos de um pesquisador específico

**Como fazer**:

1. Busque pelo nome (ex: "João Santos")
2. **Veja a lista** com múltiplos "João Santos"
3. **Leia as descrições** (instituição, área de pesquisa)
4. **Selecione o pesquisador correto**
5. **Visualize todas as publicações**
6. **Exporte em Excel profissional**

**O que você vai ver**: Publicações completas, citações, anos, co-autores, estatísticas

### 🎯 Exemplo 3: Comparar pesquisadores

**O que você quer**: Comparar diferentes pesquisadores com o mesmo nome

**Como fazer**:

1. Busque um nome comum (ex: "Maria")
2. **Veja múltiplos perfis** de pesquisadoras
3. **Compare as descrições**:
   - Universidade onde trabalham
   - Áreas de especialização
   - Número de citações
   - Índice H
4. **Selecione cada uma** para análise detalhada
5. **Exporte os dados** de cada uma separadamente

---

## 📊 Como usar a Exportação Excel Profissional

### 🎯 Passo a passo para gerar relatórios Excel

1. **Faça uma busca** (qualquer tipo: autor, tema ou completa)
2. **Aguarde os resultados** aparecerem na tela
3. **Localize o painel "Exportar Excel Profissional"** na parte inferior direita
4. **Clique em "Exportar Relatório Excel Profissional"**
5. **Aguarde a geração** (pode levar alguns segundos)
6. **Arquivo salvo** automaticamente na pasta `exports/`

### 📁 Onde encontrar os arquivos Excel gerados

```
web-scrapper/
├── exports/               ← 📁 Seus relatórios Excel ficam aqui
│   ├── pesquisa_completa_machine_learning_20251006_013014.xlsx
│   ├── pesquisa_completa_inteligencia_artificial_20251006_014022.xlsx
│   └── ...
```

### 🎨 Estrutura do Excel profissional

Cada arquivo Excel contém **4 abas organizadas**:

#### 📋 Aba 1: **Resumo Executivo**

- 📊 Estatísticas principais da busca
- 🔢 Total de pesquisadores encontrados
- 📚 Total de publicações
- 📈 Total de citações
- 🏆 Maior H-Index encontrado

#### 👨‍🎓 Aba 2: **Pesquisadores**

- 📝 Nome completo
- 🏛️ Instituição atual
- 🔢 H-Index calculado
- 📊 i10-Index
- 📈 Total de citações
- 🔗 Link do perfil

#### 📚 Aba 3: **Publicações**

- 📖 Título do artigo
- ✍️ Lista de autores
- 📅 Ano de publicação
- 📊 Número de citações
- 🔗 Link para o artigo
- 🏷️ Plataforma de origem

#### 📈 Aba 4: **Métricas Acadêmicas**

- 🔢 H-Index de cada pesquisador
- 📊 Distribuição de citações
- 📈 Análise de produtividade
- 🏆 Rankings por impacto

### 💡 Dicas para usar os relatórios Excel

- **Filtros automáticos**: Todas as tabelas têm filtros habilitados
- **Cores organizadas**: Cada tipo de dado tem sua cor
- **Fórmulas incluídas**: Totais e médias calculados automaticamente
- **Compatibilidade**: Funciona no Excel 2007+ e LibreOffice Calc
- **Gráficos prontos**: Dados organizados para criar gráficos facilmente

---

## ❓ Problemas comuns e soluções

### 🚨 "Erro: ModuleNotFoundError"

**Problema**: Alguma biblioteca não foi instalada
**Solução**:

```bash
pip install -r requirements.txt
```

### 🚨 "Erro: Port already in use"

**Problema**: A porta 8000 já está sendo usada
**Solução**:

```bash
# Use uma porta diferente
python -m uvicorn src.api_new:app --reload --host 0.0.0.0 --port 8001
```

### 🚨 "Erro: Invalid API key"

**Problema**: A chave do Google Scholar está errada
**Solução**:

1. Verifique se copiou a chave correta do site da SerpAPI
2. Verifique se colou no arquivo `.env` corretamente
3. Reinicie o programa

### 🚨 Não encontra resultados

**Possíveis causas**:

- Nome do pesquisador muito específico ou raro
- Tema muito específico
- Pesquisador não tem perfil nas plataformas
- **Solução**: Tente nomes mais comuns como "Silva", "Santos" ou temas como "medicina", "educação"

---

## 🆘 Precisa de ajuda?

### 📹 Tutoriais recomendados no YouTube:

- "Como instalar Python no Windows"
- "Como usar o Prompt de Comando/Terminal"
- "Git para iniciantes"

### 💬 Onde pedir ajuda:

- **GitHub Issues**: [Clique aqui para reportar problemas](https://github.com/Bappoz/researchs-web-scrapper-for-UniSER/issues)
- **Email**: [Contato com o desenvolvedor]

### 🔧 Comandos úteis:

**Ver se o Python está instalado**:

```bash
python --version
```

**Ver se o programa está funcionando**:

```bash
curl http://localhost:8000/health
```

**Parar o programa**:
Pressione `Ctrl + C` no terminal

---

## 🎁 Exemplos de uso na vida real

### � Para estudantes

- **Encontrar orientadores** especialistas em sua área de interesse
- **Descobrir pesquisadores** nas universidades que você quer estudar
- **Achar referências** e trabalhos relevantes para seu TCC ou dissertação
- **Identificar colaborações** entre pesquisadores da sua área

### 👩‍🏫 Para professores

- **Encontrar colaboradores** para pesquisa na sua área
- **Verificar produção científica** de colegas e concorrentes
- **Acompanhar publicações** de pesquisadores específicos
- **Mapear o campo de pesquisa** da sua especialização

### 🏛️ Para instituições

- **Mapear pesquisadores** por área de conhecimento
- **Analisar produção científica** institucional
- **Encontrar possíveis parceiros** para projetos de pesquisa
- **Avaliar impacto acadêmico** de pesquisadores

---

## 📊 O que cada plataforma oferece

| Plataforma            | O que você encontra                       | Melhor para                    |
| --------------------- | ----------------------------------------- | ------------------------------ |
| **🎓 Google Scholar** | Artigos, citações, estatísticas           | Buscar publicações científicas |
| **🇧🇷 Lattes**         | CVs completos, formação, projetos         | Pesquisadores brasileiros      |
| **🌐 ORCID**          | Identificação internacional, colaborações | Pesquisadores do mundo todo    |

---

## 🆓 É grátis?

**Sim!** O programa é completamente gratuito. Apenas a SerpAPI (para Google Scholar) tem algumas limitações:

- **Gratuito**: 100 buscas por mês
- **Pago**: Mais buscas se precisar

Para uso pessoal e estudantil, 100 buscas por mês são mais que suficientes!

---

## 🏆 Vantagens deste programa

✅ **Busca em 3 plataformas** de uma vez só
✅ **Interface simples** e fácil de usar  
✅ **Resultados organizados** em abas separadas
✅ **Exporta para Excel** para análise posterior
✅ **Gratuito** e open source
✅ **Funciona offline** (depois de instalado)

---

## 🎯 Próximos passos após instalar

1. **Teste com nomes comuns** primeiro (Silva, Santos, etc.)
2. **Experimente diferentes temas** (medicina, educação, tecnologia)
3. **Use a interface visual** - é mais fácil que comandos
4. **Exporte os resultados** para analisar no Excel
5. **Compartilhe** com colegas que podem se beneficiar

---

<div align="center">

**🎉 Pronto! Agora você pode encontrar qualquer pesquisador ou artigo científico facilmente!**

**Feito com ❤️ para facilitar a vida acadêmica**

_Se este programa te ajudou, deixe uma ⭐ no GitHub!_

</div>
