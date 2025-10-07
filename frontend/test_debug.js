/**
 * 🧪 TESTE DE DEBUG PARA FRONTEND - RESULTADOS DA BUSCA
 * Execute no console do navegador para testar a estrutura de dados
 */

console.clear();
console.log("🔬 INICIANDO ANÁLISE DE DEBUG DO FRONTEND");
console.log("=".repeat(60));

// Verificar se existe o componente ResultsDisplay
console.log("📊 VERIFICANDO ESTRUTURA DOS DADOS RECEBIDOS:");

// Aguardar por mudanças no console (dados reais da API)
let apiCallCount = 0;
const originalConsoleLog = console.log;
console.log = function (...args) {
  if (args[0] && args[0].includes && args[0].includes("🔍")) {
    apiCallCount++;
    originalConsoleLog(`📋 [${apiCallCount}]`, ...args);
  } else {
    originalConsoleLog(...args);
  }
};

// Mock para testar localmente se necessário
const testMockResponse = {
  success: true,
  message: "Busca por ORCID concluída",
  platform: "orcid",
  search_type: "profile",
  query: "Leonardo",
  total_results: 1,
  execution_time: 2.1,
  data: {
    publications: [
      {
        title: "Análise de Algoritmos de Machine Learning",
        authors: "Leonardo Silva",
        publication: "Journal of AI Research",
        year: 2023,
        cited_by: 15,
        link: "https://example.com/paper1",
        snippet: "Estudo sobre algoritmos...",
      },
    ],
    total_results: 1,
  },
};

window.testResultsDisplay = function () {
  console.log("🧪 SIMULANDO DADOS PARA RESULTSDISPLAY:");
  console.log("✅ Mock data:", testMockResponse);

  // Verificar se a estrutura está correta
  console.log("🔍 Has data:", !!testMockResponse.data);
  console.log(
    "🔍 Has publications in data:",
    !!testMockResponse.data?.publications
  );
  console.log(
    "🔍 Publications count:",
    testMockResponse.data?.publications?.length
  );

  return testMockResponse;
};

console.log("💡 COMANDOS DISPONÍVEIS:");
console.log("• Execute uma busca normal no frontend");
console.log("• Use testResultsDisplay() para simular dados");
console.log("• Observe os logs com prefixo 🔍 para debug");
