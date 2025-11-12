/**
 * 📚 LATTES SUMMARY CARD
 * Componente para exibir resumo do Lattes via Escavador
 */

import React from 'react';

interface LattesSummaryData {
  name?: string;
  summary?: string;
  institution?: string;
  area?: string;
  lattes_url?: string;
  success?: boolean;
}

interface LattesSummaryCardProps {
  data: LattesSummaryData | null;
  loading?: boolean;
}

const LattesSummaryCard: React.FC<LattesSummaryCardProps> = ({ data, loading = false }) => {
  // Se está carregando
  if (loading) {
    return (
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 shadow-sm">
        <div className="flex items-center space-x-3">
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
          <span className="text-blue-700 font-medium">
            🔍 Buscando resumo do Lattes via Escavador...
          </span>
        </div>
      </div>
    );
  }

  // Se não tem dados ou falhou
  if (!data || !data.success) {
    return null; // Não exibe nada se não encontrou
  }

  return (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6 shadow-md">
      {/* Cabeçalho */}
      <div className="flex items-center space-x-2 mb-4">
        <span className="text-2xl">📚</span>
        <h3 className="text-lg font-bold text-blue-900">
          Resumo do Currículo Lattes
        </h3>
        <span className="text-xs bg-blue-600 text-white px-2 py-1 rounded-full">
          via Escavador
        </span>
      </div>

      {/* Conteúdo */}
      <div className="space-y-3">
        {/* Nome */}
        {data.name && (
          <div>
            <span className="text-sm font-semibold text-gray-700">Nome:</span>
            <p className="text-base text-gray-900">{data.name}</p>
          </div>
        )}

        {/* Instituição */}
        {data.institution && data.institution !== "Instituição não informada" && (
          <div>
            <span className="text-sm font-semibold text-gray-700">Instituição:</span>
            <p className="text-base text-gray-900">{data.institution}</p>
          </div>
        )}

        {/* Área de Atuação */}
        {data.area && data.area !== "Área não informada" && (
          <div>
            <span className="text-sm font-semibold text-gray-700">Área de Atuação:</span>
            <p className="text-base text-gray-900">{data.area}</p>
          </div>
        )}

        {/* Resumo */}
        {data.summary && data.summary !== "Resumo não disponível" && (
          <div>
            <span className="text-sm font-semibold text-gray-700">Resumo:</span>
            <p className="text-sm text-gray-800 leading-relaxed mt-1 bg-white p-3 rounded border border-blue-100">
              {data.summary}
            </p>
          </div>
        )}

        {/* Link do Lattes */}
        {data.lattes_url && (
          <div className="pt-2">
            <a
              href={data.lattes_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-2 text-blue-600 hover:text-blue-800 font-medium hover:underline"
            >
              <span>🔗</span>
              <span>Acessar Currículo Lattes Completo</span>
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                />
              </svg>
            </a>
          </div>
        )}
      </div>

      {/* Rodapé com informação da fonte */}
      <div className="mt-4 pt-3 border-t border-blue-200">
        <p className="text-xs text-gray-600 italic">
          ℹ️ Informações obtidas através do Escavador, que agrega dados da Plataforma Lattes
        </p>
      </div>
    </div>
  );
};

export default LattesSummaryCard;
