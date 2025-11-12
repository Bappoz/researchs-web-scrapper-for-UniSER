/**
 * 📚 HISTÓRICO DE PESQUISADORES
 * Página dedicada para visualizar todos os pesquisadores coletados no MongoDB
 */

import React, { useState, useEffect } from "react";
import {
  Users,
  Trash2,
  RefreshCw,
  Search,
  AlertCircle,
  CheckCircle,
  Loader2,
  BookOpen,
  GraduationCap,
} from "lucide-react";
import DarkModeToggle from "../components/DarkModeToggle";

interface Researcher {
  id: string; // Este é o nome do pesquisador (vem do backend como "id")
  name: string;
  institution?: string;
  h_index?: number;
  i10_index?: number;
  total_citations?: number;
  total_publications?: number;
  lattes_institution?: string;
  lattes_area?: string;
  lattes_summary?: string;
  profile_url?: string;
  platform?: string;
  timestamp?: string;
}

interface MongoStats {
  total_searches: number;
  filtered_searches: number;
  total_publications: number;
  platforms: string[];
  latest_search?: string;
}

const ResearchersHistory: React.FC = () => {
  const [researchers, setResearchers] = useState<Researcher[]>([]);
  const [filteredResearchers, setFilteredResearchers] = useState<Researcher[]>(
    []
  );
  const [stats, setStats] = useState<MongoStats | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusMessage, setStatusMessage] = useState<{
    type: "success" | "error" | null;
    message: string;
  }>({ type: null, message: "" });

  useEffect(() => {
    loadResearchers();
    loadStats();
  }, []);

  useEffect(() => {
    if (searchTerm.trim()) {
      const filtered = researchers.filter(
        (r) =>
          r.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          r.institution?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          r.lattes_institution
            ?.toLowerCase()
            .includes(searchTerm.toLowerCase()) ||
          r.lattes_area?.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredResearchers(filtered);
    } else {
      setFilteredResearchers(researchers);
    }
  }, [searchTerm, researchers]);

  const loadResearchers = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:8000/mongodb/researchers");
      if (!response.ok) {
        throw new Error(`Erro ${response.status}: ${response.statusText}`);
      }
      const data = await response.json();
      setResearchers(data.researchers || []);
      setFilteredResearchers(data.researchers || []);
    } catch (error) {
      setStatusMessage({
        type: "error",
        message: `Erro ao carregar pesquisadores: ${error}`,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const response = await fetch("http://localhost:8000/mongodb/stats");
      if (response.ok) {
        const data = await response.json();
        setStats(data.stats);
      }
    } catch (error) {
      console.error("Erro ao carregar estatísticas:", error);
    }
  };

  const handleDeleteResearcher = async (id: string, name: string) => {
    const confirmed = window.confirm(
      `⚠️ Tem certeza que deseja deletar "${name}"?\n\n` +
        "Esta ação é IRREVERSÍVEL e também deletará todas as publicações associadas!"
    );

    if (!confirmed) return;

    setIsLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/mongodb/researcher/${id}`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        throw new Error(`Erro ${response.status}: ${response.statusText}`);
      }

      setStatusMessage({
        type: "success",
        message: `✅ Pesquisador "${name}" deletado com sucesso!`,
      });

      // Reload data
      await loadResearchers();
      await loadStats();

      setTimeout(() => {
        setStatusMessage({ type: null, message: "" });
      }, 3000);
    } catch (error) {
      setStatusMessage({
        type: "error",
        message: `❌ Erro ao deletar pesquisador: ${error}`,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearAll = async () => {
    const confirmed = window.confirm(
      "⚠️ ATENÇÃO!\n\n" +
        "Isso irá deletar TODOS os pesquisadores e publicações do banco de dados.\n\n" +
        "Esta ação é IRREVERSÍVEL!\n\n" +
        "Deseja realmente continuar?"
    );

    if (!confirmed) return;

    const doubleConfirm = window.confirm(
      "🚨 CONFIRMAÇÃO FINAL\n\n" +
        "Você tem CERTEZA ABSOLUTA que quer deletar TUDO?\n\n" +
        "Clique OK para confirmar a exclusão permanente."
    );

    if (!doubleConfirm) return;

    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:8000/mongodb/clear", {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error(`Erro ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();

      setStatusMessage({
        type: "success",
        message: `✅ ${data.message || "Banco de dados limpo com sucesso!"}`,
      });

      // Reload data
      await loadResearchers();
      await loadStats();
    } catch (error) {
      setStatusMessage({
        type: "error",
        message: `❌ Erro ao limpar banco de dados: ${error}`,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className='min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200'>
      {/* Header */}
      <header className='bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 transition-colors duration-200'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='flex justify-between items-center h-16'>
            <div className='flex items-center'>
              <BookOpen className='h-8 w-8 text-blue-600 dark:text-blue-400 mr-3' />
              <div>
                <h1 className='text-xl font-semibold text-gray-900 dark:text-white'>
                  Histórico de Pesquisadores
                </h1>
                <p className='text-sm text-gray-500 dark:text-gray-400'>
                  Todos os pesquisadores coletados do MongoDB
                </p>
              </div>
            </div>

            <div className='flex items-center space-x-3'>
              <DarkModeToggle />

              <button
                onClick={loadResearchers}
                disabled={isLoading}
                className='p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors disabled:opacity-50'
                title='Atualizar lista'
              >
                <RefreshCw
                  className={`h-5 w-5 ${isLoading ? "animate-spin" : ""}`}
                />
              </button>

              <button
                onClick={handleClearAll}
                disabled={isLoading}
                className='inline-flex items-center px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50'
              >
                <Trash2 className='h-4 w-4 mr-2' />
                Limpar Tudo
              </button>

              <button
                onClick={() => (window.location.hash = "#/")}
                className='inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors'
              >
                Voltar à Busca
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
        {/* Statistics Cards */}
        {stats && (
          <div className='grid grid-cols-1 md:grid-cols-4 gap-4 mb-8'>
            <div className='bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors duration-200'>
              <div className='flex items-center justify-between'>
                <div>
                  <p className='text-sm font-medium text-gray-600 dark:text-gray-400'>
                    Total de Pesquisas
                  </p>
                  <p className='text-2xl font-bold text-blue-900 dark:text-blue-400'>
                    {stats.total_searches}
                  </p>
                </div>
                <Users className='h-10 w-10 text-blue-600 dark:text-blue-400' />
              </div>
            </div>

            <div className='bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors duration-200'>
              <div className='flex items-center justify-between'>
                <div>
                  <p className='text-sm font-medium text-gray-600 dark:text-gray-400'>
                    Pesquisas Filtradas
                  </p>
                  <p className='text-2xl font-bold text-green-900 dark:text-green-400'>
                    {stats.filtered_searches}
                  </p>
                </div>
                <CheckCircle className='h-10 w-10 text-green-600 dark:text-green-400' />
              </div>
            </div>

            <div className='bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors duration-200'>
              <div className='flex items-center justify-between'>
                <div>
                  <p className='text-sm font-medium text-gray-600 dark:text-gray-400'>
                    Total de Publicações
                  </p>
                  <p className='text-2xl font-bold text-purple-900 dark:text-purple-400'>
                    {stats.total_publications}
                  </p>
                </div>
                <BookOpen className='h-10 w-10 text-purple-600 dark:text-purple-400' />
              </div>
            </div>

            <div className='bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors duration-200'>
              <div className='flex items-center justify-between'>
                <div>
                  <p className='text-sm font-medium text-gray-600 dark:text-gray-400'>
                    Pesquisadores
                  </p>
                  <p className='text-2xl font-bold text-indigo-900 dark:text-indigo-400'>
                    {researchers.length}
                  </p>
                </div>
                <GraduationCap className='h-10 w-10 text-indigo-600 dark:text-indigo-400' />
              </div>
            </div>
          </div>
        )}

        {/* Search Bar */}
        <div className='bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 mb-6 transition-colors duration-200'>
          <div className='flex items-center space-x-3'>
            <Search className='h-5 w-5 text-gray-400' />
            <input
              type='text'
              placeholder='Buscar por nome, instituição ou área de pesquisa...'
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className='flex-1 outline-none bg-transparent text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500'
            />
            {searchTerm && (
              <button
                onClick={() => setSearchTerm("")}
                className='text-gray-400 hover:text-gray-600 dark:hover:text-gray-300'
              >
                ✕
              </button>
            )}
          </div>
        </div>

        {/* Status Message */}
        {statusMessage.type && (
          <div
            className={`mb-6 rounded-lg p-4 border-2 ${
              statusMessage.type === "success"
                ? "bg-green-50 border-green-200 text-green-700"
                : "bg-red-50 border-red-200 text-red-700"
            }`}
          >
            <div className='flex items-center'>
              {statusMessage.type === "success" ? (
                <CheckCircle className='h-5 w-5 mr-2 flex-shrink-0' />
              ) : (
                <AlertCircle className='h-5 w-5 mr-2 flex-shrink-0' />
              )}
              <span className='font-medium'>{statusMessage.message}</span>
            </div>
          </div>
        )}

        {/* Researchers Table */}
        <div className='bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden'>
          <div className='overflow-x-auto'>
            {isLoading ? (
              <div className='flex items-center justify-center py-12'>
                <Loader2 className='h-8 w-8 animate-spin text-blue-600 mr-3' />
                <span className='text-gray-600'>
                  Carregando pesquisadores...
                </span>
              </div>
            ) : filteredResearchers.length === 0 ? (
              <div className='text-center py-12'>
                <Users className='h-16 w-16 text-gray-300 mx-auto mb-4' />
                <p className='text-gray-500 text-lg'>
                  {searchTerm
                    ? "Nenhum pesquisador encontrado com esses critérios"
                    : "Nenhum pesquisador coletado ainda"}
                </p>
                {!searchTerm && (
                  <p className='text-gray-400 text-sm mt-2'>
                    Faça uma busca no Google Scholar para começar a coletar
                    dados
                  </p>
                )}
              </div>
            ) : (
              <table className='min-w-full divide-y divide-gray-200'>
                <thead className='bg-gray-50'>
                  <tr>
                    <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                      Pesquisador
                    </th>
                    <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                      Instituição
                    </th>
                    <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                      Métricas Scholar
                    </th>
                    <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                      Resumo Lattes
                    </th>
                    <th className='px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider'>
                      Ações
                    </th>
                  </tr>
                </thead>
                <tbody className='bg-white divide-y divide-gray-200'>
                  {filteredResearchers.map((researcher) => (
                    <tr
                      key={researcher.id || researcher.name}
                      className='hover:bg-gray-50'
                    >
                      <td className='px-6 py-4 whitespace-nowrap'>
                        <div className='flex items-center'>
                          <GraduationCap className='h-8 w-8 text-blue-600 mr-3' />
                          <div>
                            <div className='text-sm font-medium text-gray-900'>
                              {researcher.name || "Nome não disponível"}
                            </div>
                            {researcher.profile_url && (
                              <a
                                href={researcher.profile_url}
                                target='_blank'
                                rel='noopener noreferrer'
                                className='text-xs text-blue-600 hover:underline'
                              >
                                Ver perfil →
                              </a>
                            )}
                          </div>
                        </div>
                      </td>
                      <td className='px-6 py-4'>
                        <div className='text-sm text-gray-900'>
                          {researcher.institution ||
                            researcher.lattes_institution ||
                            "-"}
                        </div>
                        {researcher.lattes_area && (
                          <div className='text-xs text-gray-500'>
                            Área: {researcher.lattes_area}
                          </div>
                        )}
                      </td>
                      <td className='px-6 py-4 whitespace-nowrap'>
                        <div className='text-sm text-gray-900'>
                          {researcher.h_index !== undefined && (
                            <div>
                              H-Index:{" "}
                              <span className='font-semibold'>
                                {researcher.h_index}
                              </span>
                            </div>
                          )}
                          {researcher.i10_index !== undefined && (
                            <div>
                              i10-Index:{" "}
                              <span className='font-semibold'>
                                {researcher.i10_index}
                              </span>
                            </div>
                          )}
                          {researcher.total_citations !== undefined && (
                            <div className='text-xs text-gray-500'>
                              {researcher.total_citations} citações
                            </div>
                          )}
                          {researcher.total_publications !== undefined && (
                            <div className='text-xs text-gray-500'>
                              {researcher.total_publications} publicações
                            </div>
                          )}
                        </div>
                      </td>
                      <td className='px-6 py-4'>
                        {researcher.lattes_summary ? (
                          <div className='text-sm text-gray-700 max-w-md'>
                            <div className='line-clamp-3'>
                              {researcher.lattes_summary}
                            </div>
                            {researcher.lattes_summary.length > 100 && (
                              <button
                                onClick={() => alert(researcher.lattes_summary)}
                                className='text-xs text-blue-600 hover:underline mt-1'
                              >
                                Ver completo
                              </button>
                            )}
                          </div>
                        ) : (
                          <span className='text-sm text-gray-400'>
                            Não disponível
                          </span>
                        )}
                      </td>
                      <td className='px-6 py-4 whitespace-nowrap text-right text-sm font-medium'>
                        <button
                          onClick={() =>
                            handleDeleteResearcher(
                              researcher.name,
                              researcher.name
                            )
                          }
                          disabled={isLoading}
                          className='text-red-600 hover:text-red-900 disabled:opacity-50'
                          title={`Deletar ${researcher.name}`}
                        >
                          <Trash2 className='h-5 w-5' />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>

        {/* Results count */}
        {filteredResearchers.length > 0 && (
          <div className='mt-4 text-center text-sm text-gray-600'>
            Mostrando {filteredResearchers.length} de {researchers.length}{" "}
            pesquisadores
          </div>
        )}
      </main>
    </div>
  );
};

export default ResearchersHistory;
