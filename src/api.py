"""
🔥 API REAL DE SCRAPING ACADÊMICO - VERSÃO MODULAR
Extração real de dados do Lattes, ORCID e Google Scholar
COM SEPARAÇÃO COMPLETA DE LATTES E ORCID
"""

import os
import re
import json
import time
import random
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from urllib.parse import quote, unquote

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Importar routers separados (NOVO!)
try:
    from src.routers.lattes_api import lattes_router
    from src.routers.orcid_api import orcid_router
    SEPARATED_APIS_AVAILABLE = True
    print("✅ APIs separadas de Lattes e ORCID carregadas!")
except ImportError as e:
    print(f"⚠️ APIs separadas não disponíveis: {e}")
    SEPARATED_APIS_AVAILABLE = False

# Importar MongoDB
try:
    from src.database.mongodb import research_db, ResearchDatabase
    from src.database.excel_consolidado import consolidated_exporter
    MONGODB_AVAILABLE = True
    print("✅ MongoDB integrado")
except ImportError as e:
    print(f"⚠️ MongoDB não disponível: {e}")
    MONGODB_AVAILABLE = False

print("🔥 API REAL DE SCRAPING CARREGADA!")

app = FastAPI(
    title="API Real de Scraping Acadêmico",
    description="Extração real de dados do Lattes, ORCID e Google Scholar",
    version="8.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers separados (NOVO!)
if SEPARATED_APIS_AVAILABLE:
    app.include_router(lattes_router, prefix="/api")
    app.include_router(orcid_router, prefix="/api")
    print("🔗 Routers do Lattes e ORCID integrados!")
else:
    print("⚠️ Usando API combinada legada")

# Headers para burlar detecção
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
}

def save_to_mongodb_if_filtered(result: Dict[str, Any], filter_keywords: bool):
    """Salvar resultado no MongoDB se filtrado por keywords OU se for dados do Scholar"""
    # Sempre salvar dados do Scholar (mesmo sem filtro) ou quando filtrado por keywords
    should_save = (
        MONGODB_AVAILABLE and 
        result.get("data", {}).get("publications") and
        (filter_keywords or result.get("platform") == "scholar")
    )
    
    if should_save:
        try:
            saved = research_db.save_research_result(result)
            if saved:
                result["saved_to_database"] = True
                platform = result.get("platform", "desconhecida")
                print(f"💾 Dados salvos no MongoDB (plataforma: {platform})")
            else:
                result["database_error"] = "Falha ao salvar no MongoDB"
        except Exception as e:
            print(f"❌ Erro ao salvar no MongoDB: {e}")
            result["database_error"] = str(e)
            result["database_error"] = str(e)

class LattesExtractor:
    """Extrator real do Lattes"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def extract_profile(self, lattes_url: str) -> Dict[str, Any]:
        """Extrair dados reais do Lattes"""
        print(f"🇧🇷 EXTRAINDO LATTES: {lattes_url}")
        
        try:
            # Aguardar para evitar bloqueio
            time.sleep(random.uniform(2, 4))
            
            response = self.session.get(lattes_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrair dados
            name = self._extract_name(soup)
            institution = self._extract_institution(soup)
            areas = self._extract_areas(soup)
            last_update = self._extract_last_update(soup)
            publications = self._extract_publications(soup)
            
            return {
                "success": True,
                "name": name,
                "institution": institution,
                "research_areas": areas,
                "last_update": last_update,
                "publications": publications,
                "total_publications": len(publications)
            }
            
        except Exception as e:
            print(f"❌ ERRO LATTES: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Erro ao extrair dados do Lattes"
            }
    
    def _extract_name(self, soup: BeautifulSoup) -> str:
        """Extrair nome do pesquisador"""
        selectors = [
            '.nome',
            '#nome-completo',
            '.infpessoais h2',
            'h2[class*="nome"]',
            '.layout-cell-pad-5 h2'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                name = element.get_text(strip=True)
                if name and len(name) > 2:
                    return name
        
        return "Nome não encontrado"
    
    def _extract_institution(self, soup: BeautifulSoup) -> str:
        """Extrair instituição"""
        selectors = [
            '.instituicao',
            '.vinculo-institucional',
            '.layout-cell-11',
            'div[class*="instituicao"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                inst = element.get_text(strip=True)
                if inst and len(inst) > 5:
                    return inst
        
        return "Instituição não encontrada"
    
    def _extract_areas(self, soup: BeautifulSoup) -> List[str]:
        """Extrair áreas de conhecimento"""
        areas = []
        
        # Procurar por áreas de conhecimento
        area_elements = soup.select('.area-conhecimento, .areas-atuacao li, .grande-area')
        
        for elem in area_elements:
            area = elem.get_text(strip=True)
            if area and area not in areas and len(area) > 3:
                areas.append(area)
        
        return areas[:5]  # Limitar a 5 áreas
    
    def _extract_last_update(self, soup: BeautifulSoup) -> str:
        """Extrair data de última atualização"""
        update_elem = soup.select_one('.data-atualizacao, .ultima-atualizacao')
        if update_elem:
            return update_elem.get_text(strip=True)
        return "Data não disponível"
    
    def _extract_publications(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extrair publicações"""
        publications = []
        
        # Procurar por artigos completos
        article_sections = soup.select('.artigo-completo, .trabalho-evento, .livro-publicado')
        
        for article in article_sections[:20]:  # Limitar a 20
            title_elem = article.select_one('.titulo-artigo, .titulo-trabalho, .titulo-livro, b')
            
            if title_elem:
                title = title_elem.get_text(strip=True)
                
                # Extrair ano
                year_match = re.search(r'\b(19|20)\d{2}\b', article.get_text())
                year = int(year_match.group()) if year_match else None
                
                # Extrair revista/local
                venue_elem = article.select_one('.titulo-periodico, .nome-evento, .editora')
                venue = venue_elem.get_text(strip=True) if venue_elem else "Não especificado"
                
                publications.append({
                    "title": title,
                    "year": year,
                    "venue": venue,
                    "type": "Artigo",
                    "platform": "lattes"
                })
        
        return publications
    
    def search_by_name(self, name: str) -> Dict[str, Any]:
        """Buscar perfil do Lattes por nome"""
        print(f"🔍 BUSCANDO NO LATTES: {name}")
        
        try:
            # Configurar headers específicos para o Lattes
            lattes_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'http://buscatextual.cnpq.br/buscatextual/index.jsp',
                'Upgrade-Insecure-Requests': '1'
            }
            
            # Criar nova sessão com headers específicos
            lattes_session = requests.Session()
            lattes_session.headers.update(lattes_headers)
            
            # Primeiro acessar a página inicial do Lattes para estabelecer sessão
            print("🌐 Inicializando sessão no Lattes...")
            init_url = "http://buscatextual.cnpq.br/buscatextual/index.jsp"
            init_response = lattes_session.get(init_url, timeout=15)
            
            if init_response.status_code != 200:
                print(f"⚠️ Falha ao inicializar sessão: {init_response.status_code}")
                return {
                    "success": False,
                    "message": "Falha ao conectar com o servidor do Lattes",
                    "debug_info": f"Status inicial: {init_response.status_code}"
                }
            
            time.sleep(random.uniform(2, 4))
            
            # URL de busca alternativa (método direto)
            search_url = f"http://buscatextual.cnpq.br/buscatextual/visualizacv.do"
            search_params = {
                'metodo': 'apresentar',
                'id': name.strip()
            }
            
            print(f"🔗 URL de busca Lattes: {search_url}")
            print(f"📋 Parâmetros: {search_params}")
            
            # Tentar busca direta primeiro
            response = lattes_session.get(search_url, params=search_params, timeout=30)
            
            print(f"📊 Status da busca direta: {response.status_code}")
            
            # Se busca direta falhou, tentar busca por lista
            if response.status_code != 200 or "Curriculum" not in response.text:
                print("🔄 Tentando busca por lista de currículos...")
                
                # URL de busca por lista
                list_url = "http://buscatextual.cnpq.br/buscatextual/busca.do"
                list_params = {
                    'metodo': 'apresentar',
                    'decorador': 'filtro',
                    'ord': 'tipo',
                    'filtro': name.strip(),
                    'tipo': '1'
                }
                
                response = lattes_session.get(list_url, params=list_params, timeout=30)
                print(f"📊 Status da busca por lista: {response.status_code}")
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": f"Erro de conexão com Lattes: {response.status_code}",
                    "debug_info": f"Status HTTP: {response.status_code}"
                }
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Verificar se já estamos numa página de currículo
            if "Curriculum" in response.text and "Lattes" in response.text:
                print("✅ Página de currículo encontrada diretamente")
                # Já estamos numa página de perfil, extrair dados diretamente
                name_found = self._extract_name(soup)
                institution = self._extract_institution(soup)
                areas = self._extract_areas(soup)
                last_update = self._extract_last_update(soup)
                publications = self._extract_publications(soup)
                
                return {
                    "success": True,
                    "name": name_found,
                    "institution": institution,
                    "research_areas": areas,
                    "last_update": last_update,
                    "publications": publications,
                    "total_publications": len(publications)
                }
            
            # Procurar por links de currículos na página de resultados
            result_links = soup.select('a[href*="visualizacv.do"], a[href*="curriculum"]')
            print(f"👥 Resultados encontrados: {len(result_links)}")
            
            if result_links:
                # Pegar o primeiro resultado
                first_link = result_links[0]
                relative_url = first_link.get('href')
                
                # Construir URL completa do perfil
                if relative_url.startswith('http'):
                    profile_url = relative_url
                else:
                    profile_url = f"http://buscatextual.cnpq.br/buscatextual/{relative_url}"
                
                print(f"🔗 URL do perfil encontrado: {profile_url}")
                
                # Extrair dados do perfil
                return self.extract_profile(profile_url)
            
            return {
                "success": False,
                "message": f"Pesquisador '{name}' não encontrado no Lattes",
                "debug_info": f"Nenhum resultado na busca por nome. Conteúdo da página: {len(response.text)} caracteres",
                "suggestion": "Para buscar no Lattes, use a URL direta do perfil (ex: http://lattes.cnpq.br/1234567890123456) ou procure manualmente no site do Lattes"
            }
                
        except Exception as e:
            print(f"❌ ERRO na busca Lattes: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Erro ao buscar '{name}' no Lattes"
            }

