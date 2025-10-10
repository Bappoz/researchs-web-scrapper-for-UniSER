"""
🔥 API REAL DE SCRAPING ACADÊMICO
Extração real de dados do Lattes, ORCID e Google Scholar
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

# Importar MongoDB
try:
    from .database.mongodb import research_db, ResearchDatabase
    from .database.excel_consolidado import consolidated_exporter
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
    """Salvar resultado no MongoDB se filtrado por keywords"""
    if MONGODB_AVAILABLE and filter_keywords and result.get("data", {}).get("publications"):
        try:
            saved = research_db.save_research_result(result)
            if saved:
                result["saved_to_database"] = True
                print("💾 Dados salvos no MongoDB")
            else:
                result["database_error"] = "Falha ao salvar no MongoDB"
        except Exception as e:
            print(f"❌ Erro ao salvar no MongoDB: {e}")
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
    
    def search_author(self, author_name: str, max_publications: int = 20) -> Dict[str, Any]:
        """Buscar autor no Google Scholar"""
        print(f"🎓 BUSCANDO NO SCHOLAR: {author_name}")
        print(f"📚 Máximo de publicações para busca: {max_publications}")
        
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
                    return self.extract_profile(profile_url, max_publications)
            
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
    
    def extract_profile(self, scholar_url: str, max_publications: int = 20) -> Dict[str, Any]:
        """Extrair perfil do Scholar com controle de número de publicações"""
        print(f"🎓 EXTRAINDO SCHOLAR PROFILE: {scholar_url}")
        print(f"📚 Máximo de publicações: {max_publications}")
        
        try:
            time.sleep(random.uniform(3, 6))
            
            response = self.session.get(scholar_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            name = self._extract_name(soup)
            affiliation = self._extract_affiliation(soup)
            h_index = self._extract_h_index(soup)
            i10_index = self._extract_i10_index(soup)
            citations = self._extract_citations(soup)
            publications = self._extract_publications_with_pagination(scholar_url, max_publications)
            
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
        
        # Estratégia 2: Usar posição conhecida mas com validação rigorosa
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
        
        # Estratégia 3: Busca mais conservadora por padrões específicos
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
        
        # Como último recurso, usar estimativa baseada nas citações (conservadora)
        if len(stats_elements) >= 1:
            citations_text = stats_elements[0].get_text(strip=True).replace(',', '')
            if citations_text.isdigit():
                citations = int(citations_text)
                # Fórmula empírica muito conservadora
                estimated_h = min(150, max(1, int((citations ** 0.5) / 10)))
                print(f"🔄 Estimativa conservadora de h-index baseada em {citations} citações: {estimated_h}")
                print("⚠️ ATENÇÃO: Este é um valor estimado, não real!")
                return f"{estimated_h} (estimado)"
        
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
        
        pub_elements = soup.select('.gsc_a_tr')
        print(f"🔍 Elementos de publicação encontrados: {len(pub_elements)}")
        
        for i, pub in enumerate(pub_elements):
            try:
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

    def _extract_publications(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Método legado - manter compatibilidade"""
        return self._extract_publications_from_soup(soup)[:20]

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
                        print(f"📊 Excel exportado: {filename}")
                    except Exception as e:
                        print(f"❌ Erro na exportação Excel: {e}")
                        result["export_error"] = str(e)
                
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
                        print(f"📊 Excel exportado: {filename}")
                    except Exception as e:
                        print(f"❌ Erro na exportação Excel: {e}")
                        result["export_error"] = str(e)
                
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
                        print(f"📊 Excel exportado: {filename}")
                    except Exception as e:
                        print(f"❌ Erro na exportação Excel: {e}")
                        result["export_error"] = str(e)
                
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
            # Assumir que é um nome para buscar no Scholar
            print("🎓 DETECTADO: BUSCA POR NOME NO SCHOLAR")
            print(f"📚 Solicitadas {max_publications} publicações")
            extractor = ScholarExtractor()
            data = extractor.search_author(url_to_process, max_publications)
            
            if data.get("success"):
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
                        print(f"📊 Excel exportado: {filename}")
                    except Exception as e:
                        print(f"❌ Erro na exportação Excel: {e}")
                        result["export_error"] = str(e)
                
                # Salvar no MongoDB se filtrado por keywords
                save_to_mongodb_if_filtered(result, filter_keywords)
                
                return result
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
        if export_excel:
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
        if export_excel:
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
    """Exportar Excel consolidado com todos os dados do MongoDB"""
    if not MONGODB_AVAILABLE:
        raise HTTPException(status_code=503, detail="MongoDB não disponível")
    
    try:
        from src.database.excel_consolidado import ConsolidatedExcelExporter
        from fastapi.responses import FileResponse
        
        # Obter dados do MongoDB
        db = ResearchDatabase()
        research_data = await db.get_all_keyword_filtered_research_async()
        
        if not research_data:
            return {
                "success": False,
                "message": "Nenhum dado encontrado no banco. Faça buscas com filtro de keywords primeiro.",
                "total_records": 0,
                "instructions": "Para gerar dados: faça buscas com 'filter_keywords=True'"
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

if __name__ == "__main__":
    print("🚀 INICIANDO API REAL DE SCRAPING...")
    print("📍 API disponível em: http://localhost:8000")
    print("🔥 SCRAPING REAL ATIVADO:")
    print("  🇧🇷 Lattes: Extração completa")
    print("  🌐 ORCID: Extração completa") 
    print("  🎓 Scholar: Busca por nome")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)