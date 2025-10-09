/**
 * 🔍 EXIBIÇÃO DE RESULTADOS
 * Componente para apresentar dados de pesquisa de forma organizada e interativa
 */

import React, { useState } from "react";
import {
  ExternalLink,
  Calendar,
  User,
  FileText,
  MapPin,
  Trophy,
  Zap,
  ChevronDown,
  ChevronUp,
  Eye,
  Award,
  Building,
  Book,
  Users,
  TrendingUp,
} from "lucide-react";

interface Publication {
  title: string;
  authors?: string;
  year?: number;
  journal?: string;
  citations?: number;
  cited_by?: number;
  doi?: string;
  url?: string;
  link?: string;
  snippet?: string;
  platform?: string;
  publication?: string;
  page_number?: number;
}

interface AuthorInfo {
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
  max_publications?: number; // Número máximo de publicações para extrair
  recent_publications: Array<{
    title: string;
    year: string;
    cited_by: number;
  }>;
}

interface Profile {
  name: string;
  institution?: string;
  current_institution?: string;
  position?: string;
  current_position?: string;
  area?: string;
  research_areas?: string[];
  summary?: string;
  biography?: string;
  education?: string[];
  lattes_id?: string;
  orcid_id?: string;
  url?: string;
  lattes_url?: string;
  publications?: Publication[];
  total_publications?: number;
  h_index?: number;
  total_citations?: number;
  last_update?: string;
  given_names?: string;
  family_name?: string;
  keywords?: string[];
  platform?: string;
}

interface ResultsByPlatform {
  scholar?: {
    publications?: Publication[];
    profiles?: Profile[];
    error?: string;
    total_results?: number;
  };
  lattes?: {
    lattes_profiles?: Profile[];
    profiles?: Profile[];
    publications?: Publication[];
    data?: {
      lattes_profiles?: Profile[];
    };
    error?: string;
    total_results?: number;
  };
  orcid?: {
    orcid_profiles?: Profile[];
    profiles?: Profile[];
    publications?: Publication[];
    data?: {
      orcid_profiles?: Profile[];
    };
    error?: string;
    total_results?: number;
  };
}

interface ResearcherInfo {
  name: string;
  institution?: string;
  research_areas?: string[];
  h_index?: string | number;
  total_citations?: string | number;
  orcid_id?: string;
  last_update?: string;
  affiliation?: string;
}

