"""
🚀 API REST PARA BUSCA ACADÊMICA (LATTES E ORCID)
==================================================
Endpoints específicos para pesquisa acadêmica brasileira e internacional
"""

import time
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List

from models.academic_models import (
    AcademicSearchRequest, AcademicSearchResponse,
    PlatformType, LattesSearchType, ORCIDSearchType,
    LattesProfile, ORCIDProfile, AcademicSummary
)
from services.academic_services import (
    LattesService, ORCIDService, AcademicResearchService
)

# Router para endpoints acadêmicos
academic_router = APIRouter(prefix="/academic", tags=["Academic Research"])

# Instâncias dos serviços
lattes_service = LattesService()
orcid_service = ORCIDService()
academic_service = AcademicResearchService()

@academic_router.get("/", response_model=dict)
async def academic_root():
    """Informações sobre os endpoints acadêmicos"""
    return {
        "message": "🎓 Academic Research API",
        "platforms": ["Lattes", "ORCID"],
        "endpoints": {
            "lattes": "/academic/lattes",
            "orcid": "/academic/orcid", 
            "comprehensive": "/academic/search",
            "health": "/academic/health"
        }
    }

@academic_router.get("/health", response_model=dict)
async def academic_health():
    """Health check dos serviços acadêmicos"""
    return {
        "status": "healthy",
        "services": {
            "lattes": "operational",
            "orcid": "operational"
        },
        "timestamp": time.time()
    }

@academic_router.post("/search", response_model=AcademicSearchResponse)
async def academic_search(request: AcademicSearchRequest):
    """
    Busca acadêmica unificada
    
    Plataformas disponíveis:
    - lattes: Plataforma Lattes (CNPq)
    - orcid: ORCID Internacional
    """
    start_time = time.time()
    
    try:
        if request.platform == PlatformType.LATTES:
            return await _search_lattes(request, start_time)
        elif request.platform == PlatformType.ORCID:
            return await _search_orcid(request, start_time)
        else:
            raise HTTPException(status_code=400, detail="Plataforma não suportada")
            
    except Exception as e:
        execution_time = time.time() - start_time
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "execution_time": execution_time,
                "platform": request.platform
            }
        )

@academic_router.get("/lattes", response_model=AcademicSearchResponse)
async def search_lattes(
    name: str = Query(..., description="Nome do pesquisador"),
    max_results: int = Query(10, ge=1, le=50, description="Máximo de resultados"),
    include_publications: bool = Query(True, description="Incluir publicações"),
    include_projects: bool = Query(True, description="Incluir projetos"),
    save_csv: bool = Query(False, description="Salvar em CSV")
):
    """Busca específica na Plataforma Lattes"""
    request = AcademicSearchRequest(
        query=name,
        platform=PlatformType.LATTES,
        search_type=LattesSearchType.NAME,
        max_results=max_results,
        include_publications=include_publications,
        include_projects=include_projects,
        save_csv=save_csv
    )
    return await academic_search(request)

@academic_router.get("/orcid", response_model=AcademicSearchResponse)
async def search_orcid(
    name: str = Query(..., description="Nome do pesquisador"),
    max_results: int = Query(10, ge=1, le=50, description="Máximo de resultados"),
    include_publications: bool = Query(True, description="Incluir publicações"),
    save_csv: bool = Query(False, description="Salvar em CSV")
):
    """Busca específica no ORCID"""
    request = AcademicSearchRequest(
        query=name,
        platform=PlatformType.ORCID,
        search_type=ORCIDSearchType.NAME,
        max_results=max_results,
        include_publications=include_publications,
        save_csv=save_csv
    )
    return await academic_search(request)

@academic_router.get("/comprehensive", response_model=AcademicSearchResponse)
async def comprehensive_search(
    researcher_name: str = Query(..., description="Nome do pesquisador"),
    max_results: int = Query(10, ge=1, le=50, description="Máximo de resultados por plataforma"),
    save_csv: bool = Query(False, description="Salvar em CSV")
):
    """Busca completa em todas as plataformas acadêmicas"""
    start_time = time.time()
    
    try:
        # Busca em todas as plataformas
        lattes_profiles, orcid_profiles, summary = academic_service.comprehensive_search(
            researcher_name, max_results
        )
        
        # Salva CSV se solicitado
        csv_file = None
        if save_csv and (lattes_profiles or orcid_profiles):
            csv_file = academic_service.save_to_csv(lattes_profiles, orcid_profiles, researcher_name)
        
        execution_time = time.time() - start_time
        total_results = len(lattes_profiles) + len(orcid_profiles)
        
        # Fontes de dados utilizadas
        data_sources = []
        if lattes_profiles:
            data_sources.append("Plataforma Lattes")
        if orcid_profiles:
            data_sources.append("ORCID")
        
        # Estatísticas agregadas
        total_publications = sum(p.total_publications for p in lattes_profiles)
        total_publications += sum(len(p.works) for p in orcid_profiles)
        
        total_projects = sum(p.total_projects for p in lattes_profiles)
        
        response = AcademicSearchResponse(
            success=True,
            message=f"Busca completa realizada. Encontrados {total_results} perfis.",
            platform=PlatformType.LATTES,  # Usando LATTES como padrão para busca completa
            search_type="comprehensive",
            query=researcher_name,
            total_results=total_results,
            execution_time=execution_time,
            lattes_profiles=lattes_profiles,
            orcid_profiles=orcid_profiles,
            total_publications=total_publications,
            total_projects=total_projects,
            csv_file=csv_file,
            data_sources=data_sources
        )
        
        return response
        
    except Exception as e:
        execution_time = time.time() - start_time
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "execution_time": execution_time
            }
        )

