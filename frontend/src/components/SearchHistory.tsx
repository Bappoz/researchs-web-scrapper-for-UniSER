/**
 * 🕒 HISTÓRICO DE BUSCAS
 * Componente para exibir pesquisas anteriores e facilitar reutilização
 */

import React from "react";
import { Clock, Repeat, Trash2, TrendingUp } from "lucide-react";

interface SearchHistoryItem {
  id: string;
  query: string;
  platform: "comprehensive" | "scholar" | "lattes" | "orcid";
  timestamp: string;
  resultCount: number;
  duration: number; // em segundos
}

interface SearchHistoryProps {
  history: SearchHistoryItem[];
  onRepeatSearch: (
    query: string,
    platform: "comprehensive" | "scholar" | "lattes" | "orcid"
  ) => void;
  onClearHistory: () => void;
  onClearItem: (id: string) => void;
}

const SearchHistory: React.FC<SearchHistoryProps> = ({
  history,
  onRepeatSearch,
  onClearHistory,
  onClearItem,
}) => {
  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInMinutes = Math.floor(
      (now.getTime() - date.getTime()) / (1000 * 60)
    );

    if (diffInMinutes < 1) return "Agora mesmo";
    if (diffInMinutes < 60) return `${diffInMinutes}min atrás`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h atrás`;
    return date.toLocaleDateString("pt-BR");
  };

  const getPlatformEmoji = (platform: string) => {
    switch (platform) {
      case "comprehensive":
        return "🎯";
      case "scholar":
        return "📚";
      case "lattes":
        return "🇧🇷";
      case "orcid":
        return "🌐";
      default:
        return "🔍";
    }
  };

  const getPlatformName = (platform: string) => {
    switch (platform) {
      case "comprehensive":
        return "Busca Completa";
      case "scholar":
        return "Google Scholar";
      case "lattes":
        return "Plataforma Lattes";
      case "orcid":
        return "ORCID";
      default:
        return "Desconhecido";
    }
  };

  if (history.length === 0) {
    return (
      <div className='bg-white rounded-lg shadow border p-6'>
        <h3 className='text-lg font-semibold text-gray-900 mb-4 flex items-center'>
          <Clock className='h-5 w-5 mr-2 text-gray-600' />
          Histórico de Buscas
        </h3>
        <div className='text-center py-8'>
          <Clock className='h-12 w-12 text-gray-300 mx-auto mb-4' />
          <p className='text-gray-500'>Nenhuma busca realizada ainda</p>
          <p className='text-sm text-gray-400 mt-1'>
            Suas pesquisas aparecerão aqui
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className='bg-white rounded-lg shadow border p-6'>
      <div className='flex items-center justify-between mb-4'>
        <h3 className='text-lg font-semibold text-gray-900 flex items-center'>
          <Clock className='h-5 w-5 mr-2 text-gray-600' />
          Histórico de Buscas ({history.length})
        </h3>
        {history.length > 0 && (
          <button
            onClick={onClearHistory}
            className='text-sm text-red-600 hover:text-red-800 flex items-center'
          >
            <Trash2 className='h-4 w-4 mr-1' />
            Limpar Tudo
          </button>
        )}
      </div>

      <div className='space-y-3 max-h-96 overflow-y-auto'>
        {history.map((item) => (
          <div
            key={item.id}
            className='border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors'
          >
            <div className='flex items-start justify-between'>
              <div className='flex-1 min-w-0'>
                <div className='flex items-center gap-2 mb-2'>
                  <span className='text-lg'>
                    {getPlatformEmoji(item.platform)}
                  </span>
                  <span className='text-sm font-medium text-gray-700'>
                    {getPlatformName(item.platform)}
                  </span>
                  <span className='text-xs text-gray-500'>
                    {formatTimestamp(item.timestamp)}
                  </span>
                </div>

                <p className='font-medium text-gray-900 mb-1 truncate'>
                  "{item.query}"
                </p>

                <div className='flex items-center gap-4 text-sm text-gray-500'>
                  <span className='flex items-center'>
                    <TrendingUp className='h-4 w-4 mr-1' />
                    {item.resultCount} resultados
                  </span>
                  <span className='flex items-center'>
                    <Clock className='h-4 w-4 mr-1' />
                    {item.duration.toFixed(1)}s
                  </span>
                </div>
              </div>

              <div className='flex items-center gap-2 ml-4'>
                <button
                  onClick={() => onRepeatSearch(item.query, item.platform)}
                  className='p-2 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-lg transition-colors'
                  title='Repetir busca'
                >
                  <Repeat className='h-4 w-4' />
                </button>
                <button
                  onClick={() => onClearItem(item.id)}
                  className='p-2 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-lg transition-colors'
                  title='Remover item'
                >
                  <Trash2 className='h-4 w-4' />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Estatísticas resumidas */}
      <div className='mt-4 pt-4 border-t border-gray-200'>
        <div className='grid grid-cols-3 gap-4 text-center'>
          <div>
            <p className='text-lg font-semibold text-gray-900'>
              {history.reduce((sum, item) => sum + item.resultCount, 0)}
            </p>
            <p className='text-xs text-gray-500'>Total Resultados</p>
          </div>
          <div>
            <p className='text-lg font-semibold text-gray-900'>
              {(
                history.reduce((sum, item) => sum + item.duration, 0) /
                history.length
              ).toFixed(1)}
              s
            </p>
            <p className='text-xs text-gray-500'>Tempo Médio</p>
          </div>
          <div>
            <p className='text-lg font-semibold text-gray-900'>
              {new Set(history.map((item) => item.platform)).size}
            </p>
            <p className='text-xs text-gray-500'>Plataformas</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchHistory;
