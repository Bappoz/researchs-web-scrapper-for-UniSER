/**
 * 📊 DASHBOARD PRINCIPAL
 * Interface principa  const checkAPIStatus = async () => {
    try {
      setApiStatus("checking");
      await academicService.healthCheck();
      setApiStatus("online");
    } catch (error) {
      console.error("API offline:", error);
      setApiStatus("offline");
    }
  };uisa acadêmica do Instituto de Pesquisa Científica
 */

import React, { useState, useEffect } from "react";
import {
  Activity,
  AlertCircle,
  RefreshCw,
  CheckCircle,
  Clock,
  Search,
  BarChart3,
  FileSpreadsheet,
  BookOpen,
} from "lucide-react";

// Serviços da API
import { academicService } from "../services/api_new";

// Componentes
import SearchFormNew from "../components/SearchFormNew";
import ResultsDisplay from "../components/ResultsDisplay";
import StatsCardsSimple from "../components/StatsCardsSimple";
import SearchHistorySimple from "../components/SearchHistorySimple";
import ExportPanelSimple from "../components/ExportPanelSimple";

// Services
import type { SearchResponse } from "../services/api_new";

interface DashboardStats {
  totalSearches: number;
  totalResearchers: number;
  totalPublications: number;
  totalProjects: number;
  lastUpdate: string;
}

