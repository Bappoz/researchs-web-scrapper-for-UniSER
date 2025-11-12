import React, { useState, useEffect } from "react";
import {
  AlertCircle,
  RefreshCw,
  CheckCircle,
  Search,
  BarChart3,
  FileSpreadsheet,
  BookOpen,
  History,
} from "lucide-react";

import { academicService } from "../services/api_new";
import SearchFormDual from "../components/SearchFormDual";
import ResultsDisplay from "../components/ResultsDisplay";
import StatsCardsSimple from "../components/StatsCardsSimple";
import SearchHistorySimple from "../components/SearchHistorySimple";
import ExportPanelSimple from "../components/ExportPanelSimple";
import type { SearchResponse } from "../services/api_new";

const Dashboard: React.FC = () => {
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState<"checking" | "online" | "offline">("checking");
  const [searchHistory, setSearchHistory] = useState<SearchResponse[]>([]);
  const [loadingPlatform, setLoadingPlatform] = useState<string>("");

  useEffect(() => {
    checkAPIStatus();
    loadSearchHistory();
  }, []);

  const checkAPIStatus = async () => {
    try {
      setApiStatus("checking");
      await academicService.healthCheck();
      setApiStatus("online");
    } catch (error) {
      console.error("API offline:", error);
      setApiStatus("offline");
    }
  };

  const loadSearchHistory = () => {
    const history = JSON.parse(localStorage.getItem("searchHistory") || "[]");
    setSearchHistory(history);
  };

  const handleSearchByNameScholar = async (query: string) => {
    if (!query.trim()) {
      alert("Por favor, digite um nome para buscar");
      return;
    }

    // Abrir Google Scholar em nova aba para o usuário escolher o perfil manualmente
    const searchUrl = `https://scholar.google.com/citations?view_op=search_authors&mauthors=${encodeURIComponent(query)}`;
    window.open(searchUrl, '_blank');
    
    // Mostrar mensagem explicativa
    alert(
      `🔍 Abrindo Google Scholar em nova aba...\n\n` +
      `Por favor:\n` +
      `1. Escolha o perfil correto do pesquisador\n` +
      `2. Copie a URL do perfil (exemplo: https://scholar.google.com/citations?user=XXXXXX)\n` +
      `3. Cole a URL no campo "Link do Perfil" abaixo\n` +
      `4. Clique em "Buscar por Link"`
    );
  };

  const handleSearchByLinkScholar = async (
    profileUrl: string,
    useKeywordFilter: boolean = false,
    maxPublications: number = 20
  ) => {
    setIsLoading(true);
    setLoadingPlatform("link-scholar");

    try {
      console.log("Extraindo perfil Scholar:", profileUrl);
      const result = await academicService.searchByProfileLink(
        profileUrl,
        "scholar",
        false,
        maxPublications,
        useKeywordFilter
      );
      setSearchResults(result);
      saveToHistory(result);
    } catch (error) {
      console.error("Erro na extração Scholar:", error);
      showError("Erro ao extrair dados do Scholar", "scholar", profileUrl);
    } finally {
      setIsLoading(false);
      setLoadingPlatform("");
    }
  };

  const saveToHistory = (result: SearchResponse) => {
    if (result && result.success !== false) {
      const newHistory = [result, ...searchHistory.slice(0, 9)];
      setSearchHistory(newHistory);
      localStorage.setItem("searchHistory", JSON.stringify(newHistory));
    }
  };

  const showError = (message: string, platform: string, query: string) => {
    setSearchResults({
      success: false,
      message,
      platform,
      search_type: "error",
      query,
      total_results: 0,
      execution_time: 0,
      timestamp: new Date().toISOString(),
    } as SearchResponse);
  };

  const getStatusIcon = () => {
    switch (apiStatus) {
      case "checking":
        return <RefreshCw className="h-4 w-4 animate-spin text-yellow-500" />;
      case "online":
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case "offline":
        return <AlertCircle className="h-4 w-4 text-red-500" />;
    }
  };

  const getStatusText = () => {
    switch (apiStatus) {
      case "checking": return "Verificando...";
      case "online": return "API Online";
      case "offline": return "API Offline";
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <BookOpen className="h-8 w-8 text-blue-600 mr-3" />
              <div>
                <h1 className="text-xl font-semibold text-gray-900">
                  Instituto de Pesquisa Científica
                </h1>
                <p className="text-sm text-gray-500">
                  Sistema de Busca Acadêmica - Google Scholar + Lattes
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => window.location.hash = "#/history"}
                className="inline-flex items-center px-3 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-medium rounded-lg transition-colors text-sm"
                title="Ver histórico de pesquisadores"
              >
                <History className="h-4 w-4 mr-2" />
                Histórico
              </button>

              <div className="flex items-center space-x-2">
                {getStatusIcon()}
                <span className="text-sm text-gray-600">{getStatusText()}</span>
              </div>
              <button
                onClick={checkAPIStatus}
                className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                title="Verificar status da API"
              >
                <RefreshCw className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {searchResults && (
          <StatsCardsSimple
            totalPublications={searchResults.total_results || 0}
            totalAuthors={1}
            totalProjects={searchResults.total_projects || 0}
            executionTime={searchResults.execution_time || 0}
          />
        )}

        <div className="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center mb-4">
                <Search className="h-5 w-5 text-blue-600 mr-2" />
                <h2 className="text-lg font-medium text-gray-900">
                  Busca Google Scholar
                </h2>
              </div>

              <SearchFormDual
                onSearchByNameScholar={handleSearchByNameScholar}
                onSearchByLinkScholar={handleSearchByLinkScholar}
                isLoading={isLoading}
                disabled={apiStatus === "offline"}
                loadingPlatform={loadingPlatform}
              />
            </div>

            {searchResults && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                <div className="p-6 border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <BarChart3 className="h-5 w-5 text-blue-600 mr-2" />
                      <h2 className="text-lg font-medium text-gray-900">
                        Resultados da Pesquisa
                      </h2>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-500">
                        {searchResults.total_results} resultados em{" "}
                        {searchResults.execution_time.toFixed(2)}s
                      </span>
                    </div>
                  </div>
                </div>
                <ResultsDisplay results={searchResults} />
              </div>
            )}

            {isLoading && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12">
                <div className="text-center">
                  <RefreshCw className="h-8 w-8 animate-spin text-blue-600 mx-auto mb-4" />
                  <p className="text-gray-600">Buscando no Google Scholar...</p>
                  <p className="text-sm text-gray-500 mt-2">
                    O resumo Lattes será carregado automaticamente
                  </p>
                </div>
              </div>
            )}
          </div>

          <div className="space-y-6">
            <ExportPanelSimple />

            <SearchHistorySimple
              history={searchHistory.map((item, index) => ({
                id: index.toString(),
                query: item.query || "Busca sem título",
                searchType: item.search_type || "query",
                platform: item.platform || "scholar",
                timestamp: new Date().toISOString(),
                totalResults: item.total_results || 0,
                executionTime: item.execution_time || 0,
              }))}
              onRepeatSearch={(historyItem) => {
                console.log("Repetir busca:", historyItem);
              }}
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
