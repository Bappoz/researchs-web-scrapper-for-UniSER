/**
 * 📊 DASHBOARD PRINCIPAL
 * Interface principal para pesquisa acadêmica do Instituto de Pesquisa Científica
 */

import React, { useState, useEffect } from "react";
import { Activity, AlertCircle, RefreshCw, CheckCircle } from "lucide-react";

// Serviços da API
import { scholarService } from "../services/api";
import lattesService from "../services/api";
import orcidService from "../services/api";
import comprehensiveService from "../services/api";
import exportService from "../services/api";

// Componentes
import SearchForm from "../components/SearchForm";
import ResultsDisplay from "../components/ResultsDisplay";
import StatsCards from "../components/StatsCards";
import SearchHistory from "../components/SearchHistory";
import ExportPanel from "../components/ExportPanel";

// Interfaces e tipos
interface SearchHistoryItem {
  id: string;
  query: string;
  platform: "comprehensive" | "scholar" | "lattes" | "orcid";
  timestamp: string;
  resultCount: number;
  duration: number;
}

interface StatsData {
  totalSearches: number;
  totalResults: number;
  avgResponseTime: number;
  successRate: number;
  platformsActive: number;
  lastUpdate: string;
}

interface ApiStatus {
  isOnline: boolean;
  lastChecked: string;
  services: {
    scholar: boolean;
    lattes: boolean;
    orcid: boolean;
  };
}

