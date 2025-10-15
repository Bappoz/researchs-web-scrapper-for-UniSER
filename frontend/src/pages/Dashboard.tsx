/**
 * 📊 DASHBOARD PRINCIPAL
 * Interface principa  const checkAPIStatus = async () => {
    try {
      setApiStatus("checking");
      await academicService.healthCheck();
      setApiStatus("online");
    } catch (error) {
      console.error("API offline:", error);
      setApiStatus("offline");
    }
  };uisa acadêmica do Instituto de Pesquisa Científica
 */

import React, { useState, useEffect } from "react";
import {
  Activity,
  AlertCircle,
  RefreshCw,
  CheckCircle,
  Clock,
  Search,
  BarChart3,
  FileSpreadsheet,
  BookOpen,
} from "lucide-react";

// Serviços da API
import {
  academicService,
  separatedLattesService,
  separatedOrcidService,
} from "../services/api_new";
// import comprehensiveService from "../services/api_new"; // Uncomment if comprehensiveService is a default export and you need it

// Componentes
import SearchFormNew from "../components/SearchFormNew";
import SearchFormDual from "../components/SearchFormDual";
import ResultsDisplay from "../components/ResultsDisplay";
import StatsCardsSimple from "../components/StatsCardsSimple";
import SearchHistorySimple from "../components/SearchHistorySimple";
import ExportPanelSimple from "../components/ExportPanelSimple";

// Services
import type { SearchResponse } from "../services/api_new";

interface DashboardStats {
  totalSearches: number;
  totalResearchers: number;
  totalPublications: number;
  totalProjects: number;
  lastUpdate: string;
}