interface ResultsDisplayProps {
  results: {
    results_by_platform?: ResultsByPlatform;
    publications?: Publication[];
    profiles?: Profile[];
    authors?: AuthorInfo[]; // Nova propriedade para múltiplos autores
    data?: any;
    researcher_info?: ResearcherInfo;
    total_results?: number;
    search_type?: string;
    query?: string;
    success?: boolean;
    message?: string;
    platform?: string;
  } | null;
  isLoading?: boolean;
  onSelectAuthor?: (author: AuthorInfo) => void; // Nova prop para seleção de autor
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({
  results,
  isLoading,
  onSelectAuthor,
}) => {
  const [expandedCards, setExpandedCards] = useState<Set<string>>(new Set());
  const [activeTab, setActiveTab] = useState<
    "all" | "scholar" | "lattes" | "orcid"
  >("all");

  // Debug log para verificar se o componente está sendo usado
  console.log("🔍 ResultsDisplay - results:", results);
  console.log("🔍 ResultsDisplay - isLoading:", isLoading);
  console.log(
    "🔍 ResultsDisplay - results_by_platform:",
    results?.results_by_platform
  );
  console.log("🔍 ResultsDisplay - results.data:", results?.data);
  console.log(
    "🔍 ResultsDisplay - results.publications:",
    results?.publications
  );

  if (isLoading) {
    return (
      <div className='bg-white rounded-lg shadow-md p-6'>
        <div className='animate-pulse'>
          <div className='h-6 bg-gray-200 rounded w-1/3 mb-4'></div>
          <div className='space-y-4'>
            {[1, 2, 3].map((i) => (
              <div key={i} className='border border-gray-200 rounded-lg p-4'>
                <div className='h-4 bg-gray-200 rounded w-3/4 mb-2'></div>
                <div className='h-3 bg-gray-200 rounded w-1/2 mb-2'></div>
                <div className='h-3 bg-gray-200 rounded w-1/4'></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (
    !results ||
    (!results.publications &&
      !results.profiles &&
      !results.authors &&
      !results.results_by_platform &&
      !results.data)
  ) {
    return (
      <div className='bg-white rounded-lg shadow-md p-6 text-center'>
        <div className='text-gray-500'>
          <Eye className='h-12 w-12 mx-auto mb-4 text-gray-300' />
          <p className='text-lg font-medium'>Nenhum resultado encontrado</p>
          <p className='text-sm'>Tente uma nova busca com termos diferentes</p>
        </div>
      </div>
    );
  }

  const toggleCard = (id: string) => {
    const newExpanded = new Set(expandedCards);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedCards(newExpanded);
  };

  const getPlatformIcon = (platform?: string) => {
    switch (platform?.toLowerCase()) {
      case "scholar":
        return "🎓";
      case "lattes":
        return "🇧🇷";
      case "orcid":
        return "🌐";
      default:
        return "📄";
    }
  };

  const getPlatformColor = (platform?: string) => {
    switch (platform?.toLowerCase()) {
      case "scholar":
        return "bg-blue-100 text-blue-800 border-blue-200";
      case "lattes":
        return "bg-green-100 text-green-800 border-green-200";
      case "orcid":
        return "bg-purple-100 text-purple-800 border-purple-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  const getPlatformName = (platform?: string) => {
    switch (platform?.toLowerCase()) {
      case "scholar":
        return "Google Scholar";
      case "lattes":
        return "Plataforma Lattes";
      case "orcid":
        return "ORCID";
      default:
        return "Plataforma Acadêmica";
    }
  };

  const formatAuthors = (authors?: string) => {
    if (!authors) return "Autores não informados";
    if (authors.length > 120) {
      return authors.substring(0, 120) + "...";
    }
    return authors;
  };

  const formatTitle = (title?: string) => {
    if (!title) return "Título não disponível";
    return title;
  };

  // Combinar todos os resultados
  const allItems: (Publication | Profile)[] = [];

  // Resultados diretos
  if (results.publications) {
    console.log(
      "🔍 Encontradas publicações diretas:",
      results.publications.length
    );
    allItems.push(
      ...results.publications.map((p) => ({
        ...p,
        platform: results.platform || "scholar",
      }))
    );
  } else {
    console.log("🔍 Nenhuma publicação direta encontrada");
  }

  if (results.profiles) {
    allItems.push(
      ...results.profiles.map((p) => ({
        ...p,
        platform: results.platform || "lattes",
      }))
    );
  }

  // Resultados do data
  if (results.data?.profiles) {
    allItems.push(
      ...results.data.profiles.map((p: Profile) => ({
        ...p,
        platform: results.platform || "lattes",
      }))
    );
  }

  if (results.data?.publications) {
    console.log(
      "🔍 Encontradas publicações em results.data:",
      results.data.publications.length
    );
    allItems.push(
      ...results.data.publications.map((p: Publication) => ({
        ...p,
        platform: results.platform || "scholar",
      }))
    );
  } else {
    console.log("🔍 Nenhuma publicação encontrada em results.data");
  }

  // Resultados por plataforma (COMPREHENSIVE SEARCH)
  if (results.results_by_platform) {
    console.log(
      "🔍 Processando results_by_platform:",
      results.results_by_platform
    );
    console.log("🔍 Lattes disponível?", !!results.results_by_platform.lattes);

    // Google Scholar
    if (results.results_by_platform.scholar) {
      const scholarData = results.results_by_platform.scholar as any;

      // Publicações diretas
      if (scholarData.publications) {
        allItems.push(
          ...scholarData.publications.map((p: Publication) => ({
            ...p,
            platform: "scholar",
          }))
        );
      }

      // Publicações dentro de data
      if (scholarData.data?.publications) {
        allItems.push(
          ...scholarData.data.publications.map((p: Publication) => ({
            ...p,
            platform: "scholar",
          }))
        );
      }

      // Perfis
      if (scholarData.profiles) {
        allItems.push(
          ...scholarData.profiles.map((p: Profile) => ({
            ...p,
            platform: "scholar",
          }))
        );
      }
    }

    // Lattes
    if (results.results_by_platform.lattes) {
      const lattesData = results.results_by_platform.lattes as any;
      console.log("🇧🇷 DEBUG Lattes - Dados recebidos:", lattesData);

      // Perfis diretos
      if (lattesData.lattes_profiles) {
        console.log(
          "🇧🇷 DEBUG Lattes - lattes_profiles encontrados:",
          lattesData.lattes_profiles.length
        );
        allItems.push(
          ...lattesData.lattes_profiles.map((p: Profile) => ({
            ...p,
            platform: "lattes",
          }))
        );
      }

      // Perfis dentro de data
      if (lattesData.data?.lattes_profiles) {
        allItems.push(
          ...lattesData.data.lattes_profiles.map((p: Profile) => ({
            ...p,
            platform: "lattes",
          }))
        );
      }

      // Perfis genéricos
      if (lattesData.profiles) {
        allItems.push(
          ...lattesData.profiles.map((p: Profile) => ({
            ...p,
            platform: "lattes",
          }))
        );
      }
    }

    // ORCID
    if (results.results_by_platform.orcid) {
      const orcidData = results.results_by_platform.orcid as any;

      // Perfis diretos
      if (orcidData.orcid_profiles) {
        allItems.push(
          ...orcidData.orcid_profiles.map((p: Profile) => ({
            ...p,
            platform: "orcid",
          }))
        );
      }

      // Perfis dentro de data
      if (orcidData.data?.orcid_profiles) {
        allItems.push(
          ...orcidData.data.orcid_profiles.map((p: Profile) => ({
            ...p,
            platform: "orcid",
          }))
        );
      }

      // Perfis genéricos
      if (orcidData.profiles) {
        allItems.push(
          ...orcidData.profiles.map((p: Profile) => ({
            ...p,
            platform: "orcid",
          }))
        );
      }
    }
  }

  console.log(`📊 Total de itens processados: ${allItems.length}`);

  // Filtrar por aba ativa
  const filteredItems =
    activeTab === "all"
      ? allItems
      : allItems.filter((item) => item.platform === activeTab);

  // Estatísticas por plataforma
  const scholarCount = allItems.filter(
    (item) => item.platform === "scholar"
  ).length;
  const lattesCount = allItems.filter(
    (item) => item.platform === "lattes"
  ).length;
  const orcidCount = allItems.filter(
    (item) => item.platform === "orcid"
  ).length;

  // Função para determinar se é publicação ou perfil
  const isPublication = (item: Publication | Profile): item is Publication => {
    // Se tem title E não tem name, é publicação
    // Se tem title E authors, é publicação (mesmo que tenha orcid_id)
    return "title" in item && (!("name" in item) || "authors" in item);
  };

  const isProfile = (item: Publication | Profile): item is Profile => {
    return (
      "name" in item &&
      ("lattes_id" in item || "orcid_id" in item || "institution" in item)
    );
  };

  const getItemLink = (item: Publication | Profile) => {
    if (isPublication(item)) {
      return item.link || item.url;
    } else if (isProfile(item)) {
      if (item.platform === "orcid" && item.orcid_id) {
        return `https://orcid.org/${item.orcid_id}`;
      }
      return item.url || item.lattes_url;
    }
    return null;
  };

  // DEBUG FINAL: verificar estado antes da renderização
  console.log("🎯 DEBUG FINAL - allItems:", allItems.length, allItems);
  console.log(
    "🎯 DEBUG FINAL - filteredItems:",
    filteredItems.length,
    filteredItems
  );
  console.log("🎯 DEBUG FINAL - activeTab:", activeTab);
  console.log("🎯 DEBUG FINAL - lattesCount:", lattesCount);

  return (
    <div className='bg-white rounded-lg shadow-lg overflow-hidden border border-gray-200'>
      {/* Header com Estatísticas MELHORADO */}
      <div className='bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6'>
        <div className='flex items-center justify-between'>
          <div>
            <h2 className='text-2xl font-bold mb-2 flex items-center gap-2'>
              <Trophy className='h-6 w-6' />
              Resultados da Busca
            </h2>
            <p className='text-blue-100'>
              {results.query && `Busca: "${results.query}"`} • {allItems.length}{" "}
              resultados encontrados
            </p>
            {/* Mostrar estatísticas por plataforma */}
            {(scholarCount > 0 || lattesCount > 0 || orcidCount > 0) && (
              <div className='mt-3 flex gap-4 text-sm text-blue-100'>
                {scholarCount > 0 && (
                  <span className='flex items-center gap-1'>
                    🎓 Scholar: <strong>{scholarCount}</strong>
                  </span>
                )}
                {lattesCount > 0 && (
                  <span className='flex items-center gap-1'>
                    🇧🇷 Lattes: <strong>{lattesCount}</strong>
                  </span>
                )}
                {orcidCount > 0 && (
                  <span className='flex items-center gap-1'>
                    🌐 ORCID: <strong>{orcidCount}</strong>
                  </span>
                )}
              </div>
            )}
          </div>
          <div className='text-right'>
            <div className='text-4xl font-bold'>{allItems.length}</div>
            <div className='text-sm text-blue-100'>Total</div>
            {(results as any).max_results_per_platform && (
              <div className='text-xs text-blue-200 mt-1'>
                {(results as any).max_results_per_platform} por plataforma
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Seção de Múltiplos Autores */}
      {results.search_type === "multiple_authors" && results.authors && (
        <div className='bg-gradient-to-r from-purple-50 to-blue-50 border-b border-gray-200 p-6'>
          <div className='mb-4'>
            <h3 className='text-xl font-bold text-gray-900 mb-2 flex items-center gap-2'>
              <Users className='h-6 w-6 text-purple-600' />
              Pesquisadores Encontrados ({results.authors.length})
            </h3>
            <p className='text-gray-600'>
              Selecione um pesquisador para ver suas publicações e poder
              exportar em Excel
            </p>
          </div>

          <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
            {results.authors.map((author, index) => (
              <div
                key={author.author_id}
                className='bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow cursor-pointer'
              >
                <div className='flex items-start justify-between mb-3'>
                  <div className='flex-1'>
                    <h4 className='font-semibold text-gray-900 mb-1'>
                      {author.name}
                    </h4>
                    <div className='flex items-center text-gray-600 text-sm mb-2'>
                      <Building className='h-4 w-4 mr-1' />
                      <span className='truncate'>{author.institution}</span>
                    </div>
                  </div>
                </div>

                <p className='text-sm text-gray-700 mb-3 line-clamp-2'>
                  {author.description}
                </p>

                {/* Áreas de pesquisa */}
                {author.research_areas && author.research_areas.length > 0 && (
                  <div className='mb-3'>
                    <div className='flex flex-wrap gap-1'>
                      {author.research_areas.slice(0, 2).map((area, idx) => (
                        <span
                          key={idx}
                          className='px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full'
                        >
                          {area}
                        </span>
                      ))}
                      {author.research_areas.length > 2 && (
                        <span className='px-2 py-1 bg-gray-100 text-gray-500 text-xs rounded-full'>
                          +{author.research_areas.length - 2}
                        </span>
                      )}
                    </div>
                  </div>
                )}

                {/* Métricas */}
                <div className='flex items-center justify-between text-sm text-gray-600 mb-3'>
                  <div className='flex items-center'>
                    <TrendingUp className='h-4 w-4 mr-1' />
                    <span>
                      {author.total_citations.toLocaleString()} citações*
                    </span>
                  </div>
                  {author.h_index > 0 && (
                    <div className='font-medium text-orange-600'>
                      H-Index: {author.h_index}*
                      <span className='text-xs text-gray-500 ml-1'>
                        (estimado)
                      </span>
                    </div>
                  )}
                </div>

                {/* Nota explicativa */}
                <div className='mb-3'>
                  <p className='text-xs text-gray-500 italic'>
                    * Valores estimados. Clique no botão abaixo para obter
                    métricas reais do Google Scholar.
                  </p>
                </div>

                {/* Publicações recentes preview */}
                {author.recent_publications &&
                  author.recent_publications.length > 0 && (
                    <div className='border-t pt-3'>
                      <div className='flex items-center mb-2'>
                        <Book className='h-4 w-4 text-gray-500 mr-1' />
                        <span className='text-xs font-medium text-gray-700'>
                          Publicações Recentes:
                        </span>
                      </div>
                      <div className='space-y-1'>
                        {author.recent_publications
                          .slice(0, 1)
                          .map((pub, idx) => (
                            <div key={idx} className='text-xs text-gray-600'>
                              <span className='font-medium'>{pub.title}</span>
                              {pub.year && (
                                <span className='text-gray-500'>
                                  {" "}
                                  ({pub.year})
                                </span>
                              )}
                            </div>
                          ))}
                      </div>
                    </div>
                  )}

                {/* Botão para ver publicações */}
                <div className='mt-4 pt-3 border-t'>
                  <button
                    onClick={() => {
                      // Abrir Google Scholar em nova aba para o usuário buscar manualmente
                      const searchUrl = `https://scholar.google.com/citations?hl=pt-BR&view_op=search_authors&mauthors=${encodeURIComponent(
                        author.name
                      )}`;
                      window.open(searchUrl, "_blank");

                      // Mostrar instruções para o usuário
                      setTimeout(() => {
                        // Primeiro, perguntar quantas publicações extrair
                        const numPublications = prompt(
                          `📚 QUANTAS PUBLICAÇÕES EXTRAIR?\n\n` +
                            `Escolha o número de publicações para extrair do Google Scholar:\n\n` +
                            `• 20 (padrão - mais rápido)\n` +
                            `• 40 (recomendado)\n` +
                            `• 60 (completo)\n` +
                            `• 100 (muito completo - pode demorar)\n\n` +
                            `Digite o número (ou deixe vazio para 20):`,
                          "20"
                        );

                        let maxPubs = 20;
                        if (
                          numPublications &&
                          !isNaN(parseInt(numPublications))
                        ) {
                          maxPubs = Math.min(
                            Math.max(parseInt(numPublications), 10),
                            200
                          );
                        }

                        const profileUrl = prompt(
                          `🔍 INSTRUÇÕES PARA OBTER H-INDEX REAL:\n\n` +
                            `1. Na aba que acabou de abrir, procure o perfil correto de "${author.name}"\n\n` +
                            `2. Clique no nome do pesquisador para abrir seu perfil completo\n\n` +
                            `3. No perfil, você verá as métricas (citações, h-index, i10-index)\n\n` +
                            `4. Copie a URL COMPLETA da página do perfil (ex: https://scholar.google.com/citations?user=XXXXXXX)\n\n` +
                            `5. Cole a URL aqui para extrair o H-INDEX REAL e ${maxPubs} publicações:`
                        );

                        if (profileUrl && profileUrl.trim()) {
                          // Verificar se é uma URL válida do Google Scholar
                          if (
                            profileUrl.includes(
                              "scholar.google.com/citations?user="
                            )
                          ) {
                            // Redirecionar para busca por URL que extrairá dados reais
                            if (onSelectAuthor) {
                              // Criar um autor modificado com a URL real e número de publicações
                              const authorWithUrl = {
                                ...author,
                                profile_url: profileUrl,
                                author_id: `url_${Date.now()}`, // ID único para URL
                                description: `Carregando dados reais do Google Scholar... (${maxPubs} publicações)`,
                                max_publications: maxPubs, // Adicionar número de publicações
                              };
                              onSelectAuthor(authorWithUrl);
                            }
                          } else {
                            alert(
                              `❌ URL inválida!\n\nA URL deve ser do Google Scholar e conter "citations?user="\n\nExemplo: https://scholar.google.com/citations?user=ABC123DEF\n\nTente novamente com a URL correta.`
                            );
                          }
                        }
                      }, 1500);
                    }}
                    className='w-full flex items-center justify-center px-3 py-2 border border-blue-300 text-sm font-medium rounded-md text-blue-700 bg-blue-50 hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors'
                  >
                    <ExternalLink className='h-4 w-4 mr-1' />
                    🎯 Obter H-Index Real
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Perfil do Pesquisador */}
      {results.researcher_info && (
        <div className='bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200 p-6'>
          <div className='flex items-start space-x-6'>
            {/* Avatar/Ícone */}
            <div className='flex-shrink-0'>
              <div
                className={`w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold text-white ${
                  results.platform === "scholar"
                    ? "bg-blue-500"
                    : results.platform === "lattes"
                    ? "bg-green-500"
                    : results.platform === "orcid"
                    ? "bg-purple-500"
                    : "bg-gray-500"
                }`}
              >
                {results.platform === "scholar"
                  ? "🎓"
                  : results.platform === "lattes"
                  ? "🇧🇷"
                  : results.platform === "orcid"
                  ? "🌐"
                  : "👤"}
              </div>
            </div>

            {/* Informações do Perfil */}
            <div className='flex-1 min-w-0'>
              <div className='flex items-start justify-between'>
                <div className='flex-1'>
                  <h3 className='text-xl font-bold text-gray-900 mb-2 flex items-center gap-2'>
                    <User className='h-5 w-5 text-gray-600' />
                    {results.researcher_info.name}
                  </h3>

                  {/* Instituição */}
                  {(results.researcher_info.institution ||
                    results.researcher_info.affiliation) && (
                    <div className='flex items-center gap-2 mb-2 text-gray-700'>
                      <Building className='h-4 w-4 text-gray-500' />
                      <span className='text-sm font-medium'>
                        {results.researcher_info.institution ||
                          results.researcher_info.affiliation}
                      </span>
                    </div>
                  )}

                  {/* Áreas de Pesquisa */}
                  {results.researcher_info.research_areas &&
                    results.researcher_info.research_areas.length > 0 && (
                      <div className='flex items-start gap-2 mb-3'>
                        <Book className='h-4 w-4 text-gray-500 mt-0.5' />
                        <div className='flex flex-wrap gap-1'>
                          {results.researcher_info.research_areas
                            .slice(0, 3)
                            .map((area, index) => (
                              <span
                                key={index}
                                className='bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium'
                              >
                                {area}
                              </span>
                            ))}
                          {results.researcher_info.research_areas.length >
                            3 && (
                            <span className='text-gray-500 text-xs'>
                              +
                              {results.researcher_info.research_areas.length -
                                3}{" "}
                              mais
                            </span>
                          )}
                        </div>
                      </div>
                    )}
                </div>

                {/* Métricas */}
                <div className='flex gap-4 ml-4'>
                  {results.researcher_info.h_index && (
                    <div className='text-center bg-white rounded-lg p-3 shadow-sm border border-gray-200'>
                      <div className='text-lg font-bold text-blue-600'>
                        {results.researcher_info.h_index}
                      </div>
                      <div className='text-xs text-gray-600 font-medium'>
                        Índice H
                      </div>
                    </div>
                  )}

                  {results.researcher_info.total_citations && (
                    <div className='text-center bg-white rounded-lg p-3 shadow-sm border border-gray-200'>
                      <div className='text-lg font-bold text-green-600'>
                        {typeof results.researcher_info.total_citations ===
                        "number"
                          ? results.researcher_info.total_citations.toLocaleString()
                          : results.researcher_info.total_citations}
                      </div>
                      <div className='text-xs text-gray-600 font-medium'>
                        Citações
                      </div>
                    </div>
                  )}

                  {results.total_results && (
                    <div className='text-center bg-white rounded-lg p-3 shadow-sm border border-gray-200'>
                      <div className='text-lg font-bold text-purple-600'>
                        {results.total_results}
                      </div>
                      <div className='text-xs text-gray-600 font-medium'>
                        Publicações
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* IDs/Links */}
              <div className='flex gap-4 mt-3 text-sm'>
                {results.researcher_info.orcid_id && (
                  <a
                    href={`https://orcid.org/${results.researcher_info.orcid_id}`}
                    target='_blank'
                    rel='noopener noreferrer'
                    className='flex items-center gap-1 text-purple-600 hover:text-purple-800 transition-colors'
                  >
                    <ExternalLink className='h-3 w-3' />
                    ORCID: {results.researcher_info.orcid_id}
                  </a>
                )}

                {results.researcher_info.last_update && (
                  <div className='flex items-center gap-1 text-gray-500'>
                    <Calendar className='h-3 w-3' />
                    Atualizado: {results.researcher_info.last_update}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tabs de Plataformas MELHORADAS */}
      {(scholarCount > 0 || lattesCount > 0 || orcidCount > 0) && (
        <div className='border-b border-gray-200 bg-gray-50'>
          <nav className='flex space-x-1 px-6' aria-label='Tabs'>
            <button
              onClick={() => setActiveTab("all")}
              className={`py-4 px-4 border-b-3 font-semibold text-sm transition-all duration-200 rounded-t-md ${
                activeTab === "all"
                  ? "border-blue-500 text-blue-700 bg-white shadow-sm"
                  : "border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300 hover:bg-gray-100"
              }`}
            >
              <span className='flex items-center gap-2'>
                📊 <span>Todos</span>
                <span className='bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-bold'>
                  {allItems.length}
                </span>
              </span>
            </button>
            {scholarCount > 0 && (
              <button
                onClick={() => setActiveTab("scholar")}
                className={`py-4 px-4 border-b-3 font-semibold text-sm transition-all duration-200 rounded-t-md ${
                  activeTab === "scholar"
                    ? "border-blue-500 text-blue-700 bg-white shadow-sm"
                    : "border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300 hover:bg-gray-100"
                }`}
              >
                <span className='flex items-center gap-2'>
                  🎓 <span>Google Scholar</span>
                  <span className='bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-bold'>
                    {scholarCount}
                  </span>
                </span>
              </button>
            )}
            {lattesCount > 0 && (
              <button
                onClick={() => setActiveTab("lattes")}
                className={`py-4 px-4 border-b-3 font-semibold text-sm transition-all duration-200 rounded-t-md ${
                  activeTab === "lattes"
                    ? "border-green-500 text-green-700 bg-white shadow-sm"
                    : "border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300 hover:bg-gray-100"
                }`}
              >
                <span className='flex items-center gap-2'>
                  🇧🇷 <span>Plataforma Lattes</span>
                  <span className='bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-bold'>
                    {lattesCount}
                  </span>
                </span>
              </button>
            )}
            {orcidCount > 0 && (
              <button
                onClick={() => setActiveTab("orcid")}
                className={`py-4 px-4 border-b-3 font-semibold text-sm transition-all duration-200 rounded-t-md ${
                  activeTab === "orcid"
                    ? "border-purple-500 text-purple-700 bg-white shadow-sm"
                    : "border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300 hover:bg-gray-100"
                }`}
              >
                <span className='flex items-center gap-2'>
                  🌐 <span>ORCID</span>
                  <span className='bg-purple-100 text-purple-800 px-2 py-1 rounded-full text-xs font-bold'>
                    {orcidCount}
                  </span>
                </span>
              </button>
            )}
          </nav>
        </div>
      )}

      {/* Lista de Resultados */}
      <div className='max-h-96 overflow-y-auto'>
        {filteredItems.length === 0 ? (
          <div className='p-8 text-center text-gray-500'>
            <Eye className='h-16 w-16 mx-auto mb-4 text-gray-300' />
            <p className='text-lg'>
              Nenhum resultado encontrado para esta plataforma
            </p>
            <p className='text-sm'>
              Experimente outro filtro ou realize uma nova busca
            </p>
          </div>
        ) : (
          <div className='divide-y divide-gray-200'>
            {filteredItems.map((item, index) => {
              const itemId = `${item.platform}-${index}`;
              const isExpanded = expandedCards.has(itemId);
              const link = getItemLink(item);

              // DEBUG: verificar item individual
              console.log(`🎯 Item ${index}:`, item);
              console.log(`🎯 isPublication(item): ${isPublication(item)}`);
              console.log(`🎯 title: "${(item as any).title}"`);
              console.log(`🎯 authors: "${(item as any).authors}"`);

              return (
                <div
                  key={itemId}
                  className='p-6 hover:bg-gray-50 transition-colors duration-150'
                >
                  <div className='flex items-start justify-between'>
                    <div className='flex-1 min-w-0'>
                      {/* Título/Nome e Plataforma */}
                      <div className='flex items-start gap-3 mb-3'>
                        <span className='text-2xl mt-1'>
                          {getPlatformIcon(item.platform)}
                        </span>
                        <div className='flex-1'>
                          <h3 className='text-lg font-semibold text-gray-900 leading-6 mb-2'>
                            {isPublication(item)
                              ? formatTitle(item.title)
                              : item.name}
                          </h3>
                          <span
                            className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${getPlatformColor(
                              item.platform
                            )}`}
                          >
                            {getPlatformName(item.platform)}
                          </span>
                        </div>
                      </div>

                      {/* Metadados */}
                      <div className='flex flex-wrap items-center gap-4 text-sm text-gray-600 mb-3'>
                        {isPublication(item) ? (
                          <>
                            {item.authors && (
                              <div className='flex items-center gap-1'>
                                <User className='h-4 w-4' />
                                <span>{formatAuthors(item.authors)}</span>
                              </div>
                            )}
                            {item.year && (
                              <div className='flex items-center gap-1'>
                                <Calendar className='h-4 w-4' />
                                <span>{item.year}</span>
                              </div>
                            )}
                            {(item.cited_by !== undefined ||
                              item.citations !== undefined) &&
                              ((item.cited_by || 0) > 0 ||
                                (item.citations || 0) > 0) && (
                                <div className='flex items-center gap-1'>
                                  <Award className='h-4 w-4 text-amber-500' />
                                  <span className='text-amber-600 font-medium'>
                                    {item.cited_by || item.citations || 0}{" "}
                                    citações
                                  </span>
                                </div>
                              )}
                            {item.journal && (
                              <div className='flex items-center gap-1'>
                                <Book className='h-4 w-4' />
                                <span>{item.journal}</span>
                              </div>
                            )}
                          </>
                        ) : (
                          <>
                            {(item.current_institution || item.institution) && (
                              <div className='flex items-center gap-1'>
                                <Building className='h-4 w-4' />
                                <span>
                                  {item.current_institution || item.institution}
                                </span>
                              </div>
                            )}
                            {(item.current_position || item.position) && (
                              <div className='flex items-center gap-1'>
                                <User className='h-4 w-4' />
                                <span>
                                  {item.current_position || item.position}
                                </span>
                              </div>
                            )}
                            {item.total_publications && (
                              <div className='flex items-center gap-1'>
                                <FileText className='h-4 w-4' />
                                <span>
                                  {item.total_publications} publicações
                                </span>
                              </div>
                            )}
                            {item.h_index !== undefined && item.h_index > 0 && (
                              <div className='flex items-center gap-1'>
                                <Award className='h-4 w-4' />
                                <span>Índice H: {item.h_index}</span>
                              </div>
                            )}
                            {item.total_citations !== undefined &&
                              item.total_citations > 0 && (
                                <div className='flex items-center gap-1'>
                                  <Trophy className='h-4 w-4' />
                                  <span>{item.total_citations} citações</span>
                                </div>
                              )}
                            {item.research_areas &&
                              item.research_areas.length > 0 && (
                                <div className='flex items-center gap-1'>
                                  <MapPin className='h-4 w-4' />
                                  <span>
                                    {item.research_areas.slice(0, 2).join(", ")}
                                    {item.research_areas.length > 2 && "..."}
                                  </span>
                                </div>
                              )}
                          </>
                        )}
                      </div>

                      {/* Snippet/Summary */}
                      {(isPublication(item)
                        ? item.snippet
                        : item.summary || item.biography) && (
                        <div className='text-sm text-gray-700 mb-3'>
                          <p className='line-clamp-2'>
                            {isPublication(item)
                              ? item.snippet
                              : item.summary || item.biography}
                          </p>
                        </div>
                      )}

                      {/* Ações */}
                      <div className='flex items-center gap-4'>
                        {link && (
                          <a
                            href={link}
                            target='_blank'
                            rel='noopener noreferrer'
                            className='inline-flex items-center gap-2 text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors'
                          >
                            <ExternalLink className='h-4 w-4' />
                            Ver no {getPlatformName(item.platform)}
                          </a>
                        )}

                        {((isPublication(item) &&
                          (item.snippet || item.publication)) ||
                          (isProfile(item) &&
                            (item.biography ||
                              item.education ||
                              item.publications))) && (
                          <button
                            onClick={() => toggleCard(itemId)}
                            className='inline-flex items-center gap-1 text-gray-500 hover:text-gray-700 text-sm transition-colors'
                          >
                            {isExpanded ? (
                              <>
                                <ChevronUp className='h-4 w-4' />
                                Menos detalhes
                              </>
                            ) : (
                              <>
                                <ChevronDown className='h-4 w-4' />
                                Mais detalhes
                              </>
                            )}
                          </button>
                        )}
                      </div>

                      {/* Detalhes Expandidos */}
                      {isExpanded && (
                        <div className='mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200'>
                          {isPublication(item) ? (
                            <div className='space-y-3 text-sm'>
                              {item.publication && (
                                <div>
                                  <span className='font-medium text-gray-700'>
                                    Publicação:
                                  </span>
                                  <span className='ml-2 text-gray-600'>
                                    {item.publication}
                                  </span>
                                </div>
                              )}
                              {item.snippet && (
                                <div>
                                  <span className='font-medium text-gray-700'>
                                    Resumo completo:
                                  </span>
                                  <p className='mt-1 text-gray-600'>
                                    {item.snippet}
                                  </p>
                                </div>
                              )}
                              {item.doi && (
                                <div>
                                  <span className='font-medium text-gray-700'>
                                    DOI:
                                  </span>
                                  <span className='ml-2 text-gray-600'>
                                    {item.doi}
                                  </span>
                                </div>
                              )}
                              {item.page_number && (
                                <div>
                                  <span className='font-medium text-gray-700'>
                                    Página:
                                  </span>
                                  <span className='ml-2 text-gray-600'>
                                    {item.page_number}
                                  </span>
                                </div>
                              )}
                            </div>
                          ) : (
                            <div className='space-y-3 text-sm'>
                              {/* Métricas Acadêmicas */}
                              {(item.h_index !== undefined ||
                                item.total_citations !== undefined) && (
                                <div>
                                  <span className='font-medium text-gray-700'>
                                    Métricas Acadêmicas:
                                  </span>
                                  <div className='mt-2 grid grid-cols-2 gap-4'>
                                    {item.h_index !== undefined && (
                                      <div className='flex items-center gap-2 p-2 bg-blue-50 rounded-lg'>
                                        <Award className='h-5 w-5 text-blue-600' />
                                        <div>
                                          <div className='font-semibold text-blue-800'>
                                            {item.h_index}
                                          </div>
                                          <div className='text-xs text-blue-600'>
                                            Índice H
                                          </div>
                                        </div>
                                      </div>
                                    )}
                                    {item.total_citations !== undefined && (
                                      <div className='flex items-center gap-2 p-2 bg-green-50 rounded-lg'>
                                        <Trophy className='h-5 w-5 text-green-600' />
                                        <div>
                                          <div className='font-semibold text-green-800'>
                                            {item.total_citations}
                                          </div>
                                          <div className='text-xs text-green-600'>
                                            Citações
                                          </div>
                                        </div>
                                      </div>
                                    )}
                                  </div>
                                </div>
                              )}

                              {item.biography && (
                                <div>
                                  <span className='font-medium text-gray-700'>
                                    Biografia:
                                  </span>
                                  <p className='mt-1 text-gray-600'>
                                    {item.biography}
                                  </p>
                                </div>
                              )}
                              {item.education && item.education.length > 0 && (
                                <div>
                                  <span className='font-medium text-gray-700'>
                                    Formação:
                                  </span>
                                  <ul className='mt-1 text-gray-600 list-disc list-inside'>
                                    {item.education.map((edu, idx) => (
                                      <li key={idx}>{edu}</li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                              {item.research_areas &&
                                item.research_areas.length > 0 && (
                                  <div>
                                    <span className='font-medium text-gray-700'>
                                      Áreas de pesquisa:
                                    </span>
                                    <div className='mt-1 flex flex-wrap gap-1'>
                                      {item.research_areas.map((area, idx) => (
                                        <span
                                          key={idx}
                                          className='inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded'
                                        >
                                          {area}
                                        </span>
                                      ))}
                                    </div>
                                  </div>
                                )}
                              {item.publications &&
                                item.publications.length > 0 && (
                                  <div>
                                    <span className='font-medium text-gray-700'>
                                      Publicações recentes:
                                    </span>
                                    <ul className='mt-1 text-gray-600 space-y-1'>
                                      {item.publications
                                        .slice(0, 3)
                                        .map((pub, idx) => (
                                          <li key={idx} className='text-xs'>
                                            {pub.title}
                                          </li>
                                        ))}
                                      {item.publications.length > 3 && (
                                        <li className='text-xs text-gray-500'>
                                          ... e mais{" "}
                                          {item.publications.length - 3}{" "}
                                          publicações
                                        </li>
                                      )}
                                    </ul>
                                  </div>
                                )}
                              {(item.lattes_id || item.orcid_id) && (
                                <div>
                                  <span className='font-medium text-gray-700'>
                                    ID:
                                  </span>
                                  <span className='ml-2 text-gray-600 font-mono text-xs'>
                                    {item.lattes_id || item.orcid_id}
                                  </span>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Footer com Resumo */}
      {allItems.length > 0 && (
        <div className='bg-gray-50 px-6 py-4 border-t border-gray-200'>
          <div className='flex items-center justify-between text-sm text-gray-600'>
            <div className='flex items-center gap-2'>
              <Zap className='h-4 w-4' />
              Mostrando {filteredItems.length} de {allItems.length} resultados
            </div>
            <div className='flex gap-4'>
              {scholarCount > 0 && (
                <span className='flex items-center gap-1'>
                  🎓 {scholarCount}
                </span>
              )}
              {lattesCount > 0 && (
                <span className='flex items-center gap-1'>
                  🇧🇷 {lattesCount}
                </span>
              )}
              {orcidCount > 0 && (
                <span className='flex items-center gap-1'>🌐 {orcidCount}</span>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;
