/**
 * 📊 DASHBOARD SIMPLIFICADO
 * Interface principal para pesquisa acadêmica - versão funcional
 */

import React, { useState, useEffect } from "react";
import {
  Activity,
  AlertCircle,
  RefreshCw,
  CheckCircle,
  BookOpen,
} from "lucide-react";

// Serviços da API
import { academicService } from "../services/api_new";
import type { SearchResponse } from "../services/api_new";

// Componentes
import SearchFormNew from "../components/SearchFormNew";
import StatsCardsSimple from "../components/StatsCardsSimple";
import SearchHistorySimple from "../components/SearchHistorySimple";
import ExportPanelSimple from "../components/ExportPanelSimple";
import ResultsDisplay from "../components/ResultsDisplay";
import TabsDemo from "../components/TabsDemo";

interface SearchData {
  query: string;
  searchType: "author" | "topic" | "profile" | "comprehensive";
  platform: "scholar" | "lattes" | "orcid" | "all";
  profileUrl?: string;
  maxResults: number;
  saveFile: boolean;
}

interface SearchHistoryItem {
  id: string;
  query: string;
  searchType: string;
  platform: string;
  timestamp: string;
  totalResults: number;
  executionTime: number;
}

const Dashboard: React.FC = () => {
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(
    null
  );
  const [isLoading, setIsLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState<"checking" | "online" | "offline">(
    "checking"
  );
  const [searchHistory, setSearchHistory] = useState<SearchHistoryItem[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    checkApiStatus();
    loadSearchHistory();
  }, []);

  const checkApiStatus = async () => {
    try {
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

  const saveSearchHistory = (newItem: SearchHistoryItem) => {
    const updatedHistory = [newItem, ...searchHistory.slice(0, 9)];
    setSearchHistory(updatedHistory);
    localStorage.setItem("searchHistory", JSON.stringify(updatedHistory));
  };

  const handleSearch = async (searchData: SearchData) => {
    setIsLoading(true);
    setError(null);
    setSearchResults(null);

    try {
      let result: SearchResponse;

      // Escolher método baseado no tipo de busca
      if (searchData.searchType === "profile") {
        result = await academicService.searchByProfileLink(
          searchData.profileUrl!,
          searchData.platform === "all" ? undefined : searchData.platform
        );
      } else if (
        searchData.searchType === "comprehensive" ||
        searchData.platform === "all"
      ) {
        result = await academicService.comprehensiveSearch(
          searchData.query,
          searchData.searchType === "comprehensive"
            ? "both"
            : searchData.searchType,
          searchData.platform === "all" ? "all" : searchData.platform,
          searchData.maxResults,
          searchData.saveFile
        );
      } else {
        // Busca específica por plataforma
        if (searchData.searchType === "author") {
          switch (searchData.platform) {
            case "scholar":
              result = await academicService.searchAuthorScholar(
                searchData.query,
                searchData.maxResults,
                searchData.saveFile
              );
              break;
            case "lattes":
              result = await academicService.searchAuthorLattes(
                searchData.query,
                searchData.maxResults
              );
              break;
            case "orcid":
              result = await academicService.searchAuthorOrcid(
                searchData.query,
                searchData.maxResults
              );
              break;
            default:
              throw new Error("Plataforma não suportada para busca por autor");
          }
        } else {
          // searchType === "topic"
          switch (searchData.platform) {
            case "scholar":
              result = await academicService.searchTopicScholar(
                searchData.query,
                searchData.maxResults,
                searchData.saveFile
              );
              break;
            case "lattes":
              result = await academicService.searchTopicLattes(
                searchData.query,
                searchData.maxResults
              );
              break;
            case "orcid":
              result = await academicService.searchTopicOrcid(
                searchData.query,
                searchData.maxResults
              );
              break;
            default:
              throw new Error("Plataforma não suportada para busca por tema");
          }
        }
      }

      setSearchResults(result);

      // Salvar no histórico
      const historyItem: SearchHistoryItem = {
        id: Date.now().toString(),
        query: searchData.query || searchData.profileUrl || "",
        searchType: searchData.searchType,
        platform: searchData.platform,
        timestamp: new Date().toISOString(),
        totalResults: result.total_results || 0,
        executionTime: result.execution_time || 0,
      };

      saveSearchHistory(historyItem);
    } catch (err) {
      console.error("Erro na busca:", err);
      setError(
        err instanceof Error ? err.message : "Erro desconhecido na busca"
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleRepeatSearch = (historyItem: SearchHistoryItem) => {
    const searchData: SearchData = {
      query: historyItem.query,
      searchType: historyItem.searchType as any,
      platform: historyItem.platform as any,
      maxResults: 10,
      saveFile: false,
    };
    handleSearch(searchData);
  };

  // Extrair dados para estatísticas
  const getStatsData = () => {
    if (!searchResults) return null;

    let totalPublications = 0;
    let totalProjects = 0;
    let totalAuthors = 0;

    if (searchResults.results_by_platform) {
      // Busca completa
      Object.values(searchResults.results_by_platform).forEach(
        (platformData: any) => {
          if (platformData && typeof platformData === "object") {
            if (platformData.publications) {
              totalPublications += platformData.publications.length;
            }
            if (platformData.lattes_profiles) {
              totalAuthors += platformData.lattes_profiles.length;
              platformData.lattes_profiles.forEach((profile: any) => {
                totalPublications += profile.total_publications || 0;
                totalProjects += profile.total_projects || 0;
              });
            }
            if (platformData.orcid_profiles) {
              totalAuthors += platformData.orcid_profiles.length;
            }
          }
        }
      );
    } else {
      // Busca específica
      if (searchResults.data?.publications) {
        totalPublications = searchResults.data.publications.length;
      }
      if (searchResults.data?.lattes_profiles) {
        totalAuthors = searchResults.data.lattes_profiles.length;
        searchResults.data.lattes_profiles.forEach((profile: any) => {
          totalPublications += profile.total_publications || 0;
          totalProjects += profile.total_projects || 0;
        });
      }
      if (searchResults.data?.orcid_profiles) {
        totalAuthors = searchResults.data.orcid_profiles.length;
      }
    }

    return {
      totalPublications,
      totalProjects,
      totalAuthors,
      executionTime: searchResults.execution_time || 0,
    };
  };

  const statsData = getStatsData();

  return (
    <div className='min-h-screen bg-gray-50'>
      {/* Header */}
      <header className='bg-white shadow-sm border-b'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6'>
          <div className='flex items-center justify-between'>
            <div className='flex items-center'>
              <BookOpen className='h-8 w-8 text-blue-600 mr-3' />
              <div>
                <h1 className='text-3xl font-bold text-gray-900'>
                  Academic Research Platform
                </h1>
                <p className='mt-1 text-sm text-gray-600'>
                  Instituto de Pesquisa Científica
                </p>
              </div>
            </div>

            <div className='flex items-center space-x-4'>
              {/* Status da API */}
              <div className='flex items-center space-x-2'>
                {apiStatus === "checking" && (
                  <div className='flex items-center'>
                    <Activity className='h-4 w-4 text-yellow-500 animate-pulse mr-2' />
                    <span className='text-sm text-gray-600'>
                      Verificando...
                    </span>
                  </div>
                )}
                {apiStatus === "online" && (
                  <div className='flex items-center'>
                    <CheckCircle className='h-4 w-4 text-green-500 mr-2' />
                    <span className='text-sm text-green-600'>API Online</span>
                  </div>
                )}
                {apiStatus === "offline" && (
                  <div className='flex items-center'>
                    <AlertCircle className='h-4 w-4 text-red-500 mr-2' />
                    <span className='text-sm text-red-600'>API Offline</span>
                  </div>
                )}
              </div>

              <button
                onClick={checkApiStatus}
                className='p-2 text-gray-400 hover:text-gray-600 transition-colors'
                title='Verificar status da API'
              >
                <RefreshCw className='h-4 w-4' />
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
        <div className='grid grid-cols-1 lg:grid-cols-4 gap-8'>
          {/* Coluna principal */}
          <div className='lg:col-span-3 space-y-8'>
            {/* Formulário de Busca */}
            <SearchFormNew onSearch={handleSearch} isLoading={isLoading} />

            {/* Estatísticas */}
            {statsData && (
              <StatsCardsSimple
                totalPublications={statsData.totalPublications}
                totalAuthors={statsData.totalAuthors}
                totalProjects={statsData.totalProjects}
                executionTime={statsData.executionTime}
              />
            )}

            {/* Erro */}
            {error && (
              <div className='bg-red-50 border border-red-200 rounded-lg p-4'>
                <div className='flex'>
                  <div className='flex-shrink-0'>
                    <AlertCircle className='h-5 w-5 text-red-400' />
                  </div>
                  <div className='ml-3'>
                    <h3 className='text-sm font-medium text-red-800'>
                      Erro na Busca
                    </h3>
                    <div className='mt-2 text-sm text-red-700'>{error}</div>
                  </div>
                </div>
              </div>
            )}

            {/* Loading */}
            {isLoading && (
              <div className='bg-blue-50 border border-blue-200 rounded-lg p-8 text-center'>
                <Activity className='h-8 w-8 text-blue-500 animate-spin mx-auto mb-4' />
                <h3 className='text-lg font-medium text-blue-900 mb-2'>
                  Pesquisando...
                </h3>
                <p className='text-blue-700'>
                  Buscando em bases acadêmicas. Isso pode levar alguns segundos.
                </p>
              </div>
            )}

            {/* Informações sobre as Abas */}
            {!searchResults && !isLoading && <TabsDemo />}

            {/* Resultados */}
            {searchResults && (
              <ResultsDisplay results={searchResults} isLoading={isLoading} />
            )}
          </div>

          {/* Sidebar */}
          <div className='lg:col-span-1 space-y-6'>
            {/* Histórico de Buscas */}
            <SearchHistorySimple
              history={searchHistory}
              onRepeatSearch={handleRepeatSearch}
            />

            {/* Painel de Export */}
            {searchResults && (
              <ExportPanelSimple
                results={searchResults}
                searchQuery={searchResults.query}
              />
            )}

            {/* Status das Plataformas */}
            <div className='bg-white rounded-lg shadow p-4'>
              <h3 className='text-lg font-medium text-gray-900 mb-3'>
                Status das Plataformas
              </h3>
              <div className='space-y-2'>
                <div className='flex items-center justify-between'>
                  <span className='text-sm text-gray-600'>Google Scholar</span>
                  <span className='text-green-500'>●</span>
                </div>
                <div className='flex items-center justify-between'>
                  <span className='text-sm text-gray-600'>
                    Plataforma Lattes
                  </span>
                  <span className='text-green-500'>●</span>
                </div>
                <div className='flex items-center justify-between'>
                  <span className='text-sm text-gray-600'>ORCID</span>
                  <span className='text-green-500'>●</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
