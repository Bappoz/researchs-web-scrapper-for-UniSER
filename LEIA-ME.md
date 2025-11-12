# 📚 Web Scrapper - Sistema de Pesquisa Acadêmica

Sistema automatizado para extração de dados de pesquisadores do **Google Scholar** e **Plataforma Lattes**, com geração de relatórios em Excel.

---

## 🚀 INÍCIO RÁPIDO (Para Pesquisadores)

### 1️⃣ Primeira Vez - Configuração Inicial

1. **Baixe o projeto** do GitHub ou extraia o arquivo ZIP
2. **Duplo clique** no arquivo `INICIAR.bat` na pasta raiz
3. Escolha a opção **[1]** para verificar pré-requisitos
4. Se faltar algo, instale conforme as instruções exibidas
5. Escolha a opção **[2]** para instalar dependências
6. Configure o MongoDB (veja seção abaixo)
7. Escolha a opção **[6]** para iniciar o sistema

### 2️⃣ Uso Diário (após configuração)

1. Duplo clique em `INICIAR.bat`
2. Se usar MongoDB local, escolha opção **[3]** primeiro
3. Escolha opção **[6]** para iniciar Backend + Frontend
4. O navegador abrirá automaticamente em `http://localhost:5173`
5. Faça suas pesquisas e exporte os dados para Excel!

---

## 📋 PRÉ-REQUISITOS

Você precisa instalar estes programas no seu computador:

### ✅ Obrigatórios

| Software    | Versão Mínima                 | Download                          |
| ----------- | ----------------------------- | --------------------------------- |
| **Python**  | 3.9+                          | https://www.python.org/downloads/ |
| **Node.js** | 18+                           | https://nodejs.org/               |
| **MongoDB** | 6.0+ (local) ou Atlas (cloud) | Ver seção abaixo                  |

### 📝 Notas Importantes

- **Python**: Durante a instalação, marque ✅ "Add Python to PATH"
- **Node.js**: A instalação padrão já inclui npm
- **MongoDB**: Escolha entre instalação local OU uso do MongoDB Atlas (cloud gratuito)

---

## 🗄️ CONFIGURANDO O MONGODB

### Opção 1: MongoDB Atlas (Cloud - RECOMENDADO) ☁️

**Vantagens**: Grátis, não precisa instalar nada, funciona de qualquer lugar

1. Acesse https://www.mongodb.com/cloud/atlas
2. Crie uma conta gratuita
3. Crie um cluster (escolha a opção FREE - M0)
4. Crie um usuário de banco de dados (Database Access)
5. Libere seu IP (Network Access → Add IP Address → Allow Access from Anywhere)
6. Copie a string de conexão (Connect → Connect your application)
7. Crie um arquivo `.env` na raiz do projeto com:
   ```
   MONGODB_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/web_scrapper
   ```

### Opção 2: MongoDB Local 💻

**Vantagens**: Funciona offline, dados ficam no seu computador

1. Baixe MongoDB Community: https://www.mongodb.com/try/download/community
2. Instale com as opções padrão
3. Ao usar o sistema, escolha opção **[3]** no menu `INICIAR.bat`

---

## 🎯 COMO USAR O SISTEMA WEB

### 1. Pesquisar por Nome

1. Acesse a aba "Nome do Pesquisador"
2. Digite o nome completo
3. Clique em "Buscar por Nome"
4. Uma nova aba abrirá no Google Acadêmico
5. **Selecione manualmente** o perfil correto
6. Copie o link do perfil e use a busca por link (abaixo)

### 2. Pesquisar por Link do Google Scholar

1. Acesse a aba "Link do Google Scholar"
2. Cole o link do perfil (ex: `https://scholar.google.com/citations?user=XXX`)
3. Escolha quantas publicações deseja extrair (padrão: 10)
4. Clique em "Buscar Publicações"
5. Aguarde a extração dos dados (leva 5-30 segundos)

### 3. Visualizar Resultados

- **Cards de Estatísticas**: H-Index, I10-Index, Total de Citações
- **Dados do Lattes**: Instituição, Área, Resumo, Link do Currículo
- **Lista de Publicações**: Título, Autores, Ano, Citações, Link

### 4. Exportar para Excel

1. Clique no botão "Gerar Excel Consolidado" (canto superior direito)
2. O arquivo será baixado automaticamente
3. Contém 2 abas:
   - **Pesquisadores**: Nome, instituição, métricas, dados Lattes
   - **Publicações**: Título, autores, ano, citações, etc.

### 5. Ver Histórico

1. Clique no botão "Histórico" no topo
2. Veja todos os pesquisadores já consultados
3. Use o campo de busca para filtrar
4. Delete pesquisadores específicos ou limpe tudo

### 6. Dark Mode 🌓

- Clique no ícone ☀️ (sol) ou 🌙 (lua) no topo para alternar
- Sua preferência é salva automaticamente

### 7. Central de Ajuda 📖

