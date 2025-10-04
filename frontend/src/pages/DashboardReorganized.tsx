/**
 * 📊 DASHBOARD REORGANIZADO
 * Interface principal para pesquisa acadêmica
 */

import React, { useState } from "react";
import SearchFormNew from "../components/SearchFormNew";
import ResultsDisplay from "../components/ResultsDisplay";
import StatsCardsSimple from "../components/StatsCardsSimple";
import SearchHistorySimple from "../components/SearchHistorySimple";
import ExportPanelSimple from "../components/ExportPanelSimple";
import { academicService } from "../services/api_new";
import type { SearchResponse } from "../services/api_new";

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

const DashboardReorganized: React.FC = () => {
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(
    null
  );
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchHistory, setSearchHistory] = useState<SearchHistoryItem[]>([]);

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

      // Adicionar ao histórico
      const historyItem: SearchHistoryItem = {
        id: Date.now().toString(),
        query: searchData.query || searchData.profileUrl || "",
        searchType: searchData.searchType,
        platform: searchData.platform,
        timestamp: new Date().toLocaleString(),
        totalResults: result.total_results || 0,
        executionTime: result.execution_time || 0,
      };

      setSearchHistory((prev) => [historyItem, ...prev.slice(0, 9)]); // Manter apenas 10 itens
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
    let platforms: string[] = [];

    if (searchResults.results_by_platform) {
      // Busca completa
      Object.keys(searchResults.results_by_platform).forEach((platform) => {
        platforms.push(platform);
        const platformData = searchResults.results_by_platform![platform];
        if (platformData.publications) {
          totalPublications += platformData.publications.length;
        }
        if (platformData.lattes_profiles) {
          platformData.lattes_profiles.forEach((profile: any) => {
            totalPublications += profile.total_publications || 0;
            totalProjects += profile.total_projects || 0;
          });
        }
      });
    } else {
      // Busca específica
      platforms = [searchResults.platform];
      if (searchResults.data?.publications) {
        totalPublications = searchResults.data.publications.length;
      }
      if (searchResults.data?.lattes_profiles) {
        searchResults.data.lattes_profiles.forEach((profile: any) => {
          totalPublications += profile.total_publications || 0;
          totalProjects += profile.total_projects || 0;
        });
      }
    }

    return {
      totalPublications,
      totalProjects,
      totalAuthors:
        searchResults.lattes_profiles?.length ||
        searchResults.orcid_profiles?.length ||
        0,
      platforms: platforms.join(", "),
      executionTime: searchResults.execution_time,
    };
  };

  const statsData = getStatsData();

  return (
    <div className='min-h-screen bg-gray-50'>
      {/* Header */}
      <header className='bg-white shadow-sm border-b'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6'>
          <div className='flex items-center justify-between'>
            <div>
              <h1 className='text-3xl font-bold text-gray-900'>
                🎓 Academic Research Platform
              </h1>
              <p className='mt-2 text-gray-600'>
                Busca integrada em Google Scholar, Plataforma Lattes e ORCID
              </p>
            </div>
            <div className='text-right'>
              <div className='text-sm text-gray-500'>
                Instituto de Pesquisa Científica
              </div>
              <div className='text-sm text-gray-500'>Versão 3.0</div>
            </div>
          </div>
        </div>
      </header>

      <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
        <div className='grid grid-cols-1 lg:grid-cols-4 gap-8'>
          {/* Coluna principal - Busca e Resultados */}
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
                    <span className='text-red-400'>⚠️</span>
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

            {/* Resultados */}
            {searchResults && (
              <ResultsDisplay
                results={searchResults}
                searchType={searchResults.platform as any}
                query={searchResults.query}
              />
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

export default DashboardReorganized;