@academic_router.get("/lattes/profile/{lattes_id}")
async def get_lattes_profile(lattes_id: str):
    """Obtém perfil completo do Lattes por ID"""
    try:
        profile = lattes_service.get_full_profile(lattes_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Perfil Lattes não encontrado")
        
        return {
            "success": True,
            "profile": profile,
            "timestamp": time.time()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@academic_router.get("/orcid/profile/{orcid_id}")
async def get_orcid_profile(orcid_id: str):
    """Obtém perfil completo do ORCID por ID"""
    try:
        profile = orcid_service.get_full_profile(orcid_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Perfil ORCID não encontrado")
        
        return {
            "success": True,
            "profile": profile,
            "timestamp": time.time()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== FUNÇÕES AUXILIARES ====================

async def _search_lattes(request: AcademicSearchRequest, start_time: float) -> AcademicSearchResponse:
    """Executa busca no Lattes"""
    
    if request.search_type == LattesSearchType.NAME:
        profiles = lattes_service.search_by_name(request.query, request.max_results)
    else:
        # Implementar outros tipos de busca conforme necessário
        profiles = lattes_service.search_by_name(request.query, request.max_results)
    
    # Busca perfis completos se solicitado
    if request.include_publications or request.include_projects:
        complete_profiles = []
        for profile in profiles:
            if profile.lattes_id:
                full_profile = lattes_service.get_full_profile(profile.lattes_id)
                if full_profile:
                    complete_profiles.append(full_profile)
                else:
                    complete_profiles.append(profile)
            else:
                complete_profiles.append(profile)
            
            # Rate limiting
            time.sleep(0.5)
        
        profiles = complete_profiles
    
    # Salva CSV se solicitado
    csv_file = None
    if request.save_csv and profiles:
        csv_file = academic_service.save_to_csv(profiles, [], request.query)
    
    execution_time = time.time() - start_time
    
    # Estatísticas
    total_publications = sum(p.total_publications for p in profiles)
    total_projects = sum(p.total_projects for p in profiles)
    
    return AcademicSearchResponse(
        success=True,
        message=f"Busca no Lattes concluída. {len(profiles)} perfis encontrados.",
        platform=PlatformType.LATTES,
        search_type=request.search_type,
        query=request.query,
        total_results=len(profiles),
        execution_time=execution_time,
        lattes_profiles=profiles,
        total_publications=total_publications,
        total_projects=total_projects,
        csv_file=csv_file,
        data_sources=["Plataforma Lattes"]
    )

async def _search_orcid(request: AcademicSearchRequest, start_time: float) -> AcademicSearchResponse:
    """Executa busca no ORCID"""
    
    if request.search_type == ORCIDSearchType.NAME:
        profiles = orcid_service.search_by_name(request.query, request.max_results)
    else:
        # Implementar outros tipos de busca conforme necessário
        profiles = orcid_service.search_by_name(request.query, request.max_results)
    
    # Salva CSV se solicitado
    csv_file = None
    if request.save_csv and profiles:
        csv_file = academic_service.save_to_csv([], profiles, request.query)
    
    execution_time = time.time() - start_time
    
    # Estatísticas
    total_publications = sum(len(p.works) for p in profiles)
    
    return AcademicSearchResponse(
        success=True,
        message=f"Busca no ORCID concluída. {len(profiles)} perfis encontrados.",
        platform=PlatformType.ORCID,
        search_type=request.search_type,
        query=request.query,
        total_results=len(profiles),
        execution_time=execution_time,
        orcid_profiles=profiles,
        total_publications=total_publications,
        total_projects=0,  # ORCID não tem projetos explícitos
        csv_file=csv_file,
        data_sources=["ORCID"]
    )

# ==================== FUNÇÕES ESPECÍFICAS PARA NOVA API ====================

async def search_lattes_profiles(name: str, max_results: int = 10):
    """Busca perfis no Lattes por nome"""
    try:
        profiles = lattes_service.search_by_name(name, max_results)
        return {
            "success": True,
            "message": f"Busca no Lattes concluída. {len(profiles)} perfis encontrados.",
            "platform": "lattes",
            "query": name,
            "total_results": len(profiles),
            "lattes_profiles": [profile.dict() for profile in profiles]
        }
    except Exception as e:
        raise Exception(f"Erro na busca no Lattes: {str(e)}")

async def search_orcid_profiles(name: str, max_results: int = 10):
    """Busca perfis no ORCID por nome"""
    try:
        profiles = orcid_service.search_by_name(name, max_results)
        return {
            "success": True,
            "message": f"Busca no ORCID concluída. {len(profiles)} perfis encontrados.",
            "platform": "orcid",
            "query": name,
            "total_results": len(profiles),
            "orcid_profiles": [profile.dict() for profile in profiles]
        }
    except Exception as e:
        raise Exception(f"Erro na busca no ORCID: {str(e)}")

async def search_lattes_by_topic(topic: str, max_results: int = 20):
    """Busca no Lattes por tema"""
    try:
        # Por enquanto, buscar pesquisadores que tenham o tema em suas áreas
        profiles = lattes_service.search_by_research_area(topic, max_results)
        return {
            "success": True,
            "message": f"Busca por tema '{topic}' no Lattes concluída.",
            "platform": "lattes",
            "query": topic,
            "total_results": len(profiles),
            "profiles": [profile.dict() for profile in profiles]
        }
    except Exception as e:
        raise Exception(f"Erro na busca por tema no Lattes: {str(e)}")

async def search_orcid_by_topic(topic: str, max_results: int = 20):
    """Busca no ORCID por tema"""
    try:
        # Buscar trabalhos com o tema
        works = orcid_service.search_works_by_keyword(topic, max_results)
        return {
            "success": True,
            "message": f"Busca por tema '{topic}' no ORCID concluída.",
            "platform": "orcid",
            "query": topic,
            "total_results": len(works),
            "works": [work.dict() for work in works] if works else []
        }
    except Exception as e:
        raise Exception(f"Erro na busca por tema no ORCID: {str(e)}")

async def get_lattes_profile_by_url(profile_url: str):
    """Busca perfil do Lattes por URL"""
    try:
        # Extrair ID do Lattes da URL
        import re
        lattes_id_match = re.search(r'lattes\.cnpq\.br\/(\d+)', profile_url)
        if not lattes_id_match:
            raise ValueError("URL do Lattes inválida")
        
        lattes_id = lattes_id_match.group(1)
        profile = lattes_service.get_profile_by_id(lattes_id)
        
        return {
            "success": True,
            "message": "Perfil do Lattes obtido com sucesso",
            "platform": "lattes",
            "profile_url": profile_url,
            "lattes_profile": profile.dict() if profile else None
        }
    except Exception as e:
        raise Exception(f"Erro ao buscar perfil do Lattes: {str(e)}")

async def get_orcid_profile_by_url(profile_url: str):
    """Busca perfil do ORCID por URL"""
    try:
        # Extrair ORCID ID da URL
        import re
        orcid_id_match = re.search(r'orcid\.org\/(\d{4}-\d{4}-\d{4}-\d{3}[\dX])', profile_url)
        if not orcid_id_match:
            raise ValueError("URL do ORCID inválida")
        
        orcid_id = orcid_id_match.group(1)
        profile = orcid_service.get_profile_by_id(orcid_id)
        
        return {
            "success": True,
            "message": "Perfil do ORCID obtido com sucesso",
            "platform": "orcid",
            "profile_url": profile_url,
            "orcid_profile": profile.dict() if profile else None
        }
    except Exception as e:
        raise Exception(f"Erro ao buscar perfil do ORCID: {str(e)}")

async def comprehensive_academic_search(
    query: str,
    search_type: str = "both",
    platforms: List[str] = ["scholar", "lattes", "orcid"],
    max_results: int = 10,
    save_csv: bool = False
):
    """Busca completa em múltiplas plataformas"""
    start_time = time.time()
    results = {
        "success": True,
        "message": f"Busca completa por '{query}' realizada",
        "query": query,
        "search_type": search_type,
        "platforms": platforms,
        "total_results": 0,
        "results_by_platform": {}
    }
    
    # Buscar em cada plataforma
    for platform in platforms:
        try:
            if platform == "lattes":
                if search_type in ["author", "both"]:
                    platform_results = await search_lattes_profiles(query, max_results)
                else:
                    platform_results = await search_lattes_by_topic(query, max_results)
                results["results_by_platform"]["lattes"] = platform_results
                
            elif platform == "orcid":
                if search_type in ["author", "both"]:
                    platform_results = await search_orcid_profiles(query, max_results)
                else:
                    platform_results = await search_orcid_by_topic(query, max_results)
                results["results_by_platform"]["orcid"] = platform_results
                
        except Exception as e:
            results["results_by_platform"][platform] = {
                "error": f"Erro na busca: {str(e)}"
            }
    
    # Calcular estatísticas
    total_results = 0
    for platform_results in results["results_by_platform"].values():
        if isinstance(platform_results, dict) and "error" not in platform_results:
            total_results += platform_results.get("total_results", 0)
    
    results["total_results"] = total_results
    results["execution_time"] = round(time.time() - start_time, 2)
    
    return results

async def test_lattes_connection():
    """Teste de conectividade com Lattes"""
    try:
        # Teste simples
        await search_lattes_profiles("teste", 1)
        return True
    except:
        return False

async def test_orcid_connection():
    """Teste de conectividade com ORCID"""
    try:
        # Teste simples
        await search_orcid_profiles("test", 1)
        return True
    except:
        return False