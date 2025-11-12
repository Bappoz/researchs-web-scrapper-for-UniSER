/**
 * 🔍 FORMULÁRIO DE BUSCA - GOOGLE SCHOLAR
 * Componente simplificado focado no Google Scholar com resumo do Lattes
 */

import React, { useState } from "react";
import {
  Search,
  Loader2,
  ExternalLink,
  FileText,
  BookOpen,
} from "lucide-react";

interface SearchFormDualProps {
  // Pesquisa por nome - Google Scholar
  onSearchByNameScholar: (query: string) => void;

  // Pesquisa por link - extrai dados completos do Scholar
  onSearchByLinkScholar: (
    profileUrl: string,
    useKeywordFilter: boolean,
    maxPublications: number
  ) => void;

  isLoading: boolean;
  disabled: boolean;
  loadingPlatform?: string;
}

const SearchFormDual: React.FC<SearchFormDualProps> = ({
  onSearchByNameScholar,
  onSearchByLinkScholar,
  isLoading,
  disabled,
  loadingPlatform,
}) => {
  const [nameQuery, setNameQuery] = useState("");
  const [linkQuery, setLinkQuery] = useState("");
  const [useKeywordFilter, setUseKeywordFilter] = useState(false);
  const [maxPublications, setMaxPublications] = useState(20);

  const isButtonLoading = (platform: string) => {
    return isLoading && loadingPlatform === platform;
  };

  const isNameButtonDisabled = (platform: string) => {
    return (
      !nameQuery.trim() ||
      disabled ||
      (isLoading && loadingPlatform !== platform)
    );
  };

  const isLinkButtonDisabled = (platform: string) => {
    return (
      !linkQuery.trim() ||
      disabled ||
      (isLoading && loadingPlatform !== platform)
    );
  };

  return (
    <div className='space-y-8'>
      {/* SEÇÃO 1: PESQUISA POR NOME - Abre site externo */}
      <div className='bg-blue-50 border-2 border-blue-200 rounded-lg p-6'>
        <div className='flex items-center mb-4'>
          <ExternalLink className='h-6 w-6 text-blue-600 mr-2' />
          <h3 className='text-lg font-semibold text-blue-800'>
            🔍 Pesquisa por Nome - Abrir Site Externo
          </h3>
        </div>

        <p className='text-blue-700 mb-4 text-sm'>
          Digite o nome do pesquisador para abrir a página de resultados no site
          oficial
        </p>

        {/* Campo nome */}
        <div className='mb-4'>
          <label className='block text-sm font-medium text-blue-700 mb-2'>
            Nome do Pesquisador
          </label>
          <div className='relative'>
            <input
              type='text'
              value={nameQuery}
              onChange={(e) => setNameQuery(e.target.value)}
              placeholder='Ex: João Silva, Maria Santos...'
              className='w-full px-4 py-3 border border-blue-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors text-base'
              disabled={disabled || isLoading}
            />
            <Search className='absolute right-3 top-3 h-5 w-5 text-blue-400' />
          </div>
        </div>

        {/* Botões para pesquisa por nome */}
        <div className='flex justify-center'>
          <button
            onClick={() => onSearchByNameScholar(nameQuery.trim())}
            disabled={isNameButtonDisabled("name-scholar")}
            className='flex items-center justify-center px-6 py-3 border-2 border-blue-500 text-base font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:border-gray-400 disabled:cursor-not-allowed transition-all min-w-[250px]'
          >
            {isButtonLoading("name-scholar") ? (
              <>
                <Loader2 className='h-5 w-5 mr-2 animate-spin' />
                Buscando...
              </>
            ) : (
              <>
                <BookOpen className='h-5 w-5 mr-2' />
                📚 Buscar no Google Scholar
              </>
            )}
          </button>
        </div>
        
        <p className='text-xs text-blue-600 mt-3 text-center italic'>
          💡 O resumo do Lattes será buscado automaticamente via Escavador
        </p>
      </div>

      {/* SEÇÃO 2: PESQUISA POR LINK - Extrai dados completos */}
      <div className='bg-green-50 border-2 border-green-200 rounded-lg p-6'>
        <div className='flex items-center mb-4'>
          <FileText className='h-6 w-6 text-green-600 mr-2' />
          <h3 className='text-lg font-semibold text-green-800'>
            📄 Pesquisa por Link - Extrair Dados Completos
          </h3>
        </div>

        <p className='text-green-700 mb-4 text-sm'>
          Cole o link do perfil para extrair publicações, artigos e projetos
          completos
        </p>

        {/* Campo link */}
        <div className='mb-4'>
          <label className='block text-sm font-medium text-green-700 mb-2'>
            Link do Perfil
          </label>
          <div className='relative'>
            <input
              type='url'
              value={linkQuery}
              onChange={(e) => setLinkQuery(e.target.value)}
              placeholder='Ex: https://scholar.google.com/citations?user=abc123...'
              className='w-full px-4 py-3 border border-green-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-colors text-base'
              disabled={disabled || isLoading}
            />
            <ExternalLink className='absolute right-3 top-3 h-5 w-5 text-green-400' />
          </div>
        </div>

        {/* Controle de filtro para Scholar e quantidade de publicações */}
        <div className='mb-4 flex flex-col md:flex-row md:items-center gap-3'>
          <div className='flex items-center bg-orange-50 border border-orange-200 rounded-lg p-3'>
            <input
              type='checkbox'
              id='keyword-filter'
              checked={useKeywordFilter}
              onChange={(e) => setUseKeywordFilter(e.target.checked)}
              className='h-4 w-4 text-orange-600 focus:ring-orange-500 border-orange-300 rounded'
              disabled={disabled || isLoading}
            />
            <label
              htmlFor='keyword-filter'
              className='ml-2 text-sm text-orange-700'
            >
              🔍 Aplicar filtro por palavras-chave (Scholar)
            </label>
          </div>
          <div className='flex items-center bg-blue-50 border border-blue-200 rounded-lg p-3'>
            <label
              htmlFor='max-publications'
              className='text-sm text-blue-700 mr-2'
            >
              📄 Máx. publicações:
            </label>
            <input
              id='max-publications'
              type='number'
              min={1}
              max={200}
              value={maxPublications}
              onChange={(e) => setMaxPublications(Number(e.target.value))}
              className='w-20 px-2 py-1 border border-blue-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent text-base'
              disabled={disabled || isLoading}
            />
          </div>
        </div>

        {/* Botões para pesquisa por link */}
        <div className='flex justify-center'>
          <button
            onClick={() =>
              onSearchByLinkScholar(
                linkQuery.trim(),
                useKeywordFilter,
                maxPublications
              )
            }
            disabled={isLinkButtonDisabled("link-scholar")}
            className='flex items-center justify-center px-6 py-3 border-2 border-green-600 text-base font-medium rounded-lg text-white bg-green-700 hover:bg-green-800 focus:outline-none focus:ring-2 focus:ring-green-600 disabled:bg-gray-400 disabled:border-gray-400 disabled:cursor-not-allowed transition-all min-w-[250px]'
          >
            {isButtonLoading("link-scholar") ? (
              <>
                <Loader2 className='h-5 w-5 mr-2 animate-spin' />
                Extraindo...
              </>
            ) : (
              <>
                <BookOpen className='h-5 w-5 mr-2' />
                📚 Extrair do Google Scholar
              </>
            )}
          </button>
        </div>
        
        <p className='text-xs text-green-600 mt-3 text-center italic'>
          💡 O resumo do Lattes será incluído automaticamente
        </p>
      </div>

      {/* Instruções */}
      <div className='bg-gray-50 border border-gray-200 rounded-lg p-4'>
        <h4 className='font-semibold text-gray-800 mb-2'>💡 Como usar:</h4>
        <div className='grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-700'>
          <div>
            <p className='font-medium text-blue-700'>🔍 Pesquisa por Nome:</p>
            <p>• Digite o nome do pesquisador</p>
            <p>• Busca publicações no Google Scholar</p>
            <p>• Inclui resumo do Lattes automaticamente</p>
          </div>
          <div>
            <p className='font-medium text-green-700'>📄 Pesquisa por Link:</p>
            <p>• Cole o link do perfil do Google Scholar</p>
            <p>• Extrai dados completos de publicações</p>
            <p>• Inclui resumo do Lattes automaticamente</p>
          </div>
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

export default SearchFormDual;