const Dashboard: React.FC = () => {
  // Estados principais
  const [results, setResults] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [currentQuery, setCurrentQuery] = useState("");
  const [currentPlatform, setCurrentPlatform] = useState<
    "comprehensive" | "scholar" | "lattes" | "orcid"
  >("comprehensive");

  // Estados para histórico e estatísticas
  const [searchHistory, setSearchHistory] = useState<SearchHistoryItem[]>([]);
  const [stats, setStats] = useState<StatsData | null>(null);
  const [apiStatus, setApiStatus] = useState<ApiStatus>({
    isOnline: false,
    lastChecked: "",
    services: {
      scholar: false,
      lattes: false,
      orcid: false,
    },
  });

  // Estados da interface
  const [isStatsLoading, setIsStatsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"search" | "history" | "export">(
    "search"
  );

  // Verificar status da API ao carregar
  useEffect(() => {
    checkApiStatus();
    loadSearchHistory();
    loadStats();

    // Verificar status a cada 30 segundos
    const interval = setInterval(checkApiStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkApiStatus = async () => {
    try {
      // Simular verificação de health check
      const response = await fetch("http://localhost:8000/health");
      const isOnline = response.ok;

      setApiStatus({
        isOnline,
        lastChecked: new Date().toISOString(),
        services: {
          scholar: isOnline,
          lattes: isOnline,
          orcid: isOnline,
        },
      });
    } catch (error) {
      setApiStatus((prev) => ({
        ...prev,
        isOnline: false,
        lastChecked: new Date().toISOString(),
      }));
    }
  };

  const loadSearchHistory = () => {
    const saved = localStorage.getItem("academ-search-history");
    if (saved) {
      try {
        setSearchHistory(JSON.parse(saved));
      } catch (error) {
        console.error("Erro ao carregar histórico:", error);
      }
    }
  };

  const loadStats = async () => {
    setIsStatsLoading(true);
    try {
      // Simular carregamento de estatísticas
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const mockStats: StatsData = {
        totalSearches: searchHistory.length || 0,
        totalResults:
          searchHistory.reduce((sum, item) => sum + item.resultCount, 0) || 0,
        avgResponseTime:
          searchHistory.length > 0
            ? searchHistory.reduce((sum, item) => sum + item.duration, 0) /
              searchHistory.length
            : 0,
        successRate: 98.5,
        platformsActive: apiStatus.isOnline ? 3 : 0,
        lastUpdate: new Date().toISOString(),
      };

      setStats(mockStats);
    } catch (error) {
      console.error("Erro ao carregar estatísticas:", error);
    } finally {
      setIsStatsLoading(false);
    }
  };

  const saveSearchToHistory = (
    query: string,
    platform: string,
    resultCount: number,
    duration: number
  ) => {
    const newSearch: SearchHistoryItem = {
      id: Date.now().toString(),
      query,
      platform: platform as any,
      timestamp: new Date().toISOString(),
      resultCount,
      duration,
    };

    const updatedHistory = [newSearch, ...searchHistory.slice(0, 19)]; // Manter apenas 20 itens
    setSearchHistory(updatedHistory);
    localStorage.setItem(
      "academ-search-history",
      JSON.stringify(updatedHistory)
    );
  };

  const handleSearch = async (
    query: string,
    platform: "comprehensive" | "scholar" | "lattes" | "orcid"
  ) => {
    if (!apiStatus.isOnline) return;

    setIsLoading(true);
    setCurrentQuery(query);
    setCurrentPlatform(platform);
    const startTime = Date.now();

    try {
      let searchResults;

      switch (platform) {
        case "comprehensive":
          searchResults = await comprehensiveService.search(query);
          break;
        case "scholar":
          searchResults = await scholarService.search(query);
          break;
        case "lattes":
          searchResults = await lattesService.searchProfiles(query);
          break;
        case "orcid":
          searchResults = await orcidService.searchProfiles(query);
          break;
        default:
          throw new Error("Plataforma não suportada");
      }

      setResults(searchResults);

      const duration = (Date.now() - startTime) / 1000;
      const resultCount = Array.isArray(searchResults)
        ? searchResults.length
        : searchResults?.total_results || 0;

      saveSearchToHistory(query, platform, resultCount, duration);

      // Atualizar estatísticas
      loadStats();
    } catch (error) {
      console.error("Erro na busca:", error);
      setResults(null);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRepeatSearch = (
    query: string,
    platform: "comprehensive" | "scholar" | "lattes" | "orcid"
  ) => {
    setActiveTab("search");
    handleSearch(query, platform);
  };

  const handleClearHistory = () => {
    setSearchHistory([]);
    localStorage.removeItem("academ-search-history");
    loadStats();
  };

  const handleClearHistoryItem = (id: string) => {
    const updatedHistory = searchHistory.filter((item) => item.id !== id);
    setSearchHistory(updatedHistory);
    localStorage.setItem(
      "academ-search-history",
      JSON.stringify(updatedHistory)
    );
    loadStats();
  };

  const handleExport = async (format: "csv" | "excel", data: any) => {
    try {
      if (format === "csv") {
        await exportService.exportCSV(data);
      } else {
        await exportService.exportExcel(data);
      }
    } catch (error) {
      throw new Error(`Falha na exportação: ${error}`);
    }
  };

  return (
    <div className='min-h-screen bg-gray-50'>
      {/* Header */}
      <header className='bg-white shadow-sm border-b'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='flex items-center justify-between py-4'>
            <div>
              <h1 className='text-2xl font-bold text-gray-900'>
                🔬 Dashboard Acadêmico
              </h1>
              <p className='text-sm text-gray-600'>
                Instituto de Pesquisa Científica - Portal de Busca Unificado
              </p>
            </div>

            {/* Status da API */}
            <div className='flex items-center gap-3'>
              <button
                onClick={checkApiStatus}
                className='p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors'
                title='Atualizar status'
              >
                <RefreshCw className='h-5 w-5' />
              </button>

              <div className='flex items-center gap-2'>
                {apiStatus.isOnline ? (
                  <CheckCircle className='h-5 w-5 text-green-500' />
                ) : (
                  <AlertCircle className='h-5 w-5 text-red-500' />
                )}
                <span
                  className={`text-sm font-medium ${
                    apiStatus.isOnline ? "text-green-700" : "text-red-700"
                  }`}
                >
                  {apiStatus.isOnline ? "API Online" : "API Offline"}
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Conteúdo principal */}
      <main className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
        {/* Estatísticas */}
        <div className='mb-8'>
          <StatsCards stats={stats} isLoading={isStatsLoading} />
        </div>

        {/* Navegação por abas */}
        <div className='mb-6'>
          <nav className='flex space-x-8' aria-label='Tabs'>
            {[
              { id: "search", name: "🔍 Buscar", icon: Activity },
              { id: "history", name: "📚 Histórico", icon: Activity },
              { id: "export", name: "📊 Exportar", icon: Activity },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                }`}
              >
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        {/* Conteúdo das abas */}
        <div className='grid grid-cols-1 lg:grid-cols-3 gap-8'>
          {/* Coluna principal */}
          <div className='lg:col-span-2'>
            {activeTab === "search" && (
              <div className='space-y-6'>
                <div className='bg-white rounded-lg shadow border p-6'>
                  <h2 className='text-lg font-semibold text-gray-900 mb-4'>
                    🎯 Nova Pesquisa
                  </h2>
                  <SearchForm
                    onSearch={handleSearch}
                    isLoading={isLoading}
                    disabled={!apiStatus.isOnline}
                  />
                </div>

                {(results || isLoading) && (
                  <div className='bg-white rounded-lg shadow border p-6'>
                    <ResultsDisplay
                      results={results}
                      searchType={currentPlatform}
                      query={currentQuery}
                    />
                  </div>
                )}
              </div>
            )}

            {activeTab === "history" && (
              <SearchHistory
                history={searchHistory}
                onRepeatSearch={handleRepeatSearch}
                onClearHistory={handleClearHistory}
                onClearItem={handleClearHistoryItem}
              />
            )}

            {activeTab === "export" && (
              <ExportPanel
                results={results}
                searchQuery={currentQuery}
                searchType={currentPlatform}
                onExport={handleExport}
                disabled={!results}
              />
            )}
          </div>

          {/* Sidebar */}
          <div className='space-y-6'>
            {/* Painel de exportação sempre visível */}
            {activeTab !== "export" && (
              <ExportPanel
                results={results}
                searchQuery={currentQuery}
                searchType={currentPlatform}
                onExport={handleExport}
                disabled={!results}
              />
            )}

            {/* Histórico sempre visível (resumido) */}
            {activeTab !== "history" && searchHistory.length > 0 && (
              <div className='bg-white rounded-lg shadow border p-6'>
                <h3 className='text-lg font-semibold text-gray-900 mb-4'>
                  🕒 Buscas Recentes
                </h3>
                <div className='space-y-2'>
                  {searchHistory.slice(0, 3).map((item) => (
                    <button
                      key={item.id}
                      onClick={() =>
                        handleRepeatSearch(item.query, item.platform)
                      }
                      className='w-full text-left p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors'
                    >
                      <p className='font-medium text-gray-900 truncate'>
                        "{item.query}"
                      </p>
                      <p className='text-sm text-gray-500'>
                        {item.platform} • {item.resultCount} resultados
                      </p>
                    </button>
                  ))}
                </div>
                <button
                  onClick={() => setActiveTab("history")}
                  className='w-full mt-3 text-sm text-blue-600 hover:text-blue-800'
                >
                  Ver histórico completo →
                </button>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
