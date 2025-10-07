// Teste simples no console do navegador
// Cole este código no DevTools para testar a comunicação frontend-backend

async function testFrontendAPI() {
  try {
    console.log("🔄 Testando API do frontend...");

    // Teste 1: Busca por tema
    const response = await fetch(
      "http://localhost:8000/search/topic/scholar?topic=python&max_results=2"
    );
    const data = await response.json();

    console.log("✅ API Response:", data);
    console.log("📊 Data structure:", {
      success: data.success,
      platform: data.platform,
      total_results: data.total_results,
      has_publications: !!data.data?.publications,
      publication_count: data.data?.publications?.length || 0,
    });

    if (data.data?.publications) {
      console.log("📚 Primeira publicação:", data.data.publications[0]);
    }

    return data;
  } catch (error) {
    console.error("❌ Erro no teste:", error);
  }
}

// Execute: testFrontendAPI()
console.log("Cole 'testFrontendAPI()' no console para testar");
