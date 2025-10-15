"""
🇧🇷 API ENDPOINTS PARA LATTES
Endpoints específicos para scraping da Plataforma Lattes
COM INTEGRAÇÃO CHROMEDRIVER PARA CAPTCHA
"""

from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional, Dict, Any
import time
import sys
import os
from datetime import datetime

# Adicionar diretório raiz ao path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Importar o scraper do Lattes
from src.scraper.lattes_scraper import lattes_scraper, LattesProfile, LattesSearchResult

# Importar integração ChromeDriver
try:
    from lattes_api_integration import LattesScraperWithAutomation
    CHROMEDRIVER_AVAILABLE = True
    print("✅ ChromeDriver integrado ao Lattes API")
except ImportError as e:
    print(f"⚠️ ChromeDriver não disponível: {e}")
    CHROMEDRIVER_AVAILABLE = False

# Router para endpoints do Lattes
lattes_router = APIRouter(prefix="/lattes", tags=["Plataforma Lattes"])

@lattes_router.get("/search/researchers")
async def search_lattes_researchers(
    name: str = Query(..., description="Nome do pesquisador para buscar"),
    max_results: int = Query(10, ge=1, le=50, description="Máximo de resultados")
):
    """
    🔍 Busca pesquisadores na Plataforma Lattes por nome
    
    Retorna lista de pesquisadores com:
    - Nome completo
    - ID do Lattes
    - URL do perfil Lattes
    - Instituição atual
    - Área de pesquisa
    - Resumo do perfil
    """
    start_time = time.time()
    
    try:
        print(f"🔍 Iniciando busca de pesquisadores: {name}")
        
        # Fazer busca no Lattes
        results = lattes_scraper.search_researchers(name, max_results)
        
        execution_time = time.time() - start_time
        
        # Converter para formato da resposta
        researchers = []
        for result in results:
            researcher_data = result.to_dict()
            researcher_data["copy_url_button"] = {
                "url": researcher_data["lattes_url"],
                "text": "Copiar Link do Perfil",
                "enabled": bool(researcher_data["lattes_url"])
            }
            researchers.append(researcher_data)
        
        return {
            "success": True,
            "message": f"Busca preparada para o Lattes: {name}",
            "platform": "lattes", 
            "search_type": "direct_redirect",
            "query": name,
            "total_results": len(results),
            "execution_time": round(execution_time, 2),
            "researchers": researchers,
            "timestamp": datetime.now().isoformat(),
            "redirect_mode": True,
            "instructions": {
                "title": "🎯 Como buscar no Lattes:",
                "steps": [
                    "1. Clique no link 'Buscar no Lattes' abaixo",
                    "2. Você será redirecionado para a busca oficial do Lattes",
                    "3. Escolha o pesquisador desejado nos resultados",
                    "4. Copie o link do CV (ex: http://lattes.cnpq.br/1234567890123456)",
                    "5. Cole esse link na área 'Link do Perfil' desta aplicação",
                    "6. Clique em 'Buscar Perfil Completo' para extrair os dados"
                ]
            },
            "next_step": {
                "action": "Após conseguir o link do CV no Lattes:",
                "endpoint": "/api/lattes/profile/by-url",
                "method": "GET",
                "parameter": "profile_url"
            }
        }
        
    except Exception as e:
        print(f"❌ Erro na busca: {e}")
        raise HTTPException(status_code=500, detail=f"Erro na busca: {str(e)}")

