/**
 * 📤 PAINEL DE EXPORTAÇÃO EXCEL SIMPLIFICADO
 * Componente para download de resultados em Excel profissional
 */

import React, { useState } from "react";
import { Download, FileSpreadsheet, CheckCircle, Loader2 } from "lucide-react";
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