- Clique no botão verde "Ajuda" no topo
- Acesse tutoriais passo a passo
- Veja respostas para dúvidas frequentes (FAQ)

---

## 📂 ESTRUTURA DO PROJETO

```
web-scrapper/
│
├── INICIAR.bat              ← DUPLO CLIQUE AQUI PARA COMEÇAR
├── .env                     ← Configure MongoDB aqui (criar se não existir)
├── main.py                  ← Backend (FastAPI)
├── requirements.txt         ← Dependências Python
│
├── scripts/                 ← Scripts de instalação e inicialização
│   ├── check_requirements.bat
│   ├── install_dependencies.bat
│   ├── start_backend.bat
│   ├── start_frontend.bat
│   └── start_mongodb.bat
│
├── frontend/                ← Interface web (React + TypeScript)
│   ├── package.json
│   └── src/
│
├── src/                     ← Código fonte do backend
│   ├── scraper/            ← Scrapers (Lattes, Scholar)
│   ├── services/           ← Lógica de negócio
│   ├── database/           ← Conexão MongoDB
│   └── export/             ← Geração de Excel
│
└── exports/                 ← Arquivos Excel gerados
```

---

## ❓ SOLUÇÃO DE PROBLEMAS

### Backend não inicia

- ✅ Verifique se o MongoDB está rodando
- ✅ Verifique se a porta 8000 não está ocupada
- ✅ Execute `scripts\check_requirements.bat` novamente

### Frontend não abre no navegador

- ✅ Verifique se o Backend está rodando
- ✅ Acesse manualmente: http://localhost:5173
- ✅ Verifique se a porta 5173 não está ocupada

### Erro ao instalar dependências

- ✅ Execute como Administrador (clique com botão direito em `INICIAR.bat` → Executar como Administrador)
- ✅ Verifique sua conexão com a internet
- ✅ Atualize pip: `python -m pip install --upgrade pip`
- ✅ **ERRO COM NUMPY/PANDAS (Python 3.12)**:
  - ✅ Use Python 3.12 com `numpy>=2.1.0` e `pandas>=2.1.0` (já configurado no requirements.txt)
  - ✅ O script instalará automaticamente as versões corretas
  - ℹ️ Se usar Python 3.10 ou 3.11, qualquer versão de numpy/pandas funciona
- ✅ **ERRO COM LXML** (Visual C++ 14.0 required):
  - ✅ O script instalará versão pré-compilada automaticamente
  - ✅ Se falhar, execute manualmente: `pip install lxml --only-binary :all:`
  - ⚠️ NUNCA tente compilar lxml no Windows sem Visual Studio instalado

### Excel exportado está vazio

- ✅ Certifique-se de fazer uma busca antes de exportar
- ✅ Verifique se há dados no Histórico de Pesquisadores

### Dados do Lattes aparecem como NULL

- ✅ O pesquisador pode não ter currículo Lattes
- ✅ O nome no Google Scholar pode ser diferente do Lattes
- ✅ Tente novamente após alguns minutos (limite de requisições)

### MongoDB não conecta

- ✅ Se usar MongoDB local: Execute `scripts\start_mongodb.bat`
- ✅ Se usar Atlas: Verifique se a string de conexão está correta no `.env`
- ✅ Verifique se liberou seu IP no MongoDB Atlas (Network Access)

---

## 🔧 REQUISITOS DO SISTEMA

- **Sistema Operacional**: Windows 10/11
- **RAM**: Mínimo 4GB (recomendado 8GB)
- **Espaço em Disco**: 2GB livres
- **Internet**: Necessária para acessar Google Scholar e Lattes
- **Navegador**: Chrome, Firefox, Edge ou Safari (atualizado)

---

## 📊 MÉTRICAS EXPLICADAS

### H-Index

Índice que mede a produtividade e o impacto das publicações de um pesquisador. Um pesquisador tem índice **h** quando possui **h** artigos com pelo menos **h** citações cada.

**Exemplo**: h=10 significa que o pesquisador tem 10 artigos com pelo menos 10 citações cada.

### I10-Index

Número total de publicações com pelo menos 10 citações.

**Exemplo**: i10=25 significa que o pesquisador tem 25 publicações com 10 ou mais citações.

### Total de Citações

Soma de todas as citações recebidas por todas as publicações do pesquisador.

---

## 🆘 SUPORTE

Se você encontrar problemas:

1. **Consulte a Central de Ajuda** no sistema (botão verde "Ajuda")
2. **Verifique a seção "Dúvidas Frequentes (FAQ)"**
3. **Execute a opção [1]** do menu `INICIAR.bat` para diagnóstico
4. **Contate o desenvolvedor** responsável pelo projeto

---

## 📝 LICENÇA

Este projeto foi desenvolvido para uso acadêmico e científico.

---

## 👨‍💻 DESENVOLVEDOR

Desenvolvido para o Instituto de Pesquisa Científica  
Sistema de Busca Acadêmica - Google Scholar + Lattes

**Versão**: 1.0.0  
**Data**: Novembro 2025
