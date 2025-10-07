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

interface ResultsDisplayProps {
  results: {
    results_by_platform?: ResultsByPlatform;
    publications?: Publication[];
    profiles?: Profile[];
    data?: any;
    total_results?: number;
    search_type?: string;
    query?: string;
    success?: boolean;
    message?: string;
    platform?: string;
  } | null;
  isLoading?: boolean;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({
  results,
  isLoading,
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
