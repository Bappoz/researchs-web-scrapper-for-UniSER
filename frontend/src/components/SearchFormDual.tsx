/**
 * 🔍 FORMULÁRIO DE BUSCA - NOME vs LINK
 * Componente com duas seções distintas de pesquisa
 */

import React, { useState } from "react";
import {
  Search,
  Loader2,
  ExternalLink,
  FileText,
  Globe,
  GraduationCap,
  BookOpen,
} from "lucide-react";

interface SearchFormDualProps {
  // Pesquisa por nome - abre site externo
  onSearchByNameLattes: (query: string) => void;
  onSearchByNameOrcid: (query: string) => void;
  onSearchByNameScholar: (query: string) => void;

  // Pesquisa por link - extrai dados completos
  onSearchByLinkLattes: (profileUrl: string) => void;
  onSearchByLinkOrcid: (profileUrl: string) => void;
  onSearchByLinkScholar: (
    profileUrl: string,
    useKeywordFilter: boolean
  ) => void;

  isLoading: boolean;
  disabled: boolean;
  loadingPlatform?: string;
}

const SearchFormDual: React.FC<SearchFormDualProps> = ({
  onSearchByNameLattes,
  onSearchByNameOrcid,
  onSearchByNameScholar,
  onSearchByLinkLattes,
  onSearchByLinkOrcid,
  onSearchByLinkScholar,
  isLoading,
  disabled,
  loadingPlatform,
}) => {
  const [nameQuery, setNameQuery] = useState("");
  const [linkQuery, setLinkQuery] = useState("");
  const [useKeywordFilter, setUseKeywordFilter] = useState(false);

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
        <div className='grid grid-cols-1 md:grid-cols-3 gap-3'>
          <button
            onClick={() => onSearchByNameLattes(nameQuery.trim())}
            disabled={isNameButtonDisabled("name-lattes")}
            className='flex items-center justify-center px-4 py-3 border-2 border-green-500 text-sm font-medium rounded-lg text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:bg-gray-400 disabled:border-gray-400 disabled:cursor-not-allowed transition-all'
          >
            {isButtonLoading("name-lattes") ? (
              <>
                <Loader2 className='h-4 w-4 mr-2 animate-spin' />
                Abrindo...
              </>
            ) : (
              <>
                <GraduationCap className='h-4 w-4 mr-2' />
                🇧🇷 Lattes
              </>
            )}
          </button>

          <button
            onClick={() => onSearchByNameOrcid(nameQuery.trim())}
            disabled={isNameButtonDisabled("name-orcid")}
            className='flex items-center justify-center px-4 py-3 border-2 border-blue-500 text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:border-gray-400 disabled:cursor-not-allowed transition-all'
          >
            {isButtonLoading("name-orcid") ? (
              <>
                <Loader2 className='h-4 w-4 mr-2 animate-spin' />
                Abrindo...
              </>
            ) : (
              <>
                <Globe className='h-4 w-4 mr-2' />
                🌐 ORCID
              </>
            )}
          </button>

          <button
            onClick={() => onSearchByNameScholar(nameQuery.trim())}
            disabled={isNameButtonDisabled("name-scholar")}
            className='flex items-center justify-center px-4 py-3 border-2 border-orange-500 text-sm font-medium rounded-lg text-white bg-orange-600 hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-orange-500 disabled:bg-gray-400 disabled:border-gray-400 disabled:cursor-not-allowed transition-all'
          >
            {isButtonLoading("name-scholar") ? (
              <>
                <Loader2 className='h-4 w-4 mr-2 animate-spin' />
                Abrindo...
              </>
            ) : (
              <>
                <BookOpen className='h-4 w-4 mr-2' />
                📚 Scholar
              </>
            )}
          </button>
        </div>
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
              placeholder='Ex: http://lattes.cnpq.br/1234567890123456, https://orcid.org/0000-0000-0000-0000...'
              className='w-full px-4 py-3 border border-green-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-colors text-base'
              disabled={disabled || isLoading}
            />
            <ExternalLink className='absolute right-3 top-3 h-5 w-5 text-green-400' />
          </div>
        </div>

        {/* Controle de filtro para Scholar */}
        <div className='mb-4 bg-orange-50 border border-orange-200 rounded-lg p-3'>
          <div className='flex items-center'>
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
          <p className='text-xs text-orange-600 mt-1 ml-6'>
            {useKeywordFilter
              ? "Filtra publicações por relevância científica específica"
              : "Mostra todas as publicações do perfil (recomendado)"}
          </p>
        </div>

        {/* Botões para pesquisa por link */}
        <div className='grid grid-cols-1 md:grid-cols-3 gap-3'>
          <button
            onClick={() => onSearchByLinkLattes(linkQuery.trim())}
            disabled={isLinkButtonDisabled("link-lattes")}
            className='flex items-center justify-center px-4 py-3 border-2 border-green-600 text-sm font-medium rounded-lg text-white bg-green-700 hover:bg-green-800 focus:outline-none focus:ring-2 focus:ring-green-600 disabled:bg-gray-400 disabled:border-gray-400 disabled:cursor-not-allowed transition-all'
          >
            {isButtonLoading("link-lattes") ? (
              <>
                <Loader2 className='h-4 w-4 mr-2 animate-spin' />
                Extraindo...
              </>
            ) : (
              <>
                <GraduationCap className='h-4 w-4 mr-2' />
                Extrair Lattes
              </>
            )}
          </button>

          <button
            onClick={() => onSearchByLinkOrcid(linkQuery.trim())}
            disabled={isLinkButtonDisabled("link-orcid")}
            className='flex items-center justify-center px-4 py-3 border-2 border-blue-600 text-sm font-medium rounded-lg text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-600 disabled:bg-gray-400 disabled:border-gray-400 disabled:cursor-not-allowed transition-all'
          >
            {isButtonLoading("link-orcid") ? (
              <>
                <Loader2 className='h-4 w-4 mr-2 animate-spin' />
                Extraindo...
              </>
            ) : (
              <>
                <Globe className='h-4 w-4 mr-2' />
                Extrair ORCID
              </>
            )}
          </button>

          <button
            onClick={() =>
              onSearchByLinkScholar(linkQuery.trim(), useKeywordFilter)
            }
            disabled={isLinkButtonDisabled("link-scholar")}
            className='flex items-center justify-center px-4 py-3 border-2 border-orange-600 text-sm font-medium rounded-lg text-white bg-orange-700 hover:bg-orange-800 focus:outline-none focus:ring-2 focus:ring-orange-600 disabled:bg-gray-400 disabled:border-gray-400 disabled:cursor-not-allowed transition-all'
          >
            {isButtonLoading("link-scholar") ? (
              <>
                <Loader2 className='h-4 w-4 mr-2 animate-spin' />
                Extraindo...
              </>
            ) : (
              <>
                <BookOpen className='h-4 w-4 mr-2' />
                Extrair Scholar*
              </>
            )}
          </button>
        </div>
      </div>

      {/* Instruções */}
      <div className='bg-gray-50 border border-gray-200 rounded-lg p-4'>
        <h4 className='font-semibold text-gray-800 mb-2'>💡 Como usar:</h4>
        <div className='grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-700'>
          <div>
            <p className='font-medium text-blue-700'>🔍 Pesquisa por Nome:</p>
            <p>• Digite o nome do pesquisador</p>
            <p>• Clique na plataforma desejada</p>
            <p>• Será aberto o site oficial com os resultados</p>
          </div>
          <div>
            <p className='font-medium text-green-700'>📄 Pesquisa por Link:</p>
            <p>• Cole o link do perfil encontrado</p>
            <p>• Clique para extrair dados completos</p>
            <p>• Veja publicações, artigos e projetos</p>
            <p className='text-orange-600 text-xs mt-1'>
              * Scholar pode ter limitações por anti-bot
            </p>
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