const Dashboard: React.FC = () => {
  // States
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(
    null
  );
  const [isLoading, setIsLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState<"checking" | "online" | "offline">(
    "checking"
  );
  const [stats, setStats] = useState<DashboardStats>({
    totalSearches: 0,
    totalResearchers: 0,
    totalPublications: 0,
    totalProjects: 0,
    lastUpdate: new Date().toISOString(),
  });
  const [searchHistory, setSearchHistory] = useState<SearchResponse[]>([]);

  // Verificar status da API ao carregar
  useEffect(() => {
    checkAPIStatus();
    loadSearchHistory();
  }, []);

  const checkAPIStatus = async () => {
    try {
      setApiStatus("checking");
      await healthService.checkAPI();
      await healthService.checkAcademic();
      setApiStatus("online");
    } catch (error) {
      console.error("API offline:", error);
      setApiStatus("offline");
    }
  };

  const loadSearchHistory = () => {
    const history = JSON.parse(localStorage.getItem("searchHistory") || "[]");
    setSearchHistory(history);
    updateStats(history);
  };

  const updateStats = (history: SearchResponse[]) => {
    const totalPublications = history.reduce(
      (sum, search) => sum + search.total_publications,
      0
    );
    const totalProjects = history.reduce(
      (sum, search) => sum + search.total_projects,
      0
    );
    const totalResearchers = history.reduce((sum, search) => {
      const lattesCount = search.lattes_profiles?.length || 0;
      const orcidCount = search.orcid_profiles?.length || 0;
      return sum + lattesCount + orcidCount;
    }, 0);

    setStats({
      totalSearches: history.length,
      totalResearchers,
      totalPublications,
      totalProjects,
      lastUpdate: new Date().toISOString(),
    });
  };

  const handleSearch = async (
    query: string,
    platform: "comprehensive" | "scholar" | "lattes" | "orcid"
  ) => {
    setIsLoading(true);

    try {
      let result: SearchResponse;

      // Por enquanto, só comprehensive está implementado
      result = await comprehensiveService.search(query, 20, false);

      setSearchResults(result);

      // Salvar no histórico
      const newHistory = [result, ...searchHistory.slice(0, 9)]; // Manter apenas 10 últimas
      setSearchHistory(newHistory);
      localStorage.setItem("searchHistory", JSON.stringify(newHistory));
      updateStats(newHistory);
    } catch (error) {
      console.error("Erro na busca:", error);
      // TODO: Mostrar toast de erro
    } finally {
      setIsLoading(false);
    }
  };

  const handleExportToExcel = async () => {
    if (!searchResults) return;

    try {
      const filename = `pesquisa_${searchResults.query}_${
        new Date().toISOString().split("T")[0]
      }`;
      await exportToExcel(searchResults, filename);
      // TODO: Mostrar toast de sucesso
    } catch (error) {
      console.error("Erro no export:", error);
      // TODO: Mostrar toast de erro
    }
  };

  const getStatusIcon = () => {
    switch (apiStatus) {
      case "checking":
        return <RefreshCw className='h-4 w-4 animate-spin text-yellow-500' />;
      case "online":
        return <CheckCircle className='h-4 w-4 text-green-500' />;
      case "offline":
        return <AlertCircle className='h-4 w-4 text-red-500' />;
    }
  };

  const getStatusText = () => {
    switch (apiStatus) {
      case "checking":
        return "Verificando...";
      case "online":
        return "API Online";
      case "offline":
        return "API Offline";
    }
  };

  return (
    <div className='min-h-screen bg-gray-50'>
      {/* Header */}
      <header className='bg-white shadow-sm border-b border-gray-200'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='flex justify-between items-center h-16'>
            <div className='flex items-center'>
              <BookOpen className='h-8 w-8 text-blue-600 mr-3' />
              <div>
                <h1 className='text-xl font-semibold text-gray-900'>
                  Instituto de Pesquisa Científica
                </h1>
                <p className='text-sm text-gray-500'>
                  Sistema de Busca Acadêmica
                </p>
              </div>
            </div>

            <div className='flex items-center space-x-4'>
              <div className='flex items-center space-x-2'>
                {getStatusIcon()}
                <span className='text-sm text-gray-600'>{getStatusText()}</span>
              </div>

              <button
                onClick={checkAPIStatus}
                className='p-2 text-gray-400 hover:text-gray-600 transition-colors'
                title='Verificar status da API'
              >
                <RefreshCw className='h-4 w-4' />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
        {/* Stats Cards */}
        {searchResults && (
          <StatsCardsSimple
            totalPublications={searchResults.total_results || 0}
            totalAuthors={
              searchResults.lattes_profiles?.length ||
              searchResults.orcid_profiles?.length ||
              0
            }
            totalProjects={searchResults.total_projects || 0}
            executionTime={searchResults.execution_time || 0}
          />
        )}

        <div className='mt-8 grid grid-cols-1 lg:grid-cols-3 gap-8'>
          {/* Search Panel */}
          <div className='lg:col-span-2 space-y-6'>
            {/* Search Form */}
            <div className='bg-white rounded-lg shadow-sm border border-gray-200 p-6'>
              <div className='flex items-center mb-4'>
                <Search className='h-5 w-5 text-blue-600 mr-2' />
                <h2 className='text-lg font-medium text-gray-900'>
                  Nova Pesquisa
                </h2>
              </div>

              <SearchForm
                onSearch={handleSearch}
                isLoading={isLoading}
                disabled={apiStatus === "offline"}
              />
            </div>

            {/* Results */}
            {searchResults && (
              <div className='bg-white rounded-lg shadow-sm border border-gray-200'>
                <div className='p-6 border-b border-gray-200'>
                  <div className='flex items-center justify-between'>
                    <div className='flex items-center'>
                      <BarChart3 className='h-5 w-5 text-blue-600 mr-2' />
                      <h2 className='text-lg font-medium text-gray-900'>
                        Resultados da Pesquisa
                      </h2>
                    </div>

                    <div className='flex items-center space-x-2'>
                      <span className='text-sm text-gray-500'>
                        {searchResults.total_results} resultados em{" "}
                        {searchResults.execution_time.toFixed(2)}s
                      </span>

                      <button
                        onClick={handleExportToExcel}
                        className='inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded text-white bg-green-600 hover:bg-green-700 transition-colors'
                      >
                        <FileSpreadsheet className='h-3 w-3 mr-1' />
                        Excel
                      </button>
                    </div>
                  </div>
                </div>

                <ResultsDisplay results={searchResults} />
              </div>
            )}

            {/* Loading State */}
            {isLoading && (
              <div className='bg-white rounded-lg shadow-sm border border-gray-200 p-12'>
                <div className='text-center'>
                  <RefreshCw className='h-8 w-8 animate-spin text-blue-600 mx-auto mb-4' />
                  <p className='text-gray-600'>
                    Realizando busca nas plataformas acadêmicas...
                  </p>
                  <p className='text-sm text-gray-500 mt-2'>
                    Isso pode levar alguns segundos
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className='space-y-6'>
            {/* Export Panel */}
            {searchResults && (
              <ExportPanelSimple
                results={searchResults}
                searchQuery={searchResults.query || "pesquisa"}
              />
            )}

            {/* Search History */}
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
                // Implementar repetição de busca
                console.log("Repetir busca:", historyItem);
              }}
            />

            {/* Quick Stats */}
            <div className='bg-white rounded-lg shadow-sm border border-gray-200 p-6'>
              <div className='flex items-center mb-4'>
                <Clock className='h-5 w-5 text-blue-600 mr-2' />
                <h3 className='text-lg font-medium text-gray-900'>
                  Status do Sistema
                </h3>
              </div>

              <div className='space-y-3'>
                <div className='flex justify-between items-center'>
                  <span className='text-sm text-gray-600'>Google Scholar</span>
                  <span className='text-sm font-medium text-green-600'>
                    Ativo
                  </span>
                </div>
                <div className='flex justify-between items-center'>
                  <span className='text-sm text-gray-600'>
                    Plataforma Lattes
                  </span>
                  <span className='text-sm font-medium text-green-600'>
                    Ativo
                  </span>
                </div>
                <div className='flex justify-between items-center'>
                  <span className='text-sm text-gray-600'>ORCID</span>
                  <span className='text-sm font-medium text-green-600'>
                    Ativo
                  </span>
                </div>
                <div className='flex justify-between items-center pt-2 border-t border-gray-200'>
                  <span className='text-sm text-gray-600'>
                    Última verificação
                  </span>
                  <span className='text-sm text-gray-500'>
                    {new Date().toLocaleTimeString("pt-BR")}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
