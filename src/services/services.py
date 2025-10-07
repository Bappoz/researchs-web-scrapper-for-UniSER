"""
🔍 SERVIÇO DE BUSCA GOOGLE SCHOLAR
==================================
Camada de serviço para operações de busca no Google Scholar
"""

import os
import re
import time
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from serpapi import GoogleSearch
from dotenv import load_dotenv
import pandas as pd

from ..models import (
    PublicationData, AuthorProfile, AuthorSummary, 
    CitationData, SearchType
)
from ..utils.academic_metrics import calculate_academic_metrics

# Carregar variáveis de ambiente
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(env_path)

class GoogleScholarService:
    """Serviço para busca no Google Scholar usando SerpAPI"""
    
    def __init__(self):
        self.api_key = os.getenv("API_KEY") or "demo_key_for_testing"
        self.api_calls_count = 0
    
    def test_connection(self) -> Tuple[bool, str]:
        """Testa a conexão com a API SerpAPI"""
        try:
            params = {
                "api_key": self.api_key,
                "engine": "google_scholar",
                "q": "test",
                "hl": "en",
                "num": 1
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            self.api_calls_count += 1
            
            if 'error' in results:
                return False, f"Erro da API: {results['error']}"
            
            return True, "Conexão OK"
            
        except Exception as e:
            return False, f"Erro de conexão: {str(e)}"
    
    def search_by_query(self, query: str, max_results: int = 20, max_pages: int = 3) -> List[PublicationData]:
        """Busca geral por query"""
        params = {
            "api_key": self.api_key,
            "engine": "google_scholar",
            "q": query,
            "hl": "en",
            "num": 20,
            "start": 0
        }
        
        all_results = []
        page = 1
        
        while len(all_results) < max_results and page <= max_pages:
            search = GoogleSearch(params)
            results = search.get_dict()
            self.api_calls_count += 1
            
            if 'error' in results:
                raise Exception(f"Erro da API: {results['error']}")
            
            organic_results = results.get("organic_results", [])
            
            if not organic_results:
                break
            
            for result in organic_results:
                if len(all_results) >= max_results:
                    break
                    
                pub_data = self._extract_publication_data(result, page)
                all_results.append(pub_data)
            
            # Próxima página
            if "next" in results.get("serpapi_pagination", {}):
                params["start"] += 20
                page += 1
            else:
                break
            
            # Delay entre requests
            time.sleep(0.5)
        
        return all_results
    
    def search_by_author_profile(self, author_name: str) -> Tuple[Optional[AuthorProfile], List[PublicationData]]:
        """Busca usando query regular (API de perfis foi descontinuada)"""
        try:
            # Como a API de perfis foi descontinuada, vamos usar busca regular por autor
            query = f'author:"{author_name}"'
            publications = self.search_by_query(query, max_results=20)
            
            # Criar um perfil básico baseado nas publicações encontradas
            if publications:
                # Extrair informações do primeiro autor das publicações
                first_pub = publications[0]
                authors_list = first_pub.authors.split(',') if first_pub.authors else [author_name]
                main_author = authors_list[0].strip()
                
                # Calcular métricas para o perfil
                publications_dict = [{"cited_by": pub.cited_by or 0} for pub in publications]
                metrics = calculate_academic_metrics(publications_dict)
                
                author_profile = AuthorProfile(
                    name=main_author,
                    author_id="",  # Não disponível sem API de perfis
                    affiliations="",
                    cited_by=metrics.get("total_citations", 0),
                    email_domain="",
                    interests=[],
                    h_index=metrics.get("h_index", 0),
                    i10_index=metrics.get("i10_index", 0)
                )
                
                return author_profile, publications
            else:
                # Se não encontrou nada, tenta busca mais ampla
                broader_query = author_name
                publications = self.search_by_query(broader_query, max_results=10)
                
                if publications:
                    # Calcular métricas para busca ampla
                    publications_dict = [{"cited_by": pub.cited_by or 0} for pub in publications]
                    metrics = calculate_academic_metrics(publications_dict)
                    
                    author_profile = AuthorProfile(
                        name=author_name,
                        author_id="",
                        affiliations="",
                        cited_by=metrics.get("total_citations", 0),
                        email_domain="",
                        interests=[],
                        h_index=metrics.get("h_index", 0),
                        i10_index=metrics.get("i10_index", 0)
                    )
                    return author_profile, publications
                    
            return None, []
            
        except Exception as e:
            print(f"⚠️ Erro na busca por perfil: {e}")
            # Fallback: busca simples por nome
            try:
                publications = self.search_by_author_name(author_name, max_results=10)
                if publications:
                    # Calcular métricas para fallback
                    publications_dict = [{"cited_by": pub.cited_by or 0} for pub in publications]
                    metrics = calculate_academic_metrics(publications_dict)
                    
                    author_profile = AuthorProfile(
                        name=author_name,
                        author_id="",
                        affiliations="",
                        cited_by=metrics.get("total_citations", 0),
                        email_domain="",
                        interests=[],
                        h_index=metrics.get("h_index", 0),
                        i10_index=metrics.get("i10_index", 0)
                    )
                    return author_profile, publications
            except:
                pass
                
            return None, []
    
    def search_by_author_name(self, author_name: str, max_results: int = 50) -> List[PublicationData]:
        """Busca por nome do autor usando operador author:"""
        query = f'author:"{author_name}"'
        return self.search_by_query(query, max_results)
    
    def comprehensive_author_search(self, author_name: str) -> Tuple[Optional[AuthorProfile], List[PublicationData], AuthorSummary]:
        """Busca completa por autor"""
        # Método 1: Busca por perfil (mais precisa)
        author_profile, publications = self.search_by_author_profile(author_name)
        
        if not publications:
            # Método 2: Busca por nome
            publications = self.search_by_author_name(author_name)
        
        # Gera resumo estatístico
        summary = self._generate_author_summary(author_name, publications)
        
        return author_profile, publications, summary
    
    def search_citations(self, query: str, max_results: int = 3) -> List[CitationData]:
        """Busca citações para uma query"""
        # Primeiro, busca os resultados principais
        organic_results = self.search_by_query(query, max_results=max_results)
        
        citations = []
        
        for result in organic_results:
            if not result.result_id:
                continue
            
            try:
                params = {
                    "api_key": self.api_key,
                    "engine": "google_scholar_cite",
                    "q": result.result_id
                }
                
                search = GoogleSearch(params)
                cite_results = search.get_dict()
                self.api_calls_count += 1
                
                if 'error' in cite_results:
                    continue
                
                for citation in cite_results.get("citations", []):
                    citation_data = CitationData(
                        original_title=result.title,
                        citation_title=citation.get("title", ""),
                        citation_snippet=citation.get("snippet")
                    )
                    citations.append(citation_data)
                
                # Delay entre requests
                time.sleep(0.5)
                    
            except Exception:
                continue
        
        return citations
    
    def _get_author_publications(self, author_id: str) -> List[PublicationData]:
        """Pega publicações usando ID do autor"""
        params = {
            "api_key": self.api_key,
            "engine": "google_scholar_author",
            "author_id": author_id,
            "num": 100
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        self.api_calls_count += 1
        
        if 'error' in results:
            raise Exception(f"Erro: {results['error']}")
        
        articles = results.get("articles", [])
        
        publications = []
        for article in articles:
            pub_data = PublicationData(
                title=article.get("title", ""),
                authors=article.get("authors", ""),
                publication=article.get("publication", ""),
                year=article.get("year"),
                cited_by=article.get("cited_by", {}).get("value", 0),
                link=article.get("link", ""),
                result_id=article.get("citation_id", ""),
                result_type="author_publication",
                page_number=1
            )
            publications.append(pub_data)
        
        return publications
    
    def _extract_publication_data(self, result: Dict[str, Any], page_number: int = 1) -> PublicationData:
        """Extrai dados de uma publicação de forma segura"""
        # Informações básicas
        title = result.get("title", "")
        link = result.get("link", "")
        snippet = result.get("snippet", "")
        result_id = result.get("result_id", "")
        result_type = result.get("type", "")
        
        # Informações de publicação
        pub_info = result.get("publication_info", {}).get("summary", "")
        authors = pub_info.split(" - ")[0] if pub_info else ""
        year = self._extract_year(pub_info)
        
        # Citações
        cited_by_count = 0
        try:
            cited_by_count = int(result.get("inline_links", {}).get("cited_by", {}).get("total", 0))
        except:
            pass
        
        # Recursos de arquivo
        file_info = {}
        try:
            resources = result.get("resources", [])
            if resources:
                file_info = {
                    "file_title": resources[0].get("title"),
                    "file_link": resources[0].get("link"),
                    "file_format": resources[0].get("file_format")
                }
        except:
            file_info = {"file_title": None, "file_link": None, "file_format": None}
        
        return PublicationData(
            page_number=page_number,
            title=title,
            authors=authors,
            publication=pub_info,
            year=year,
            cited_by=cited_by_count,
            link=link,
            snippet=snippet,
            result_id=result_id,
            result_type=result_type,
            **file_info
        )
    
    def _extract_year(self, publication_info: str) -> Optional[int]:
        """Extrai ano da publicação"""
        if not publication_info:
            return None
        match = re.search(r'\b(19|20)\d{2}\b', publication_info)
        return int(match.group()) if match else None
    
    def _generate_author_summary(self, author_name: str, publications: List[PublicationData]) -> AuthorSummary:
        """Gera resumo estatístico do autor"""
        if not publications:
            return AuthorSummary(
                author_name=author_name,
                total_publications=0,
                total_citations=0,
                h_index=0,
                i10_index=0
            )
        
        # Converter publicações para formato dict para usar nas métricas
        publications_dict = []
        for pub in publications:
            pub_dict = {
                "title": pub.title,
                "cited_by": pub.cited_by or 0,
                "year": pub.year,
                "authors": pub.authors,
                "publication": pub.publication
            }
            publications_dict.append(pub_dict)
        
        # Calcular todas as métricas
        metrics = calculate_academic_metrics(publications_dict)
        
        return AuthorSummary(
            author_name=author_name,
            total_publications=metrics.get("total_publications", 0),
            total_citations=metrics.get("total_citations", 0),
            h_index=metrics.get("h_index", 0),
            i10_index=metrics.get("i10_index", 0),
            year_range=metrics.get("year_range"),
            top_cited=metrics.get("top_cited", []),
            publications_by_year=metrics.get("publications_by_year", {})
        )
    
    def save_to_csv(self, data: List[PublicationData], filename_prefix: str, query: str = "") -> str:
        """Salva dados em CSV"""
        if not data:
            raise ValueError("Nenhum dado para salvar")
        
        # Converte para dicionários
        data_dicts = [pub.dict() for pub in data]
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_clean = query.replace(" ", "_").replace('"', '').lower()[:20]
        filename = f"{filename_prefix}_{query_clean}_{timestamp}.csv"
        
        df = pd.DataFrame(data_dicts)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        return filename

    # ==================== MÉTODOS PARA NOVA API ====================
    
    async def search_publications(self, topic: str, max_results: int = 20, export_excel: bool = False):
        """Busca publicações por tema"""
        try:
            publications = self.search_by_query(topic, max_results)
            
            result = {
                "publications": [pub.dict() for pub in publications],
                "total_results": len(publications),
                "query": topic
            }
            
            if export_excel:
                # Importar função de exportação Excel
                from ..export.excel_exporter import export_research_to_excel
                
                # Preparar dados para exportação
                search_data = {
                    "query": topic,
                    "search_type": "topic",
                    "execution_time": 0,  # Será calculado no endpoint
                    "platforms": ["scholar"],
                    "results_by_platform": {
                        "scholar": {
                            "publications": [pub.dict() for pub in publications],
                            "total_results": len(publications),
                            "query": topic
                        }
                    },
                    "total_authors": 0,
                    "total_publications": len(publications),
                    "total_citations": sum([pub.cited_by for pub in publications if pub.cited_by]),
                    "max_h_index": 0,
                    "top_publication_citations": max([pub.cited_by for pub in publications if pub.cited_by] + [0])
                }
                
                filename = export_research_to_excel(search_data, f"busca_tema_{topic}")
                result["excel_file"] = filename
                
            return result
            
        except Exception as e:
            raise Exception(f"Erro na busca por publicações: {str(e)}")
    
    async def search_author(self, author: str, max_results: int = 10, export_excel: bool = False):
        """Busca autor no Google Scholar"""
        try:
            # Verificar se é um URL de perfil do Google Scholar
            if self._is_scholar_profile_url(author):
                author_id = self._extract_author_id_from_url(author)
                if author_id:
                    # Tentar buscar usando o ID do perfil
                    author_profile, publications = self._search_by_author_id(author_id)
                else:
                    # Se não conseguir extrair ID, usar busca genérica
                    author_profile, publications = self.search_by_author_profile("pesquisador")
            else:
                # Busca normal por nome
                author_profile, publications = self.search_by_author_profile(author)
            
            # Limitar publicações se necessário
            if len(publications) > max_results:
                publications = publications[:max_results]
            
            result = {
                "author_profile": author_profile.dict() if author_profile else None,
                "publications": [pub.dict() for pub in publications],
                "total_results": len(publications),
                "query": author
            }
            
            if export_excel:
                # Importar função de exportação Excel
                from ..export.excel_exporter import export_research_to_excel
                
                # Preparar dados para exportação
                search_data = {
                    "query": author,
                    "search_type": "author",
                    "execution_time": 0,  # Será calculado no endpoint
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
                    "max_h_index": author_profile.h_index if author_profile and author_profile.h_index else 0,
                    "top_publication_citations": max([pub.cited_by for pub in publications if pub.cited_by] + [0])
                }
                
                filename = export_research_to_excel(search_data, f"busca_autor_{author}")
                result["excel_file"] = filename
                
            return result
            
        except Exception as e:
            raise Exception(f"Erro na busca por autor: {str(e)}")
    
    def _is_scholar_profile_url(self, text: str) -> bool:
        """Verifica se é um URL de perfil do Google Scholar"""
        return "scholar.google.com/citations" in text and "user=" in text
    
    def _extract_author_id_from_url(self, url: str) -> Optional[str]:
        """Extrai o ID do autor de um URL do Google Scholar"""
        import re
        match = re.search(r'user=([^&]+)', url)
        return match.group(1) if match else None
    
    def _search_by_author_id(self, author_id: str) -> Tuple[Optional[AuthorProfile], List[PublicationData]]:
        """Busca usando ID específico do autor"""
        try:
            # Buscar perfil do autor usando SerpAPI
            params = {
                "api_key": self.api_key,
                "engine": "google_scholar_author",
                "author_id": author_id,
                "hl": "en"
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            self.api_calls_count += 1
            
            if 'error' in results:
                # Se der erro, tentar busca genérica
                return self.search_by_author_profile("pesquisador")
            
            # Extrair dados do perfil
            author_data = results.get("author", {})
            
            if not author_data:
                return None, []
            
            # Calcular métricas se houver artigos
            articles = results.get("articles", [])
            publications = []
            
            for article in articles:
                pub_data = PublicationData(
                    title=article.get("title", ""),
                    authors=article.get("authors", ""),
                    publication=article.get("publication", ""),
                    year=article.get("year"),
                    cited_by=article.get("cited_by", {}).get("value", 0),
                    link=article.get("link", ""),
                    result_id=article.get("citation_id", ""),
                    result_type="author_publication",
                    page_number=1
                )
                publications.append(pub_data)
            
            # Calcular métricas acadêmicas
            publications_dict = [{"cited_by": pub.cited_by or 0} for pub in publications]
            metrics = calculate_academic_metrics(publications_dict)
            
            # Criar perfil do autor
            author_profile = AuthorProfile(
                name=author_data.get("name", ""),
                author_id=author_id,
                affiliations=author_data.get("affiliations", ""),
                cited_by=metrics.get("total_citations", 0),
                email_domain=author_data.get("email", "").split("@")[-1] if author_data.get("email") else "",
                interests=[interest.get("title", "") for interest in author_data.get("interests", [])],
                h_index=metrics.get("h_index", 0),
                i10_index=metrics.get("i10_index", 0)
            )
            
            return author_profile, publications
            
        except Exception as e:
            print(f"⚠️ Erro na busca por ID: {e}")
            # Fallback para busca genérica
            return self.search_by_author_profile("pesquisador")
                
            return result
            
        except Exception as e:
            raise Exception(f"Erro na busca por autor: {str(e)}")
    
    async def get_author_profile_by_url(self, profile_url: str):
        """Busca perfil do autor por URL"""
        try:
            # Extrair user ID da URL do Google Scholar
            user_match = re.search(r'user=([^&]+)', profile_url)
            if not user_match:
                raise ValueError("URL do Google Scholar inválida")
            
            user_id = user_match.group(1)
            
            params = {
                "api_key": self.api_key,
                "engine": "google_scholar_author",
                "author_id": user_id,
                "hl": "pt"
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            self.api_calls_count += 1
            
            if 'error' in results:
                raise Exception(f"Erro da API: {results['error']}")
            
            # Processar dados do autor
            author_data = results.get('author', {})
            articles = results.get('articles', [])
            
            # Extrair user_id da URL novamente
            user_match = re.search(r'user=([^&]+)', profile_url)
            user_id = user_match.group(1) if user_match else 'unknown'
            
            # Processar interesses corretamente
            interests_raw = author_data.get('interests', [])
            interests = []
            print(f"🔍 Processando interesses: {interests_raw}")
            for interest in interests_raw:
                if isinstance(interest, dict) and 'title' in interest:
                    interests.append(interest['title'])
                    print(f"✅ Adicionado interesse (dict): {interest['title']}")
                elif isinstance(interest, str):
                    interests.append(interest)
                    print(f"✅ Adicionado interesse (str): {interest}")
            print(f"🎯 Interesses finais: {interests}")
            
            author_profile = AuthorProfile(
                name=author_data.get('name', ''),
                author_id=user_id,
                affiliations=author_data.get('affiliation', ''),
                cited_by=author_data.get('cited_by', {}).get('table', [{}])[0].get('citations', {}).get('all', 0) if author_data.get('cited_by') else 0,
                email_domain=author_data.get('email_domain', ''),
                interests=interests
            )
            
            publications = []
            for article in articles[:20]:  # Limitar a 20 artigos
                pub = PublicationData(
                    title=article.get('title', ''),
                    authors=article.get('authors', ''),
                    publication=article.get('publication', ''),
                    year=article.get('year'),
                    cited_by=article.get('cited_by', {}).get('value', 0) if article.get('cited_by') else 0,
                    link=article.get('link', ''),
                    snippet=''
                )
                publications.append(pub)
            
            return {
                "author_profile": author_profile.dict(),
                "publications": [pub.dict() for pub in publications],
                "total_results": len(publications),
                "profile_url": profile_url
            }
            
        except Exception as e:
            raise Exception(f"Erro na busca por URL: {str(e)}")