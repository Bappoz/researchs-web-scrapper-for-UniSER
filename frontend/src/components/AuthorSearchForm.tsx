/**
 * 🔍 FORMULÁRIO DE BUSCA DE PESQUISADORES
 * Componente para buscar pesquisadores por nome
 */

import React, { useState } from "react";
import { Search, Loader2, Users } from "lucide-react";

interface AuthorSearchFormProps {
  onSearch: (authorName: string, maxResults: number) => void;
  isLoading: boolean;
  disabled: boolean;
}

const AuthorSearchForm: React.FC<AuthorSearchFormProps> = ({
  onSearch,
  isLoading,
  disabled,
}) => {
  const [authorName, setAuthorName] = useState("");
  const [maxResults, setMaxResults] = useState(20);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (authorName.trim() && !isLoading && !disabled) {
      onSearch(authorName.trim(), maxResults);
    }
  };

  return (
    <div className='bg-white rounded-lg shadow-lg p-6'>
      <div className='mb-6'>
        <div className='flex items-center mb-2'>
          <Users className='h-6 w-6 text-blue-600 mr-2' />
          <h2 className='text-xl font-bold text-gray-900'>
            Buscar Pesquisadores
          </h2>
        </div>
        <p className='text-gray-600'>
          Digite o nome de um pesquisador para encontrar múltiplos perfis no
          Google Scholar
        </p>
      </div>

      <form onSubmit={handleSubmit} className='space-y-4'>
        {/* Campo de busca */}
        <div>
          <label
            htmlFor='authorName'
            className='block text-sm font-medium text-gray-700 mb-2'
          >
            Nome do Pesquisador
          </label>
          <div className='relative'>
            <input
              type='text'
              id='authorName'
              value={authorName}
              onChange={(e) => setAuthorName(e.target.value)}
              placeholder='Ex: Silva, João Santos, Maria Oliveira...'
              className='w-full px-4 py-3 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors'
              disabled={disabled || isLoading}
            />
            <Search className='absolute left-3 top-3 h-5 w-5 text-gray-400' />
          </div>
          <p className='mt-1 text-xs text-gray-500'>
            💡 Use nomes comuns como "Silva", "Santos" para encontrar mais
            pesquisadores
          </p>
        </div>

        {/* Número máximo de resultados */}
        <div>
          <label
            htmlFor='maxResults'
            className='block text-sm font-medium text-gray-700 mb-2'
          >
            Número de Pesquisadores
          </label>
          <select
            id='maxResults'
            value={maxResults}
            onChange={(e) => setMaxResults(Number(e.target.value))}
            className='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors'
            disabled={disabled || isLoading}
          >
            <option value={5}>5 pesquisadores</option>
            <option value={10}>10 pesquisadores</option>
            <option value={20}>20 pesquisadores</option>
            <option value={30}>30 pesquisadores</option>
            <option value={40}>40 pesquisadores</option>
            <option value={50}>50 pesquisadores</option>
          </select>
        </div>

        {/* Informações sobre a busca */}
        <div className='bg-blue-50 border border-blue-200 rounded-lg p-4'>
          <h4 className='font-medium text-blue-900 mb-2'>📚 Como funciona:</h4>
          <ul className='text-sm text-blue-800 space-y-1'>
            <li>• Busca pesquisadores no Google Scholar por nome</li>
            <li>• Mostra informações como instituição e áreas de pesquisa</li>
            <li>
              • Permite selecionar um pesquisador para ver todas as publicações
            </li>
            <li>• Exporta dados para Excel com formatação profissional</li>
          </ul>
        </div>

        {/* Botão de busca */}
        <button
          type='submit'
          disabled={!authorName.trim() || isLoading || disabled}
          className='w-full flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors'
        >
          {isLoading ? (
            <>
              <Loader2 className='h-5 w-5 mr-2 animate-spin' />
              Buscando Pesquisadores...
            </>
          ) : (
            <>
              <Search className='h-5 w-5 mr-2' />
              Buscar Pesquisadores
            </>
          )}
        </button>

        {disabled && (
          <div className='bg-red-50 border border-red-200 rounded-lg p-3'>
            <p className='text-sm text-red-800'>
              ⚠️ API offline. Verifique a conexão com o servidor.
            </p>
          </div>
        )}
      </form>

      {/* Exemplos de uso */}
      <div className='mt-6 p-4 bg-gray-50 rounded-lg'>
        <h4 className='font-medium text-gray-900 mb-2'>
          🎯 Exemplos de busca:
        </h4>
        <div className='grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-600'>
          <button
            type='button'
            onClick={() => setAuthorName("Silva")}
            className='text-left hover:text-blue-600 transition-colors'
          >
            • "Silva" - Nome comum brasileiro
          </button>
          <button
            type='button'
            onClick={() => setAuthorName("Santos")}
            className='text-left hover:text-blue-600 transition-colors'
          >
            • "Santos" - Pesquisadores com sobrenome Santos
          </button>
          <button
            type='button'
            onClick={() => setAuthorName("Maria")}
            className='text-left hover:text-blue-600 transition-colors'
          >
            • "Maria" - Pesquisadoras chamadas Maria
          </button>
          <button
            type='button'
            onClick={() => setAuthorName("José")}
            className='text-left hover:text-blue-600 transition-colors'
          >
            • "José" - Pesquisadores chamados José
          </button>
        </div>
      </div>
    </div>
  );
};

export default AuthorSearchForm;
