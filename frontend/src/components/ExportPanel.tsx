/**
 * 📊 PAINEL DE EXPORTAÇÃO
 * Componente para exportar dados em diferentes formatos
 */

import React, { useState } from "react";
import {
  Download,
  FileText,
  FileSpreadsheet,
  Loader2,
  CheckCircle,
  AlertCircle,
} from "lucide-react";

interface ExportPanelProps {
  results: any;
  searchQuery: string;
  searchType: "comprehensive" | "scholar" | "lattes" | "orcid";
  onExport: (format: "csv" | "excel", data: any) => Promise<void>;
  disabled: boolean;
}

const ExportPanel: React.FC<ExportPanelProps> = ({
  results,
  searchQuery,
  searchType,
  onExport,
  disabled,
}) => {
  const [isExporting, setIsExporting] = useState<"csv" | "excel" | null>(null);
  const [exportStatus, setExportStatus] = useState<{
    type: "success" | "error" | null;
    message: string;
  }>({ type: null, message: "" });

  const handleExport = async (format: "csv" | "excel") => {
    if (!results || disabled) return;

    setIsExporting(format);
    setExportStatus({ type: null, message: "" });

    try {
      await onExport(format, {
        results,
        searchQuery,
        searchType,
        timestamp: new Date().toISOString(),
      });

      setExportStatus({
        type: "success",
        message: `Arquivo ${format.toUpperCase()} exportado com sucesso!`,
      });
    } catch (error) {
      setExportStatus({
        type: "error",
        message: `Erro ao exportar arquivo: ${error}`,
      });
    } finally {
      setIsExporting(null);
      // Limpar status após 3 segundos
      setTimeout(() => {
        setExportStatus({ type: null, message: "" });
      }, 3000);
    }
  };

  const getResultCount = () => {
    if (!results) return 0;

    if (
      searchType === "comprehensive" &&
      typeof results === "object" &&
      "query" in results
    ) {
      let total = 0;
      if (results.scholar) total += results.scholar.total_results;
      if (results.lattes) total += results.lattes.total_results;
      if (results.orcid) total += results.orcid.total_results;
      return total;
    }

    if (Array.isArray(results)) {
      return results.length;
    }

    return 0;
  };

  const resultCount = getResultCount();
  const hasResults = resultCount > 0;

  return (
    <div className='bg-white rounded-lg shadow border p-6'>
      <h3 className='text-lg font-semibold text-gray-900 mb-4 flex items-center'>
        <Download className='h-5 w-5 mr-2 text-gray-600' />
        Exportar Resultados
      </h3>

      {!hasResults ? (
        <div className='text-center py-8'>
          <FileText className='h-12 w-12 text-gray-300 mx-auto mb-4' />
          <p className='text-gray-500'>Nenhum resultado para exportar</p>
          <p className='text-sm text-gray-400 mt-1'>
            Realize uma busca primeiro
          </p>
        </div>
      ) : (
        <div className='space-y-4'>
          {/* Informações dos dados */}
          <div className='bg-blue-50 border border-blue-200 rounded-lg p-4'>
            <div className='flex items-center justify-between mb-2'>
              <h4 className='font-medium text-blue-900'>Dados Disponíveis</h4>
              <span className='text-sm text-blue-700 font-medium'>
                {resultCount} {resultCount === 1 ? "resultado" : "resultados"}
              </span>
            </div>
            <p className='text-sm text-blue-700'>
              📝 Consulta: "{searchQuery}"
            </p>
            <p className='text-sm text-blue-700'>
              🎯 Plataforma:{" "}
              {searchType === "comprehensive"
                ? "Busca Completa"
                : searchType === "scholar"
                ? "Google Scholar"
                : searchType === "lattes"
                ? "Plataforma Lattes"
                : "ORCID"}
            </p>
          </div>

          {/* Opções de exportação */}
          <div className='space-y-3'>
            {/* Export CSV */}
            <button
              onClick={() => handleExport("csv")}
              disabled={disabled || isExporting !== null}
              className='w-full flex items-center justify-between p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:bg-gray-100 disabled:cursor-not-allowed'
            >
              <div className='flex items-center'>
                <FileText className='h-6 w-6 text-green-600 mr-3' />
                <div className='text-left'>
                  <p className='font-medium text-gray-900'>Exportar CSV</p>
                  <p className='text-sm text-gray-500'>
                    Formato compatível com Excel e análise de dados
                  </p>
                </div>
              </div>
              {isExporting === "csv" ? (
                <Loader2 className='h-5 w-5 animate-spin text-gray-600' />
              ) : (
                <Download className='h-5 w-5 text-gray-400' />
              )}
            </button>

            {/* Export Excel */}
            <button
              onClick={() => handleExport("excel")}
              disabled={disabled || isExporting !== null}
              className='w-full flex items-center justify-between p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:bg-gray-100 disabled:cursor-not-allowed'
            >
              <div className='flex items-center'>
                <FileSpreadsheet className='h-6 w-6 text-blue-600 mr-3' />
                <div className='text-left'>
                  <p className='font-medium text-gray-900'>Exportar Excel</p>
                  <p className='text-sm text-gray-500'>
                    Planilha Excel com formatação avançada
                  </p>
                </div>
              </div>
              {isExporting === "excel" ? (
                <Loader2 className='h-5 w-5 animate-spin text-gray-600' />
              ) : (
                <Download className='h-5 w-5 text-gray-400' />
              )}
            </button>
          </div>

          {/* Status da exportação */}
          {exportStatus.type && (
            <div
              className={`rounded-lg p-4 ${
                exportStatus.type === "success"
                  ? "bg-green-50 border border-green-200"
                  : "bg-red-50 border border-red-200"
              }`}
            >
              <div className='flex items-center'>
                {exportStatus.type === "success" ? (
                  <CheckCircle className='h-5 w-5 text-green-500 mr-2' />
                ) : (
                  <AlertCircle className='h-5 w-5 text-red-500 mr-2' />
                )}
                <p
                  className={`text-sm ${
                    exportStatus.type === "success"
                      ? "text-green-700"
                      : "text-red-700"
                  }`}
                >
                  {exportStatus.message}
                </p>
              </div>
            </div>
          )}

          {/* Informações sobre os arquivos */}
          <div className='text-xs text-gray-500 bg-gray-50 rounded p-3'>
            📁 <strong>Local dos arquivos:</strong> Os arquivos exportados são
            salvos na pasta <code>src/export/</code> do projeto.
            <br />
            🕒 <strong>Nome do arquivo:</strong> Inclui data, hora e tipo de
            busca para fácil identificação.
          </div>
        </div>
      )}
    </div>
  );
};

export default ExportPanel;
