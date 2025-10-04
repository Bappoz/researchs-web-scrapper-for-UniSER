/**
 * 🕒 HISTÓRICO DE BUSCAS SIMPLIFICADO
 * Componente para exibir pesquisas anteriores
 */

import React from "react";
import { Clock, Repeat, Search } from "lucide-react";

interface SearchHistoryItem {
  id: string;
  query: string;
  searchType: string;
  platform: string;
  timestamp: string;
  totalResults: number;
  executionTime: number;
}

interface SearchHistoryProps {
  history: SearchHistoryItem[];
  onRepeatSearch: (historyItem: SearchHistoryItem) => void;
}

const SearchHistory: React.FC<SearchHistoryProps> = ({
  history,
  onRepeatSearch,
}) => {
  if (history.length === 0) {
    return (
      <div className='bg-white rounded-lg shadow p-4'>
        <h3 className='text-lg font-medium text-gray-900 mb-3'>
          📜 Histórico de Buscas
        </h3>
        <div className='text-center py-8'>
          <Search size={48} className='mx-auto text-gray-300 mb-3' />
          <p className='text-gray-500'>Nenhuma busca realizada ainda</p>
        </div>
      </div>
    );
  }

  return (
    <div className='bg-white rounded-lg shadow p-4'>
      <h3 className='text-lg font-medium text-gray-900 mb-3'>
        📜 Histórico de Buscas
      </h3>
      <div className='space-y-3 max-h-96 overflow-y-auto'>
        {history.map((item) => (
          <div
            key={item.id}
            className='border border-gray-200 rounded-lg p-3 hover:bg-gray-50 transition-colors'
          >
            <div className='flex items-start justify-between'>
              <div className='flex-1 min-w-0'>
                <p className='text-sm font-medium text-gray-900 truncate'>
                  {item.query}
                </p>
                <div className='flex items-center space-x-3 mt-1'>
                  <span className='inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800'>
                    {item.platform}
                  </span>
                  <span className='inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800'>
                    {item.searchType}
                  </span>
                </div>
                <div className='flex items-center space-x-4 mt-2 text-xs text-gray-500'>
                  <div className='flex items-center'>
                    <Clock size={12} className='mr-1' />
                    {new Date(item.timestamp).toLocaleString()}
                  </div>
                  <span>{item.totalResults} resultados</span>
                  <span>{item.executionTime.toFixed(1)}s</span>
                </div>
              </div>
              <button
                onClick={() => onRepeatSearch(item)}
                className='ml-2 p-1 text-gray-400 hover:text-blue-600 transition-colors'
                title='Repetir busca'
              >
                <Repeat size={16} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SearchHistory;