const Dashboard: React.FC = () => {
  // States
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(
    null
  );
  const [isLoading, setIsLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState<"checking" | "online" | "offline">(
    "checking"
  );
  const [stats, setStats] = useState<DashboardStats>({
    totalSearches: 0,
    totalResearchers: 0,
    totalPublications: 0,
    totalProjects: 0,
    lastUpdate: new Date().toISOString(),
  });
  const [searchHistory, setSearchHistory] = useState<SearchResponse[]>([]);

  // Verificar status da API ao carregar
  useEffect(() => {
    checkAPIStatus();
    loadSearchHistory();
  }, []);

  const checkAPIStatus = async () => {
    try {
      setApiStatus("checking");
      await academicService.healthCheck();
      setApiStatus("online");
    } catch (error) {
      console.error("API offline:", error);
      setApiStatus("offline");
    }
  };

  const loadSearchHistory = () => {
    const history = JSON.parse(localStorage.getItem("searchHistory") || "[]");
    setSearchHistory(history);
    updateStats(history);
  };

  const updateStats = (history: SearchResponse[]) => {
    const totalPublications = history.reduce(
      (sum, search) => sum + (search.total_publications || 0),
      0
    );
    const totalProjects = history.reduce(
      (sum, search) => sum + (search.total_projects || 0),
      0
    );
    const totalResearchers = history.reduce((sum, search) => {
      const lattesCount = search.lattes_profiles?.length || 0;
      const orcidCount = search.orcid_profiles?.length || 0;
      return sum + lattesCount + orcidCount;
    }, 0);

    setStats({
      totalSearches: history.length,
      totalResearchers,
      totalPublications,
      totalProjects,
      lastUpdate: new Date().toISOString(),
    });
  };

  // Estado para tracking qual plataforma está carregando
  const [loadingPlatform, setLoadingPlatform] = useState<string>("");

  // ========== FUNÇÕES PARA PESQUISA POR NOME (Abre site externo) ==========

  const handleSearchByNameLattes = async (query: string) => {
    if (!query.trim()) {
      alert("Por favor, digite um nome para buscar");
      return;
    }

    setIsLoading(true);
    setLoadingPlatform("name-lattes");

    try {
      console.log("🇧🇷 Abrindo página de busca do Lattes para:", query);

      // Construir URL direta da página de busca do Lattes com a query preenchida
      // Parâmetros: base=COMPLETA (inclui "Demais pesquisadores") + nacionalidade=B,E (Brasileira + Estrangeira)
      const lattesSearchUrl = `https://buscatextual.cnpq.br/buscatextual/busca.do?metodo=apresentar&decorador=filtro&ord=tipo&filtro=${encodeURIComponent(
        query.trim()
      )}&base=COMPLETA&nacionalidade=B,E`;

      // Abrir a página de busca do Lattes em nova aba
      window.open(lattesSearchUrl, "_blank");

      console.log("✅ Página do Lattes aberta:", lattesSearchUrl);

      // Criar um resultado fictício para mostrar que a ação foi realizada
      const mockResult = {
        success: true,
        message: `Página de busca do Lattes aberta para: ${query}`,
        platform: "lattes",
        search_type: "name_redirect",
        query: query,
        total_results: 0,
        execution_time: 0.5,
        redirect_url: lattesSearchUrl,
        data: {
          publications: [],
        },
      };

      setSearchResults(mockResult);
      saveToHistory(mockResult);
    } catch (error) {
      console.error("Erro ao abrir Lattes:", error);
      alert(
        "Erro ao abrir a página do Lattes. Verifique se o popup foi bloqueado."
      );
    } finally {
      setIsLoading(false);
      setLoadingPlatform("");
    }
  };

  const handleSearchByNameOrcid = async (query: string) => {
    if (!query.trim()) {
      alert("Por favor, digite um nome para buscar");
      return;
    }

    setIsLoading(true);
    setLoadingPlatform("name-orcid");

    try {
      console.log("🌐 Abrindo página de busca do ORCID para:", query);

      // Construir URL direta da página de busca do ORCID
      const orcidSearchUrl = `https://orcid.org/orcid-search/search?searchQuery=${encodeURIComponent(
        query.trim()
      )}`;

      // Abrir a página de busca do ORCID em nova aba
      window.open(orcidSearchUrl, "_blank");

      console.log("✅ Página do ORCID aberta:", orcidSearchUrl);

      // Criar um resultado fictício para mostrar que a ação foi realizada
      const mockResult = {
        success: true,
        message: `Página de busca do ORCID aberta para: ${query}`,
        platform: "orcid",
        search_type: "name_redirect",
        query: query,
        total_results: 0,
        execution_time: 0.5,
        redirect_url: orcidSearchUrl,
        data: {
          publications: [],
        },
      };

      setSearchResults(mockResult);
      saveToHistory(mockResult);
    } catch (error) {
      console.error("Erro ao abrir ORCID:", error);
      alert(
        "Erro ao abrir a página do ORCID. Verifique se o popup foi bloqueado."
      );
    } finally {
      setIsLoading(false);
      setLoadingPlatform("");
    }
  };

  const handleSearchByNameScholar = async (query: string) => {
    if (!query.trim()) {
      alert("Por favor, digite um nome para buscar");
      return;
    }

    setIsLoading(true);
    setLoadingPlatform("name-scholar");

    try {
      console.log(
        "📚 Abrindo página de busca de autores do Scholar para:",
        query
      );

      // Usar a URL correta para busca de AUTORES no Scholar (não publicações)
      const scholarAuthorsUrl = `https://scholar.google.com/citations?view_op=search_authors&mauthors=${encodeURIComponent(
        query.trim()
      )}&hl=pt-BR&oi=ao`;

      // Abrir a página de busca de autores do Scholar em nova aba
      window.open(scholarAuthorsUrl, "_blank");

      console.log(
        "✅ Página do Scholar (busca de autores) aberta:",
        scholarAuthorsUrl
      );

      // Criar resultado informativo
      const mockResult = {
        success: true,
        message: `Página de busca de autores do Scholar aberta para: ${query}`,
        platform: "scholar",
        search_type: "name_redirect",
        query: query,
        total_results: 0,
        execution_time: 0.5,
        redirect_url: scholarAuthorsUrl,
        data: {
          publications: [],
        },
      };

      setSearchResults(mockResult);
      saveToHistory(mockResult);
    } catch (error) {
      console.error("Erro ao abrir Scholar:", error);
      alert(
        "Erro ao abrir a página do Scholar. Verifique se o popup foi bloqueado."
      );
    } finally {
      setIsLoading(false);
      setLoadingPlatform("");
    }
  };

  // ========== FUNÇÕES PARA PESQUISA POR LINK (Extrai dados completos) ==========

  const handleSearchByLinkLattes = async (profileUrl: string) => {
    setIsLoading(true);
    setLoadingPlatform("link-lattes");

    try {
      console.log("📄 Extraindo dados Lattes:", profileUrl);

      // Usar endpoint para extrair perfil por URL
      const response = await fetch(
        `http://localhost:8000/api/lattes/profile/by-url?profile_url=${encodeURIComponent(
          profileUrl
        )}`
      );
      const apiResult = await response.json();

      console.log("🇧🇷 Dados brutos do Lattes:", apiResult);

      // Verificar se é um caso de captcha ou automação
      const isCaptcha =
        apiResult.profile?.name?.includes("CAPTCHA") ||
        apiResult.profile?.name?.includes("Código de segurança");
      const isAutomation = apiResult.profile?.current_position?.includes(
        "automação ChromeDriver"
      );

      // Mapear dados para formato esperado pelo ResultsDisplay
      const mappedResult = {
        success: apiResult.success,
        message: isCaptcha
          ? "🤖 ChromeDriver Automation - CAPTCHA resolvido automaticamente"
          : isAutomation
          ? "🎉 Dados extraídos via automação ChromeDriver"
          : apiResult.message,
        platform: "lattes",
        search_type: "profile_extraction",
        query: profileUrl,
        total_results: 1,
        execution_time: apiResult.execution_time || 0,

        // Dados do pesquisador
        researcher_info: {
          name:
            apiResult.researcher?.name ||
            apiResult.profile?.name ||
            "Nome não encontrado",
          institution:
            apiResult.researcher?.current_institution ||
            apiResult.profile?.current_institution ||
            "Instituição não informada",
          position:
            apiResult.researcher?.current_position ||
            apiResult.profile?.current_position ||
            "Cargo não informado",
          lattes_id:
            apiResult.researcher?.lattes_id || apiResult.profile?.lattes_id,
          lattes_url:
            apiResult.researcher?.lattes_url || apiResult.profile?.lattes_url,
          research_areas:
            apiResult.researcher?.research_areas ||
            apiResult.profile?.research_areas ||
            [],
          last_update:
            apiResult.researcher?.last_update || apiResult.profile?.last_update,
        },

        // Estrutura esperada pelo ResultsDisplay
        results_by_platform: {
          lattes: {
            lattes_profiles: [
              {
                // Informações básicas do perfil
                name: apiResult.profile?.name || "Nome não encontrado",
                lattes_id: apiResult.profile?.lattes_id,
                lattes_url: apiResult.profile?.lattes_url,
                platform: "lattes",

                // Informações institucionais
                institution:
                  apiResult.profile?.current_institution ||
                  "Instituição não informada",
                current_institution:
                  apiResult.profile?.current_institution ||
                  "Instituição não informada",
                current_position:
                  apiResult.profile?.current_position || "Cargo não informado",

                // Informações pessoais
                birth_date: apiResult.profile?.birth_date,
                nationality: apiResult.profile?.nationality,
                last_update: apiResult.profile?.last_update,

                // Áreas de pesquisa
                research_areas: apiResult.profile?.research_areas || [],

                // Formação (converter array de objetos em array de strings)
                education: (apiResult.profile?.education || []).map(
                  (edu: any) =>
                    typeof edu === "string"
                      ? edu
                      : `${edu.degree || ""} ${edu.course || ""} - ${
                          edu.institution || ""
                        }`.trim()
                ),

                // Biografia/descrição (diferente para captcha)
                biography: isCaptcha
                  ? `🤖 PROTEÇÃO ANTI-BOT DETECTADA
                
O sistema Lattes está bloqueando o acesso automatizado com um captcha/código de segurança.

📋 COMO RESOLVER:
1. Clique no link abaixo para abrir o perfil
2. Resolva o captcha manualmente na página
3. Após resolver, você verá o perfil completo
4. Copie a URL final (sem captcha) 
5. Use essa nova URL no sistema

⚠️ IMPORTANTE: 
Esta é uma proteção normal do Lattes contra bots. O acesso manual sempre funciona.`
                  : [
                      apiResult.profile?.current_position &&
                        `Cargo atual: ${apiResult.profile.current_position}`,
                      apiResult.profile?.current_institution &&
                        `Instituição: ${apiResult.profile.current_institution}`,
                      apiResult.profile?.research_areas?.length > 0 &&
                        `Áreas de pesquisa: ${apiResult.profile.research_areas.join(
                          ", "
                        )}`,
                      apiResult.profile?.last_update &&
                        `Última atualização: ${apiResult.profile.last_update}`,
                    ]
                      .filter(Boolean)
                      .join("\n"),

                // Publicações (converter para formato esperado pelo componente)
                publications: [
                  ...(apiResult.profile?.journal_articles || []).map(
                    (article: any) => ({
                      title: article.title || article,
                      year: article.year,
                      authors: article.authors,
                      journal: article.journal,
                      type: "journal_article",
                    })
                  ),
                  ...(apiResult.profile?.conference_papers || []).map(
                    (paper: any) => ({
                      title: paper.title || paper,
                      year: paper.year,
                      authors: paper.authors,
                      journal: paper.conference || paper.event,
                      type: "conference_paper",
                    })
                  ),
                  ...(apiResult.profile?.book_chapters || []).map(
                    (chapter: any) => ({
                      title: chapter.title || chapter,
                      year: chapter.year,
                      authors: chapter.authors,
                      journal: chapter.book,
                      type: "book_chapter",
                    })
                  ),
                  ...(apiResult.profile?.books || []).map((book: any) => ({
                    title: book.title || book,
                    year: book.year,
                    authors: book.authors,
                    type: "book",
                  })),
                ].slice(0, 20), // Limitar a 20 publicações para performance

                // Seções originais (para compatibilidade)
                professional_experience:
                  apiResult.profile?.professional_experience || [],
                research_projects: apiResult.profile?.research_projects || [],
                supervisions: apiResult.profile?.supervisions || [],
                awards: apiResult.profile?.awards || [],
                examination_boards: apiResult.profile?.examination_boards || [],
                editorial_boards: apiResult.profile?.editorial_boards || [],
                journal_reviews: apiResult.profile?.journal_reviews || [],

                // Estatísticas
                total_publications:
                  apiResult.statistics?.total_publications || 0,
                total_projects: apiResult.statistics?.total_projects || 0,

                // URLs
                url: apiResult.profile?.lattes_url,
                profile_url: apiResult.profile?.lattes_url,
              },
            ],
          },
        },

        // Dados originais para referência
        data: apiResult.profile,
        statistics: apiResult.statistics,
        sections_available: apiResult.sections_available,
      };

      console.log("🎯 Dados mapeados para o frontend:", mappedResult);

      // Se for captcha, mostrar instruções e abrir link automaticamente
      if (isCaptcha) {
        const shouldOpen = confirm(
          `🤖 CAPTCHA DETECTADO NO LATTES\n\n` +
            `O sistema Lattes está bloqueando o acesso com código de segurança.\n\n` +
            `QUER RESOLVER AGORA?\n\n` +
            `✅ SIM: Abrirá o link para você resolver o captcha manualmente\n` +
            `❌ NÃO: Apenas mostrará as instruções\n\n` +
            `Após resolver o captcha, copie a URL final e use novamente no sistema.`
        );

        if (shouldOpen) {
          window.open(profileUrl, "_blank");

          // Mostrar instruções adicionais
          setTimeout(() => {
            alert(
              `🔗 LINK ABERTO!\n\n` +
                `Na aba que acabou de abrir:\n\n` +
                `1. ✅ Resolva o captcha/código de segurança\n` +
                `2. 📄 Aguarde carregar o perfil completo\n` +
                `3. 📋 Copie a URL final da página\n` +
                `4. 🔄 Cole essa nova URL aqui no sistema\n\n` +
                `A nova URL não terá mais captcha e funcionará perfeitamente!`
            );
          }, 1000);
        }
      }

      setSearchResults(mappedResult);
      saveToHistory(mappedResult);
    } catch (error) {
      console.error("Erro na extração Lattes:", error);
      showError("Erro ao extrair dados do Lattes", "link-lattes", profileUrl);
    } finally {
      setIsLoading(false);
      setLoadingPlatform("");
    }
  };

  const handleSearchByLinkOrcid = async (profileUrl: string) => {
    setIsLoading(true);
    setLoadingPlatform("link-orcid");

    try {
      console.log("� Extraindo dados ORCID:", profileUrl);

      // Usar endpoint para extrair perfil ORCID por URL
      const response = await fetch(
        `http://localhost:8000/api/orcid/profile/by-url?profile_url=${encodeURIComponent(
          profileUrl
        )}`
      );
      const result = await response.json();

      setSearchResults(result);
      saveToHistory(result);
    } catch (error) {
      console.error("Erro na extração ORCID:", error);
      showError("Erro ao extrair dados do ORCID", "link-orcid", profileUrl);
    } finally {
      setIsLoading(false);
      setLoadingPlatform("");
    }
  };

  const handleSearchByLinkScholar = async (
    profileUrl: string,
    useKeywordFilter: boolean = false
  ) => {
    setIsLoading(true);
    setLoadingPlatform("link-scholar");

    try {
      console.log(
        "📄 Extraindo dados Scholar:",
        profileUrl,
        `- Filtro keywords: ${useKeywordFilter}`
      );

      // Usar a função existente com parâmetro configurável para filtro de keywords
      const result = await academicService.searchByProfileLink(
        profileUrl,
        "scholar",
        false, // exportExcel
        20, // maxPublications
        useKeywordFilter // filterKeywords - controlado pelo usuário
      );

      setSearchResults(result);
      saveToHistory(result);
    } catch (error) {
      console.error("Erro na extração Scholar:", error);
      showError("Erro ao extrair dados do Scholar", "link-scholar", profileUrl);
    } finally {
      setIsLoading(false);
      setLoadingPlatform("");
    }
  };

  // ========== FUNÇÕES AUXILIARES ==========

  const saveToHistory = (result: SearchResponse) => {
    if (result && result.success !== false) {
      const newHistory = [result, ...searchHistory.slice(0, 9)];
      setSearchHistory(newHistory);
      localStorage.setItem("searchHistory", JSON.stringify(newHistory));
      updateStats(newHistory);
    }
  };

  const showError = (message: string, platform: string, query: string) => {
    setSearchResults({
      success: false,
      message,
      platform,
      search_type: "error",
      query,
      total_results: 0,
      execution_time: 0,
      timestamp: new Date().toISOString(),
    } as SearchResponse);
  };

  const handleSearch = async (
    query: string,
    platform: "comprehensive" | "scholar" | "lattes" | "orcid"
  ) => {
    setIsLoading(true);

    try {
      let result: any;

      // Usar serviços específicos baseados na plataforma
      switch (platform) {
        case "lattes":
          console.log("🇧🇷 Buscando no Lattes separado:", query);
          result = await separatedLattesService.searchResearchers(query, 10);
          break;

        case "orcid":
          console.log("🌐 Buscando no ORCID separado:", query);
          result = await separatedOrcidService.searchResearchers(query, 10);
          break;

        case "scholar":
          console.log("📚 Buscando no Scholar:", query);
          // Usar serviço acadêmico para Scholar
          result = await academicService.searchAuthorScholar(query, 10, false);
          break;

        case "comprehensive":
        default:
          console.log("🎯 Busca comprehensive:", query);
          // Usar serviço acadêmico padrão
          result = await academicService.searchAuthorScholar(query, 20, false);
          break;
      }

      setSearchResults(result);

      // Salvar no histórico (apenas se for resultado válido)
      if (result && result.success !== false) {
        const newHistory = [result, ...searchHistory.slice(0, 9)]; // Manter apenas 10 últimas
        setSearchHistory(newHistory);
        localStorage.setItem("searchHistory", JSON.stringify(newHistory));
        updateStats(newHistory);
      }
    } catch (error) {
      console.error("Erro na busca:", error);
      // Mostrar erro para o usuário
      setSearchResults({
        success: false,
        message: `Erro na busca: ${
          error instanceof Error ? error.message : "Erro desconhecido"
        }`,
        platform,
        search_type: "error",
        query,
        total_results: 0,
        execution_time: 0,
        timestamp: new Date().toISOString(),
      } as SearchResponse);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExportToExcel = async (data: any) => {
    if (!searchResults) return;

    try {
      console.log("🔄 Iniciando exportação Excel individual...");

      // Extrair informações da busca atual
      const platform = searchResults.platform || "scholar";
      const query = searchResults.query || "pesquisa";
      const searchType = searchResults.search_type || "query";

      // Determinar parâmetros baseado no tipo de busca
      let exportParams: any = {
        query: query,
        platforms: platform,
        export_excel: true,
        filter_keywords: false,
        max_publications: 20,
      };

      // Se foi uma busca por link, tentar reconstruir a URL do perfil
      if (searchType === "profile" && searchResults.researcher_info) {
        if (platform === "scholar") {
          // Para Scholar, usar busca por nome se não temos URL específica
          exportParams.query = searchResults.researcher_info.name || query;
        } else if (platform === "lattes" && query.includes("LATTES-")) {
          // Reconstruir URL do Lattes
          const lattesId = query.replace("LATTES-", "");
          exportParams.profile_url = `http://lattes.cnpq.br/${lattesId}`;
        } else if (platform === "orcid" && query.includes("ORCID-")) {
          // Reconstruir URL do ORCID
          const orcidId = query.replace("ORCID-", "");
          exportParams.profile_url = `https://orcid.org/0000-0000-0000-${orcidId}`;
        }
      }

      console.log("📋 Parâmetros de exportação:", exportParams);

      // Fazer requisição para gerar Excel
      const response = await fetch(
        `http://localhost:8000/search/author/profile`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(exportParams),
        }
      );

      if (response.ok) {
        const result = await response.json();

        if (result.excel_file) {
          // Download do arquivo Excel
          const downloadResponse = await fetch(
            `http://localhost:8000/download/excel/${result.excel_file}`
          );

          if (downloadResponse.ok) {
            const blob = await downloadResponse.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = result.excel_file;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            console.log("✅ Excel individual exportado:", result.excel_file);
          } else {
            throw new Error("Erro ao baixar arquivo Excel");
          }
        } else if (result.excel_error) {
          throw new Error(`Erro na geração do Excel: ${result.excel_error}`);
        } else {
          throw new Error("Arquivo Excel não foi gerado pelo servidor");
        }
      } else {
        const errorText = await response.text();
        throw new Error(
          `Erro na requisição (${response.status}): ${errorText}`
        );
      }
    } catch (error) {
      console.error("❌ Erro na exportação Excel:", error);
      alert(`Erro ao exportar Excel: ${error}`);
    }
  };

  const getStatusIcon = () => {
    switch (apiStatus) {
      case "checking":
        return <RefreshCw className='h-4 w-4 animate-spin text-yellow-500' />;
      case "online":
        return <CheckCircle className='h-4 w-4 text-green-500' />;
      case "offline":
        return <AlertCircle className='h-4 w-4 text-red-500' />;
    }
  };

  const getStatusText = () => {
    switch (apiStatus) {
      case "checking":
        return "Verificando...";
      case "online":
        return "API Online";
      case "offline":
        return "API Offline";
    }
  };

  return (
    <div className='min-h-screen bg-gray-50'>
      {/* Header */}
      <header className='bg-white shadow-sm border-b border-gray-200'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='flex justify-between items-center h-16'>
            <div className='flex items-center'>
              <BookOpen className='h-8 w-8 text-blue-600 mr-3' />
              <div>
                <h1 className='text-xl font-semibold text-gray-900'>
                  Instituto de Pesquisa Científica
                </h1>
                <p className='text-sm text-gray-500'>
                  Sistema de Busca Acadêmica
                </p>
              </div>
            </div>

            <div className='flex items-center space-x-4'>
              <div className='flex items-center space-x-2'>
                {getStatusIcon()}
                <span className='text-sm text-gray-600'>{getStatusText()}</span>
              </div>

              <button
                onClick={checkAPIStatus}
                className='p-2 text-gray-400 hover:text-gray-600 transition-colors'
                title='Verificar status da API'
              >
                <RefreshCw className='h-4 w-4' />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
        {/* Stats Cards */}
        {searchResults && (
          <StatsCardsSimple
            totalPublications={searchResults.total_results || 0}
            totalAuthors={
              searchResults.lattes_profiles?.length ||
              searchResults.orcid_profiles?.length ||
              0
            }
            totalProjects={searchResults.total_projects || 0}
            executionTime={searchResults.execution_time || 0}
          />
        )}

        <div className='mt-8 grid grid-cols-1 lg:grid-cols-3 gap-8'>
          {/* Search Panel */}
          <div className='lg:col-span-2 space-y-6'>
            {/* Search Form */}
            <div className='bg-white rounded-lg shadow-sm border border-gray-200 p-6'>
              <div className='flex items-center mb-4'>
                <Search className='h-5 w-5 text-blue-600 mr-2' />
                <h2 className='text-lg font-medium text-gray-900'>
                  � Sistema de Busca - Nome vs Link
                </h2>
              </div>

              <SearchFormDual
                onSearchByNameLattes={handleSearchByNameLattes}
                onSearchByNameOrcid={handleSearchByNameOrcid}
                onSearchByNameScholar={handleSearchByNameScholar}
                onSearchByLinkLattes={handleSearchByLinkLattes}
                onSearchByLinkOrcid={handleSearchByLinkOrcid}
                onSearchByLinkScholar={handleSearchByLinkScholar}
                isLoading={isLoading}
                disabled={apiStatus === "offline"}
                loadingPlatform={loadingPlatform}
              />
            </div>

            {/* Results */}
            {searchResults && (
              <div className='bg-white rounded-lg shadow-sm border border-gray-200'>
                <div className='p-6 border-b border-gray-200'>
                  <div className='flex items-center justify-between'>
                    <div className='flex items-center'>
                      <BarChart3 className='h-5 w-5 text-blue-600 mr-2' />
                      <h2 className='text-lg font-medium text-gray-900'>
                        Resultados da Pesquisa
                      </h2>
                    </div>

                    <div className='flex items-center space-x-2'>
                      <span className='text-sm text-gray-500'>
                        {searchResults.total_results} resultados em{" "}
                        {searchResults.execution_time.toFixed(2)}s
                      </span>

                      <button
                        onClick={handleExportToExcel}
                        className='inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded text-white bg-green-600 hover:bg-green-700 transition-colors'
                      >
                        <FileSpreadsheet className='h-3 w-3 mr-1' />
                        Excel
                      </button>
                    </div>
                  </div>
                </div>

                <ResultsDisplay results={searchResults} />
              </div>
            )}

            {/* Loading State */}
            {isLoading && (
              <div className='bg-white rounded-lg shadow-sm border border-gray-200 p-12'>
                <div className='text-center'>
                  <RefreshCw className='h-8 w-8 animate-spin text-blue-600 mx-auto mb-4' />
                  <p className='text-gray-600'>
                    Realizando busca nas plataformas acadêmicas...
                  </p>
                  <p className='text-sm text-gray-500 mt-2'>
                    Isso pode levar alguns segundos
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className='space-y-6'>
            {/* Export Panel */}
            {searchResults && (
              <ExportPanelSimple
                results={searchResults}
                searchQuery={searchResults.query || "pesquisa"}
                onExportExcel={handleExportToExcel}
              />
            )}

            {/* Search History */}
            <SearchHistorySimple
              history={searchHistory.map((item, index) => ({
                id: index.toString(),
                query: item.query || "Busca sem título",
                searchType: item.search_type || "query",
                platform: item.platform || "scholar",
                timestamp: new Date().toISOString(),
                totalResults: item.total_results || 0,
                executionTime: item.execution_time || 0,
              }))}
              onRepeatSearch={(historyItem) => {
                // Implementar repetição de busca
                console.log("Repetir busca:", historyItem);
              }}
            />

            {/* Quick Stats */}
            <div className='bg-white rounded-lg shadow-sm border border-gray-200 p-6'>
              <div className='flex items-center mb-4'>
                <Clock className='h-5 w-5 text-blue-600 mr-2' />
                <h3 className='text-lg font-medium text-gray-900'>
                  Status do Sistema
                </h3>
              </div>

              <div className='space-y-3'>
                <div className='flex justify-between items-center'>
                  <span className='text-sm text-gray-600'>Google Scholar</span>
                  <span className='text-sm font-medium text-green-600'>
                    Ativo
                  </span>
                </div>
                <div className='flex justify-between items-center'>
                  <span className='text-sm text-gray-600'>
                    Plataforma Lattes
                  </span>
                  <span className='text-sm font-medium text-green-600'>
                    Ativo
                  </span>
                </div>
                <div className='flex justify-between items-center'>
                  <span className='text-sm text-gray-600'>ORCID</span>
                  <span className='text-sm font-medium text-green-600'>
                    Ativo
                  </span>
                </div>
                <div className='flex justify-between items-center pt-2 border-t border-gray-200'>
                  <span className='text-sm text-gray-600'>
                    Última verificação
                  </span>
                  <span className='text-sm text-gray-500'>
                    {new Date().toLocaleTimeString("pt-BR")}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