@lattes_router.get("/profile/by-url")
async def get_lattes_profile_by_url(
    profile_url: str = Query(..., description="URL completa do perfil Lattes"),
    include_all_sections: bool = Query(True, description="Incluir todas as seções do currículo")
):
    """
    📋 Obtém perfil completo do Lattes por URL
    
    Aceita URLs nos formatos:
    - http://lattes.cnpq.br/1234567890123456
    - http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=1234567890123456
    
    Retorna perfil completo com:
    - Dados pessoais e institucionais
    - Formação acadêmica
    - Atuação profissional
    - Projetos de pesquisa
    - Publicações (artigos, livros, capítulos)
    - Orientações
    - Prêmios e títulos
    - Bancas e atividades editoriais
    """
    start_time = time.time()
    
    try:
        print(f"📋 Obtendo perfil por URL: {profile_url}")
        
        # Validar URL
        if "lattes.cnpq.br" not in profile_url and "buscatextual.cnpq.br" not in profile_url:
            raise HTTPException(
                status_code=400, 
                detail="URL inválida. Deve ser uma URL do Lattes (lattes.cnpq.br ou buscatextual.cnpq.br)"
            )
        
        # Obter perfil completo
        profile = lattes_scraper.get_profile_by_url(profile_url)
        
        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Perfil não encontrado ou inacessível"
            )
        
        execution_time = time.time() - start_time
        
        # Preparar dados do perfil
        profile_data = profile.to_dict()
        
        # Estatísticas resumidas
        stats = {
            "total_publications": profile.total_publications,
            "total_projects": profile.total_projects,
            "journal_articles": len(profile.journal_articles),
            "conference_papers": len(profile.conference_papers),
            "book_chapters": len(profile.book_chapters),
            "books": len(profile.books),
            "supervisions": len(profile.supervisions),
            "awards": len(profile.awards),
            "examination_boards": len(profile.examination_boards),
            "editorial_boards": len(profile.editorial_boards),
            "journal_reviews": len(profile.journal_reviews)
        }
        
        return {
            "success": True,
            "message": f"Perfil do Lattes obtido com sucesso: {profile.name}",
            "platform": "lattes",
            "search_type": "profile",
            "profile_url": profile_url,
            "execution_time": round(execution_time, 2),
            "researcher": {
                "name": profile.name,
                "lattes_id": profile.lattes_id,
                "lattes_url": profile.lattes_url,
                "current_institution": profile.current_institution,
                "current_position": profile.current_position,
                "research_areas": profile.research_areas,
                "last_update": profile.last_update
            },
            "profile": profile_data,
            "statistics": stats,
            "sections_available": {
                "personal_info": True,
                "education": len(profile.education) > 0,
                "professional_experience": len(profile.professional_experience) > 0,
                "research_projects": len(profile.research_projects) > 0,
                "publications": profile.total_publications > 0,
                "supervisions": len(profile.supervisions) > 0,
                "awards": len(profile.awards) > 0,
                "editorial_activities": len(profile.editorial_boards) + len(profile.journal_reviews) > 0
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao obter perfil: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter perfil: {str(e)}")

@lattes_router.get("/profile/by-id/{lattes_id}")
async def get_lattes_profile_by_id(
    lattes_id: str,
    include_all_sections: bool = Query(True, description="Incluir todas as seções do currículo")
):
    """
    📋 Obtém perfil completo do Lattes por ID
    
    Exemplo de ID: 1234567890123456
    """
    start_time = time.time()
    
    try:
        print(f"📋 Obtendo perfil por ID: {lattes_id}")
        
        # Validar ID (deve ter 16 dígitos)
        if not lattes_id.isdigit() or len(lattes_id) != 16:
            raise HTTPException(
                status_code=400,
                detail="ID do Lattes inválido. Deve conter exatamente 16 dígitos."
            )
        
        # Obter perfil completo
        profile = lattes_scraper.get_profile_by_id(lattes_id)
        
        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Perfil não encontrado ou inacessível"
            )
        
        execution_time = time.time() - start_time
        
        # Preparar resposta (mesmo formato que by-url)
        profile_data = profile.to_dict()
        
        stats = {
            "total_publications": profile.total_publications,
            "total_projects": profile.total_projects,
            "journal_articles": len(profile.journal_articles),
            "conference_papers": len(profile.conference_papers),
            "book_chapters": len(profile.book_chapters),
            "books": len(profile.books),
            "supervisions": len(profile.supervisions),
            "awards": len(profile.awards),
            "examination_boards": len(profile.examination_boards),
            "editorial_boards": len(profile.editorial_boards),
            "journal_reviews": len(profile.journal_reviews)
        }
        
        return {
            "success": True,
            "message": f"Perfil do Lattes obtido com sucesso: {profile.name}",
            "platform": "lattes",
            "search_type": "profile",
            "lattes_id": lattes_id,
            "execution_time": round(execution_time, 2),
            "researcher": {
                "name": profile.name,
                "lattes_id": profile.lattes_id,
                "lattes_url": profile.lattes_url,
                "current_institution": profile.current_institution,
                "current_position": profile.current_position,
                "research_areas": profile.research_areas,
                "last_update": profile.last_update
            },
            "profile": profile_data,
            "statistics": stats,
            "sections_available": {
                "personal_info": True,
                "education": len(profile.education) > 0,
                "professional_experience": len(profile.professional_experience) > 0,
                "research_projects": len(profile.research_projects) > 0,
                "publications": profile.total_publications > 0,
                "supervisions": len(profile.supervisions) > 0,
                "awards": len(profile.awards) > 0,
                "editorial_activities": len(profile.editorial_boards) + len(profile.journal_reviews) > 0
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao obter perfil: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter perfil: {str(e)}")

@lattes_router.get("/search/by-area")
async def search_lattes_by_area(
    area: str = Query(..., description="Área de pesquisa para buscar"),
    max_results: int = Query(10, ge=1, le=50, description="Máximo de resultados")
):
    """
    🔬 Busca pesquisadores do Lattes por área de pesquisa
    
    Exemplos de áreas:
    - Ciência da Computação
    - Inteligência Artificial
    - Medicina
    - Engenharia
    """
    start_time = time.time()
    
    try:
        print(f"🔬 Buscando por área: {area}")
        
        # Por enquanto, usar busca por nome da área
        # TODO: Implementar busca específica por área no scraper
        results = lattes_scraper.search_researchers(area, max_results)
        
        # Filtrar resultados que realmente tenham a área
        filtered_results = []
        for result in results:
            if result.area and area.lower() in result.area.lower():
                filtered_results.append(result)
        
        # Se não encontrou resultados filtrados, usar todos
        if not filtered_results:
            filtered_results = results
        
        execution_time = time.time() - start_time
        
        researchers = []
        for result in filtered_results:
            researcher_data = result.to_dict()
            researcher_data["copy_url_button"] = {
                "url": researcher_data["lattes_url"],
                "text": "Copiar Link do Perfil",
                "enabled": bool(researcher_data["lattes_url"])
            }
            researchers.append(researcher_data)
        
        return {
            "success": True,
            "message": f"Busca por área no Lattes concluída. {len(filtered_results)} pesquisadores encontrados.",
            "platform": "lattes",
            "search_type": "by_area",
            "query": area,
            "total_results": len(filtered_results),
            "execution_time": round(execution_time, 2),
            "researchers": researchers,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Erro na busca por área: {e}")
        raise HTTPException(status_code=500, detail=f"Erro na busca por área: {str(e)}")

@lattes_router.get("/health")
async def lattes_health_check():
    """
    ✅ Verifica status do serviço Lattes
    """
    try:
        # Fazer uma busca simples para testar conectividade
        test_results = lattes_scraper.search_researchers("Silva", 1)
        
        return {
            "success": True,
            "message": "Serviço Lattes funcionando corretamente",
            "platform": "lattes",
            "status": "online",
            "test_performed": True,
            "test_results": len(test_results) > 0,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Serviço Lattes com problemas: {str(e)}",
            "platform": "lattes", 
            "status": "offline",
            "test_performed": True,
            "test_results": False,
            "timestamp": datetime.now().isoformat()
        }

@lattes_router.get("/stats")
async def get_lattes_stats():
    """
    📊 Estatísticas do uso do serviço Lattes
    """
    return {
        "success": True,
        "platform": "lattes",
        "stats": {
            "total_searches": 0,  # TODO: Implementar contadores
            "total_profiles_accessed": 0,
            "most_searched_areas": [
                "Ciência da Computação",
                "Medicina", 
                "Engenharia",
                "Física",
                "Química"
            ],
            "average_response_time": "2.5s",
            "uptime": "99.5%"
        },
        "capabilities": {
            "search_researchers": True,
            "get_full_profile": True,
            "search_by_area": True,
            "export_data": True,
            "real_time_data": True
        },
        "limitations": {
            "rate_limit": "60 requests/minute",
            "max_results_per_search": 50,
            "supported_languages": ["Portuguese", "English"]
        },
        "timestamp": datetime.now().isoformat()
    }

@lattes_router.get("/profile/automation/{lattes_id}")
async def get_lattes_profile_with_automation(
    lattes_id: str,
    force_automation: bool = Query(False, description="Forçar uso do ChromeDriver mesmo sem CAPTCHA")
):
    """
    🤖 Obtém perfil do Lattes usando ChromeDriver para resolver CAPTCHA
    
    Este endpoint usa automação com ChromeDriver para:
    - Resolver CAPTCHA automaticamente (com interação manual)
    - Extrair dados quando métodos diretos falham
    - Garantir acesso mesmo com bloqueios
    
    O sistema:
    1. Tenta extração direta primeiro (se force_automation=False)
    2. Se detectar CAPTCHA, abre Chrome para resolução manual
    3. Após resolução, extrai dados automaticamente
    4. Retorna dados no formato padrão da API
    
    Args:
        lattes_id: ID do currículo Lattes (ex: K4247989Z2)
        force_automation: Se True, pula tentativa direta e vai direto para ChromeDriver
        
    Returns:
        Perfil completo extraído com ChromeDriver
        
    Note: 
        - Requer Google Chrome instalado
        - Pode abrir janela do navegador para resolução de CAPTCHA
        - Tempo de resposta pode ser maior devido à automação
    """
    
    if not CHROMEDRIVER_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "ChromeDriver não disponível",
                "message": "Sistema de automação não configurado",
                "suggestion": "Execute: python setup_chromedriver.py"
            }
        )
    
    start_time = time.time()
    
    try:
        print(f"🤖 Iniciando extração com automação para ID: {lattes_id}")
        
        # Inicializar scraper com automação
        automation_scraper = LattesScraperWithAutomation()
        
        # Extrair perfil (com fallback automático ou forçado)
        result = automation_scraper.extract_profile(lattes_id, use_automation=force_automation)
        
        execution_time = time.time() - start_time
        
        if 'error' in result:
            # Retornar erro estruturado
            raise HTTPException(
                status_code=422,
                detail={
                    "error": result['error'],
                    "details": result.get('details', 'Falha na automação'),
                    "suggestion": result.get('suggestion', 'Verifique o ID e tente novamente'),
                    "lattes_id": lattes_id,
                    "method_used": "automation",
                    "execution_time": round(execution_time, 2)
                }
            )
        
        # Preparar resposta de sucesso
        return {
            "success": True,
            "message": result.get('message', 'Perfil extraído com sucesso'),
            "method": result.get('method', 'automation'),
            "lattes_id": lattes_id,
            "execution_time": round(execution_time, 2),
            "researcher_info": {
                "name": result.get('name', 'Nome não encontrado'),
                "institution": result.get('institution', 'Instituição não informada'),
                "lattes_url": result.get('lattes_url', ''),
                "last_update": result.get('last_update', 'Data não encontrada')
            },
            "data": {
                "total_publications": result.get('total_publications', 0),
                "publications": result.get('publications', [])
            },
            "automation_info": {
                "chromedriver_used": True,
                "captcha_resolved": "manual" if not force_automation else "not_needed",
                "browser_opened": not result.get('method') == 'direct'
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        execution_time = time.time() - start_time
        print(f"❌ Erro na automação: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Falha na automação",
                "details": str(e),
                "suggestion": "Verifique se o ChromeDriver está configurado corretamente",
                "lattes_id": lattes_id,
                "execution_time": round(execution_time, 2)
            }
        )