/**
 * 🔍 FORMULÁRIO DE BUSCA COM BOTÕES SEPARADOS
 * Componente com botões distintos para cada plataforma
 */

import React, { useState } from "react";
import {
  Search,
  Loader2,
  BookOpen,
  Globe,
  GraduationCap,
  FileText,
} from "lucide-react";

interface SearchFormSeparatedProps {
  onSearchLattes: (query: string) => void;
  onSearchOrcid: (query: string) => void;
  onSearchScholar: (query: string) => void;
  onSearchComprehensive: (query: string) => void;
  isLoading: boolean;
  disabled: boolean;
  loadingPlatform?: string;
}

const SearchFormSeparated: React.FC<SearchFormSeparatedProps> = ({
  onSearchLattes,
  onSearchOrcid,
  onSearchScholar,
  onSearchComprehensive,
  isLoading,
  disabled,
  loadingPlatform,
}) => {
  const [query, setQuery] = useState("");

  const handleLattesSearch = () => {
    if (query.trim() && !isLoading && !disabled) {
      onSearchLattes(query.trim());
    }
  };

  const handleOrcidSearch = () => {
    if (query.trim() && !isLoading && !disabled) {
      onSearchOrcid(query.trim());
    }
  };

  const handleScholarSearch = () => {
    if (query.trim() && !isLoading && !disabled) {
      onSearchScholar(query.trim());
    }
  };

  const handleComprehensiveSearch = () => {
    if (query.trim() && !isLoading && !disabled) {
      onSearchComprehensive(query.trim());
    }
  };

  const isButtonLoading = (platform: string) => {
    return isLoading && loadingPlatform === platform;
  };

  const isButtonDisabled = (platform: string) => {
    return (
      !query.trim() || disabled || (isLoading && loadingPlatform !== platform)
    );
  };

  return (
    <div className='space-y-6'>
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
            className='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors text-base'
            disabled={disabled || isLoading}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                handleLattesSearch(); // Default para Lattes
              }
            }}
          />
          <Search className='absolute right-3 top-3 h-5 w-5 text-gray-400' />
        </div>
      </div>

      {/* Botões de Busca Separados */}
      <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
        {/* Botão Lattes - DESTAQUE */}
        <button
          onClick={handleLattesSearch}
          disabled={isButtonDisabled("lattes")}
          className='flex items-center justify-center px-6 py-4 border-2 border-green-500 text-base font-medium rounded-lg text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:bg-gray-400 disabled:border-gray-400 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105'
        >
          {isButtonLoading("lattes") ? (
            <>
              <Loader2 className='h-5 w-5 mr-2 animate-spin' />
              Buscando no Lattes...
            </>
          ) : (
            <>
              <GraduationCap className='h-5 w-5 mr-2' />
              🇧🇷 Buscar no Lattes
            </>
          )}
        </button>

        {/* Botão ORCID */}
        <button
          onClick={handleOrcidSearch}
          disabled={isButtonDisabled("orcid")}
          className='flex items-center justify-center px-6 py-4 border-2 border-blue-500 text-base font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:border-gray-400 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105'
        >
          {isButtonLoading("orcid") ? (
            <>
              <Loader2 className='h-5 w-5 mr-2 animate-spin' />
              Buscando no ORCID...
            </>
          ) : (
            <>
              <Globe className='h-5 w-5 mr-2' />
              🌐 Buscar no ORCID
            </>
          )}
        </button>

        {/* Botão Scholar */}
        <button
          onClick={handleScholarSearch}
          disabled={isButtonDisabled("scholar")}
          className='flex items-center justify-center px-6 py-4 border-2 border-orange-500 text-base font-medium rounded-lg text-white bg-orange-600 hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 disabled:bg-gray-400 disabled:border-gray-400 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105'
        >
          {isButtonLoading("scholar") ? (
            <>
              <Loader2 className='h-5 w-5 mr-2 animate-spin' />
              Buscando no Scholar...
            </>
          ) : (
            <>
              <BookOpen className='h-5 w-5 mr-2' />
              📚 Buscar no Scholar
            </>
          )}
        </button>

        {/* Botão Busca Completa */}
        <button
          onClick={handleComprehensiveSearch}
          disabled={isButtonDisabled("comprehensive")}
          className='flex items-center justify-center px-6 py-4 border-2 border-purple-500 text-base font-medium rounded-lg text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:bg-gray-400 disabled:border-gray-400 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105'
        >
          {isButtonLoading("comprehensive") ? (
            <>
              <Loader2 className='h-5 w-5 mr-2 animate-spin' />
              Busca Completa...
            </>
          ) : (
            <>
              <FileText className='h-5 w-5 mr-2' />
              🎯 Busca Completa
            </>
          )}
        </button>
      </div>

      {/* Descrições das Plataformas */}
      <div className='grid grid-cols-1 md:grid-cols-2 gap-4 text-sm'>
        <div className='bg-green-50 border border-green-200 rounded-lg p-3'>
          <h4 className='font-semibold text-green-800 mb-1'>
            🇧🇷 Plataforma Lattes
          </h4>
          <p className='text-green-700'>
            Redireciona para a busca oficial do CNPq. Copie o link do CV para
            extração completa.
          </p>
        </div>

        <div className='bg-blue-50 border border-blue-200 rounded-lg p-3'>
          <h4 className='font-semibold text-blue-800 mb-1'>🌐 ORCID</h4>
          <p className='text-blue-700'>
            Busca pesquisadores internacionais com identificador ORCID único.
          </p>
        </div>

        <div className='bg-orange-50 border border-orange-200 rounded-lg p-3'>
          <h4 className='font-semibold text-orange-800 mb-1'>
            📚 Google Scholar
          </h4>
          <p className='text-orange-700'>
            Busca publicações científicas e métricas de citação.
          </p>
        </div>

        <div className='bg-purple-50 border border-purple-200 rounded-lg p-3'>
          <h4 className='font-semibold text-purple-800 mb-1'>
            🎯 Busca Completa
          </h4>
          <p className='text-purple-700'>
            Combina resultados de todas as plataformas disponíveis.
          </p>
        </div>
      </div>

      {disabled && (
        <div className='bg-red-50 border border-red-200 rounded-lg p-3'>
          <p className='text-sm text-red-800'>
            ⚠️ API offline. Verifique a conexão com o servidor.
          </p>
        </div>
      )}
    </div>
  );
};

export default SearchFormSeparated;
