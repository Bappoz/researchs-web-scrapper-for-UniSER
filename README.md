# 🔬 Web Scraper UniSER - Busca de Pesquisadores Acadêmicos

<div align="center">

**Um programa simples para encontrar informações de pesquisadores e seus trabalhos científicos**

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Status](https://img.shields.io/badge/Status-Funcionando-green.svg)

_Perfeito para estudantes, professores e pesquisadores_

</div>

---

## 🤔 O que este programa faz?

Este programa te ajuda a **encontrar pesquisadores e suas publicações** de forma rápida e organizada. É como um "Google" especializado em buscar:

- 👨‍🎓 **Múltiplos perfis de pesquisadores por nome**
- 📚 **Lista completa de publicações de cada pesquisador**
- 🏛️ **Informações sobre universidades e instituições**
- 📊 **Estatísticas de publicações e citações**
- 🔢 **Cálculo automático do Índice H dos pesquisadores**
- 🎯 **Sistema de seleção de pesquisadores para exportação**

### 🎯 Como funciona?

1. **Digite um nome** (ex: "Silva", "Santos", "Maria")
2. **Veja múltiplos pesquisadores** com esse nome
3. **Selecione o pesquisador** que você quer analisar
4. **Exporte todas as publicações** em Excel profissional

### 📊 Onde ele busca?

- **Google Scholar** - O maior banco de artigos científicos do mundo
- **Busca inteligente de pesquisadores** - Encontra múltiplos perfis por nome
- **Dados completos** - Instituição, áreas de pesquisa, índices acadêmicos

### 📊 Exportação Profissional em Excel

Uma das principais funcionalidades é a **exportação automática em Excel** com formatação profissional:

- 📋 **Múltiplas abas organizadas**: Resumo, Pesquisadores, Publicações e Métricas
- 🎨 **Formatação profissional**: Cores, fontes e layouts elegantes
- 📈 **Métricas acadêmicas**: Índice H, i10-Index, total de citações
- 📊 **Gráficos e estatísticas**: Visualização clara dos dados
- 💼 **Pronto para apresentações**: Formato compatível com Excel 2007+

**Exemplo de estrutura do Excel gerado**:

- **Aba Resumo**: Visão geral com estatísticas principais
- **Aba Pesquisadores**: Lista completa com dados acadêmicos e H-Index
- **Aba Publicações**: Artigos com título, autores, ano, citações e links
- **Aba Métricas**: Análises de impacto e indicadores de produtividade

---

## 🚀 Como instalar? (Passo a passo simples)

### ⚠️ Antes de começar, você precisa ter:

1. **Python** instalado no seu computador ([Baixar aqui](https://python.org/downloads/))
2. **Git** para baixar o código ([Baixar aqui](https://git-scm.com/downloads))

_💡 Se não sabe como instalar, procure no YouTube: "como instalar Python Windows"_

### 📥 Passo 1: Baixar o programa

Abra o **Prompt de Comando** (Windows) ou **Terminal** (Mac/Linux) e digite:

```bash
git clone https://github.com/Bappoz/Web-Scraper-UniSER.git
cd Web-Scraper-UniSER
```

### 🔧 Passo 2: Instalar as dependências

```bash
pip install -r requirements.txt
```

_⏳ Isso pode demorar alguns minutos..._

### 🔑 Passo 3: Configurar a chave da API (IMPORTANTE!)

Para o Google Scholar funcionar, você precisa de uma "chave":

1. **Vá para**: https://serpapi.com/users/sign_up
2. **Crie uma conta grátis** (pode usar seu email normal)
3. **Entre no painel**: https://serpapi.com/dashboard
4. **Copie sua "API Key"** (uma sequência de letras e números)

Agora crie um arquivo chamado `.env` na pasta do programa:

```bash
# Copie o arquivo de exemplo
copy .env.example .env
```

Abra o arquivo `.env` com o Bloco de Notas e cole sua chave onde está escrito `sua_chave_aqui`:

```
SERPAPI_KEY=sua_chave_aqui
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
```

### 🎉 Passo 4: Rodar o programa

```bash
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
