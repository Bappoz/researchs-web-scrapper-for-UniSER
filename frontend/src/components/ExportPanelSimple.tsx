/**
 * 📤 PAINEL DE EXPORTAÇÃO EXCEL SIMPLIFICADO
 * Componente para download de resultados em Excel profissional
 */

import React, { useState } from "react";
import {
  Download,
  FileSpreadsheet,
  CheckCircle,
  Loader2,
  BarChart3,
} from "lucide-react";
import type { SearchResponse } from "../services/api_new";

interface ExportPanelProps {
  results: SearchResponse;
  searchQuery: string;
  onExportExcel?: (data: any) => Promise<void>;
}

const ExportPanel: React.FC<ExportPanelProps> = ({
  results,
  searchQuery,
  onExportExcel,
}) => {
  const [isExporting, setIsExporting] = useState(false);
  const [exportSuccess, setExportSuccess] = useState(false);
  const [consolidatedStatus, setConsolidatedStatus] = useState<{
    type: "success" | "error" | null;
    message: string;
  }>({ type: null, message: "" });

  const handleExportExcel = async () => {
    if (!onExportExcel) {
      // Fallback para download direto do servidor (se disponível)
      if (results.excel_file) {
        const link = document.createElement("a");
        link.setAttribute("href", `/download/excel/${results.excel_file}`);
        link.setAttribute("download", results.excel_file);
        link.style.visibility = "hidden";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
      return;
    }

    setIsExporting(true);
    setExportSuccess(false);

    try {
      await onExportExcel({
        results,
        searchQuery,
        searchType: results.platform || "unknown",
        timestamp: new Date().toISOString(),
      });

      setExportSuccess(true);
      setTimeout(() => setExportSuccess(false), 3000);
    } catch (error) {
      console.error("Erro ao exportar Excel:", error);
    } finally {
      setIsExporting(false);
    }
  };

  const handleDownloadConsolidated = async () => {
    setIsExporting(true);
    setConsolidatedStatus({ type: null, message: "" });

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

      setConsolidatedStatus({
        type: "success",
        message: "Excel consolidado baixado com sucesso! 📊",
      });
    } catch (error) {
      setConsolidatedStatus({
        type: "error",
        message: `Erro ao baixar Excel consolidado: ${error}`,
      });
    } finally {
      setIsExporting(false);
      // Limpar status após 4 segundos
      setTimeout(() => {
        setConsolidatedStatus({ type: null, message: "" });
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

  const getResultsStatistics = () => {
    let authors = 0;
    let publications = 0;
    let totalCitations = 0;

    if (results.data?.publications) {
      publications = results.data.publications.length;
      totalCitations = results.data.publications.reduce(
        (sum: number, pub: any) => sum + (pub.cited_by || 0),
        0
      );
    }

    if (results.data?.lattes_profiles) {
      authors += results.data.lattes_profiles.length;
    }

    if (results.data?.orcid_profiles) {
      authors += results.data.orcid_profiles.length;
    }

    if (results.data?.author_profile) {
      authors += 1;
    }

    if (results.results_by_platform) {
      Object.values(results.results_by_platform).forEach(
        (platformData: any) => {
          if (platformData.publications) {
            publications += platformData.publications.length;
            totalCitations += platformData.publications.reduce(
              (sum: number, pub: any) => sum + (pub.cited_by || 0),
              0
            );
          }
          if (platformData.lattes_profiles)
            authors += platformData.lattes_profiles.length;
          if (platformData.orcid_profiles)
            authors += platformData.orcid_profiles.length;
          if (platformData.author_profile) authors += 1;
        }
      );
    }

    return { authors, publications, totalCitations };
  };

  const stats = getResultsStatistics();
  const hasResults = stats.authors > 0 || stats.publications > 0;

  return (
    <div className='bg-white rounded-lg shadow-lg border border-gray-200 p-6'>
      <h3 className='text-lg font-bold text-gray-900 mb-4 flex items-center'>
        <FileSpreadsheet className='h-5 w-5 mr-2 text-green-600' />
        Exportar Excel Profissional
      </h3>

      {!hasResults ? (
        <div className='text-center py-6'>
          <FileSpreadsheet className='h-12 w-12 text-gray-300 mx-auto mb-3' />
          <p className='text-gray-500'>Nenhum resultado para exportar</p>
        </div>
      ) : (
        <div className='space-y-4'>
          {/* Estatísticas rápidas */}
          <div className='bg-gradient-to-r from-blue-50 to-green-50 border border-blue-200 rounded-lg p-4'>
            <div className='grid grid-cols-3 gap-4 text-center'>
              <div>
                <p className='text-lg font-bold text-blue-900'>
                  {stats.authors}
                </p>
                <p className='text-xs text-blue-700'>Pesquisadores</p>
              </div>
              <div>
                <p className='text-lg font-bold text-green-900'>
                  {stats.publications}
                </p>
                <p className='text-xs text-green-700'>Publicações</p>
              </div>
              <div>
                <p className='text-lg font-bold text-purple-900'>
                  {stats.totalCitations}
                </p>
                <p className='text-xs text-purple-700'>Citações</p>
              </div>
            </div>

            <div className='mt-3 pt-3 border-t border-blue-200'>
              <p className='text-sm text-blue-800'>
                <strong>Busca:</strong> "{searchQuery}"
              </p>
              <p className='text-sm text-blue-800'>
                <strong>Fonte:</strong>{" "}
                {results.platform === "scholar"
                  ? "Google Scholar"
                  : results.platform === "lattes"
                  ? "Plataforma Lattes"
                  : results.platform === "orcid"
                  ? "ORCID"
                  : "Múltiplas Plataformas"}
              </p>
            </div>
          </div>

          {/* Botão de exportação */}
          <div className='space-y-3'>
            <button
              onClick={handleExportExcel}
              disabled={isExporting}
              className='w-full flex items-center justify-center space-x-3 px-6 py-3 bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white font-semibold rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl'
            >
              {isExporting ? (
                <>
                  <Loader2 className='h-5 w-5 animate-spin' />
                  <span>Gerando Excel...</span>
                </>
              ) : (
                <>
                  <Download className='h-5 w-5' />
                  <span>Exportar Relatório Excel</span>
                </>
              )}
            </button>

            {exportSuccess && (
              <div className='flex items-center justify-center space-x-2 text-green-700 bg-green-50 border border-green-200 rounded-lg py-2'>
                <CheckCircle className='h-5 w-5' />
                <span className='font-medium'>
                  Excel exportado com sucesso!
                </span>
              </div>
            )}
          </div>

          {/* Seção de Relatórios Consolidados */}
          <div className='bg-gradient-to-r from-purple-50 to-indigo-50 border-2 border-purple-200 rounded-lg p-4'>
            <div className='flex items-center justify-between mb-3'>
              <div>
                <h4 className='text-sm font-bold text-gray-900'>
                  📊 Relatórios Consolidados
                </h4>
                <p className='text-xs text-gray-600 mt-1'>
                  Excel com TODAS as pesquisas filtradas do banco de dados
                </p>
              </div>
              <BarChart3 className='h-8 w-8 text-purple-600' />
            </div>

            <div className='grid grid-cols-1 sm:grid-cols-2 gap-2 mb-3'>
              <button
                onClick={handleDownloadConsolidated}
                disabled={isExporting}
                className='flex items-center justify-center p-2 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-medium rounded-lg transition-all duration-200 disabled:bg-gray-400 disabled:cursor-not-allowed text-sm'
              >
                {isExporting ? (
                  <>
                    <Loader2 className='h-4 w-4 animate-spin mr-1' />
                    Exportando...
                  </>
                ) : (
                  <>
                    <FileSpreadsheet className='h-4 w-4 mr-1' />
                    Excel Consolidado
                  </>
                )}
              </button>

              <button
                onClick={handleViewStats}
                disabled={isExporting}
                className='flex items-center justify-center p-2 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-medium rounded-lg transition-all duration-200 disabled:bg-gray-400 disabled:cursor-not-allowed text-sm'
              >
                <BarChart3 className='h-4 w-4 mr-1' />
                Ver Estatísticas
              </button>
            </div>

            {/* Status da exportação consolidada */}
            {consolidatedStatus.type && (
              <div
                className={`text-xs rounded-lg p-2 border-2 ${
                  consolidatedStatus.type === "success"
                    ? "bg-green-50 border-green-200 text-green-700"
                    : "bg-red-50 border-red-200 text-red-700"
                }`}
              >
                <div className='flex items-center'>
                  {consolidatedStatus.type === "success" ? (
                    <CheckCircle className='h-4 w-4 mr-2' />
                  ) : (
                    <BarChart3 className='h-4 w-4 mr-2' />
                  )}
                  <span className='font-medium'>
                    {consolidatedStatus.message}
                  </span>
                </div>
              </div>
            )}
          </div>

          {/* Informações sobre o Excel */}
          <div className='bg-gray-50 rounded-lg p-3 border'>
            <h4 className='text-sm font-semibold text-gray-700 mb-2'>
              O Excel inclui:
            </h4>
            <ul className='text-xs text-gray-600 space-y-1'>
              <li>✅ Dados organizados em múltiplas abas</li>
              <li>✅ Formatação profissional com cores</li>
              <li>✅ Métricas acadêmicas (H-Index, citações)</li>
              <li>✅ Compatível com Excel 2007+</li>
            </ul>
          </div>

          {/* Status do arquivo no servidor */}
          {results.excel_file && (
            <div className='text-xs text-green-700 bg-green-50 border border-green-200 rounded p-2'>
              <p>
                ✅ <strong>Excel disponível no servidor:</strong>{" "}
                {results.excel_file}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ExportPanel;
