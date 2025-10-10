/**
 * 📊 DASHBOARD DE BUSCA DE PESQUISADORES
 * Interface principal para buscar e selecionar pesquisadores
 */

import React, { useState, useEffect } from "react";
import {
  Activity,
  AlertCircle,
  RefreshCw,
  CheckCircle,
  Users,
  Download,
  BookOpen,
} from "lucide-react";

// Serviços da API
import { academicService, authorsService } from "../services/api_new";
import type {
  AuthorsSearchResponse,
  AuthorPublicationsResponse,
  AuthorInfo,
} from "../services/api_new";

// Componentes
import AuthorSearchForm from "../components/AuthorSearchForm";
import AuthorsList from "../components/AuthorsList";
import ResultsDisplay from "../components/ResultsDisplay";

interface SearchHistoryItem {
  id: string;
  query: string;
  timestamp: string;
  totalAuthors: number;
  selectedAuthor?: string;
}

const ResearchersDashboard: React.FC = () => {
  // Estados principais
  const [authorsResults, setAuthorsResults] =
    useState<AuthorsSearchResponse | null>(null);
  const [selectedAuthor, setSelectedAuthor] = useState<AuthorInfo | null>(null);
  const [authorPublications, setAuthorPublications] =
    useState<AuthorPublicationsResponse | null>(null);

  // Estados de controle
  const [isSearchingAuthors, setIsSearchingAuthors] = useState(false);
  const [isLoadingPublications, setIsLoadingPublications] = useState(false);
  const [isExporting, setIsExporting] = useState(false);

  // Estados de status
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
    const history = JSON.parse(
      localStorage.getItem("researchersSearchHistory") || "[]"
    );
    setSearchHistory(history);
  };

  const saveSearchHistory = (newItem: SearchHistoryItem) => {
    const updatedHistory = [newItem, ...searchHistory.slice(0, 9)];
    setSearchHistory(updatedHistory);
    localStorage.setItem(
      "researchersSearchHistory",
      JSON.stringify(updatedHistory)
    );
  };

  const handleSearchAuthors = async (
    authorName: string,
    maxResults: number
  ) => {
    setIsSearchingAuthors(true);
    setError(null);
    setAuthorsResults(null);
    setSelectedAuthor(null);
    setAuthorPublications(null);

    try {
      console.log(`🔍 Buscando autores: ${authorName}`);

      const result = await authorsService.searchMultipleAuthors(
        authorName,
        maxResults
      );

      if (result.success) {
        setAuthorsResults(result);

        // Salvar no histórico
        const historyItem: SearchHistoryItem = {
          id: Date.now().toString(),
          query: authorName,
          timestamp: new Date().toLocaleString("pt-BR"),
          totalAuthors: result.total_results,
        };
        saveSearchHistory(historyItem);

        console.log(`✅ Encontrados ${result.total_results} autores`);
      } else {
        setError(result.message || "Nenhum autor encontrado");
      }
    } catch (error: any) {
      console.error("Erro na busca de autores:", error);
      setError(error.message || "Erro ao buscar pesquisadores");
    } finally {
      setIsSearchingAuthors(false);
    }
  };

  const handleSelectAuthor = async (author: AuthorInfo) => {
    setSelectedAuthor(author);
    setIsLoadingPublications(true);
    setError(null);
    setAuthorPublications(null);

    try {
      console.log(`📚 Carregando publicações de: ${author.name}`);

      const result = await authorsService.getAuthorPublications(
        author.author_id,
        50,
        false
      );

      if (result.success) {
        setAuthorPublications(result);
        console.log(`✅ Carregadas ${result.total_results} publicações`);
      } else {
        setError(result.message || "Erro ao carregar publicações");
      }
    } catch (error: any) {
      console.error("Erro ao carregar publicações:", error);
      setError(error.message || "Erro ao carregar publicações do pesquisador");
    } finally {
      setIsLoadingPublications(false);
    }
  };

  const handleExportToExcel = async () => {
    if (!selectedAuthor) return;

    setIsExporting(true);
    setError(null);

    try {
      console.log(`📊 Exportando dados de: ${selectedAuthor.name}`);

      const result = await authorsService.getAuthorPublications(
        selectedAuthor.author_id,
        100,
        true // Solicitar exportação Excel
      );

      if (result.success) {
        if (result.excel_file) {
          // Simular download (o arquivo já foi criado no servidor)
          alert(
            `✅ Excel gerado com sucesso!\nArquivo: ${result.excel_file}\nLocalização: pasta exports/`
          );
        } else if (result.excel_error) {
          setError(`Erro na exportação: ${result.excel_error}`);
        } else {
          alert("✅ Dados exportados com sucesso!");
        }
      } else {
        setError(result.message || "Erro na exportação");
      }
    } catch (error: any) {
      console.error("Erro na exportação:", error);
      setError(error.message || "Erro ao exportar dados");
    } finally {
      setIsExporting(false);
    }
  };

  const renderApiStatus = () => {
    if (apiStatus === "checking") {
      return (
        <div className='flex items-center text-gray-600'>
          <RefreshCw className='h-4 w-4 mr-2 animate-spin' />
          Verificando API...
        </div>
      );
    }

    if (apiStatus === "online") {
      return (
        <div className='flex items-center text-green-600'>
          <CheckCircle className='h-4 w-4 mr-2' />
          API Online
        </div>
      );
    }

    return (
      <div className='flex items-center text-red-600'>
        <AlertCircle className='h-4 w-4 mr-2' />
        API Offline
      </div>
    );
  };

  return (
    <div className='min-h-screen bg-gray-50'>
      {/* Header */}
      <div className='bg-white border-b border-gray-200'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='flex justify-between items-center py-6'>
            <div className='flex items-center'>
              <Users className='h-8 w-8 text-blue-600 mr-3' />
              <div>
                <h1 className='text-2xl font-bold text-gray-900'>
                  Busca de Pesquisadores
                </h1>
                <p className='text-gray-600'>
                  Encontre pesquisadores no Google Scholar e explore suas
                  publicações
                </p>
              </div>
            </div>
            <div className='flex items-center space-x-4'>
              {renderApiStatus()}
              <button
                onClick={checkApiStatus}
                className='p-2 text-gray-400 hover:text-gray-600 transition-colors'
                title='Verificar status da API'
              >
                <RefreshCw className='h-5 w-5' />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
        <div className='grid grid-cols-1 lg:grid-cols-3 gap-8'>
          {/* Coluna da Esquerda - Formulário de Busca */}
          <div className='lg:col-span-1'>
            <AuthorSearchForm
              onSearch={handleSearchAuthors}
              isLoading={isSearchingAuthors}
              disabled={apiStatus === "offline"}
            />

            {/* Histórico de Buscas */}
            {searchHistory.length > 0 && (
              <div className='mt-6 bg-white rounded-lg shadow-lg p-4'>
                <h3 className='text-lg font-semibold text-gray-800 mb-3'>
                  📋 Histórico de Buscas
                </h3>
                <div className='space-y-2'>
                  {searchHistory.slice(0, 5).map((item) => (
                    <div
                      key={item.id}
                      className='p-2 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors'
                      onClick={() => handleSearchAuthors(item.query, 10)}
                    >
                      <div className='font-medium text-sm text-gray-900'>
                        {item.query}
                      </div>
                      <div className='text-xs text-gray-500'>
                        {item.totalAuthors} autores • {item.timestamp}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Coluna do Meio - Lista de Autores */}
          <div className='lg:col-span-1'>
            {authorsResults && (
              <div className='bg-white rounded-lg shadow-lg p-6'>
                <AuthorsList
                  authors={authorsResults.authors}
                  isLoading={isSearchingAuthors}
                  onSelectAuthor={handleSelectAuthor}
                  selectedAuthor={selectedAuthor || undefined}
                />
              </div>
            )}
          </div>

          {/* Coluna da Direita - Publicações e Exportação */}
          <div className='lg:col-span-1'>
            {selectedAuthor && (
              <div className='space-y-6'>
                {/* Painel de Informações do Autor Selecionado */}
                <div className='bg-white rounded-lg shadow-lg p-6'>
                  <h3 className='text-lg font-semibold text-gray-800 mb-4'>
                    👨‍🎓 Pesquisador Selecionado
                  </h3>
                  <div className='space-y-3'>
                    <div>
                      <span className='font-medium text-gray-900'>
                        {selectedAuthor.name}
                      </span>
                    </div>
                    <div className='text-sm text-gray-600'>
                      {selectedAuthor.institution}
                    </div>
                    <div className='flex items-center space-x-4 text-sm text-gray-600'>
                      <span>
                        {selectedAuthor.total_citations.toLocaleString()}{" "}
                        citações
                      </span>
                      {selectedAuthor.h_index > 0 && (
                        <span>H-Index: {selectedAuthor.h_index}</span>
                      )}
                      {selectedAuthor.i10_index > 0 && (
                        <span>• i10: {selectedAuthor.i10_index}</span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Painel de Exportação */}
                <div className='bg-white rounded-lg shadow-lg p-6'>
                  <h3 className='text-lg font-semibold text-gray-800 mb-4'>
                    📊 Exportar Dados
                  </h3>
                  <p className='text-sm text-gray-600 mb-4'>
                    Exporte todas as publicações deste pesquisador para Excel
                    com formatação profissional.
                  </p>

                  <button
                    onClick={handleExportToExcel}
                    disabled={isExporting || isLoadingPublications}
                    className='w-full flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors'
                  >
                    {isExporting ? (
                      <>
                        <RefreshCw className='h-4 w-4 mr-2 animate-spin' />
                        Gerando Excel...
                      </>
                    ) : (
                      <>
                        <Download className='h-4 w-4 mr-2' />
                        Exportar para Excel
                      </>
                    )}
                  </button>

                  {authorPublications && (
                    <div className='mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg'>
                      <div className='flex items-center mb-2'>
                        <BookOpen className='h-4 w-4 text-blue-600 mr-2' />
                        <span className='text-sm font-medium text-blue-900'>
                          Publicações Carregadas
                        </span>
                      </div>
                      <p className='text-sm text-blue-800'>
                        {authorPublications.total_results} publicações
                        encontradas
                      </p>
                    </div>
                  )}
                </div>

                {/* Prévia das Publicações */}
                {authorPublications && authorPublications.publications && (
                  <div className='bg-white rounded-lg shadow-lg p-6'>
                    <h3 className='text-lg font-semibold text-gray-800 mb-4'>
                      📚 Publicações ({authorPublications.total_results})
                    </h3>

                    <ResultsDisplay
                      results={{
                        success: true,
                        message: "Publicações carregadas",
                        platform: "scholar",
                        search_type: "author_publications",
                        query: selectedAuthor.name,
                        total_results: authorPublications.total_results,
                        publications: authorPublications.publications,
                      }}
                      isLoading={isLoadingPublications}
                    />
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Mensagens de Erro */}
        {error && (
          <div className='mt-6 bg-red-50 border border-red-200 rounded-lg p-4'>
            <div className='flex items-center'>
              <AlertCircle className='h-5 w-5 text-red-600 mr-2' />
              <span className='text-red-800'>{error}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResearchersDashboard;
