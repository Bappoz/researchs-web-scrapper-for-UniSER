# Web Scraper UniSER

**Sistema simples para encontrar informações de pesquisadores e trabalhos científicos**

![Status](https://img.shields.io/badge/Status-Funcionando-green.svg)

---

## 🎯 Funcionalidades Principais

- ✅ **Google Scholar**: Busca completa de publicações e autores
- ✅ **Resumo do Lattes**: Informações do currículo Lattes via Escavador
- ✅ **Exportação Excel**: Exporte todos os dados para planilhas
- ✅ **Métricas Acadêmicas**: H-index, citações, i10-index
- ✅ **Interface Moderna**: Design responsivo e intuitivo

> **Nota**: As funcionalidades de Lattes direto e ORCID foram removidas. O sistema agora foca no Google Scholar como fonte principal, complementado pelo resumo do Lattes via Escavador.

---

## Instalação Rápida

### Para Windows

1. **Baixe e instale os programas necessários:**

   - Python 3.12+: https://www.python.org/downloads/
   - Node.js 18+: https://nodejs.org/
   - MongoDB: https://www.mongodb.com/try/download/community

2. **Execute o instalador automático:**

   ```bash
   # Clique duas vezes no arquivo:
   ./install_and_setup.bat
   ```

3. **Configure as chaves API:**

   - Abra o arquivo `.env` (criado pelo instalador)
   - Adicione sua chave do SerpAPI: `SERPAPI_KEY=sua_chave_aqui`
   - Pegue a chave gratuita em: https://serpapi.com/

4. **Inicie o projeto:**

   ```bash
   # Backend (mantenha esta janela aberta):
   ./start_backend.bat

   # Frontend (em outra janela do terminal):
   ./start_frontend.bat
   ```

### Para Linux/Mac

1. **Instale os programas necessários:**

   ```bash
   # Ubuntu/Debian:
   sudo apt update
   sudo apt install python3 python3-pip nodejs npm mongodb

   # Mac:
   brew install python3 node mongodb-community
   ```

2. **Execute o instalador automático:**

   ```bash
   chmod +x install_and_setup.sh
   ./install_and_setup.sh
   ```

3. **Configure as chaves API:**

   - Edite o arquivo `.env`
   - Adicione: `SERPAPI_KEY=sua_chave_aqui`
   - Chave gratuita: https://serpapi.com/

4. **Inicie o projeto:**

   ```bash
   # Backend:
   ./start_backend.sh &

   # Frontend:
   ./start_frontend.sh &
   ```

### Instalação com Docker (Mais Fácil)

Se preferir uma instalação automática:

```bash
cd docker
docker-compose up -d
```

Acesse em: http://localhost:3000

---

## Como Usar

1. **Abra o navegador:** http://localhost:5173 (desenvolvimento) ou http://localhost:3000 (Docker)

2. **Faça uma busca:**

   - Digite o nome do pesquisador (ex: "João Silva")
   - Escolha a plataforma (Google Scholar, Lattes, ORCID)
   - Clique em "Buscar"

3. **Veja os resultados:**

   - Lista de pesquisadores encontrados
   - Clique em um pesquisador para ver detalhes
   - Veja publicações, citações, etc.

4. **Exporte os dados:**
   - Clique em "Exportar Excel"
   - Arquivo será salvo na pasta `exports/`

---

## ❓ Problemas Comuns

### "Python não encontrado"

- Instale Python 3.12+ do site oficial
- Reinicie o computador

### "Node.js não encontrado"

- Instale Node.js 18+ do site oficial
- Reinicie o computador

### "Erro de API"

- Verifique se colocou a chave correta no `.env`
- Chave gratuita em: https://serpapi.com/

### "Porta ocupada"

- Feche outros programas usando a porta 8000 ou 5173
- Ou mude a porta no arquivo de configuração

---

## Suporte

- **GitHub Issues:** https://github.com/Bappoz/web-scrapper/issues

---

## ��� Licença

Este projeto é gratuito e open source (MIT License).

---

<div align="center">

**Feito com ❤️ para facilitar pesquisa acadêmica**

</div>
