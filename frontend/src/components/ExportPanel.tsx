/**
 * 📊 PAINEL DE EXPORTAÇÃO EXCEL PROFISSIONAL
 * Componente para exportar dados acadêmicos em Excel formatado
 */

import React, { useState } from "react";
import {
  Download,
  FileSpreadsheet,
  Loader2,
  CheckCircle,
  AlertCircle,
  BarChart3,
  Users,
  BookOpen,
  Award,
} from "lucide-react";

interface ExportPanelProps {
  results: any;
  searchQuery: string;
  searchType: "comprehensive" | "scholar" | "lattes" | "orcid";
  onExport: (format: "excel", data: any) => Promise<void>;
  disabled: boolean;
}

const ExportPanel: React.FC<ExportPanelProps> = ({
  results,
  searchQuery,
  searchType,
  onExport,
  disabled,
}) => {
  const [isExporting, setIsExporting] = useState<boolean>(false);
  const [exportStatus, setExportStatus] = useState<{
    type: "success" | "error" | null;
    message: string;
  }>({ type: null, message: "" });

  const handleExport = async () => {
    if (!results || disabled) return;

    setIsExporting(true);
    setExportStatus({ type: null, message: "" });

    try {
      await onExport("excel", {
        results,
        searchQuery,
        searchType,
        timestamp: new Date().toISOString(),
      });

      setExportStatus({
        type: "success",
        message: `Relatório Excel profissional exportado com sucesso!`,
      });
    } catch (error) {
      setExportStatus({
        type: "error",
        message: `Erro ao exportar relatório: ${error}`,
      });
    } finally {
      setIsExporting(false);
      // Limpar status após 4 segundos
      setTimeout(() => {
        setExportStatus({ type: null, message: "" });
      }, 4000);
    }
  };

  const handleDownloadConsolidated = async () => {
    setIsExporting(true);
    setExportStatus({ type: null, message: "" });

    try {
      const response = await fetch("http://localhost:8000/export/consolidated");

      if (!response.ok) {
        throw new Error(`Erro ${response.status}: ${response.statusText}`);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `excel_consolidado_${
        new Date().toISOString().split("T")[0]
      }.xlsx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      setExportStatus({
        type: "success",
        message: "Excel consolidado baixado com sucesso! 📊",
      });
    } catch (error) {
      setExportStatus({
        type: "error",
        message: `Erro ao baixar Excel consolidado: ${error}`,
      });
    } finally {
      setIsExporting(false);
      // Limpar status após 4 segundos
      setTimeout(() => {
        setExportStatus({ type: null, message: "" });
      }, 4000);
    }
  };

  const handleViewStats = async () => {
    try {
      const response = await fetch("http://localhost:8000/mongodb/stats");

      if (!response.ok) {
        throw new Error(`Erro ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      const stats = data.stats || {};

      const statsMessage =
        `📊 Estatísticas do Banco de Dados:\n\n` +
        `🔍 Total de Pesquisas: ${stats.total_searches || 0}\n` +
        `📚 Pesquisas Filtradas: ${stats.filtered_searches || 0}\n` +
        `📝 Total de Publicações: ${stats.total_publications || 0}\n` +
        `🌐 Plataformas: ${stats.platforms?.join(", ") || "Nenhuma"}\n` +
        `📅 Última Busca: ${
          stats.latest_search
            ? new Date(stats.latest_search).toLocaleString("pt-BR")
            : "N/A"
        }`;

      alert(statsMessage);
    } catch (error) {
      alert(`❌ Erro ao carregar estatísticas: ${error}`);
    }
  };

  const getResultStatistics = () => {
    if (!results)
      return {
        authors: 0,
        publications: 0,
        totalCitations: 0,
        maxHIndex: 0,
        maxI10Index: 0,
      };

    if (
      searchType === "comprehensive" &&
      typeof results === "object" &&
      "query" in results
    ) {
      let authors = 0;
      let publications = 0;
      let totalCitations = 0;
      let maxHIndex = 0;
      let maxI10Index = 0;

      // Contar dados do Scholar
      if (results.scholar?.publications) {
        publications += results.scholar.publications.length;
        totalCitations += results.scholar.publications.reduce(
          (sum: number, pub: any) => sum + (pub.cited_by || 0),
          0
        );
      }
      if (results.scholar?.author_profile) {
        authors += 1;
        maxHIndex = Math.max(
          maxHIndex,
          results.scholar.author_profile.h_index || 0
        );
        maxI10Index = Math.max(
          maxI10Index,
          results.scholar.author_profile.i10_index || 0
        );
      }

      // Contar dados do Lattes
      if (results.lattes?.lattes_profiles) {
        authors += results.lattes.lattes_profiles.length;
        results.lattes.lattes_profiles.forEach((profile: any) => {
          maxHIndex = Math.max(maxHIndex, profile.h_index || 0);
          maxI10Index = Math.max(maxI10Index, profile.i10_index || 0);
        });
      }

      // Contar dados do ORCID
      if (results.orcid?.orcid_profiles) {
        authors += results.orcid.orcid_profiles.length;
        results.orcid.orcid_profiles.forEach((profile: any) => {
          maxHIndex = Math.max(maxHIndex, profile.h_index || 0);
          maxI10Index = Math.max(maxI10Index, profile.i10_index || 0);
        });
      }

      return { authors, publications, totalCitations, maxHIndex, maxI10Index };
    }

    // Para buscas específicas de plataforma
    if (Array.isArray(results)) {
      return {
        authors: results.length,
        publications: 0,
        totalCitations: 0,
        maxHIndex: Math.max(...results.map((r) => r.h_index || 0), 0),
        maxI10Index: Math.max(...results.map((r) => r.i10_index || 0), 0),
      };
    }

    return {
      authors: 0,
      publications: 0,
      totalCitations: 0,
      maxHIndex: 0,
      maxI10Index: 0,
    };
  };

  const stats = getResultStatistics();
  const hasResults = stats.authors > 0 || stats.publications > 0;

  return (
    <div className='bg-white rounded-lg shadow-lg border border-gray-200 p-6'>
      <h3 className='text-xl font-bold text-gray-900 mb-6 flex items-center'>
        <FileSpreadsheet className='h-6 w-6 mr-3 text-green-600' />
        Exportar Relatório Excel Profissional
      </h3>

      {!hasResults ? (
        <div className='text-center py-12'>
          <BarChart3 className='h-16 w-16 text-gray-300 mx-auto mb-4' />
          <p className='text-gray-500 text-lg font-medium'>
            Nenhum resultado para exportar
          </p>
          <p className='text-sm text-gray-400 mt-2'>
            Realize uma busca primeiro para gerar o relatório
          </p>
        </div>
      ) : (
        <div className='space-y-6'>
          {/* Estatísticas dos dados */}
          <div className='bg-gradient-to-r from-blue-50 to-green-50 border border-blue-200 rounded-xl p-6'>
            <h4 className='font-bold text-blue-900 mb-4 flex items-center'>
              <BarChart3 className='h-5 w-5 mr-2' />
              Dados Disponíveis para Exportação
            </h4>

            <div className='grid grid-cols-2 md:grid-cols-5 gap-4 mb-4'>
              <div className='text-center'>
                <Users className='h-8 w-8 text-blue-600 mx-auto mb-2' />
                <p className='text-2xl font-bold text-blue-900'>
                  {stats.authors}
                </p>
                <p className='text-sm text-blue-700'>Pesquisadores</p>
              </div>
              <div className='text-center'>
                <BookOpen className='h-8 w-8 text-green-600 mx-auto mb-2' />
                <p className='text-2xl font-bold text-green-900'>
                  {stats.publications}
                </p>
                <p className='text-sm text-green-700'>Publicações</p>
              </div>
              <div className='text-center'>
                <Award className='h-8 w-8 text-purple-600 mx-auto mb-2' />
                <p className='text-2xl font-bold text-purple-900'>
                  {stats.totalCitations}
                </p>
                <p className='text-sm text-purple-700'>Citações Total</p>
              </div>
              <div className='text-center'>
                <BarChart3 className='h-8 w-8 text-orange-600 mx-auto mb-2' />
                <p className='text-2xl font-bold text-orange-900'>
                  {stats.maxHIndex}
                </p>
                <p className='text-sm text-orange-700'>Maior H-Index</p>
              </div>
              <div className='text-center'>
                <BarChart3 className='h-8 w-8 text-green-600 mx-auto mb-2' />
                <p className='text-2xl font-bold text-green-900'>
                  {stats.maxI10Index}
                </p>
                <p className='text-sm text-green-700'>Maior i10-Index</p>
              </div>
            </div>

            <div className='text-sm text-blue-800 space-y-1'>
              <p>
                📝 <strong>Consulta:</strong> "{searchQuery}"
              </p>
              <p>
                🎯 <strong>Fonte:</strong>{" "}
                {searchType === "comprehensive"
                  ? "Busca Completa (Scholar + Lattes + ORCID)"
                  : searchType === "scholar"
                  ? "Google Scholar"
                  : searchType === "lattes"
                  ? "Plataforma Lattes"
                  : "ORCID"}
              </p>
            </div>
          </div>

          {/* Botão de exportação principal */}
          <div className='bg-gradient-to-r from-green-50 to-blue-50 border-2 border-green-200 rounded-xl p-6'>
            <div className='flex items-center justify-between mb-4'>
              <div>
                <h4 className='text-lg font-bold text-gray-900'>
                  Relatório Excel Profissional
                </h4>
                <p className='text-sm text-gray-600 mt-1'>
                  Planilha formatada com múltiplas abas: Resumo, Pesquisadores,
                  Publicações e Métricas
                </p>
              </div>
              <FileSpreadsheet className='h-12 w-12 text-green-600' />
            </div>

            <div className='bg-white rounded-lg p-4 mb-4'>
              <h5 className='font-semibold text-gray-800 mb-2'>
                O relatório inclui:
              </h5>
              <ul className='text-sm text-gray-600 space-y-1'>
                <li>
                  ✅ <strong>Aba Resumo:</strong> Visão geral com gráficos e
                  estatísticas
                </li>
                <li>
                  ✅ <strong>Aba Pesquisadores:</strong> Dados completos dos
                  autores com H-Index e i10-Index
                </li>
                <li>
                  ✅ <strong>Aba Publicações:</strong> Lista detalhada de
                  artigos e citações
                </li>
                <li>
                  ✅ <strong>Aba Métricas:</strong> Análises acadêmicas e
                  indicadores de impacto
                </li>
                <li>
                  ✅ <strong>Formatação:</strong> Cores, fontes e layouts
                  profissionais
                </li>
              </ul>
            </div>

            <button
              onClick={handleExport}
              disabled={disabled || isExporting}
              className='w-full flex items-center justify-center p-4 bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white font-semibold rounded-lg transition-all duration-200 disabled:bg-gray-400 disabled:cursor-not-allowed shadow-lg hover:shadow-xl'
            >
              {isExporting ? (
                <>
                  <Loader2 className='h-6 w-6 animate-spin mr-3' />
                  Gerando Relatório Excel...
                </>
              ) : (
                <>
                  <Download className='h-6 w-6 mr-3' />
                  Exportar Relatório Excel Profissional
                </>
              )}
            </button>
          </div>

          {/* Seção de Relatórios Consolidados */}
          <div className='bg-gradient-to-r from-purple-50 to-indigo-50 border-2 border-purple-200 rounded-xl p-6'>
            <div className='flex items-center justify-between mb-4'>
              <div>
                <h4 className='text-lg font-bold text-gray-900'>
                  📊 Relatórios Consolidados
                </h4>
                <p className='text-sm text-gray-600 mt-1'>
                  Excel com TODAS as pesquisas filtradas do banco de dados
                </p>
              </div>
              <BarChart3 className='h-12 w-12 text-purple-600' />
            </div>

            <div className='bg-white rounded-lg p-4 mb-4'>
              <h5 className='font-semibold text-gray-800 mb-2'>
                Relatório consolidado inclui:
              </h5>
              <ul className='text-sm text-gray-600 space-y-1'>
                <li>
                  ✅ <strong>Resumo Executivo:</strong> Estatísticas de todas as
                  buscas
                </li>
                <li>
                  ✅ <strong>Dados Agregados:</strong> Todos os pesquisadores e
                  publicações
                </li>
                <li>
                  ✅ <strong>Métricas Globais:</strong> Análise cross-platform
                </li>
                <li>
                  ✅ <strong>Filtros Aplicados:</strong> Apenas dados com
                  keywords de aging
                </li>
              </ul>
            </div>

            <div className='grid grid-cols-1 sm:grid-cols-2 gap-3'>
              <button
                onClick={handleDownloadConsolidated}
                disabled={isExporting}
                className='flex items-center justify-center p-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold rounded-lg transition-all duration-200 disabled:bg-gray-400 disabled:cursor-not-allowed shadow-lg hover:shadow-xl'
              >
                {isExporting ? (
                  <>
                    <Loader2 className='h-5 w-5 animate-spin mr-2' />
                    Exportando...
                  </>
                ) : (
                  <>
                    <FileSpreadsheet className='h-5 w-5 mr-2' />
                    Excel Consolidado
                  </>
                )}
              </button>

              <button
                onClick={handleViewStats}
                disabled={isExporting}
                className='flex items-center justify-center p-3 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-semibold rounded-lg transition-all duration-200 disabled:bg-gray-400 disabled:cursor-not-allowed shadow-lg hover:shadow-xl'
              >
                <BarChart3 className='h-5 w-5 mr-2' />
                Ver Estatísticas
              </button>
            </div>
          </div>

          {/* Status da exportação */}
          {exportStatus.type && (
            <div
              className={`rounded-xl p-4 border-2 ${
                exportStatus.type === "success"
                  ? "bg-green-50 border-green-200"
                  : "bg-red-50 border-red-200"
              }`}
            >
              <div className='flex items-center'>
                {exportStatus.type === "success" ? (
                  <CheckCircle className='h-6 w-6 text-green-600 mr-3' />
                ) : (
                  <AlertCircle className='h-6 w-6 text-red-600 mr-3' />
                )}
                <p
                  className={`font-medium ${
                    exportStatus.type === "success"
                      ? "text-green-800"
                      : "text-red-800"
                  }`}
                >
                  {exportStatus.message}
                </p>
              </div>
            </div>
          )}

          {/* Informações sobre o arquivo */}
          <div className='text-sm text-gray-500 bg-gray-50 rounded-lg p-4 border'>
            <div className='flex items-start space-x-2'>
              <FileSpreadsheet className='h-5 w-5 text-gray-400 mt-0.5' />
              <div>
                <p className='font-medium text-gray-700 mb-2'>
                  Informações do Arquivo Excel:
                </p>
                <ul className='space-y-1 text-xs'>
                  <li>
                    📁 <strong>Local:</strong> Pasta <code>src/export/</code> do
                    projeto
                  </li>
                  <li>
                    📝 <strong>Nome:</strong>{" "}
                    pesquisa_completa_[consulta]_[data-hora].xlsx
                  </li>
                  <li>
                    🎨 <strong>Formato:</strong> Excel com formatação
                    profissional e cores
                  </li>
                  <li>
                    📊 <strong>Compatibilidade:</strong> Excel 2007+ e
                    LibreOffice Calc
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExportPanel;
