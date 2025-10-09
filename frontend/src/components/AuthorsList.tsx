/**
 * 👨‍🎓 COMPONENTE DE SELEÇÃO DE AUTORES
 * Lista de pesquisadores encontrados para seleção
 */

import React from "react";
import {
  User,
  Building,
  BookOpen,
  TrendingUp,
  ExternalLink,
} from "lucide-react";

interface Author {
  author_id: string;
  name: string;
  institution: string;
  email_domain: string;
  total_citations: number;
  research_areas: string[];
  description: string;
  profile_url: string;
  h_index: number;
  i10_index: number;
  recent_publications: Array<{
    title: string;
    year: string;
    cited_by: number;
  }>;
}

interface AuthorsListProps {
  authors: Author[];
  isLoading: boolean;
  onSelectAuthor: (author: Author) => void;
  selectedAuthor?: Author;
}

const AuthorsList: React.FC<AuthorsListProps> = ({
  authors,
  isLoading,
  onSelectAuthor,
  selectedAuthor,
}) => {
  if (isLoading) {
    return (
      <div className='space-y-4'>
        <h3 className='text-lg font-semibold text-gray-800 mb-4'>
          🔍 Buscando pesquisadores...
        </h3>
        <div className='space-y-3'>
          {[...Array(3)].map((_, i) => (
            <div
              key={i}
              className='animate-pulse bg-gray-100 rounded-lg p-4 h-32'
            />
          ))}
        </div>
      </div>
    );
  }

  if (!authors || authors.length === 0) {
    return (
      <div className='text-center py-8'>
        <User className='h-12 w-12 text-gray-400 mx-auto mb-4' />
        <p className='text-gray-600'>Nenhum pesquisador encontrado</p>
      </div>
    );
  }

  return (
    <div className='space-y-4'>
      <h3 className='text-lg font-semibold text-gray-800 mb-4'>
        👨‍🎓 Pesquisadores Encontrados ({authors.length})
      </h3>
      <p className='text-sm text-gray-600 mb-4'>
        Selecione um pesquisador para ver suas publicações e exportar em Excel:
      </p>

      <div className='space-y-3'>
        {authors.map((author) => (
          <div
            key={author.author_id}
            className={`border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md ${
              selectedAuthor?.author_id === author.author_id
                ? "border-blue-500 bg-blue-50 shadow-md"
                : "border-gray-200 bg-white hover:border-gray-300"
            }`}
            onClick={() => onSelectAuthor(author)}
          >
            <div className='flex items-start justify-between'>
              <div className='flex-1'>
                {/* Nome e Instituição */}
                <div className='flex items-center mb-2'>
                  <User className='h-5 w-5 text-blue-600 mr-2' />
                  <h4 className='font-semibold text-gray-900'>{author.name}</h4>
                  {selectedAuthor?.author_id === author.author_id && (
                    <span className='ml-2 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full'>
                      Selecionado
                    </span>
                  )}
                </div>

                <div className='flex items-center text-gray-600 mb-2'>
                  <Building className='h-4 w-4 mr-2' />
                  <span className='text-sm'>{author.institution}</span>
                </div>

                {/* Descrição */}
                <p className='text-sm text-gray-700 mb-3'>
                  {author.description}
                </p>

                {/* Áreas de Pesquisa */}
                {author.research_areas && author.research_areas.length > 0 && (
                  <div className='mb-3'>
                    <div className='flex flex-wrap gap-1'>
                      {author.research_areas.slice(0, 3).map((area, index) => (
                        <span
                          key={index}
                          className='px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full'
                        >
                          {area}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Métricas */}
                <div className='flex items-center space-x-4 text-sm text-gray-600'>
                  <div className='flex items-center'>
                    <TrendingUp className='h-4 w-4 mr-1' />
                    <span>
                      {author.total_citations.toLocaleString()} citações
                    </span>
                  </div>
                  {author.h_index > 0 && (
                    <div className='flex items-center'>
                      <span className='font-medium'>
                        H-Index: {author.h_index}
                      </span>
                    </div>
                  )}
                  {author.i10_index > 0 && (
                    <div className='flex items-center'>
                      <span className='font-medium'>
                        i10: {author.i10_index}
                      </span>
                    </div>
                  )}
                </div>

                {/* Publicações Recentes (preview) */}
                {author.recent_publications &&
                  author.recent_publications.length > 0 && (
                    <div className='mt-3 pt-3 border-t border-gray-100'>
                      <div className='flex items-center mb-2'>
                        <BookOpen className='h-4 w-4 text-gray-500 mr-2' />
                        <span className='text-sm font-medium text-gray-700'>
                          Publicações Recentes:
                        </span>
                      </div>
                      <div className='space-y-1'>
                        {author.recent_publications
                          .slice(0, 2)
                          .map((pub, index) => (
                            <div key={index} className='text-xs text-gray-600'>
                              <span className='font-medium'>{pub.title}</span>
                              {pub.year && (
                                <span className='text-gray-500'>
                                  {" "}
                                  ({pub.year})
                                </span>
                              )}
                              {pub.cited_by > 0 && (
                                <span className='text-gray-500'>
                                  {" "}
                                  • {pub.cited_by} citações
                                </span>
                              )}
                            </div>
                          ))}
                      </div>
                    </div>
                  )}
              </div>

              {/* Link para perfil */}
              <div className='ml-4'>
                <a
                  href={author.profile_url}
                  target='_blank'
                  rel='noopener noreferrer'
                  className='inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'
                  onClick={(e) => e.stopPropagation()}
                >
                  <ExternalLink className='h-4 w-4 mr-1' />
                  Perfil
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className='mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg'>
        <p className='text-sm text-yellow-800'>
          💡 <strong>Dica:</strong> Clique em um pesquisador para ver todas as
          suas publicações e poder exportar em Excel.
        </p>
      </div>
    </div>
  );
};

export default AuthorsList;
