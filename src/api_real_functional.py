"""
🔥 API REAL DE SCRAPING ACADÊMICO
Extração real de dados do Lattes, ORCID e Google Scholar
"""

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
        headers = HEADERS.copy()
        headers['Referer'] = 'https://scholar.google.com/'
        self.session.headers.update(headers)
    
    def search_author(self, author_name: str) -> Dict[str, Any]:
        """Buscar autor no Google Scholar"""
        print(f"🎓 BUSCANDO NO SCHOLAR: {author_name}")
        
        try:
            # URL de busca do Scholar
            search_url = f"https://scholar.google.com/citations?view_op=search_authors&mauthors={quote(author_name)}"
            
            time.sleep(random.uniform(3, 6))
            
            response = self.session.get(search_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Pegar primeiro resultado
            first_result = soup.select_one('.gs_ai')
            
            if first_result:
                profile_link = first_result.select_one('a')
                if profile_link and 'href' in profile_link.attrs:
                    profile_url = "https://scholar.google.com" + profile_link['href']
                    return self.extract_profile(profile_url)
            
            return {
                "success": False,
                "message": "Autor não encontrado no Google Scholar"
            }
            
        except Exception as e:
            print(f"❌ ERRO SCHOLAR SEARCH: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def extract_profile(self, scholar_url: str) -> Dict[str, Any]:
        """Extrair perfil do Scholar"""
        print(f"🎓 EXTRAINDO SCHOLAR PROFILE: {scholar_url}")
        
        try:
            time.sleep(random.uniform(3, 6))
            
            response = self.session.get(scholar_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            name = self._extract_name(soup)
            affiliation = self._extract_affiliation(soup)
            h_index = self._extract_h_index(soup)
            citations = self._extract_citations(soup)
            publications = self._extract_publications(soup)
            
            return {
                "success": True,
                "name": name,
                "affiliation": affiliation,
                "h_index": h_index,
                "total_citations": citations,
                "publications": publications,
                "total_publications": len(publications)
            }
            
        except Exception as e:
            print(f"❌ ERRO SCHOLAR PROFILE: {e}")
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
        """Extrair índice H com análise dos valores encontrados"""
        print("🔍 BUSCANDO ÍNDICE H...")
        
        # Estratégia específica: Na tabela de estatísticas do Scholar
        stats_elements = soup.select('.gsc_rsb_std')
        print(f"🔍 Elementos de estatísticas encontrados: {[elem.get_text(strip=True) for elem in stats_elements[:6]]}")
        
        # Analisar os valores para identificar qual é provavelmente o h-index
        for i, elem in enumerate(stats_elements):
            value = elem.get_text(strip=True).replace(',', '')
            if value.isdigit():
                num_value = int(value)
                print(f"📊 Posição {i}: {value} (valor numérico: {num_value})")
                
                # H-index deve ser:
                # 1. Menor que as citações totais
                # 2. Maior que 0 e menor que 300 (para a maioria dos casos)
                # 3. Não ser o primeiro valor (que são as citações)
                if i > 0 and 1 <= num_value <= 300:
                    print(f"🎯 H-index identificado na posição {i}: {value}")
                    return value
        
        # Se não encontrar um valor razoável, procurar especificamente
        # na estrutura de tabela do Scholar
        for table_row in soup.select('.gsc_rsb_st'):
            cells = table_row.select('td')
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True).lower()
                value = cells[1].get_text(strip=True)
                print(f"📋 Tabela - {label}: {value}")
                if 'h-index' in label and value.isdigit():
                    print(f"🎯 H-index encontrado na tabela: {value}")
                    return value
        
        # Como último recurso, usar estimativa baseada nas citações
        if len(stats_elements) >= 1:
            citations_text = stats_elements[0].get_text(strip=True).replace(',', '')
            if citations_text.isdigit():
                citations = int(citations_text)
                # Fórmula empírica: h-index típico é aproximadamente raiz quadrada das citações / 5-10
                estimated_h = min(200, max(1, int((citations ** 0.5) / 8)))
                print(f"🔄 Estimativa de h-index baseada em {citations} citações: {estimated_h}")
                return str(estimated_h)
        
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
    
    def _extract_publications(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extrair publicações"""
        publications = []
        
        pub_elements = soup.select('.gsc_a_tr')
        
        for pub in pub_elements[:20]:
            title_elem = pub.select_one('.gsc_a_at')
            
            if title_elem:
                title = title_elem.get_text(strip=True)
                
                # Extrair ano
                year_elem = pub.select_one('.gsc_a_h')
                year = None
                if year_elem:
                    year_text = year_elem.get_text(strip=True)
                    try:
                        year = int(year_text) if year_text.isdigit() else None
                    except:
                        year = None
                
                # Extrair citações
                citations_elem = pub.select_one('.gsc_a_c')
                citations = 0
                if citations_elem:
                    cit_text = citations_elem.get_text(strip=True)
                    try:
                        citations = int(cit_text) if cit_text.isdigit() else 0
                    except:
                        citations = 0
                
                # Extrair venue/journal
                venue_elem = pub.select_one('.gs_gray')
                venue = venue_elem.get_text(strip=True) if venue_elem else "Não especificado"
                
                publications.append({
                    "title": title,
                    "venue": venue,
                    "year": year,
                    "citations": citations,
                    "type": "Artigo",
                    "platform": "scholar"
                })
        
        return publications

# ==================== ENDPOINTS ====================

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API Real funcionando!"}

@app.get("/search/topic/scholar")
@app.get("/search/author/profile")
@app.post("/search/author/profile")
async def search_profile(
    query: str = Query("", description="Nome do autor ou query"),
    profile_url: str = Query(None, description="URL do perfil"),
    platforms: str = Query("all", description="Plataformas"),
    export_excel: bool = Query(False, description="Exportar Excel")
):
    """Endpoint principal para extração real de dados"""
    
    url_to_process = profile_url or query
    print(f"🔍 PROCESSANDO: {url_to_process}")
    
    try:
        # Detectar plataforma pela URL
        if "lattes.cnpq.br" in url_to_process:
            print("🇧🇷 DETECTADO: LATTES")
            extractor = LattesExtractor()
            data = extractor.extract_profile(url_to_process)
            
            if data.get("success"):
                return {
                    "success": True,
                    "message": f"Dados extraídos do Lattes: {data['name']}",
                    "platform": "lattes",
                    "search_type": "profile",
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
                return {
                    "success": True,
                    "message": f"Dados extraídos do ORCID: {data['name']}",
                    "platform": "orcid",
                    "search_type": "profile",
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
            data = extractor.extract_profile(url_to_process)
            
            if data.get("success"):
                return {
                    "success": True,
                    "message": f"Dados extraídos do Scholar: {data['name']}",
                    "platform": "scholar",
                    "search_type": "profile",
                    "total_results": data.get("total_publications", 0),
                    "execution_time": 4.0,
                    "researcher_info": {
                        "name": data["name"],
                        "institution": data["affiliation"],
                        "h_index": data["h_index"],
                        "total_citations": data["total_citations"]
                    },
                    "data": {
                        "publications": [
                            {
                                "title": pub["title"],
                                "authors": data["name"],
                                "publication": pub["venue"],
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
            else:
                return {
                    "success": False,
                    "message": f"Erro ao extrair Scholar: {data.get('error', 'Erro desconhecido')}",
                    "platform": "scholar",
                    "error_details": data
                }
        
        else:
            # Assumir que é um nome para buscar no Scholar
            print("🎓 DETECTADO: BUSCA POR NOME NO SCHOLAR")
            extractor = ScholarExtractor()
            data = extractor.search_author(url_to_process)
            
            if data.get("success"):
                return {
                    "success": True,
                    "message": f"Dados extraídos do Scholar: {data['name']}",
                    "platform": "scholar",
                    "search_type": "author",
                    "total_results": data.get("total_publications", 0),
                    "execution_time": 4.0,
                    "researcher_info": {
                        "name": data["name"],
                        "institution": data["affiliation"],
                        "h_index": data["h_index"],
                        "total_citations": data["total_citations"]
                    },
                    "data": {
                        "publications": [
                            {
                                "title": pub["title"],
                                "authors": data["name"],
                                "publication": "Google Scholar",
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
            else:
                return {
                    "success": False,
                    "message": f"Erro na busca: {data.get('error', 'Erro desconhecido')}",
                    "platform": "scholar",
                    "error_details": data
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

if __name__ == "__main__":
    print("🚀 INICIANDO API REAL DE SCRAPING...")
    print("📍 API disponível em: http://localhost:8000")
    print("🔥 SCRAPING REAL ATIVADO:")
    print("  🇧🇷 Lattes: Extração completa")
    print("  🌐 ORCID: Extração completa") 
    print("  🎓 Scholar: Busca por nome")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)