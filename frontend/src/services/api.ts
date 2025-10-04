/**
 * 🔗 API SERVICE - REORGANIZADO
 * Comunicação com backend de pesquisa acadêmica
 */

import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

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
  saveExcel?: boolean;
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
  current_position?: string;
  research_areas: string[];
  total_publications: number;
  total_projects: number;
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
}

// ==================== SERVIÇOS REORGANIZADOS ====================

export const academicService = {
  // ========== BUSCA POR AUTOR ==========
  
  async searchAuthorScholar(author: string, maxResults = 10, saveExcel = false): Promise<SearchResponse> {
    const response = await api.get("/search/author/scholar", {
      params: { author, max_results: maxResults, save_excel: saveExcel }
    });
    return response.data;
  },

  async searchAuthorLattes(name: string, maxResults = 10): Promise<SearchResponse> {
    const response = await api.get("/search/author/lattes", {
      params: { name, max_results: maxResults }
    });
    return response.data;
  },

  async searchAuthorOrcid(name: string, maxResults = 10): Promise<SearchResponse> {
    const response = await api.get("/search/author/orcid", {
      params: { name, max_results: maxResults }
    });
    return response.data;
  },

  async searchByProfileLink(profileUrl: string, platform?: string): Promise<SearchResponse> {
    const params: any = { profile_url: profileUrl };
    if (platform) params.platform = platform;
    
    const response = await api.get("/search/author/profile", { params });
    return response.data;
  },

  // ========== BUSCA POR TEMA ==========
  
  async searchTopicScholar(topic: string, maxResults = 20, saveExcel = false): Promise<SearchResponse> {
    const response = await api.get("/search/topic/scholar", {
      params: { topic, max_results: maxResults, save_excel: saveExcel }
    });
    return response.data;
  },

  async searchTopicLattes(topic: string, maxResults = 20): Promise<SearchResponse> {
    const response = await api.get("/search/topic/lattes", {
      params: { topic, max_results: maxResults }
    });
    return response.data;
  },

  async searchTopicOrcid(topic: string, maxResults = 20): Promise<SearchResponse> {
    const response = await api.get("/search/topic/orcid", {
      params: { topic, max_results: maxResults }
    });
    return response.data;
  },

  // ========== BUSCA COMPLETA ==========
  
  async comprehensiveSearch(
    query: string, 
    searchType: "author" | "topic" | "both" = "both",
    platforms: string = "all",
    maxResults = 10,
    saveCsv = false
  ): Promise<SearchResponse> {
    const response = await api.get("/search/comprehensive", {
      params: {
        query,
        search_type: searchType,
        platforms,
        max_results: maxResults,
        save_csv: saveCsv
      }
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
  }
};
      params: {
        author,
        save_csv: saveExcel,
      },
    });
    return response.data;
  },

  async searchCitations(
    query: string,
    maxResults = 5
  ): Promise<SearchResponse> {
    const response = await api.get("/search/citations", {
      params: {
        q: query,
        max_results: maxResults,
      },
    });
    return response.data;
  },
};

// ==================== LATTES ====================

export const lattesService = {
  async searchByName(
    name: string,
    maxResults = 10,
    saveExcel = false
  ): Promise<SearchResponse> {
    const response = await api.get("/academic/lattes", {
      params: {
        name,
        max_results: maxResults,
        include_publications: true,
        include_projects: true,
        save_csv: saveExcel,
      },
    });
    return response.data;
  },

  // Método adicional para compatibilidade com o frontend
  async searchProfiles(name: string, maxResults = 10): Promise<any[]> {
    const response = await this.searchByName(name, maxResults);
    return (response as any).profiles || [];
  },

  async getProfile(lattesId: string) {
    const response = await api.get(`/academic/lattes/profile/${lattesId}`);
    return response.data;
  },
};

// ==================== ORCID ====================

export const orcidService = {
  async searchByName(
    name: string,
    maxResults = 10,
    saveExcel = false
  ): Promise<SearchResponse> {
    const response = await api.get("/academic/orcid", {
      params: {
        name,
        max_results: maxResults,
        include_publications: true,
        save_csv: saveExcel,
      },
    });
    return response.data;
  },

  // Método adicional para compatibilidade com o frontend
  async searchProfiles(name: string, maxResults = 10): Promise<any[]> {
    const response = await this.searchByName(name, maxResults);
    return (response as any).profiles || [];
  },

  async getProfile(orcidId: string) {
    const response = await api.get(`/academic/orcid/profile/${orcidId}`);
    return response.data;
  },
};

// ==================== BUSCA COMPLETA ====================

export const comprehensiveService = {
  async search(
    researcherName: string,
    maxResults = 10,
    saveExcel = false
  ): Promise<SearchResponse> {
    const response = await api.get("/academic/comprehensive", {
      params: {
        researcher_name: researcherName,
        max_results: maxResults,
        save_csv: saveExcel,
      },
    });
    return response.data;
  },
};

// ==================== EXPORT ====================

export const exportService = {
  async exportToExcel(
    data: SearchResponse,
    filename?: string
  ): Promise<string> {
    const response = await api.post("/export/excel", {
      data,
      filename: filename || `research_export_${Date.now()}`,
    });
    return response.data.file_path;
  },

  // Métodos adicionais para compatibilidade com o frontend
  async exportCSV(data: any): Promise<void> {
    await api.post("/export/csv", data);
  },

  async exportExcel(data: any): Promise<void> {
    await api.post("/export/excel", data);
  },

  async downloadFile(filePath: string) {
    const response = await api.get(`/export/download/${filePath}`, {
      responseType: "blob",
    });
    return response.data;
  },
};

// ==================== HEALTH CHECK ====================

export const healthService = {
  async checkAPI(): Promise<{ status: string; api_key_valid: boolean }> {
    const response = await api.get("/health");
    return response.data;
  },

  async checkAcademic(): Promise<{
    status: string;
    services: Record<string, string>;
  }> {
    const response = await api.get("/academic/health");
    return response.data;
  },
};

export default api;
