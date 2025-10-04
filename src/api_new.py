"""
🚀 API REST ACADEMIC RESEARCH - VERSÃO REORGANIZADA
=====================================================
API completa para pesquisa acadêmica com endpoints organizados
"""

import time
import json
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
from typing import Optional, List
import pandas as pd

from .models import (
    SearchRequest, SearchResponse, ErrorResponse, HealthResponse,
    SearchType, PublicationData, AuthorProfile, AuthorSummary
)
from .services import GoogleScholarService
from .services.academic_services import LattesService, ORCIDService

# Configuração da aplicação
app = FastAPI(
    title="🎓 Academic Research API - Reorganizada",
    description="""
    API REST completa para pesquisa acadêmica
    
    ## 🔍 BUSCA POR AUTOR:
    - `/search/author/scholar` - Google Scholar
    - `/search/author/lattes` - Plataforma Lattes  
    - `/search/author/orcid` - ORCID
    - `/search/author/profile` - Por link direto do perfil
    
    ## 📚 BUSCA POR TEMA:
    - `/search/topic/scholar` - Google Scholar
    - `/search/topic/lattes` - Plataforma Lattes
    - `/search/topic/orcid` - ORCID
    
    ## 🎯 BUSCA COMPLETA:
    - `/search/comprehensive` - Todas as plataformas
    """,
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instância dos serviços
scholar_service = GoogleScholarService()
lattes_service = LattesService()
orcid_service = ORCIDService()

# ==================== ENDPOINTS PRINCIPAIS ====================

@app.get("/")
async def root():
    """🏠 Endpoint raiz com informações da API"""
    return {
        "message": "🎓 Academic Research API - Reorganizada",
        "version": "3.0.0",
        "endpoints": {
            "author_search": {
                "scholar": "/search/author/scholar",
                "lattes": "/search/author/lattes", 
                "orcid": "/search/author/orcid",
                "by_profile": "/search/author/profile"
            },
            "topic_search": {
                "scholar": "/search/topic/scholar",
                "lattes": "/search/topic/lattes",
                "orcid": "/search/topic/orcid"
            },
            "comprehensive": "/search/comprehensive"
        },
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """🔍 Health check endpoint"""
    try:
        is_valid, message = scholar_service.test_connection()
        return {
            "status": "healthy" if is_valid else "warning",
            "message": "Academic Research API está funcionando!",
            "google_scholar": "ok" if is_valid else "error",
            "timestamp": datetime.now().isoformat(),
            "version": "3.0.0"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erro no health check: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

# ==================== BUSCA POR AUTOR ====================

@app.get("/search/author/scholar")
async def search_author_scholar(
    author: str = Query(..., description="Nome do autor para buscar"),
    max_results: int = Query(10, ge=1, le=50, description="Máximo de resultados"),
    save_excel: bool = Query(False, description="Salvar resultados em Excel")
):
    """🔍 Busca autor no Google Scholar"""
    try:
        start_time = time.time()
        results = await scholar_service.search_author(author, max_results, save_excel)
        execution_time = time.time() - start_time
        
        response = {
            "success": True,
            "message": f"Busca por autor '{author}' concluída no Google Scholar",
            "platform": "google_scholar",
            "search_type": "author",
            "query": author,
            "total_results": len(results.get("publications", [])),
            "execution_time": round(execution_time, 2),
            "data": results
        }
        
        if save_excel:
            response["excel_file"] = results.get("excel_file")
            
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro na busca por autor no Google Scholar: {str(e)}"
        )

@app.get("/search/author/lattes")
async def search_author_lattes(
    name: str = Query(..., description="Nome do pesquisador"),
    max_results: int = Query(10, ge=1, le=50, description="Máximo de resultados")
):
    """📚 Busca autor na Plataforma Lattes"""
    try:
        start_time = time.time()
        
        # Usar o serviço atualizado
        results = lattes_service.search_by_name(name, max_results)
        
        execution_time = time.time() - start_time
        
        return {
            "success": True,
            "message": f"Busca por '{name}' concluída na Plataforma Lattes",
            "platform": "lattes",
            "search_type": "author",
            "query": name,
            "total_results": len(results),
            "execution_time": round(execution_time, 2),
            "data": {"lattes_profiles": results}
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na busca por autor no Lattes: {str(e)}"
        )

@app.get("/search/author/orcid")
async def search_author_orcid(
    name: str = Query(..., description="Nome do pesquisador"),
    max_results: int = Query(10, ge=1, le=50, description="Máximo de resultados")
):
    """🌐 Busca autor no ORCID"""
    try:
        start_time = time.time()
        
        # Usar o serviço atualizado
        results = orcid_service.search_by_name(name, max_results)
        
        execution_time = time.time() - start_time
        
        return {
            "success": True,
            "message": f"Busca por '{name}' concluída no ORCID",
            "platform": "orcid",
            "search_type": "author",
            "query": name,
            "total_results": len(results),
            "execution_time": round(execution_time, 2),
            "data": {"orcid_profiles": results}
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na busca por autor no ORCID: {str(e)}"
        )

# ==================== BUSCA POR LINK DE PERFIL ====================

@app.get("/search/author/profile")
async def search_by_profile_link(
    profile_url: str = Query(..., description="Link direto do perfil do autor"),
    platform: Optional[str] = Query(None, description="Plataforma: scholar, lattes, orcid (auto-detecta se não especificado)")
):
    """🔗 Busca por link direto do perfil do autor"""
    try:
        start_time = time.time()
        print(f"🔗 Buscando perfil: {profile_url}")
        
        # Auto-detectar plataforma se não especificada
        if not platform:
            if "scholar.google" in profile_url:
                platform = "scholar"
            elif "lattes.cnpq.br" in profile_url:
                platform = "lattes"
            elif "orcid.org" in profile_url:
                platform = "orcid"
            else:
                raise HTTPException(
                    status_code=400, 
                    detail="Não foi possível detectar a plataforma. Especifique o parâmetro 'platform'"
                )
        
        platform = platform.lower()
        print(f"📍 Plataforma detectada: {platform}")
        
        if platform == "scholar":
            print("🔍 Iniciando busca no Google Scholar...")
            results = await scholar_service.get_author_profile_by_url(profile_url)
            print(f"✅ Busca Scholar concluída")
        elif platform == "lattes":
            print("🔍 Iniciando busca no Lattes...")
            # Usar o serviço atualizado
            lattes_id = profile_url.split('/')[-1]  # Extrair ID do URL
            profile = lattes_service.get_full_profile(lattes_id)
            results = {"lattes_profile": profile} if profile else {"lattes_profile": None}
            print(f"✅ Busca Lattes concluída")
        elif platform == "orcid":
            print("🔍 Iniciando busca no ORCID...")
            # Usar o serviço atualizado
            orcid_id = profile_url.split('/')[-1]  # Extrair ID do URL
            profile = orcid_service.get_full_profile(orcid_id)
            results = {"orcid_profile": profile} if profile else {"orcid_profile": None}
            print(f"✅ Busca ORCID concluída")
        else:
            raise HTTPException(
                status_code=400, 
                detail="Plataforma deve ser: scholar, lattes ou orcid"
            )
        
        execution_time = time.time() - start_time
        print(f"⏱️ Tempo total: {execution_time:.2f}s")
        
        return {
            "success": True,
            "message": f"Perfil obtido com sucesso de {platform}",
            "platform": platform,
            "search_type": "profile_url",
            "profile_url": profile_url,
            "execution_time": round(execution_time, 2),
            "data": results
        }
        
    except Exception as e:
        print(f"❌ ERRO na busca de perfil: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar perfil: {str(e)}"
        )

# ==================== BUSCA POR TEMA ====================

@app.get("/search/topic/scholar")
async def search_topic_scholar(
    topic: str = Query(..., description="Tema de pesquisa"),
    max_results: int = Query(20, ge=1, le=100, description="Máximo de resultados"),
    save_excel: bool = Query(False, description="Salvar resultados em Excel")
):
    """🔍 Busca tema no Google Scholar"""
    try:
        start_time = time.time()
        results = await scholar_service.search_publications(topic, max_results, save_excel)
        execution_time = time.time() - start_time
        
        response = {
            "success": True,
            "message": f"Busca por tema '{topic}' concluída no Google Scholar",
            "platform": "google_scholar",
            "search_type": "topic",
            "query": topic,
            "total_results": len(results.get("publications", [])),
            "execution_time": round(execution_time, 2),
            "data": results
        }
        
        if save_excel:
            response["excel_file"] = results.get("excel_file")
            
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na busca por tema no Google Scholar: {str(e)}"
        )

@app.get("/search/topic/lattes")
async def search_topic_lattes(
    topic: str = Query(..., description="Tema de pesquisa"),
    max_results: int = Query(20, ge=1, le=100, description="Máximo de resultados")
):
    """📚 Busca tema na Plataforma Lattes"""
    try:
        start_time = time.time()
        
        # Usar o serviço atualizado
        results = lattes_service.search_by_topic(topic, max_results)
        
        execution_time = time.time() - start_time
        
        return {
            "success": True,
            "message": f"Busca por tema '{topic}' concluída na Plataforma Lattes",
            "platform": "lattes",
            "search_type": "topic",
            "query": topic,
            "total_results": len(results),
            "execution_time": round(execution_time, 2),
            "data": {"lattes_profiles": results}
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na busca por tema no Lattes: {str(e)}"
        )

@app.get("/search/topic/orcid")
async def search_topic_orcid(
    topic: str = Query(..., description="Tema de pesquisa"),
    max_results: int = Query(20, ge=1, le=100, description="Máximo de resultados")
):
    """🌐 Busca tema no ORCID"""
    try:
        start_time = time.time()
        
        # Usar o serviço atualizado
        results = orcid_service.search_by_topic(topic, max_results)
        
        execution_time = time.time() - start_time
        
        return {
            "success": True,
            "message": f"Busca por tema '{topic}' concluída no ORCID",
            "platform": "orcid",
            "search_type": "topic",
            "query": topic,
            "total_results": len(results),
            "execution_time": round(execution_time, 2),
            "data": {"orcid_profiles": results}
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na busca por tema no ORCID: {str(e)}"
        )

# ==================== BUSCA COMPLETA ====================

@app.get("/search/comprehensive")
async def comprehensive_search(
    query: str = Query(..., description="Termo de busca (autor ou tema)"),
    search_type: str = Query("both", description="Tipo: author, topic, both"),
    platforms: str = Query("all", description="Plataformas: scholar,lattes,orcid ou all"),
    max_results: int = Query(10, ge=1, le=50, description="Máximo de resultados POR PLATAFORMA (não total)"),
    save_csv: bool = Query(False, description="Salvar resultados em CSV")
):
    """🎯 Busca completa em todas as plataformas - max_results aplicado POR PLATAFORMA"""
    try:
        start_time = time.time()
        
        # Determinar plataformas
        if platforms == "all":
            platform_list = ["scholar", "lattes", "orcid"]
        else:
            platform_list = [p.strip() for p in platforms.split(",")]
        
        results = {
            "success": True,
            "message": f"Busca completa por '{query}' - {max_results} resultados por plataforma",
            "query": query,
            "search_type": search_type,
            "platforms": platform_list,
            "max_results_per_platform": max_results,
            "total_results": 0,
            "results_by_platform": {},
            "platform_stats": {}
        }
        
        # Buscar em cada plataforma COM LIMITE POR PLATAFORMA
        for platform in platform_list:
            platform_start = time.time()
            try:
                print(f"🔍 Buscando em {platform}: '{query}' (limite: {max_results})")
                
                if platform == "scholar":
                    if search_type in ["author", "both"]:
                        scholar_results = await scholar_service.search_author(query, max_results)
                    else:
                        scholar_results = await scholar_service.search_publications(query, max_results)
                    
                    # Garantir que o Scholar respeite o limite
                    if "publications" in scholar_results:
                        scholar_results["publications"] = scholar_results["publications"][:max_results]
                    
                    results["results_by_platform"]["scholar"] = scholar_results
                    results["platform_stats"]["scholar"] = {
                        "requested": max_results,
                        "returned": len(scholar_results.get("publications", [])),
                        "time": round(time.time() - platform_start, 2)
                    }
                    
                elif platform == "lattes":
                    lattes_results = lattes_service.search_by_name(query, max_results)
                    formatted_results = {"lattes_profiles": lattes_results}
                    
                    results["results_by_platform"]["lattes"] = formatted_results
                    results["platform_stats"]["lattes"] = {
                        "requested": max_results,
                        "returned": len(lattes_results),
                        "time": round(time.time() - platform_start, 2)
                    }
                    
                elif platform == "orcid":
                    orcid_results = orcid_service.search_by_name(query, max_results)
                    formatted_results = {"orcid_profiles": orcid_results}
                    
                    results["results_by_platform"]["orcid"] = formatted_results
                    results["platform_stats"]["orcid"] = {
                        "requested": max_results,
                        "returned": len(orcid_results),
                        "time": round(time.time() - platform_start, 2)
                    }
                    
                print(f"✅ {platform} concluído: {results['platform_stats'][platform]['returned']} resultados")
                    
            except Exception as e:
                print(f"❌ Erro em {platform}: {str(e)}")
                results["results_by_platform"][platform] = {
                    "error": f"Erro na busca: {str(e)}"
                }
                results["platform_stats"][platform] = {
                    "requested": max_results,
                    "returned": 0,
                    "error": str(e),
                    "time": round(time.time() - platform_start, 2)
                }
        
        # Calcular estatísticas finais
        total_results = 0
        successful_platforms = 0
        
        for platform, platform_results in results["results_by_platform"].items():
            if isinstance(platform_results, dict) and "error" not in platform_results:
                successful_platforms += 1
                if "publications" in platform_results:
                    total_results += len(platform_results["publications"])
                elif "lattes_profiles" in platform_results:
                    total_results += len(platform_results["lattes_profiles"])
                elif "orcid_profiles" in platform_results:
                    total_results += len(platform_results["orcid_profiles"])
        
        results["total_results"] = total_results
        results["successful_platforms"] = successful_platforms
        results["expected_total"] = len(platform_list) * max_results
        results["execution_time"] = round(time.time() - start_time, 2)
        
        # Atualizar mensagem com estatísticas
        results["message"] = f"Busca completa: {total_results} resultados de {successful_platforms}/{len(platform_list)} plataformas"
        
        # Salvar CSV se solicitado
        if save_csv:
            csv_filename = f"comprehensive_search_{query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            results["csv_file"] = csv_filename
        
        return results
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na busca completa: {str(e)}"
        )

# ==================== ENDPOINTS DE TESTE ====================

@app.get("/test/platforms")
async def test_all_platforms():
    """🧪 Teste rápido de todas as plataformas"""
    results = {
        "google_scholar": "❌",
        "lattes": "❌", 
        "orcid": "❌"
    }
    
    try:
        # Teste Google Scholar
        is_valid, message = scholar_service.test_connection()
        results["google_scholar"] = "✅" if is_valid else "❌"
    except:
        pass
    
    try:
        # Teste Lattes (usando dados de demonstração)
        results["lattes"] = "✅ (Demo)"
    except:
        results["lattes"] = "❌"
        
    try:
        # Teste ORCID (usando serviço real)
        test_results = orcid_service.search_by_name("test", 1)
        results["orcid"] = "✅" if test_results else "⚠️"
    except:
        results["orcid"] = "❌"
    
    return {
        "message": "Teste de conectividade das plataformas",
        "results": results,
        "timestamp": datetime.now().isoformat()
    }

# ==================== MAIN ====================

if __name__ == "__main__":
    uvicorn.run(
        "api_new:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )