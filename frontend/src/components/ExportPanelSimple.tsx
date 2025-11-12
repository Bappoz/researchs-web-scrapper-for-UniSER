/**
 * 📤 PAINEL DE EXPORTAÇÃO EXCEL CONSOLIDADO
 * Componente para download do Excel consolidado com todas as pesquisas
 */

import React, { useState } from "react";
import {
  FileSpreadsheet,
  CheckCircle,
  Loader2,
  BarChart3,
  Trash2,
} from "lucide-react";

const ExportPanel: React.FC = () => {
  const [isExporting, setIsExporting] = useState(false);
  const [consolidatedStatus, setConsolidatedStatus] = useState<{
    type: "success" | "error" | null;
    message: string;
  }>({ type: null, message: "" });

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

  const handleClearDatabase = async () => {
    const confirmed = window.confirm(
      "⚠️ ATENÇÃO!\n\n" +
        "Isso irá deletar TODAS as pesquisas e publicações do banco de dados.\n\n" +
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

    setIsExporting(true);
    setConsolidatedStatus({ type: null, message: "" });

    try {
      const response = await fetch("http://localhost:8000/mongodb/clear", {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error(`Erro ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();

      setConsolidatedStatus({
        type: "success",
        message: `✅ ${data.message || "Banco de dados limpo com sucesso!"}`,
      });
    } catch (error) {
      setConsolidatedStatus({
        type: "error",
        message: `❌ Erro ao limpar banco de dados: ${error}`,
      });
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className='bg-white rounded-lg shadow-lg border border-gray-200 p-6'>
      <h3 className='text-lg font-bold text-gray-900 mb-4 flex items-center'>
        <FileSpreadsheet className='h-5 w-5 mr-2 text-purple-600' />
        Relatórios Consolidados
      </h3>

      <div className='space-y-4'>
        {/* Descrição */}
        <div className='bg-gradient-to-r from-purple-50 to-indigo-50 border border-purple-200 rounded-lg p-4'>
          <div className='flex items-start space-x-3'>
            <BarChart3 className='h-6 w-6 text-purple-600 flex-shrink-0 mt-1' />
            <div>
              <h4 className='text-sm font-bold text-gray-900 mb-1'>
                Excel com TODAS as pesquisas
              </h4>
              <p className='text-xs text-gray-600'>
                Baixe um relatório Excel profissional com todos os pesquisadores
                e publicações coletados do banco de dados MongoDB.
              </p>
            </div>
          </div>
        </div>

        {/* Botões de ação */}
        <div className='grid grid-cols-1 gap-3'>
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
                Baixar Excel Consolidado
              </>
            )}
          </button>

          <div className='grid grid-cols-2 gap-2'>
            <button
              onClick={handleViewStats}
              disabled={isExporting}
              className='flex items-center justify-center p-2 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-medium rounded-lg transition-all duration-200 disabled:bg-gray-400 disabled:cursor-not-allowed text-sm'
            >
              <BarChart3 className='h-4 w-4 mr-1' />
              Estatísticas
            </button>

            <button
              onClick={handleClearDatabase}
              disabled={isExporting}
              className='flex items-center justify-center p-2 bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 text-white font-medium rounded-lg transition-all duration-200 disabled:bg-gray-400 disabled:cursor-not-allowed text-sm'
            >
              <Trash2 className='h-4 w-4 mr-1' />
              Limpar Tudo
            </button>
          </div>
        </div>

        {/* Status feedback */}
        {consolidatedStatus.type && (
          <div
            className={`text-sm rounded-lg p-3 border-2 ${
              consolidatedStatus.type === "success"
                ? "bg-green-50 border-green-200 text-green-700"
                : "bg-red-50 border-red-200 text-red-700"
            }`}
          >
            <div className='flex items-center'>
              {consolidatedStatus.type === "success" ? (
                <CheckCircle className='h-5 w-5 mr-2 flex-shrink-0' />
              ) : (
                <BarChart3 className='h-5 w-5 mr-2 flex-shrink-0' />
              )}
              <span className='font-medium'>
                {consolidatedStatus.message}
              </span>
            </div>
          </div>
        )}

        {/* Informações sobre o Excel */}
        <div className='bg-gray-50 rounded-lg p-3 border'>
          <h4 className='text-sm font-semibold text-gray-700 mb-2'>
            📊 O Excel Consolidado inclui:
          </h4>
          <ul className='text-xs text-gray-600 space-y-1'>
            <li>✅ Todos os pesquisadores coletados</li>
            <li>✅ Todas as publicações encontradas</li>
            <li>✅ Resumos Lattes (via Escavador)</li>
            <li>✅ Métricas acadêmicas completas</li>
            <li>✅ Formatação profissional</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ExportPanel;