class ORCIDExtractor:
    """Extrator real do ORCID"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def extract_profile(self, orcid_url: str) -> Dict[str, Any]:
        """Extrair dados reais do ORCID"""
        print(f"🌐 EXTRAINDO ORCID: {orcid_url}")
        
        try:
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(orcid_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            name = self._extract_name(soup)
            orcid_id = self._extract_orcid_id(orcid_url)
            affiliation = self._extract_affiliation(soup)
            works = self._extract_works(soup)
            
            return {
                "success": True,
                "name": name,
                "orcid_id": orcid_id,
                "affiliation": affiliation,
                "works": works,
                "total_works": len(works)
            }
            
        except Exception as e:
            print(f"❌ ERRO ORCID: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Erro ao extrair dados do ORCID"
            }
    
    def _extract_name(self, soup: BeautifulSoup) -> str:
        """Extrair nome"""
        name_selectors = [
            '.full-name',
            '.given-names',
            '.family-name',
            'h1[class*="name"]',
            '.personal-details h1'
        ]
        
        for selector in name_selectors:
            element = soup.select_one(selector)
            if element:
                name = element.get_text(strip=True)
                if name and len(name) > 2:
                    return name
        
        return "Nome não encontrado"
    
    def _extract_orcid_id(self, url: str) -> str:
        """Extrair ORCID ID da URL"""
        match = re.search(r'orcid\.org/(\d{4}-\d{4}-\d{4}-\d{4})', url)
        return match.group(1) if match else "ID não encontrado"
    
    def _extract_affiliation(self, soup: BeautifulSoup) -> str:
        """Extrair afiliação"""
        affil_selectors = [
            '.affiliation-name',
            '.employment-summary',
            '.org-name'
        ]
        
        for selector in affil_selectors:
            element = soup.select_one(selector)
            if element:
                affil = element.get_text(strip=True)
                if affil and len(affil) > 3:
                    return affil
        
        return "Afiliação não encontrada"
    
    def _extract_works(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extrair trabalhos"""
        works = []
        
        work_elements = soup.select('.work-item, .work-summary, .work')
        
        for work in work_elements[:15]:
            title_elem = work.select_one('.work-title, .title, h3')
            
            if title_elem:
                title = title_elem.get_text(strip=True)
                
                # Extrair ano
                year_elem = work.select_one('.date, .year, .publication-date')
                year = None
                if year_elem:
                    year_text = year_elem.get_text(strip=True)
                    year_match = re.search(r'\b(19|20)\d{2}\b', year_text)
                    year = int(year_match.group()) if year_match else None
                
                # Extrair journal
                journal_elem = work.select_one('.journal-title, .container-name')
                journal = journal_elem.get_text(strip=True) if journal_elem else "Não especificado"
                
                works.append({
                    "title": title,
                    "year": year,
                    "journal": journal,
                    "type": "Trabalho",
                    "platform": "orcid"
                })
        
        return works

