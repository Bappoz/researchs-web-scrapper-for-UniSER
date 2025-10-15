/**
 * 🔗 API SERVICE - REORGANIZADO
 * Comunicação com backend de pesquisa acadêmica
 */

import axios from "axios";

// Configuração da URL base da API - compatível com Docker
const getApiBaseUrl = () => {
  // Em desenvolvimento local
  if (
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
  ) {
    return "http://localhost:8000";
  }
  // Em produção com Docker (usa proxy do nginx)
  return "/api";
};

const API_BASE_URL = getApiBaseUrl();
console.log("🔗 API Base URL:", API_BASE_URL);

// Configuração do axios
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 segundos para pesquisas longas
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor para logging
api.interceptors.request.use(
  (config) => {
    console.log(
      `🔍 API Request: ${config.method?.toUpperCase()} ${config.url}`
    );
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.config.url} - ${response.status}`);
    return response;
  },
  (error) => {
    console.error(
      `❌ API Error: ${error.config?.url} - ${error.response?.status}`
    );
    return Promise.reject(error);
  }
);

// ==================== TIPOS ====================

export interface SearchParams {
  query: string;
  maxResults?: number;
  exportExcel?: boolean;
  platform?: string;
  searchType?: string;
}

export interface Publication {
  title: string;
  authors?: string;
  publication?: string;
  year?: number;
  cited_by: number;
  link?: string;
  snippet?: string;
  platform?: string;
}

export interface LattesProfile {
  name: string;
  lattes_id?: string;
  current_institution?: string;
  profile_url?: string;
  current_position?: string;
  research_areas: string[];
  total_publications: number;
  total_projects: number;
  h_index?: number;
  i10_index?: number;
  total_citations?: number;
  orcid_id?: string;
  publications: Publication[];
  projects: Array<{
    title: string;
    description?: string;
    year_start?: number;
    year_end?: number;
    funding_agency?: string;
  }>;
}

export interface ORCIDProfile {
  orcid_id: string;
  given_names?: string;
  family_name?: string;
  credit_name?: string;
  biography?: string;
  total_works?: number;
  h_index?: number;
  i10_index?: number;
  total_citations?: number;
  employments: Array<{
    organization: string;
    role_title?: string;
    start_date?: string;
    end_date?: string;
    city?: string;
    country?: string;
  }>;
  works: Array<{
    title: string;
    journal_title?: string;
    type?: string;
    publication_date?: string;
    cited_by?: number;
    external_ids: Array<{ type: string; value: string }>;
  }>;
}

export interface SearchResponse {
  success: boolean;
  message: string;
  platform: string;
  search_type: string;
  query: string;
  total_results: number;
  execution_time: number;
  publications?: Publication[];
  lattes_profiles?: LattesProfile[];
  orcid_profiles?: ORCIDProfile[];
  total_publications?: number;
  total_projects?: number;
  csv_file?: string;
  excel_file?: string;
  data_sources?: string[];
  data?: any;
  results_by_platform?: any;
  // Novos campos para suporte ao perfil do autor
  author_profile?: any;
  researcher_info?: {
    name: string;
    institution?: string;
    h_index?: number;
    i10_index?: number;
    total_citations?: number;
  };
}

// ==================== SERVIÇOS REORGANIZADOS ====================

export const academicService = {
  // ========== BUSCA POR AUTOR ==========

  async searchAuthorScholar(
    author: string,
    maxResults = 10,
    exportExcel = false
  ): Promise<SearchResponse> {
    const response = await api.get("/search/author/scholar", {
      params: { author, max_results: maxResults, export_excel: exportExcel },
    });
    return response.data;
  },

  async searchAuthorLattes(
    name: string,
    maxResults = 10
  ): Promise<SearchResponse> {
    const response = await api.get("/search/author/lattes", {
      params: { name, max_results: maxResults },
    });
    return response.data;
  },

  async searchAuthorOrcid(
    name: string,
    maxResults = 10
  ): Promise<SearchResponse> {
    const response = await api.get("/search/author/orcid", {
      params: { name, max_results: maxResults },
    });
    return response.data;
  },

  async searchByProfileLink(
    profileUrl: string,
    platform?: string,
    exportExcel = false,
    maxPublications = 20,
    filterKeywords = true
  ): Promise<SearchResponse> {
    // Extrair o query do profileUrl (nome do autor)
    let query = "Autor";
    let detectedPlatform = platform;

    if (profileUrl.includes("leonardo")) {
      query = "Leonardo";
    } else if (profileUrl.includes("scholar.google.com")) {
      // Para Google Scholar, extrair nome da URL se possível
      const urlParams = new URLSearchParams(profileUrl.split("?")[1]);
      const userParam = urlParams.get("user");
      if (userParam) {
        query = `Scholar-${userParam}`;
      }
      detectedPlatform = "scholar";
    } else if (profileUrl.includes("orcid.org")) {
      // Para ORCID, usar parte do ID como query
      const idMatch = profileUrl.match(/\/(\d{4}-\d{4}-\d{4}-\d{4})$/);
      if (idMatch) {
        query = `ORCID-${idMatch[1].split("-")[3]}`;
      }
      detectedPlatform = "orcid";
    } else if (profileUrl.includes("lattes.cnpq.br")) {
      // Para Lattes, extrair o ID e usar como query
      const lattesIdMatch = profileUrl.match(/\/(\d{16})$/);
      if (lattesIdMatch) {
        query = `LATTES-${lattesIdMatch[1]}`;
      }
      detectedPlatform = "lattes";
    }

    const data: any = {
      query: query,
      export_excel: exportExcel,
      filter_keywords: filterKeywords,
      platforms: detectedPlatform || "scholar",
      profile_url: profileUrl, // Enviar a URL original também
      max_publications: maxPublications, // Número de publicações a extrair
    };

    console.log("🔍 Enviando POST para /search/author/profile:", data);
    const response = await api.post("/search/author/profile", null, {
      params: data,
    });
    return response.data;
  },

  // ========== BUSCA POR TEMA ==========

  async searchTopicScholar(
    topic: string,
    maxResults = 20,
    exportExcel = false
  ): Promise<SearchResponse> {
    const response = await api.get("/search/topic/scholar", {
      params: { topic, max_results: maxResults, export_excel: exportExcel },
    });
    return response.data;
  },

  async searchTopicLattes(
    topic: string,
    maxResults = 20
  ): Promise<SearchResponse> {
    const response = await api.get("/search/topic/lattes", {
      params: { topic, max_results: maxResults },
    });
    return response.data;
  },

  async searchTopicOrcid(
    topic: string,
    maxResults = 20
  ): Promise<SearchResponse> {
    const response = await api.get("/search/topic/orcid", {
      params: { topic, max_results: maxResults },
    });
    return response.data;
  },

  // ========== BUSCA COMPLETA ==========

  async comprehensiveSearch(
    query: string,
    searchType: "author" | "topic" | "both" = "both",
    platforms: string = "all",
    maxResults = 10,
    exportExcel = false
  ): Promise<SearchResponse> {
    const response = await api.get("/search/comprehensive", {
      params: {
        query,
        search_type: searchType,
        platforms,
        max_results: maxResults,
        export_excel: exportExcel,
      },
    });
    return response.data;
  },

  // ========== UTILITÁRIOS ==========

  async healthCheck(): Promise<any> {
    const response = await api.get("/health");
    return response.data;
  },

  async testPlatforms(): Promise<any> {
    const response = await api.get("/test/platforms");
    return response.data;
  },
};

// ==================== MÉTODOS DE CONVENIÊNCIA ====================

// Para compatibilidade com o código existente
export const scholarService = {
  async search(query: string): Promise<Publication[]> {
    const response = await academicService.searchTopicScholar(query);
    return response.data?.publications || [];
  },

  async searchByQuery(params: SearchParams): Promise<SearchResponse> {
    return academicService.searchTopicScholar(
      params.query,
      params.maxResults,
      params.exportExcel
    );
  },

  async searchByAuthor(
    author: string,
    exportExcel = false
  ): Promise<SearchResponse> {
    return academicService.searchAuthorScholar(author, 10, exportExcel);
  },
};

export interface AuthorInfo {
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

export interface AuthorsSearchResponse {
  success: boolean;
  message: string;
  query: string;
  search_type: string;
  platform: string;
  total_results: number;
  authors: AuthorInfo[];
  execution_time: number;
}

export interface AuthorPublicationsResponse {
  success: boolean;
  message: string;
  author_id: string;
  search_type: string;
  platform: string;
  total_results: number;
  publications: Publication[];
  execution_time: number;
  excel_file?: string;
  excel_error?: string;
}

export const lattesService = {
  async search(name: string, maxResults = 10): Promise<SearchResponse> {
    return academicService.searchAuthorLattes(name, maxResults);
  },
};

export const orcidService = {
  async search(name: string, maxResults = 10): Promise<SearchResponse> {
    return academicService.searchAuthorOrcid(name, maxResults);
  },
};

// ==================== NOVOS SERVIÇOS SEPARADOS (MODULAR) ====================

export const separatedLattesService = {
  /**
   * Busca pesquisadores no Lattes usando endpoints separados
   */
  async searchResearchers(
    name: string,
    maxResults = 10
  ): Promise<SearchResponse> {
    try {
      const response = await api.get("/api/lattes/search/researchers", {
        params: {
          name,
          max_results: maxResults,
        },
      });
      return response.data;
    } catch (error: any) {
      console.error("Erro na busca de pesquisadores Lattes:", error);
      throw new Error(error.response?.data?.detail || "Erro na busca Lattes");
    }
  },

  /**
   * Obtém perfil completo por URL do Lattes
   */
  async getProfileByUrl(profileUrl: string) {
    try {
      const response = await api.get("/api/lattes/profile/by-url", {
        params: {
          profile_url: profileUrl,
        },
      });
      return response.data;
    } catch (error: any) {
      console.error("Erro ao obter perfil Lattes:", error);
      throw new Error(
        error.response?.data?.detail || "Erro ao obter perfil Lattes"
      );
    }
  },

  /**
   * Health check do serviço Lattes
   */
  async healthCheck() {
    try {
      const response = await api.get("/api/lattes/health");
      return response.data;
    } catch (error: any) {
      throw new Error("Serviço Lattes indisponível");
    }
  },
};

export const separatedOrcidService = {
  /**
   * Busca pesquisadores no ORCID usando endpoints separados
   */
  async searchResearchers(
    name: string,
    maxResults = 10
  ): Promise<SearchResponse> {
    try {
      const response = await api.get("/api/orcid/search/researchers", {
        params: {
          name,
          max_results: maxResults,
        },
      });
      return response.data;
    } catch (error: any) {
      console.error("Erro na busca de pesquisadores ORCID:", error);
      throw new Error(error.response?.data?.detail || "Erro na busca ORCID");
    }
  },

  /**
   * Obtém perfil completo por URL do ORCID
   */
  async getProfileByUrl(profileUrl: string) {
    try {
      const response = await api.get("/api/orcid/profile/by-url", {
        params: {
          profile_url: profileUrl,
        },
      });
      return response.data;
    } catch (error: any) {
      console.error("Erro ao obter perfil ORCID:", error);
      throw new Error(
        error.response?.data?.detail || "Erro ao obter perfil ORCID"
      );
    }
  },

  /**
   * Busca por palavra-chave no ORCID
   */
  async searchByKeyword(keyword: string, maxResults = 10) {
    try {
      const response = await api.get("/api/orcid/search/by-keyword", {
        params: {
          keyword,
          max_results: maxResults,
        },
      });
      return response.data;
    } catch (error: any) {
      console.error("Erro na busca por keyword ORCID:", error);
      throw new Error(
        error.response?.data?.detail || "Erro na busca por keyword"
      );
    }
  },

  /**
   * Health check do serviço ORCID
   */
  async healthCheck() {
    try {
      const response = await api.get("/api/orcid/health");
      return response.data;
    } catch (error: any) {
      throw new Error("Serviço ORCID indisponível");
    }
  },
};

// ==================== NOVOS SERVIÇOS PARA MÚLTIPLOS AUTORES ====================

export const authorsService = {
  /**
   * Busca múltiplos autores por nome no Google Scholar
   */
  async searchMultipleAuthors(
    authorName: string,
    maxResults = 10
  ): Promise<AuthorsSearchResponse> {
    try {
      const response = await api.get("/search/authors/scholar", {
        params: {
          name: authorName,
          max_results: maxResults,
        },
      });
      return response.data;
    } catch (error: any) {
      console.error("Erro na busca de múltiplos autores:", error);
      throw new Error(
        error.response?.data?.detail || "Erro na busca de autores"
      );
    }
  },

  /**
   * Busca todas as publicações de um autor específico
   */
  async getAuthorPublications(
    authorId: string,
    maxResults = 50,
    exportExcel = false,
    authorName?: string
  ): Promise<AuthorPublicationsResponse> {
    try {
      const params: any = {
        max_results: maxResults,
        export_excel: exportExcel,
      };

      // Adicionar nome do autor se fornecido
      if (authorName) {
        params.author_name = authorName;
      }

      const response = await api.get(
        `/search/author/publications/${authorId}`,
        { params }
      );
      return response.data;
    } catch (error: any) {
      console.error("Erro na busca de publicações do autor:", error);
      throw new Error(
        error.response?.data?.detail || "Erro na busca de publicações"
      );
    }
  },
};

// ==================== EXPORTAÇÕES PARA COMPATIBILIDADE ====================

export default academicService;
