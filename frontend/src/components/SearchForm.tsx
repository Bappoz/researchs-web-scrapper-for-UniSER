/**
 * 📝 FORMULÁRIO DE BUSCA
 * Componente para entrada de dados de pesquisa
 */

import React, { useState } from "react";
import { Search, Loader2 } from "lucide-react";

interface SearchFormProps {
  onSearch: (
    query: string,
    platform: "comprehensive" | "scholar" | "lattes" | "orcid"
  ) => void;
  isLoading: boolean;
  disabled: boolean;
}

const SearchForm: React.FC<SearchFormProps> = ({
  onSearch,
  isLoading,
  disabled,
}) => {
  const [query, setQuery] = useState("");
  const [platform, setPlatform] = useState<
    "comprehensive" | "scholar" | "lattes" | "orcid"
  >("comprehensive");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading && !disabled) {
      onSearch(query.trim(), platform);
    }
  };

  return (
    <form onSubmit={handleSubmit} className='space-y-4'>
      {/* Campo de busca */}
      <div>
        <label
          htmlFor='query'
          className='block text-sm font-medium text-gray-700 mb-2'
        >
          Termo de Busca
        </label>
        <div className='relative'>
          <input
            type='text'
            id='query'
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder='Ex: João Silva, Machine Learning, Inteligência Artificial...'
            className='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors'
            disabled={disabled || isLoading}
          />
          <Search className='absolute right-3 top-3 h-5 w-5 text-gray-400' />
        </div>
      </div>

      {/* Seleção de plataforma */}
      <div>
        <label
          htmlFor='platform'
          className='block text-sm font-medium text-gray-700 mb-2'
        >
          Plataforma de Busca
        </label>
        <select
          id='platform'
          value={platform}
          onChange={(e) => setPlatform(e.target.value as any)}
          className='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors'
          disabled={disabled || isLoading}
        >
          <option value='comprehensive'>
            🎯 Busca Completa (Todas as plataformas)
          </option>
          <option value='scholar'>📚 Google Scholar</option>
          <option value='lattes'>🇧🇷 Plataforma Lattes</option>
          <option value='orcid'>🌐 ORCID</option>
        </select>
      </div>

      {/* Descrição da plataforma selecionada */}
      <div className='bg-blue-50 border border-blue-200 rounded-lg p-3'>
        <p className='text-sm text-blue-800'>
          {platform === "comprehensive" &&
            "🎯 Busca em todas as plataformas simultaneamente para resultados mais completos"}
          {platform === "scholar" &&
            "📚 Busca publicações científicas no Google Scholar"}
          {platform === "lattes" &&
            "🇧🇷 Busca currículos de pesquisadores brasileiros na Plataforma Lattes"}
          {platform === "orcid" &&
            "🌐 Busca perfis de pesquisadores internacionais no ORCID"}
        </p>
      </div>

      {/* Botão de busca */}
      <button
        type='submit'
        disabled={!query.trim() || isLoading || disabled}
        className='w-full flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors'
      >
        {isLoading ? (
          <>
            <Loader2 className='h-5 w-5 mr-2 animate-spin' />
            Pesquisando...
          </>
        ) : (
          <>
            <Search className='h-5 w-5 mr-2' />
            Iniciar Pesquisa
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
  );
};

export default SearchForm;