class ScholarExtractor:
    """Extrator para Google Scholar"""
    
    def __init__(self):
        self.session = requests.Session()
        self.current_url = None  # Armazenar URL atual para fallback
        self.serpapi_author_data = {}  # Para armazenar dados do autor via SerpAPI
        self.requested_publications = 20  # Número de publicações solicitadas
        # Headers mais robustos para evitar bloqueios
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://scholar.google.com/'
        }
        self.session.headers.update(headers)
    
    def search_author(self, author_name: str, max_publications: int = 20) -> Dict[str, Any]:
        """Buscar autor no Google Scholar usando URL correta de pesquisa de pesquisadores"""
        print(f"🎓 BUSCANDO NO SCHOLAR: {author_name}")
        print(f"📚 Máximo de publicações para busca: {max_publications}")
        
        try:
            # Primeiro, acessar página inicial do Scholar para estabelecer sessão
            print("🌐 Inicializando sessão no Google Scholar...")
            init_response = self.session.get('https://scholar.google.com/', timeout=15)
            time.sleep(random.uniform(2, 4))
            
            # URL de busca de PESQUISADORES (não publicações) com parâmetros otimizados
            search_url = f"https://scholar.google.com/citations?view_op=search_authors&mauthors={quote(author_name)}&hl=pt-BR&oi=ao"
            print(f"🔗 URL de busca: {search_url}")
            
            time.sleep(random.uniform(3, 6))
            
            response = self.session.get(search_url, timeout=30)
            response.raise_for_status()
            
            print(f"📊 Status da resposta: {response.status_code}")
            
            # Verificar se foi redirecionado para login
            if 'accounts.google.com' in response.url or 'signin' in response.text.lower():
                print("⚠️ Google Scholar bloqueou o acesso - redirecionamento para login detectado")
                return {
                    "success": False,
                    "message": "Google Scholar bloqueou o acesso automatizado",
                    "debug_info": "Redirecionado para página de login"
                }
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Debug: verificar o que foi retornado
            print(f"🔍 Conteúdo da página (primeiros 200 chars): {response.text[:200]}...")
            
            # Procurar por resultados de pesquisadores (estrutura correta)
            author_results = soup.select('.gs_ai_chpr, .gs_ai')
            print(f"👥 Resultados de pesquisadores encontrados: {len(author_results)}")
            
            if author_results:
                first_result = author_results[0]
                
                # Extrair nome do pesquisador
                name_elem = first_result.select_one('h3 a, .gs_ai_name a')
                if name_elem:
                    researcher_name = name_elem.get_text(strip=True)
                    print(f"👤 Pesquisador encontrado: {researcher_name}")
                
                # Pegar link do perfil
                profile_link = first_result.select_one('h3 a, .gs_ai_name a')
                if profile_link and 'href' in profile_link.attrs:
                    profile_url = "https://scholar.google.com" + profile_link['href']
                    print(f"🔗 URL do perfil: {profile_url}")
                    return self.extract_profile(profile_url, max_publications)
            
            # Se não encontrou resultados na estrutura esperada, tentar seletores alternativos
            alternative_results = soup.select('div[data-aid]')
            print(f"🔄 Resultados alternativos encontrados: {len(alternative_results)}")
            
            if alternative_results:
                first_alt = alternative_results[0]
                alt_link = first_alt.select_one('a')
                if alt_link and 'href' in alt_link.attrs:
                    alt_url = "https://scholar.google.com" + alt_link['href']
                    print(f"🔗 URL alternativa: {alt_url}")
                    return self.extract_profile(alt_url, max_publications)
            
            return {
                "success": False,
                "message": "Autor não encontrado no Google Scholar",
                "debug_info": f"Página retornou {len(author_results)} resultados principais e {len(alternative_results)} alternativos"
            }
            
        except Exception as e:
            print(f"❌ ERRO SCHOLAR SEARCH: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def extract_profile(self, scholar_url: str, max_publications: int = 20) -> Dict[str, Any]:
        """Extrair perfil do Scholar com controle de número de publicações"""
        print(f"🎓 EXTRAINDO SCHOLAR PROFILE: {scholar_url}")
        print(f"📚 Máximo de publicações: {max_publications}")
        
        # Armazenar URL para fallback
        self.current_url = scholar_url
        self.requested_publications = max_publications  # Para usar no SerpAPI
        # Limpar dados anteriores do SerpAPI
        self.serpapi_author_data = {}
        
        try:
            time.sleep(random.uniform(3, 6))
            
            response = self.session.get(scholar_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Verificar se há CAPTCHA na página
            if soup.find(id="gsc_captcha_ccl") or "gs_captcha" in response.text:
                print("🚫 CAPTCHA DETECTADO! Usando SerpAPI como fallback principal...")
                return self._extract_via_serpapi_only(scholar_url, max_publications)
            
            name = self._extract_name(soup)
            affiliation = self._extract_affiliation(soup)
            h_index = self._extract_h_index(soup)
            i10_index = self._extract_i10_index(soup)
            citations = self._extract_citations(soup)
            publications = self._extract_publications_with_pagination(scholar_url, max_publications)
            
            # Se os dados básicos não foram encontrados via scraping, usar SerpAPI se disponível
            if (name == "Nome não encontrado" or h_index == "0" or i10_index == "0" or citations == "0") and self.serpapi_author_data:
                print("🔄 USANDO DADOS DO SERPAPI PARA COMPLETAR PERFIL...")
                
                if name == "Nome não encontrado" and self.serpapi_author_data.get('name'):
                    name = self.serpapi_author_data['name']
                    print(f"📝 Nome obtido via SerpAPI: {name}")
                
                if affiliation == "Afiliação não encontrada" and self.serpapi_author_data.get('affiliation'):
                    affiliation = self.serpapi_author_data['affiliation']
                    print(f"🏛️ Afiliação obtida via SerpAPI: {affiliation}")
                
                if h_index == "0" and self.serpapi_author_data.get('h_index'):
                    h_index = self.serpapi_author_data['h_index']
                    print(f"📊 H-index obtido via SerpAPI: {h_index}")
                
                if i10_index == "0" and self.serpapi_author_data.get('i10_index'):
                    i10_index = self.serpapi_author_data['i10_index']
                    print(f"📊 i10-index obtido via SerpAPI: {i10_index}")
                
                if citations == "0" and self.serpapi_author_data.get('total_citations'):
                    citations = self.serpapi_author_data['total_citations']
                    print(f"📈 Citações obtidas via SerpAPI: {citations}")
            
            return {
                "success": True,
                "name": name,
                "affiliation": affiliation,
                "h_index": h_index,
                "i10_index": i10_index,
                "total_citations": citations,
                "publications": publications,
                "total_publications": len(publications)
            }
            
        except Exception as e:
            print(f"❌ ERRO SCHOLAR PROFILE: {e}")
            print("🔄 Tentando usar SerpAPI como fallback de emergência...")
            return self._extract_via_serpapi_only(scholar_url, max_publications)
    
    def _extract_via_serpapi_only(self, scholar_url: str, max_publications: int = 20) -> Dict[str, Any]:
        """Extrair perfil usando apenas SerpAPI quando HTML scraping falha"""
        try:
            from serpapi import GoogleSearch
            import os
            
            # Carregar chave da API
            api_key = os.getenv("API_KEY") or os.getenv("SERPAPI_KEY") or "cf9d570296f13373cb9d7e7d592b5cea456e756748bea542232bcc05c28a5e1a"
            if not api_key:
                print("❌ SerpAPI key não encontrada")
                return {"success": False, "error": "API key não disponível"}
            
            # Extrair author ID da URL
            author_id = None
            if "user=" in scholar_url:
                author_id = scholar_url.split("user=")[1].split("&")[0]
            
            if not author_id:
                return {"success": False, "error": "Não foi possível extrair Author ID da URL"}
            
            print(f"🎯 Extraindo dados via SerpAPI para Author ID: {author_id}")
            
            # Buscar publicações usando SerpAPI
            params = {
                "api_key": api_key,
                "engine": "google_scholar_author", 
                "author_id": author_id,
                "hl": "pt-BR",
                "num": min(100, max_publications)
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            if 'error' in results:
                print(f"❌ Erro SerpAPI: {results['error']}")
                return {"success": False, "error": f"SerpAPI error: {results['error']}"}
            
            # Extrair dados do autor
            name = "Nome não encontrado"
            affiliation = "Afiliação não encontrada"
            h_index = "0"
            i10_index = "0"
            total_citations = "0"
            
            if 'author' in results:
                author_info = results['author']
                name = author_info.get('name', name)
                affiliation = author_info.get('affiliations', affiliation)
            
            # Os índices estão no nível raiz da resposta, não em author
            if 'cited_by' in results:
                cited_by = results['cited_by']
                print(f"📊 CITED_BY encontrado: {list(cited_by.keys())}")
                
                # Verificar se há tabela com índices
                if 'table' in cited_by and cited_by['table']:
                    print(f"📊 PROCESSANDO TABELA DE CITAÇÕES:")
                    for i, table_entry in enumerate(cited_by['table']):
                        print(f"  Entrada {i}: {table_entry}")
                        
                        # Verificar diferentes formatos de chaves para h-index e i10-index
                        for key in table_entry.keys():
                            key_lower = key.lower()
                            # Verificar h-index (pode ser 'h-index', 'h_index', 'Índice_h', etc.)
                            if ('h' in key_lower and ('index' in key_lower or 'índice' in key_lower)) or key == 'Índice_h':
                                h_index = str(table_entry[key].get('all', '0'))
                                print(f"✅ H-index encontrado na chave '{key}': {h_index}")
                            # Verificar i10-index (pode ser 'i10-index', 'i10_index', 'Índice_i10', etc.)
                            elif ('i10' in key_lower) or key == 'Índice_i10':
                                i10_index = str(table_entry[key].get('all', '0'))
                                print(f"✅ i10-index encontrado na chave '{key}': {i10_index}")
                
                # Tentar extrair citações totais do gráfico
                if 'graph' in cited_by and cited_by['graph']:
                    total_cites = sum(int(year.get('citations', 0)) for year in cited_by['graph'])
                    total_citations = str(total_cites)
                    print(f"📈 Citações calculadas do gráfico: {total_citations}")
            else:
                print("❌ Nenhuma informação de cited_by encontrada na resposta SerpAPI")
            
            # Extrair publicações
            publications = []
            if 'articles' in results:
                for article in results['articles'][:max_publications]:
                    publications.append({
                        "title": article.get("title", "Título não disponível"),
                        "venue": article.get("publication", "Venue não especificada"), 
                        "authors": article.get("authors", "Autores não especificados"),
                        "year": article.get("year"),
                        "citations": article.get("cited_by", {}).get("value", 0) if article.get("cited_by") else 0,
                        "type": "Artigo",
                        "platform": "scholar_serpapi"
                    })
            
            print(f"✅ SerpAPI extraído com sucesso:")
            print(f"   👤 Nome: {name}")
            print(f"   🏛️ Afiliação: {affiliation}")
            print(f"   📊 H-index: {h_index}")
            print(f"   📊 i10-index: {i10_index}")
            print(f"   📈 Citações: {total_citations}")
            print(f"   📚 Publicações: {len(publications)}")
            
            return {
                "success": True,
                "name": name,
                "affiliation": affiliation,
                "h_index": h_index,
                "i10_index": i10_index,
                "total_citations": total_citations,
                "publications": publications,
                "total_publications": len(publications)
            }
            
        except Exception as e:
            print(f"❌ Erro no SerpAPI fallback: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _extract_name(self, soup: BeautifulSoup) -> str:
        """Extrair nome"""
        name_elem = soup.select_one('#gsc_prf_in, .gsc_prf_in')
        return name_elem.get_text(strip=True) if name_elem else "Nome não encontrado"
    
    def _extract_affiliation(self, soup: BeautifulSoup) -> str:
        """Extrair afiliação"""
        affil_elem = soup.select_one('.gsc_prf_il')
        return affil_elem.get_text(strip=True) if affil_elem else "Afiliação não encontrada"
    
    def _extract_h_index(self, soup: BeautifulSoup) -> str:
        """Extrair índice H com análise rigorosa dos valores encontrados"""
        print("🔍 BUSCANDO ÍNDICE H...")
        
        # Estratégia 1: Buscar especificamente por h-index na estrutura da tabela
        table_rows = soup.select('.gsc_rsb_st')
        print(f"🔍 Linhas da tabela encontradas: {len(table_rows)}")
        
        for i, row in enumerate(table_rows):
            cells = row.select('td')
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True).lower()
                value = cells[1].get_text(strip=True)
                print(f"📋 Linha {i}: {label} = {value}")
                
                # Procurar especificamente por h-index
                if 'h-index' in label and value.replace(',', '').isdigit():
                    h_value = int(value.replace(',', ''))
                    if 1 <= h_value <= 500:  # Validação de range razoável
                        print(f"🎯 H-index encontrado na tabela: {value}")
                        return value
        
        # Estratégia 2: Buscar por seletores mais modernos do Google Scholar
        modern_selectors = [
            '#gsc_rsb_st tbody tr td:nth-child(2)',  # Seletor direto da célula
            '.gsc_rsb_std',  # Elementos de estatísticas
            '#gsc_rsb_st tr:nth-child(3) td:nth-child(2)',  # Linha específica do h-index
            '[data-testid="h-index"]',  # Possível atributo data
            'td[class*="h_index"]',  # Classe que contenha h_index
        ]
        
        for selector in modern_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"🔍 Tentando seletor {selector}: {len(elements)} elementos")
                for i, elem in enumerate(elements):
                    text = elem.get_text(strip=True)
                    print(f"  Elemento {i}: '{text}'")
                    if text.replace(',', '').isdigit():
                        h_value = int(text.replace(',', ''))
                        if 1 <= h_value <= 500:
                            print(f"🎯 H-index encontrado via {selector}: {text}")
                            return text
        
        # Estratégia 3: Usar posição conhecida mas com validação rigorosa
        stats_elements = soup.select('.gsc_rsb_std')
        print(f"🔍 Elementos de estatísticas encontrados: {[elem.get_text(strip=True) for elem in stats_elements[:6]]}")
        
        if len(stats_elements) >= 4:
            # No Google Scholar, a estrutura típica é:
            # [0] Citações total, [1] Citações desde 2019, [2] H-index total, [3] H-index desde 2019
            try:
                citations_total = int(stats_elements[0].get_text(strip=True).replace(',', ''))
                citations_2019 = int(stats_elements[1].get_text(strip=True).replace(',', '')) if len(stats_elements) > 1 else 0
                h_index_total = int(stats_elements[2].get_text(strip=True).replace(',', '')) if len(stats_elements) > 2 else 0
                h_index_2019 = int(stats_elements[3].get_text(strip=True).replace(',', '')) if len(stats_elements) > 3 else 0
                
                print(f"📊 Análise detalhada:")
                print(f"  Citações total (pos 0): {citations_total}")
                print(f"  Citações 2019 (pos 1): {citations_2019}")
                print(f"  H-index total (pos 2): {h_index_total}")
                print(f"  H-index 2019 (pos 3): {h_index_2019}")
                
                # Validações rigorosas
                valid_h_index = None
                
                # Validar h_index_total
                if (1 <= h_index_total <= 500 and 
                    h_index_total < citations_total and 
                    h_index_total != citations_total and
                    h_index_total != citations_2019):
                    valid_h_index = h_index_total
                    print(f"✅ H-index total validado: {h_index_total}")
                
                # Se h_index_total não for válido, tentar h_index_2019
                elif (1 <= h_index_2019 <= 500 and 
                      h_index_2019 < citations_2019 and 
                      h_index_2019 != citations_total and
                      h_index_2019 != citations_2019):
                    valid_h_index = h_index_2019
                    print(f"✅ H-index 2019 validado: {h_index_2019}")
                
                if valid_h_index:
                    return str(valid_h_index)
                else:
                    print(f"❌ Nenhum H-index válido encontrado. Valores suspeitos:")
                    print(f"  H-index total: {h_index_total} (muito grande? = citações?)")
                    print(f"  H-index 2019: {h_index_2019} (muito grande? = citações?)")
                    
            except (ValueError, IndexError) as e:
                print(f"❌ Erro ao analisar valores: {e}")
        
        # Estratégia 4: Busca mais conservadora por padrões específicos
        print("🔄 Tentando busca alternativa por h-index...")
        
        # Procurar por elementos que contenham explicitamente "h-index"
        for element in soup.find_all(string=lambda text: text and 'h-index' in text.lower()):
            parent = element.parent if element.parent else None
            if parent:
                # Procurar valor numérico próximo
                next_elem = parent.find_next('.gsc_rsb_std')
                if next_elem:
                    value_text = next_elem.get_text(strip=True)
                    if value_text.replace(',', '').isdigit():
                        h_value = int(value_text.replace(',', ''))
                        if 1 <= h_value <= 500:
                            print(f"🎯 H-index encontrado por busca textual: {value_text}")
                            return value_text
        
        # Estratégia 5: Buscar em qualquer parte do HTML por padrões h-index
        all_text = soup.get_text()
        import re
        h_patterns = [
            r'h-index[:\s]*(\d+)',
            r'H-index[:\s]*(\d+)',
            r'Índice h[:\s]*(\d+)',
            r'h index[:\s]*(\d+)'
        ]
        
        for pattern in h_patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            for match in matches:
                h_value = int(match)
                if 1 <= h_value <= 500:
                    print(f"🎯 H-index encontrado por regex: {h_value}")
                    return str(h_value)
        
        print("❌ H-index não encontrado")
        return "0"
    
    def _extract_citations(self, soup: BeautifulSoup) -> str:
        """Extrair total de citações com debug"""
        print("🔍 BUSCANDO CITAÇÕES...")
        
        # Primeiro elemento da tabela de estatísticas (geralmente citações)
        citations_elem = soup.select_one('.gsc_rsb_std')
        if citations_elem:
            citations_value = citations_elem.get_text(strip=True)
            print(f"🎯 Citações encontradas: {citations_value}")
            return citations_value
        
        print("❌ Citações não encontradas")
        return "0"
    
    def _extract_i10_index(self, soup: BeautifulSoup) -> str:
        """Extrair i10-index com debug detalhado"""
        print("🔍 BUSCANDO I10-INDEX...")
        
        # Estratégia 1: Buscar especificamente por i10-index na estrutura da tabela
        table_rows = soup.select('.gsc_rsb_st')
        print(f"🔍 Linhas da tabela encontradas: {len(table_rows)}")
        
        for i, row in enumerate(table_rows):
            cells = row.select('td')
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True).lower()
                value = cells[1].get_text(strip=True)
                print(f"📋 Linha {i}: {label} = {value}")
                
                # Procurar especificamente por i10-index
                if 'i10' in label and value.replace(',', '').isdigit():
                    i10_value = int(value.replace(',', ''))
                    if 0 <= i10_value <= 1000:  # Validação de range razoável
                        print(f"🎯 i10-index encontrado na tabela: {value}")
                        return value
        
        # Estratégia 2: Usar posição conhecida na estrutura típica do Scholar
        stats_elements = soup.select('.gsc_rsb_std')
        print(f"🔍 Elementos de estatísticas: {[elem.get_text(strip=True) for elem in stats_elements[:6]]}")
        
        if len(stats_elements) >= 6:
            # No Google Scholar, a estrutura típica é:
            # [0] Citações total, [1] Citações desde 2019, [2] H-index total, [3] H-index desde 2019, [4] i10-index total, [5] i10-index desde 2019
            try:
                i10_total = int(stats_elements[4].get_text(strip=True).replace(',', ''))
                i10_2019 = int(stats_elements[5].get_text(strip=True).replace(',', '')) if len(stats_elements) > 5 else 0
                
                print(f"📊 Análise i10-index:")
                print(f"  i10-index total (pos 4): {i10_total}")
                print(f"  i10-index 2019 (pos 5): {i10_2019}")
                
                # Validar i10-index total
                if 0 <= i10_total <= 1000:
                    print(f"✅ i10-index total validado: {i10_total}")
                    return str(i10_total)
                
                # Se i10_total não for válido, tentar i10_2019
                elif 0 <= i10_2019 <= 1000:
                    print(f"✅ i10-index 2019 validado: {i10_2019}")
                    return str(i10_2019)
                    
            except (ValueError, IndexError) as e:
                print(f"❌ Erro ao analisar i10-index: {e}")
        
        # Estratégia 3: Busca textual por "i10"
        print("🔄 Tentando busca alternativa por i10-index...")
        
        # Procurar por elementos que contenham explicitamente "i10"
        for element in soup.find_all(string=lambda text: text and 'i10' in text.lower()):
            parent = element.parent if element.parent else None
            if parent:
                # Procurar valor numérico próximo
                next_elem = parent.find_next('.gsc_rsb_std')
                if next_elem:
                    value_text = next_elem.get_text(strip=True)
                    if value_text.replace(',', '').isdigit():
                        i10_value = int(value_text.replace(',', ''))
                        if 0 <= i10_value <= 1000:
                            print(f"🎯 i10-index encontrado por busca textual: {value_text}")
                            return value_text
        
        print("❌ i10-index não encontrado")
        return "0"
    
    def _extract_publications_with_pagination(self, scholar_url: str, max_publications: int = 20) -> List[Dict[str, Any]]:
        """Extrair publicações com suporte a paginação"""
        print(f"📚 EXTRAINDO {max_publications} PUBLICAÇÕES COM PAGINAÇÃO...")
        
        # Armazenar número solicitado para uso no fallback
        self.requested_publications = max_publications
        
        all_publications = []
        current_start = 0
        publications_per_page = 20
        
        # Extrair o user ID da URL para construir URLs de paginação
        user_id = None
        if "user=" in scholar_url:
            user_id = scholar_url.split("user=")[1].split("&")[0]
        
        if not user_id:
            print("❌ Não foi possível extrair user ID da URL")
            return self._extract_publications_single_page(scholar_url)
        
        while len(all_publications) < max_publications:
            try:
                # Construir URL para a página específica
                if current_start == 0:
                    # Primeira página - usar URL original
                    page_url = scholar_url
                else:
                    # Páginas subsequentes
                    page_url = f"https://scholar.google.com/citations?user={user_id}&cstart={current_start}&pagesize={publications_per_page}"
                
                print(f"📄 Carregando página com start={current_start}: {page_url}")
                
                # Aguardar entre requisições para evitar bloqueio
                if current_start > 0:
                    time.sleep(random.uniform(3, 5))
                
                response = self.session.get(page_url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extrair publicações desta página
                page_publications = self._extract_publications_from_soup(soup)
                
                if not page_publications:
                    print(f"📄 Nenhuma publicação encontrada na página {current_start//publications_per_page + 1}")
                    break
                
                print(f"📄 Encontradas {len(page_publications)} publicações na página")
                
                # Adicionar apenas as publicações necessárias
                remaining_needed = max_publications - len(all_publications)
                publications_to_add = page_publications[:remaining_needed]
                all_publications.extend(publications_to_add)
                
                # Se esta página trouxe menos que o esperado, provavelmente chegamos ao fim
                if len(page_publications) < publications_per_page:
                    print(f"📄 Última página detectada (apenas {len(page_publications)} publicações)")
                    break
                
                # Se já temos o suficiente, parar
                if len(all_publications) >= max_publications:
                    break
                
                # Preparar para próxima página
                current_start += publications_per_page
                
            except Exception as e:
                print(f"❌ Erro ao carregar página {current_start//publications_per_page + 1}: {e}")
                break
        
        print(f"✅ Total de {len(all_publications)} publicações extraídas")
        return all_publications[:max_publications]  # Garantir que não exceda o limite
    
    def _extract_publications_single_page(self, scholar_url: str) -> List[Dict[str, Any]]:
        """Fallback: extrair publicações de uma única página"""
        try:
            response = self.session.get(scholar_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            return self._extract_publications_from_soup(soup)
        except Exception as e:
            print(f"❌ Erro ao extrair página única: {e}")
            return []
    
    def _extract_publications_from_soup(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extrair publicações de um soup BeautifulSoup"""
        publications = []
        
        # Múltiplos seletores para tentar (Google Scholar pode mudar a estrutura)
        selectors_to_try = [
            '.gsc_a_tr',           # Seletor original
            'tr.gsc_a_tr',         # Mais específico
            '.gs_or_cit',          # Alternativo 1
            '.gs_ri',              # Alternativo 2
            'tbody tr',            # Genérico
            '[data-aid]',          # Por atributo
            '.publication-item',   # Possível novo
            '.result-item'         # Possível novo
        ]
        
        pub_elements = []
        for selector in selectors_to_try:
            pub_elements = soup.select(selector)
            if pub_elements:
                print(f"🔍 Elementos de publicação encontrados: {len(pub_elements)} (seletor: {selector})")
                break
        
        if not pub_elements:
            print(f"🔍 Elementos de publicação encontrados: 0")
            print("⚠️ NENHUM SELETOR FUNCIONOU - Tentando SerpAPI como fallback...")
            return self._fallback_to_serpapi()
        
        for i, pub in enumerate(pub_elements):
            try:
                # Múltiplos seletores para título
                title_selectors = ['.gsc_a_at', 'a.gsc_a_at', '.gs_rt a', 'h3 a', '.title-link']
                title_elem = None
                for title_selector in title_selectors:
                    title_elem = pub.select_one(title_selector)
                    if title_elem:
                        break
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    
                    # Múltiplos seletores para ano
                    year_selectors = ['.gsc_a_h', '.gsc_a_y', '.gs_fl', '.year']
                    year = None
                    for year_selector in year_selectors:
                        year_elem = pub.select_one(year_selector)
                        if year_elem:
                            year_text = year_elem.get_text(strip=True)
                            try:
                                year = int(year_text) if year_text.isdigit() else None
                                if year:
                                    break
                            except:
                                continue
                    
                    # Múltiplos seletores para citações
                    citations_selectors = ['.gsc_a_c', '.gs_fl a', '.citations']
                    citations = 0
                    for cit_selector in citations_selectors:
                        citations_elem = pub.select_one(cit_selector)
                        if citations_elem:
                            cit_text = citations_elem.get_text(strip=True)
                            try:
                                citations = int(cit_text) if cit_text.isdigit() else 0
                                break
                            except:
                                continue
                    
                    # Extrair venue/journal - melhor seletor
                    venue_elem = pub.select_one('.gs_gray')
                    venue_text = venue_elem.get_text(strip=True) if venue_elem else "Não especificado"
                    
                    # Separar autores e revista do campo venue
                    authors = venue_text  # Por padrão, venue contém autores + revista
                    journal = venue_text  # Para compatibilidade
                    
                    # Tentar separar autores da revista (formato comum: "Autores - Revista, Ano")
                    if " - " in venue_text:
                        parts = venue_text.split(" - ", 1)
                        authors = parts[0].strip()
                        journal = parts[1].strip() if len(parts) > 1 else venue_text
                    
                    publications.append({
                        "title": title,
                        "venue": journal,  # Revista/periódico
                        "authors": authors,  # Lista de autores
                        "year": year,
                        "citations": citations,
                        "type": "Artigo",
                        "platform": "scholar"
                    })
                    
            except Exception as e:
                print(f"❌ Erro ao processar publicação {i}: {e}")
                continue
        
        return publications
    
    def _fallback_to_serpapi(self) -> List[Dict[str, Any]]:
        """Fallback para SerpAPI quando scraping direto falha"""
        try:
            print("🔄 ATIVANDO FALLBACK SERPAPI...")
            
            # Importar SerpAPI
            from serpapi import GoogleSearch
            import os
            
            # Carregar chave da API
            api_key = os.getenv("API_KEY") or os.getenv("SERPAPI_KEY") or "cf9d570296f13373cb9d7e7d592b5cea456e756748bea542232bcc05c28a5e1a"
            if not api_key:
                print("❌ SerpAPI key não encontrada - fallback não disponível")
                return []
            
            # Extrair author ID da URL atual se disponível
            author_id = None
            query = "machine learning"  # Query padrão
            
            if self.current_url and "user=" in self.current_url:
                try:
                    author_id = self.current_url.split("user=")[1].split("&")[0]
                    # Para perfis específicos, fazer busca por author ID usando SerpAPI
                    params = {
                        "api_key": api_key,
                        "engine": "google_scholar_author",
                        "author_id": author_id,
                        "hl": "pt-BR",
                        "num": min(100, max(20, getattr(self, 'requested_publications', 20)))  # Usar número solicitado ou padrão
                    }
                    print(f"🎯 Usando Author ID: {author_id}")
                except:
                    # Se falhar em extrair ID, usar busca geral
                    params = {
                        "api_key": api_key,
                        "engine": "google_scholar",
                        "q": query,
                        "hl": "pt-BR", 
                        "num": 20
                    }
            else:
                # Busca geral
                params = {
                    "api_key": api_key,
                    "engine": "google_scholar",
                    "q": query,
                    "hl": "pt-BR",
                    "num": 20
                }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            if 'error' in results:
                print(f"❌ Erro SerpAPI: {results['error']}")
                return []
            
            # Para author search, usar articles
            if author_id and "articles" in results:
                articles = results.get("articles", [])
                publications = []
                
                # NOVA PARTE: Capturar dados do perfil do autor quando disponível
                if 'author' in results:
                    author_info = results['author']
                    print("📊 CAPTURANDO DADOS DO PERFIL VIA SERPAPI...")
                    
                    # Extrair e armazenar dados do autor para uso posterior
                    self.serpapi_author_data = {
                        'name': author_info.get('name', 'Nome não encontrado'),
                        'affiliation': author_info.get('affiliations', 'Afiliação não encontrada'),
                        'email': author_info.get('email', ''),
                        'interests': author_info.get('interests', [])
                    }
                    
                    # Tentar capturar índices se disponíveis
                    if 'cited_by' in author_info:
                        cited_by_info = author_info['cited_by']
                        if 'graph' in cited_by_info:
                            # Alguns perfis têm gráfico de citações com anos
                            years_data = cited_by_info['graph']
                            if years_data:
                                total_citations = sum(int(year.get('citations', 0)) for year in years_data)
                                self.serpapi_author_data['total_citations'] = str(total_citations)
                        
                        # Tabela de índices se disponível
                        if 'table' in cited_by_info:
                            table = cited_by_info['table']
                            for row in table:
                                if 'h_index' in row:
                                    self.serpapi_author_data['h_index'] = str(row['h_index'].get('all', '0'))
                                if 'i10_index' in row:
                                    self.serpapi_author_data['i10_index'] = str(row['i10_index'].get('all', '0'))
                    
                    print(f"👤 Nome: {self.serpapi_author_data.get('name', 'N/A')}")
                    print(f"🏛️ Afiliação: {self.serpapi_author_data.get('affiliation', 'N/A')}")
                    print(f"📊 H-index: {self.serpapi_author_data.get('h_index', '0')}")
                    print(f"📊 i10-index: {self.serpapi_author_data.get('i10_index', '0')}")
                    print(f"📈 Citações: {self.serpapi_author_data.get('total_citations', '0')}")
                
                for article in articles:
                    publications.append({
                        "title": article.get("title", "Título não disponível"),
                        "venue": article.get("publication", "Venue não especificada"),
                        "authors": article.get("authors", "Autores não especificados"),
                        "year": article.get("year"),
                        "citations": article.get("cited_by", {}).get("value", 0) if article.get("cited_by") else 0,
                        "type": "Artigo",
                        "platform": "scholar_serpapi"
                    })
                
                print(f"✅ SerpAPI (Author) retornou {len(publications)} publicações")
                return publications
            
            # Para busca geral, usar organic_results
            organic_results = results.get("organic_results", [])
            publications = []
            
            for result in organic_results:
                publications.append({
                    "title": result.get("title", "Título não disponível"),
                    "venue": result.get("publication_info", {}).get("summary", "Venue não especificada"),
                    "authors": result.get("authors", "Autores não especificados"),
                    "year": result.get("year"),
                    "citations": result.get("inline_links", {}).get("cited_by", {}).get("total", 0) if result.get("inline_links") else 0,
                    "type": "Artigo", 
                    "platform": "scholar_serpapi"
                })
            
            print(f"✅ SerpAPI fallback retornou {len(publications)} publicações")
            return publications
            
        except Exception as e:
            print(f"❌ Erro no fallback SerpAPI: {e}")
            return []

    def _extract_publications(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Método legado - manter compatibilidade"""
        return self._extract_publications_from_soup(soup)[:20]

# ==================== ENDPOINTS ====================

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API Real funcionando!"}

@app.get("/")
async def api_info():
    """
    📋 Informações da API com nova arquitetura separada
    """
    return {
        "title": "API Real de Scraping Acadêmico - VERSÃO MODULAR",
        "version": "8.0.0",
        "description": "Extração real de dados com separação completa de Lattes e ORCID",
        "status": "online",
        "separated_apis": SEPARATED_APIS_AVAILABLE,
        "new_endpoints": {
            "lattes": {
                "search_researchers": "/api/lattes/search/researchers",
                "profile_by_url": "/api/lattes/profile/by-url",
                "profile_by_id": "/api/lattes/profile/by-id",
                "health": "/api/lattes/health",
                "stats": "/api/lattes/stats"
            },
            "orcid": {
                "search_researchers": "/api/orcid/search/researchers",
                "search_by_keyword": "/api/orcid/search/by-keyword",
                "search_by_affiliation": "/api/orcid/search/by-affiliation",
                "profile_by_url": "/api/orcid/profile/by-url",
                "profile_by_id": "/api/orcid/profile/by-id/{orcid_id}",
                "health": "/api/orcid/health",
                "stats": "/api/orcid/stats"
            }
        },
        "workflow": {
            "step_1": "Use endpoints de busca (/search/researchers)",
            "step_2": "Copie o link do perfil desejado",
            "step_3": "Use endpoints de perfil (/profile/by-url) para obter dados completos",
            "step_4": "Exporte os dados conforme necessário"
        },
        "features": {
            "separated_scrapers": True,
            "copy_link_buttons": True,
            "comprehensive_profiles": True,
            "multiple_search_strategies": True,
            "export_capabilities": True,
            "mongodb_integration": MONGODB_AVAILABLE
        },
        "legacy_endpoints": "Mantidos para compatibilidade",
        "documentation": "/docs",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/search/topic/scholar")
@app.get("/search/author/profile")
@app.post("/search/author/profile")
async def search_profile(
    query: str = Query("", description="Nome do autor ou query"),
    profile_url: str = Query(None, description="URL do perfil"),
    platforms: str = Query("all", description="Plataformas"),
    export_excel: bool = Query(False, description="Exportar Excel"),
    filter_keywords: bool = Query(True, description="Filtrar por palavras-chave relacionadas ao envelhecimento"),
    max_publications: int = Query(20, description="Número máximo de publicações a extrair (padrão: 20)")
):
    """Endpoint principal para extração real de dados"""
    
    url_to_process = profile_url or query
    print(f"🔍 PROCESSANDO: {url_to_process}")
    print(f"📚 Máximo de publicações solicitadas: {max_publications}")
    
    try:
        # Detectar plataforma pela URL
        if "lattes.cnpq.br" in url_to_process:
            print("🇧🇷 DETECTADO: LATTES")
            extractor = LattesExtractor()
            data = extractor.extract_profile(url_to_process)
            
            if data.get("success"):
                result = {
                    "success": True,
                    "message": f"Dados extraídos do Lattes: {data['name']}",
                    "platform": "lattes",
                    "search_type": "profile",
                    "query": data["name"],  # Adicionar o nome do pesquisador como query
                    "total_results": data.get("total_publications", 0),
                    "execution_time": 3.0,
                    "researcher_info": {
                        "name": data["name"],
                        "institution": data["institution"],
                        "research_areas": data["research_areas"],
                        "last_update": data["last_update"]
                    },
                    "data": {
                        "publications": [
                            {
                                "title": pub["title"],
                                "authors": data["name"],
                                "publication": pub["venue"],
                                "year": pub["year"],
                                "cited_by": 0,
                                "link": url_to_process,
                                "snippet": f"Publicação de {data['name']}",
                                "platform": "lattes",
                                "type": pub["type"],
                                "issn": "N/A",
                                "volume": "N/A",
                                "pages": "N/A",
                                "doi": "N/A",
                                "qualis": "N/A"
                            }
                            for pub in data["publications"]
                        ]
                    }
                }
                
                
                # Aplicar filtro por keywords se solicitado
                if filter_keywords:
                    from src.export.excel_exporter import ProfessionalExcelExporter
                    exporter = ProfessionalExcelExporter()
                    
                    # Filtrar publicações
                    original_publications = result["data"]["publications"]
                    filtered_publications = exporter._filter_publications_by_keywords(original_publications)
                    
                    # Atualizar resultado com publicações filtradas
                    result["data"]["publications"] = filtered_publications
                    result["total_results"] = len(filtered_publications)
                    result["filtered_by_keywords"] = True
                    result["original_total"] = len(original_publications)
                    
                    print(f"🔍 Filtro aplicado: {len(original_publications)} -> {len(filtered_publications)} publicações")
                
                # Verificar se deve exportar para Excel
                if export_excel and result["data"]["publications"]:
                    try:
                        from src.export.excel_exporter import ProfessionalExcelExporter
                        exporter = ProfessionalExcelExporter()
                        filename = exporter.export_api_data(result, filter_by_keywords=filter_keywords)
                        result["excel_file"] = filename
                        print(f"📊 Excel exportado: {filename} (publicações: {len(result['data']['publications'])})")
                    except Exception as e:
                        print(f"❌ Erro na exportação Excel: {e}")
                        result["excel_error"] = str(e)
                
                # Salvar no MongoDB se filtrado por keywords
                save_to_mongodb_if_filtered(result, filter_keywords)
                
                return result
            else:
                return {
                    "success": False,
                    "message": f"Erro ao extrair Lattes: {data.get('error', 'Erro desconhecido')}",
                    "platform": "lattes",
                    "error_details": data
                }
        
        elif "orcid.org" in url_to_process:
            print("🌐 DETECTADO: ORCID")
            extractor = ORCIDExtractor()
            data = extractor.extract_profile(url_to_process)
            
            if data.get("success"):
                result = {
                    "success": True,
                    "message": f"Dados extraídos do ORCID: {data['name']}",
                    "platform": "orcid",
                    "search_type": "profile",
                    "query": data["name"],  # Adicionar o nome do pesquisador como query
                    "total_results": data.get("total_works", 0),
                    "execution_time": 2.0,
                    "researcher_info": {
                        "name": data["name"],
                        "orcid_id": data["orcid_id"],
                        "institution": data["affiliation"]
                    },
                    "data": {
                        "publications": [
                            {
                                "title": work["title"],
                                "authors": data["name"],
                                "publication": work["journal"],
                                "year": work["year"],
                                "cited_by": 0,
                                "link": url_to_process,
                                "snippet": f"Trabalho de {data['name']}",
                                "platform": "orcid",
                                "type": work["type"],
                                "issn": "N/A",
                                "volume": "N/A",
                                "pages": "N/A",
                                "doi": "N/A",
                                "qualis": "N/A"
                            }
                            for work in data["works"]
                        ]
                    }
                }
                
                
                # Aplicar filtro por keywords se solicitado
                if filter_keywords:
                    from src.export.excel_exporter import ProfessionalExcelExporter
                    exporter = ProfessionalExcelExporter()
                    
                    # Filtrar publicações
                    original_publications = result["data"]["publications"]
                    filtered_publications = exporter._filter_publications_by_keywords(original_publications)
                    
                    # Atualizar resultado com publicações filtradas
                    result["data"]["publications"] = filtered_publications
                    result["total_results"] = len(filtered_publications)
                    result["filtered_by_keywords"] = True
                    result["original_total"] = len(original_publications)
                    
                    print(f"🔍 Filtro aplicado: {len(original_publications)} -> {len(filtered_publications)} publicações")
                
                # Verificar se deve exportar para Excel
                if export_excel and result["data"]["publications"]:
                    try:
                        from src.export.excel_exporter import ProfessionalExcelExporter
                        exporter = ProfessionalExcelExporter()
                        filename = exporter.export_api_data(result, filter_by_keywords=filter_keywords)
                        result["excel_file"] = filename
                        print(f"📊 Excel exportado: {filename} (publicações: {len(result['data']['publications'])})")
                    except Exception as e:
                        print(f"❌ Erro na exportação Excel: {e}")
                        result["excel_error"] = str(e)
                
                # Salvar no MongoDB se filtrado por keywords
                save_to_mongodb_if_filtered(result, filter_keywords)
                
                return result
            else:
                return {
                    "success": False,
                    "message": f"Erro ao extrair ORCID: {data.get('error', 'Erro desconhecido')}",
                    "platform": "orcid",
                    "error_details": data
                }
        
        elif "scholar.google.com" in url_to_process:
            print("🎓 DETECTADO: SCHOLAR PROFILE")
            extractor = ScholarExtractor()
            data = extractor.extract_profile(url_to_process, max_publications)
            
            if data.get("success"):
                result = {
                    "success": True,
                    "message": f"Dados extraídos do Scholar: {data['name']}",
                    "platform": "scholar",
                    "search_type": "profile",
                    "query": data["name"],  # Adicionar o nome do pesquisador como query
                    "total_results": data.get("total_publications", 0),
                    "execution_time": 4.0,
                    "researcher_info": {
                        "name": data["name"],
                        "institution": data["affiliation"],
                        "h_index": data["h_index"],
                        "i10_index": data.get("i10_index", "0"),
                        "total_citations": data["total_citations"]
                    },
                    "data": {
                        "publications": [
                            {
                                "title": pub["title"],
                                "authors": pub.get("authors", data["name"]),  # Usar campo authors separado
                                "publication": pub.get("venue", "N/A"),  # Usar venue para revista
                                "year": pub["year"],
                                "cited_by": pub["citations"],
                                "link": url_to_process,
                                "snippet": f"Publicação de {data['name']}",
                                "platform": "scholar",
                                "type": "article",
                                "issn": "N/A",
                                "volume": "N/A",
                                "pages": "N/A",
                                "doi": "N/A",
                                "qualis": "N/A"
                            }
                            for pub in data["publications"]
                        ]
                    }
                }
                
                
                # Aplicar filtro por keywords se solicitado
                if filter_keywords:
                    from src.export.excel_exporter import ProfessionalExcelExporter
                    exporter = ProfessionalExcelExporter()
                    
                    # Filtrar publicações
                    original_publications = result["data"]["publications"]
                    filtered_publications = exporter._filter_publications_by_keywords(original_publications)
                    
                    # Atualizar resultado com publicações filtradas
                    result["data"]["publications"] = filtered_publications
                    result["total_results"] = len(filtered_publications)
                    result["filtered_by_keywords"] = True
                    result["original_total"] = len(original_publications)
                    
                    print(f"🔍 Filtro aplicado: {len(original_publications)} -> {len(filtered_publications)} publicações")
                
                # Verificar se deve exportar para Excel
                if export_excel and result["data"]["publications"]:
                    try:
                        from src.export.excel_exporter import ProfessionalExcelExporter
                        exporter = ProfessionalExcelExporter()
                        filename = exporter.export_api_data(result, filter_by_keywords=filter_keywords)
                        result["excel_file"] = filename
                        print(f"📊 Excel exportado: {filename} (publicações: {len(result['data']['publications'])})")
                    except Exception as e:
                        print(f"❌ Erro na exportação Excel: {e}")
                        result["excel_error"] = str(e)
                
                # Salvar no MongoDB se filtrado por keywords
                save_to_mongodb_if_filtered(result, filter_keywords)
                
                return result
            else:
                return {
                    "success": False,
                    "message": f"Erro ao extrair Scholar: {data.get('error', 'Erro desconhecido')}",
                    "platform": "scholar",
                    "error_details": data
                }
        
        else:
            # Detectar se é um nome para busca - tentar primeiro Lattes, depois Scholar
            print("🔍 DETECTADO: BUSCA POR NOME")
            print(f"📚 Tentando primeiro no Lattes, depois Scholar se necessário")
            
            # Primeiro tentar no Lattes (para pesquisadores brasileiros)
            lattes_extractor = LattesExtractor()
            data = lattes_extractor.search_by_name(url_to_process)
            
            # Se não encontrou no Lattes, tentar no Scholar
            if not data.get("success"):
                print("⚠️ Não encontrado no Lattes, tentando Scholar...")
                extractor = ScholarExtractor()
                data = extractor.search_author(url_to_process, max_publications)
            
            # Se a busca por nome falhou, tentar busca de publicações como alternativa
            if not data.get("success"):
                print("⚠️ Busca por autor falhou (Google Scholar bloqueou), tentando busca por publicações...")
                try:
                    # Usar a busca por publicações para encontrar trabalhos do autor
                    search_publications_url = f"https://scholar.google.com/scholar?q=author:\"{url_to_process}\""
                    print(f"🔗 Tentativa alternativa: {search_publications_url}")
                    
                    time.sleep(random.uniform(2, 4))
                    pub_response = extractor.session.get(search_publications_url, timeout=20)
                    
                    if pub_response.status_code == 200 and 'accounts.google.com' not in pub_response.url:
                        pub_soup = BeautifulSoup(pub_response.content, 'html.parser')
                        
                        # Extrair publicações da busca
                        publications = []
                        results = pub_soup.select('.gs_r.gs_or.gs_scl')[:max_publications]
                        
                        print(f"📚 Encontradas {len(results)} publicações na busca alternativa")
                        
                        for result in results:
                            title_elem = result.select_one('.gs_rt a, h3 a')
                            authors_elem = result.select_one('.gs_a')
                            year_elem = result.select_one('.gs_a')
                            
                            if title_elem:
                                title = title_elem.get_text(strip=True)
                                
                                # Extrair ano da string de autores
                                year = "N/A"
                                if year_elem:
                                    year_text = year_elem.get_text()
                                    year_match = re.search(r'(\d{4})', year_text)
                                    if year_match:
                                        year = year_match.group(1)
                                
                                # Extrair autores
                                authors = url_to_process  # Nome pesquisado como autor principal
                                if authors_elem:
                                    authors_text = authors_elem.get_text(strip=True)
                                    # Pegar a parte antes do ano como autores
                                    if ' - ' in authors_text:
                                        authors = authors_text.split(' - ')[0]
                                
                                publications.append({
                                    "title": title,
                                    "authors": authors,
                                    "year": year,
                                    "citations": 0,
                                    "type": "article",
                                    "venue": "Google Scholar Search"
                                })
                        
                        if publications:
                            data = {
                                "success": True,
                                "name": url_to_process,
                                "affiliation": "Instituição não identificada (busca por publicações)",
                                "h_index": "N/A",
                                "i10_index": "N/A", 
                                "total_citations": "N/A",
                                "publications": publications,
                                "total_publications": len(publications)
                            }
                            print(f"✅ Busca alternativa por publicações encontrou {len(publications)} resultados")
                        else:
                            print("❌ Busca alternativa por publicações não retornou resultados")
                    else:
                        print("❌ Busca alternativa por publicações também foi bloqueada")
                        
                except Exception as e:
                    print(f"❌ Erro na busca alternativa: {e}")
            
            if data.get("success"):
                # Detectar se os dados vêm do Lattes ou Scholar
                is_lattes_data = "research_areas" in data or "institution" in data
                platform = "lattes" if is_lattes_data else "scholar"
                
                if is_lattes_data:
                    # Dados do Lattes
                    result = {
                        "success": True,
                        "message": f"Dados extraídos do Lattes: {data['name']}",
                        "platform": "lattes",
                        "search_type": "name_search",
                        "query": url_to_process,
                        "total_results": data.get("total_publications", 0),
                        "execution_time": 3.0,
                        "researcher_info": {
                            "name": data["name"],
                            "institution": data["institution"],
                            "research_areas": data["research_areas"],
                            "last_update": data["last_update"]
                        },
                        "data": {
                            "publications": [
                                {
                                    "title": pub["title"],
                                    "authors": data["name"],
                                    "publication": pub["venue"],
                                    "year": pub["year"],
                                    "cited_by": 0,
                                    "link": None,
                                    "snippet": f"Publicação de {data['name']}",
                                    "platform": "lattes",
                                    "type": pub["type"],
                                    "issn": "N/A",
                                    "volume": "N/A", 
                                    "pages": "N/A",
                                    "doi": "N/A",
                                    "qualis": "N/A"
                                }
                                for pub in data["publications"]
                            ]
                        }
                    }
                else:
                    # Dados do Scholar
                    result = {
                        "success": True,
                        "message": f"Dados extraídos do Scholar: {data['name']}",
                        "platform": "scholar",
                        "search_type": "author",
                        "query": url_to_process,  # Nome pesquisado como query
                        "total_results": data.get("total_publications", 0),
                        "execution_time": 4.0,
                        "researcher_info": {
                            "name": data["name"],
                            "institution": data.get("affiliation", "N/A"),
                            "h_index": data.get("h_index", "N/A"),
                            "i10_index": data.get("i10_index", "0"),
                            "total_citations": data.get("total_citations", "N/A")
                        },
                    "data": {
                        "publications": [
                            {
                                "title": pub["title"],
                                "authors": pub.get("authors", data["name"]),  # Usar campo authors separado
                                "publication": pub.get("venue", "Google Scholar"),  # Usar venue para revista
                                "year": pub["year"],
                                "cited_by": pub["citations"],
                                "link": None,
                                "snippet": f"Artigo de {data['name']}",
                                "platform": "scholar",
                                "type": pub["type"],
                                "issn": "N/A",
                                "volume": "N/A",
                                "pages": "N/A",
                                "doi": "N/A",
                                "qualis": "N/A"
                            }
                            for pub in data["publications"]
                        ]
                    }
                }
                
                
                # Aplicar filtro por keywords se solicitado
                if filter_keywords:
                    from src.export.excel_exporter import ProfessionalExcelExporter
                    exporter = ProfessionalExcelExporter()
                    
                    # Filtrar publicações
                    original_publications = result["data"]["publications"]
                    filtered_publications = exporter._filter_publications_by_keywords(original_publications)
                    
                    # Atualizar resultado com publicações filtradas
                    result["data"]["publications"] = filtered_publications
                    result["total_results"] = len(filtered_publications)
                    result["filtered_by_keywords"] = True
                    result["original_total"] = len(original_publications)
                    
                    print(f"🔍 Filtro aplicado: {len(original_publications)} -> {len(filtered_publications)} publicações")
                
                # Verificar se deve exportar para Excel
                if export_excel and result["data"]["publications"]:
                    try:
                        from src.export.excel_exporter import ProfessionalExcelExporter
                        exporter = ProfessionalExcelExporter()
                        filename = exporter.export_api_data(result, filter_by_keywords=filter_keywords)
                        result["excel_file"] = filename
                        print(f"📊 Excel exportado: {filename} (publicações: {len(result['data']['publications'])})")
                    except Exception as e:
                        print(f"❌ Erro na exportação Excel: {e}")
                        result["excel_error"] = str(e)
                
                # Salvar no MongoDB se filtrado por keywords
                save_to_mongodb_if_filtered(result, filter_keywords)
                
                return result
            else:
                # Determinar se tentou Lattes ou Scholar primeiro
                platform_attempted = "lattes" if "research_areas" in str(data) or "institution" in str(data) else "scholar"
                
                if platform_attempted == "lattes":
                    message = f"Pesquisador '{url_to_process}' não encontrado no Lattes nem no Scholar"
                    suggestion = "Dica: Para buscar no Lattes, use a URL direta do perfil (ex: http://lattes.cnpq.br/1234567890123456). Para Scholar, use URLs diretas de perfil ou verifique se o pesquisador tem perfil público."
                else:
                    message = f"Pesquisador '{url_to_process}' não encontrado (Google Scholar pode estar bloqueando buscas automáticas)"
                    suggestion = "Dica: Use URLs diretas de perfil do Scholar (https://scholar.google.com/citations?user=XXXXXXX) ou do Lattes (http://lattes.cnpq.br/XXXXXXXXXXXXXXXX)"
                
                return {
                    "success": False,
                    "message": message,
                    "platform": platform_attempted,
                    "error_details": data,
                    "suggestion": suggestion,
                    "help": {
                        "lattes_example": "http://lattes.cnpq.br/1234567890123456",
                        "scholar_example": "https://scholar.google.com/citations?user=JicYPdAAAAAJ",
                        "how_to_find": "Acesse manualmente o Lattes ou Scholar, encontre o pesquisador e copie a URL do perfil"
                    }
                }
    
    except Exception as e:
        print(f"💥 ERRO GERAL: {e}")
        return {
            "success": False,
            "message": f"Erro interno: {str(e)}",
            "platform": "error",
            "search_type": "error",
            "total_results": 0,
            "execution_time": 1.0,
            "data": {"publications": []}
        }

# Endpoints de compatibilidade
@app.get("/search/topic/lattes")
async def search_topic_lattes(topic: str = Query(...), max_results: int = Query(10)):
    return await search_profile(query=topic)

@app.get("/search/topic/orcid")
async def search_topic_orcid(topic: str = Query(...), max_results: int = Query(10)):
    return await search_profile(query=topic)

@app.get("/search/authors/scholar")
async def search_multiple_authors(
    name: str = Query(..., description="Nome do pesquisador para buscar múltiplos autores"),
    max_results: int = Query(10, description="Número máximo de autores a retornar")
):
    """Endpoint para buscar múltiplos autores no Google Scholar"""
    try:
        print(f"🔍 Buscando múltiplos autores: {name}")
        
        # Importar o novo serviço
        from .services.scholar_authors_service import GoogleScholarAuthorsService
        
        # Executar busca
        service = GoogleScholarAuthorsService()
        authors = service.search_authors_by_name(name, max_results)
        
        if not authors:
            return {
                "success": False,
                "message": f"Nenhum autor encontrado para '{name}'",
                "authors": [],
                "total_results": 0
            }
        
        return {
            "success": True,
            "message": f"Encontrados {len(authors)} autores para '{name}'",
            "query": name,
            "search_type": "multiple_authors",
            "platform": "scholar",
            "total_results": len(authors),
            "authors": authors,
            "execution_time": 3.0
        }
        
    except Exception as e:
        print(f"❌ Erro na busca de múltiplos autores: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/search/author/scholar")
async def search_single_author_scholar(
    author: str = Query(..., description="Nome do autor para buscar"),
    max_results: int = Query(10, description="Número máximo de publicações"),
    export_excel: bool = Query(False, description="Exportar para Excel")
):
    """Endpoint para buscar um autor específico no Google Scholar"""
    try:
        print(f"🔍 Buscando autor individual: {author}")
        
        # Importar serviço
        from .services.services import GoogleScholarService
        
        # Executar busca
        service = GoogleScholarService()
        author_profile, publications = service.search_by_author_profile(author)
        
        # Limitar publicações se necessário
        if len(publications) > max_results:
            publications = publications[:max_results]
        
        # Estruturar resposta no formato esperado pelo frontend
        result = {
            "success": True,
            "message": f"Encontradas {len(publications)} publicações para '{author}'",
            "query": author,
            "search_type": "author",
            "platform": "scholar",
            "total_results": len(publications),
            "execution_time": 2.0,
            # Dados estruturados como o frontend espera
            "data": {
                "publications": [pub.dict() for pub in publications],
                "author_profile": author_profile.dict() if author_profile else None
            },
            # Também manter compatibilidade com outros formatos
            "publications": [pub.dict() for pub in publications],
            "author_profile": author_profile.dict() if author_profile else None,
            # Informações do pesquisador para exibição
            "researcher_info": {
                "name": author_profile.name if author_profile else author,
                "institution": author_profile.affiliation if (author_profile and hasattr(author_profile, 'affiliation')) else "Instituição não informada",
                "h_index": author_profile.h_index if (author_profile and hasattr(author_profile, 'h_index')) else 0,
                "total_citations": author_profile.total_citations if (author_profile and hasattr(author_profile, 'total_citations')) else 0,
            } if author_profile else {
                "name": author,
                "institution": "Instituição não informada",
                "h_index": 0,
                "total_citations": 0
            }
        }
        
        # Se solicitado, exportar para Excel
        if export_excel and result["data"]["publications"]:
            try:
                from .export.excel_exporter import export_research_to_excel
                
                # Preparar dados para exportação
                search_data = {
                    "query": author,
                    "search_type": "author",
                    "execution_time": 2.0,
                    "platforms": ["scholar"],
                    "results_by_platform": {
                        "scholar": {
                            "author_profile": author_profile.dict() if author_profile else None,
                            "publications": [pub.dict() for pub in publications],
                            "total_results": len(publications),
                            "query": author
                        }
                    },
                    "total_authors": 1 if author_profile else 0,
                    "total_publications": len(publications),
                    "total_citations": sum([pub.cited_by for pub in publications if pub.cited_by]),
                    "max_h_index": author_profile.h_index if author_profile and hasattr(author_profile, 'h_index') else 0,
                    "top_publication_citations": max([pub.cited_by for pub in publications if pub.cited_by] + [0])
                }
                
                filename = export_research_to_excel(search_data, f"autor_{author}")
                result["excel_file"] = filename
                
            except Exception as e:
                print(f"❌ Erro na exportação Excel: {e}")
                result["excel_error"] = str(e)
        
        return result
        
    except Exception as e:
        print(f"❌ Erro na busca de autor: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/search/author/publications/{author_id}")
async def get_author_publications(
    author_id: str,
    author_name: str = Query(None, description="Nome do autor (opcional, usado se author_id for sintético)"),
    max_results: int = Query(50, description="Número máximo de publicações"),
    export_excel: bool = Query(False, description="Exportar para Excel")
):
    """Endpoint para buscar todas as publicações de um autor específico"""
    try:
        print(f"📚 Buscando publicações do autor: {author_id}")
        
        # Importar serviços necessários
        from .services.scholar_authors_service import GoogleScholarAuthorsService
        
        # Executar busca
        service = GoogleScholarAuthorsService()
        
        # Se author_name foi fornecido, usar busca por nome
        # Caso contrário, tentar usar o author_id
        if author_name:
            print(f"📚 Usando busca por nome: {author_name}")
            publications = service.get_author_publications_by_name(author_name, max_results)
            search_query = author_name
        else:
            print(f"📚 Usando busca por ID: {author_id}")
            publications = service.get_author_publications(author_id, max_results)
            search_query = author_id
        
        if not publications:
            return {
                "success": False,
                "message": f"Nenhuma publicação encontrada para o autor {search_query}",
                "publications": [],
                "total_results": 0
            }
        
        result = {
            "success": True,
            "message": f"Encontradas {len(publications)} publicações",
            "author_id": author_id,
            "author_name": author_name,
            "search_type": "author_publications",
            "platform": "scholar",
            "total_results": len(publications),
            "publications": publications,
            "execution_time": 2.0
        }
        
        # Se solicitado, exportar para Excel
        if export_excel and result["data"]["publications"]:
            try:
                from .export.excel_exporter import export_research_to_excel
                
                # Preparar dados para exportação
                search_data = {
                    "query": f"Autor {author_id}",
                    "search_type": "author_publications",
                    "execution_time": 2.0,
                    "platforms": ["scholar"],
                    "results_by_platform": {
                        "scholar": {
                            "publications": publications,
                            "total_results": len(publications),
                            "query": f"Autor {author_id}"
                        }
                    },
                    "total_authors": 1,
                    "total_publications": len(publications),
                    "total_citations": sum([pub.get("cited_by", 0) for pub in publications]),
                    "max_h_index": 0,
                    "top_publication_citations": max([pub.get("cited_by", 0) for pub in publications] + [0])
                }
                
                filename = export_research_to_excel(search_data, f"autor_{author_id}")
                result["excel_file"] = filename
                
            except Exception as e:
                print(f"❌ Erro na exportação Excel: {e}")
                result["excel_error"] = str(e)
        
        return result
        
    except Exception as e:
        print(f"❌ Erro na busca de publicações: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# ========== ENDPOINTS DE MONGODB E EXPORTAÇÃO CONSOLIDADA ==========

@app.get("/mongodb/stats")
async def get_mongodb_stats():
    """Estatísticas dos dados armazenados no MongoDB"""
    if not MONGODB_AVAILABLE:
        raise HTTPException(status_code=503, detail="MongoDB não disponível")
    
    try:
        db = ResearchDatabase()
        stats = await db.get_research_statistics_async()
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        print(f"❌ Erro ao obter estatísticas: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/mongodb/research")
async def get_all_research():
    """Obter todos os dados de pesquisa filtrados do MongoDB"""
    if not MONGODB_AVAILABLE:
        raise HTTPException(status_code=503, detail="MongoDB não disponível")
    
    try:
        db = ResearchDatabase()
        research_data = await db.get_all_keyword_filtered_research_async()
        return {
            "success": True,
            "total_records": len(research_data),
            "data": research_data
        }
    except Exception as e:
        print(f"❌ Erro ao obter dados de pesquisa: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/export/consolidated")
async def export_consolidated_excel():
    """Exportar Excel consolidado com todos os dados do Scholar no MongoDB"""
    if not MONGODB_AVAILABLE:
        raise HTTPException(status_code=503, detail="MongoDB não disponível")
    
    try:
        from src.database.excel_consolidado import ConsolidatedExcelExporter
        from fastapi.responses import FileResponse
        
        # Obter dados do MongoDB - TODOS os dados do Scholar (com ou sem filtro)
        db = ResearchDatabase()
        research_data = await db.get_all_scholar_research_async()
        
        if not research_data:
            return {
                "success": False,
                "message": "Nenhum dado do Scholar encontrado no banco.",
                "total_records": 0,
                "instructions": "Para gerar dados: faça buscas no Scholar primeiro"
            }
        
        # Exportar Excel consolidado
        exporter = ConsolidatedExcelExporter()
        filename = exporter.export_consolidated_excel(research_data)
        
        # Caminho completo do arquivo
        filepath = os.path.join(exporter.exports_dir, filename)
        
        # Verificar se o arquivo foi criado
        if not os.path.exists(filepath):
            raise HTTPException(status_code=500, detail="Arquivo Excel não foi criado")
        
        # Retornar arquivo para download
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }
        )
        
    except Exception as e:
        print(f"❌ Erro na exportação consolidada: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.delete("/mongodb/clear")
async def clear_mongodb():
    """Limpar todos os dados do MongoDB (uso com cuidado!)"""
    if not MONGODB_AVAILABLE:
        raise HTTPException(status_code=503, detail="MongoDB não disponível")
    
    try:
        db = ResearchDatabase()
        # Implementar método clear se necessário
        return {
            "success": True,
            "message": "Funcionalidade de limpeza não implementada por segurança"
        }
    except Exception as e:
        print(f"❌ Erro ao limpar dados: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/download/excel/{filename}")
async def download_excel_file(filename: str):
    """Endpoint para download de arquivos Excel gerados"""
    try:
        # Sanitizar nome do arquivo
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        # Verificar se contém apenas caracteres seguros
        import re
        if not re.match(r'^[a-zA-Z0-9_\-\.]+\.xlsx$', filename):
            raise HTTPException(status_code=400, detail="Nome de arquivo inválido")
        
        # Caminho do arquivo
        exports_dir = "exports"
        filepath = os.path.join(exports_dir, filename)
        
        # Verificar se arquivo existe
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        
        # Retornar arquivo para download
        from fastapi.responses import FileResponse
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Cache-Control": "no-cache"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro no download do Excel: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

if __name__ == "__main__":
    print("🚀 INICIANDO API REAL DE SCRAPING...")
    print("📍 API disponível em: http://localhost:8000")
    print("🔥 SCRAPING REAL ATIVADO:")
    print("  🇧🇷 Lattes: Extração completa")
    print("  🌐 ORCID: Extração completa") 
    print("  🎓 Scholar: Busca por nome")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)
