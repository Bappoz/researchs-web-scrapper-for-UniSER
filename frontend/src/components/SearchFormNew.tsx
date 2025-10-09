/**
 * 📝 FORMULÁRIO DE BUSCA REORGANIZADO
 * Componente para busca por autor e tema em diferentes plataformas
 */

import React, { useState } from "react";
import {
  Search,
  Loader2,
  User,
  BookOpen,
  Link,
  Globe,
  Users,
} from "lucide-react";

interface SearchFormProps {
  onSearch: (searchData: {
    query: string;
    searchType:
      | "author"
      | "topic"
      | "profile"
      | "comprehensive"
      | "multiple_authors";
    platform: "scholar" | "lattes" | "orcid" | "all";
    profileUrl?: string;
    maxResults: number;
    saveFile: boolean;
  }) => void;
  isLoading: boolean;
}

const SearchForm: React.FC<SearchFormProps> = ({ onSearch, isLoading }) => {
  const [query, setQuery] = useState("");
  const [profileUrl, setProfileUrl] = useState("");
  const [searchType, setSearchType] = useState<
    "author" | "topic" | "profile" | "comprehensive" | "multiple_authors"
  >("author");
  const [platform, setPlatform] = useState<
    "scholar" | "lattes" | "orcid" | "all"
  >("all");
  const [maxResults, setMaxResults] = useState(10);
  const [saveFile, setSaveFile] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if ((query.trim() || profileUrl.trim()) && !isLoading) {
      const searchData = {
        query: query.trim(),
        searchType,
        platform,
        profileUrl: profileUrl.trim(),
        maxResults,
        saveFile,
      };

      console.log("🔍 Enviando busca:", searchData);
      onSearch(searchData);
    }
  };

  const searchTypeOptions = [
    {
      value: "author",
      label: "Buscar Autor",
      icon: User,
      description: "Buscar por nome do pesquisador",
    },
    {
      value: "multiple_authors",
      label: "Múltiplos Pesquisadores",
      icon: Users,
      description: "Encontrar vários pesquisadores por nome",
    },
    {
      value: "profile",
      label: "Link do Perfil",
      icon: Link,
      description: "Buscar por link direto do perfil",
    },
    {
      value: "comprehensive",
      label: "Busca Completa",
      icon: Globe,
      description: "Buscar em todas as plataformas",
    },
  ];

  const platformOptions = [
    { value: "all", label: "Todas as Plataformas", emoji: "🌍" },
    { value: "scholar", label: "Google Scholar", emoji: "📚" },
    { value: "lattes", label: "Plataforma Lattes", emoji: "🇧🇷" },
    { value: "orcid", label: "ORCID", emoji: "🌐" },
  ];

  return (
    <div className='bg-white rounded-lg shadow-lg p-6 mb-6'>
      <form onSubmit={handleSubmit} className='space-y-6'>
        {/* Tipo de Busca */}
        <div>
          <label className='block text-sm font-medium text-gray-700 mb-3'>
            Tipo de Busca
          </label>
          <div className='grid grid-cols-1 md:grid-cols-5 gap-3'>
            {searchTypeOptions.map((option) => {
              const IconComponent = option.icon;
              return (
                <button
                  key={option.value}
                  type='button'
                  onClick={() => setSearchType(option.value as any)}
                  className={`p-4 rounded-lg border-2 transition-all text-left ${
                    searchType === option.value
                      ? "border-blue-500 bg-blue-50"
                      : "border-gray-200 hover:border-gray-300"
                  }`}
                >
                  <div className='flex items-center space-x-2 mb-2'>
                    <IconComponent
                      size={16}
                      className={
                        searchType === option.value
                          ? "text-blue-600"
                          : "text-gray-600"
                      }
                    />
                    <span
                      className={`font-medium text-sm ${
                        searchType === option.value
                          ? "text-blue-900"
                          : "text-gray-900"
                      }`}
                    >
                      {option.label}
                    </span>
                  </div>
                  <p className='text-xs text-gray-600'>{option.description}</p>
                </button>
              );
            })}
          </div>
        </div>

        {/* Campo de entrada baseado no tipo */}
        <div>
          {searchType === "profile" ? (
            <div>
              <label
                htmlFor='profileUrl'
                className='block text-sm font-medium text-gray-700 mb-2'
              >
                Link do Perfil
              </label>
              <input
                type='url'
                id='profileUrl'
                value={profileUrl}
                onChange={(e) => setProfileUrl(e.target.value)}
                placeholder='https://scholar.google.com/citations?user=... ou https://lattes.cnpq.br/... ou https://orcid.org/...'
                className='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
                disabled={isLoading}
              />
            </div>
          ) : (
            <div>
              <label
                htmlFor='query'
                className='block text-sm font-medium text-gray-700 mb-2'
              >
                {searchType === "author"
                  ? "Nome do Pesquisador"
                  : searchType === "multiple_authors"
                  ? "Nome para Buscar Múltiplos Pesquisadores"
                  : searchType === "topic"
                  ? "Tema de Pesquisa"
                  : "Termo de Busca"}
              </label>
              <div className='relative'>
                <input
                  type='text'
                  id='query'
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder={
                    searchType === "author"
                      ? "Ex: João Silva"
                      : searchType === "multiple_authors"
                      ? "Ex: Silva, Santos, Maria - encontrará vários pesquisadores"
                      : searchType === "topic"
                      ? "Ex: machine learning"
                      : "Ex: inteligência artificial"
                  }
                  className='w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
                  disabled={isLoading}
                />
                <Search
                  className='absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400'
                  size={20}
                />
              </div>
            </div>
          )}
        </div>

        {/* Plataforma */}
        {searchType !== "comprehensive" && (
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-3'>
              Plataforma
            </label>
            <div className='grid grid-cols-2 md:grid-cols-4 gap-3'>
              {platformOptions.map((option) => (
                <button
                  key={option.value}
                  type='button'
                  onClick={() => setPlatform(option.value as any)}
                  className={`p-3 rounded-lg border-2 transition-all text-center ${
                    platform === option.value
                      ? "border-blue-500 bg-blue-50"
                      : "border-gray-200 hover:border-gray-300"
                  }`}
                >
                  <div className='text-lg mb-1'>{option.emoji}</div>
                  <div
                    className={`text-sm font-medium ${
                      platform === option.value
                        ? "text-blue-900"
                        : "text-gray-900"
                    }`}
                  >
                    {option.label}
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Opções avançadas */}
        <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
          <div>
            <label
              htmlFor='maxResults'
              className='block text-sm font-medium text-gray-700 mb-2'
            >
              Máximo de Resultados
            </label>
            <select
              id='maxResults'
              value={maxResults}
              onChange={(e) => setMaxResults(Number(e.target.value))}
              className='w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
              disabled={isLoading}
            >
              <option value={5}>5 resultados</option>
              <option value={10}>10 resultados</option>
              <option value={20}>20 resultados</option>
              <option value={50}>50 resultados</option>
            </select>
          </div>

          <div className='flex items-center'>
            <input
              type='checkbox'
              id='saveFile'
              checked={saveFile}
              onChange={(e) => setSaveFile(e.target.checked)}
              className='h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
              disabled={isLoading}
            />
            <label htmlFor='saveFile' className='ml-2 text-sm text-gray-700'>
              Salvar resultados em arquivo
            </label>
          </div>
        </div>

        {/* Botão de busca */}
        <button
          type='submit'
          disabled={isLoading || (!query.trim() && !profileUrl.trim())}
          className='w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2'
        >
          {isLoading ? (
            <>
              <Loader2 className='animate-spin' size={20} />
              <span>Pesquisando...</span>
            </>
          ) : (
            <>
              <Search size={20} />
              <span>Pesquisar</span>
            </>
          )}
        </button>
      </form>

      {/* Dicas de uso */}
      <div className='mt-6 p-4 bg-gray-50 rounded-lg'>
        <h4 className='text-sm font-medium text-gray-700 mb-2'>
          💡 Dicas de Uso:
        </h4>
        <ul className='text-sm text-gray-600 space-y-1'>
          <li>
            • <strong>Busca por Autor:</strong> Use o nome completo ou parcial
            do pesquisador
          </li>
          <li>
            • <strong>Busca por Tema:</strong> Use palavras-chave relacionadas à
            área de pesquisa
          </li>
          <li>
            • <strong>Link do Perfil:</strong> Cole o link direto do perfil do
            Google Scholar, Lattes ou ORCID
          </li>
          <li>
            • <strong>Busca Completa:</strong> Pesquisa em todas as plataformas
            simultaneamente
          </li>
        </ul>
      </div>
    </div>
  );
};

export default SearchForm;
