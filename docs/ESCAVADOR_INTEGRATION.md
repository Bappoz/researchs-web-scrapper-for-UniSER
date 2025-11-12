# 🔍 Integração com Escavador - Resumo do Lattes

## Visão Geral

Esta nova funcionalidade adiciona a capacidade de buscar o **resumo do currículo Lattes** através do **Escavador**, complementando os dados obtidos do Google Scholar.

## 🎯 Objetivo

Fornecer informações resumidas do perfil acadêmico de pesquisadores brasileiros através da Plataforma Lattes, sem a necessidade de navegar diretamente pelo site do CNPq.

## 🚀 Como Funciona

### Backend

1. **Novo Scraper**: `src/scraper/escavador_scraper.py`

   - Busca informações no site Escavador
   - Extrai resumo do perfil Lattes
   - Retorna dados estruturados

2. **Serviço Integrado**: `src/services/services.py`

   - Método `get_lattes_summary_via_escavador()`
   - Integrado ao `GoogleScholarService`

3. **API Endpoint**:
   - **GET** `/search/lattes-summary/escavador?name={nome_pesquisador}`
   - **GET** `/search/author/scholar?author={nome}&include_lattes_summary=true`

### Frontend

1. **Novo Componente**: `LattesSummaryCard.tsx`

   - Exibe resumo do Lattes de forma elegante
   - Card estilizado com informações estruturadas

2. **Serviço de API**: `api_new.ts`

   - Método `getLattesSummaryViaEscavador()`

3. **Integração**: `ResultsDisplay.tsx`
   - Exibe automaticamente o resumo quando disponível

## 📊 Dados Retornados

O resumo do Lattes via Escavador inclui:

- ✅ **Nome** do pesquisador
- ✅ **Resumo/Biografia** do perfil
- ✅ **Instituição** de vínculo
- ✅ **Área de atuação**
- ✅ **Link** para o currículo Lattes completo

## 🔧 Uso

### Busca Automática (Recomendado)

Ao buscar um autor no Google Scholar, o resumo do Lattes é buscado automaticamente:

```typescript
// Frontend
const response = await academicService.searchAuthorScholar(
  "Nome do Pesquisador",
  10, // max_results
  false, // export_excel
  true // include_lattes_summary (padrão: true)
);

// Acessar resumo do Lattes
if (response.data?.lattes_summary?.success) {
  console.log(response.data.lattes_summary.summary);
}
```

### Busca Manual

Para buscar apenas o resumo do Lattes:

```typescript
// Frontend
const response = await academicService.getLattesSummaryViaEscavador(
  "Nome do Pesquisador"
);

console.log(response.data);
```

```python
# Backend
from src.services.services import GoogleScholarService

service = GoogleScholarService()
lattes_data = service.get_lattes_summary_via_escavador("Nome do Pesquisador")

print(lattes_data['summary'])
```

## 📝 Exemplo de Resposta

```json
{
  "success": true,
  "message": "Resumo do Lattes encontrado para 'João Silva'",
  "query": "João Silva",
  "search_type": "lattes_summary",
  "platform": "escavador",
  "data": {
    "name": "João Silva",
    "summary": "Professor Doutor em Ciência da Computação...",
    "institution": "Universidade Federal de São Paulo",
    "area": "Inteligência Artificial",
    "lattes_url": "http://lattes.cnpq.br/1234567890123456",
    "source": "escavador"
  }
}
```

## 🎨 Interface

O resumo é exibido em um card elegante com:

- 📚 Ícone e título destacado
- 📋 Informações estruturadas
- 🔗 Link direto para o Lattes completo
- ℹ️ Nota sobre a fonte dos dados

## ⚙️ Configuração

Não é necessária nenhuma configuração adicional. O scraper funciona sem API keys ou credenciais.

## 🔒 Considerações

- ✅ **Sem necessidade de API key**
- ✅ **Totalmente integrado ao fluxo existente**
- ✅ **Não quebra funcionalidades existentes**
- ✅ **Google Scholar continua sendo a fonte principal**
- ✅ **Lattes é apenas complementar**

## 🐛 Tratamento de Erros

O sistema é robusto e lida com falhas graciosamente:

- Se o Escavador não retornar dados, a busca continua normalmente
- Se o resumo não for encontrado, simplesmente não é exibido
- Não há impacto nas funcionalidades do Google Scholar

## 📚 Arquivos Modificados/Criados

### Novos Arquivos

- `src/scraper/escavador_scraper.py`
- `frontend/src/components/LattesSummaryCard.tsx`
- `docs/ESCAVADOR_INTEGRATION.md`

### Modificados

- `src/services/services.py`
- `src/api.py`
- `frontend/src/services/api_new.ts`
- `frontend/src/components/ResultsDisplay.tsx`

## 🎯 Benefícios

1. **Informações Complementares**: Enriquece os dados do Google Scholar com informações do Lattes
2. **Experiência Unificada**: Usuário não precisa sair da aplicação
3. **Contexto Brasileiro**: Especialmente útil para pesquisadores brasileiros
4. **Implementação Limpa**: Não afeta o código existente

## 🚦 Status

✅ **Implementado e Funcional**

A funcionalidade está totalmente implementada e pronta para uso. Todos os componentes foram criados e integrados ao sistema existente.
