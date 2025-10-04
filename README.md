# 🔬 Web Scraper UniSER - Busca de Pesquisadores Acadêmicos

<div align="center">

**Um programa simples para encontrar informações de pesquisadores e seus trabalhos científicos**

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Status](https://img.shields.io/badge/Status-Funcionando-green.svg)

_Perfeito para estudantes, professores e pesquisadores_

</div>

---

## 🤔 O que este programa faz?

Este programa te ajuda a **encontrar informações sobre pesquisadores** de forma rápida e organizada. É como um "Google" especializado em buscar:

- 👨‍🎓 **Perfis de professores e pesquisadores**
- 📚 **Artigos e trabalhos científicos**
- 🏛️ **Informações sobre universidades e instituições**
- 📊 **Estatísticas de publicações e citações**

### 🎯 Onde ele busca?

- **Google Scholar** - O maior banco de artigos científicos
- **Plataforma Lattes** - CVs de pesquisadores brasileiros
- **ORCID** - Identificação internacional de pesquisadores

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
python -m uvicorn api_new:app --reload --host 0.0.0.0 --port 8000
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

#### 🔍 Buscar um pesquisador:

```
http://localhost:8000/search/author/scholar?name=João Silva&max_results=5
```

#### 📚 Buscar por tema:

```
http://localhost:8000/search/topic/scholar?topic=inteligência artificial&max_results=10
```

#### 🌐 Buscar em todas as plataformas:

```
http://localhost:8000/search/comprehensive?query=Maria Santos&search_type=author&platforms=all&max_results=3
```

---

## 💡 Exemplos práticos

### 🎯 Exemplo 1: Encontrar um professor

**O que você quer**: Informações sobre o professor "Carlos Silva"

**Como fazer**:

1. Abra: http://localhost:3000
2. Escolha "Busca por autor"
3. Digite: "Carlos Silva"
4. Selecione "Todas as plataformas"
5. Clique em "Buscar"

**O que você vai ver**: Perfis, artigos, universidade onde trabalha, áreas de pesquisa

### 🎯 Exemplo 2: Pesquisar sobre um tema

**O que você quer**: Artigos sobre "inteligência artificial"

**Como fazer**:

1. Escolha "Busca por tema"
2. Digite: "inteligência artificial"
3. Selecione "Google Scholar"
4. Clique em "Buscar"

**O que você vai ver**: Lista de artigos, autores, ano de publicação, quantas vezes foi citado

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

- **GitHub Issues**: [Clique aqui para reportar problemas](https://github.com/Bappoz/Web-Scraper-UniSER/issues)
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

### 👨‍🎓 **Para estudantes**:

- Encontrar professores especialistas em sua área de interesse
- Descobrir quais universidades têm os melhores pesquisadores
- Achar artigos relevantes para seu TCC ou dissertação

### 👩‍🏫 **Para professores**:

- Encontrar colaboradores para pesquisa
- Verificar o que outros estão pesquisando na sua área
- Acompanhar publicações de colegas

### 🏛️ **Para instituições**:

- Mapear pesquisadores por área
- Analisar produção científica
- Encontrar possíveis parceiros para projetos

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
