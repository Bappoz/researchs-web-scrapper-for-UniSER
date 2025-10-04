from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
import pandas as pd
import os
import re
from dotenv import load_dotenv
from datetime import datetime

# Carregar o arquivo .env da mesma pasta
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

class GoogleScholarScraper:
    """Scraper completo para Google Scholar usando SerpAPI"""
    
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("❌ API_KEY não encontrada no arquivo .env")
        print(f"🔑 API Key carregada: {self.api_key[:10]}...")

    def test_connection(self, query="machine learning"):
        """Testa a conexão com a API"""
        params = {
            "api_key": self.api_key,
            "engine": "google_scholar",
            "q": query,
            "hl": "en",
            "num": 5
        }
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            if 'error' in results:
                print(f"❌ Erro da API: {results['error']}")
                return False
            
            organic_results = results.get("organic_results", [])
            print(f"✅ Conexão OK - {len(organic_results)} resultados encontrados")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao testar API: {e}")
            return False

    def search_by_query(self, query, max_results=50, max_pages=5):
        """Busca geral por query"""
        print(f"🔍 Buscando: '{query}' (máximo {max_results} resultados)")
        
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
            print(f"📄 Processando página {page}...")
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            if 'error' in results:
                print(f"❌ Erro: {results['error']}")
                break
            
            organic_results = results.get("organic_results", [])
            
            if not organic_results:
                print("✅ Não há mais resultados")
                break
            
            for result in organic_results:
                if len(all_results) >= max_results:
                    break
                    
                all_results.append(self._extract_result_data(result, page))
            
            # Próxima página
            if "next" in results.get("serpapi_pagination", {}):
                params["start"] += 20
                page += 1
            else:
                break
        
        print(f"✅ Total coletado: {len(all_results)} resultados")
        return all_results

    def search_by_author_name(self, author_name, max_results=50):
        """Busca por nome do autor usando operador author:"""
        query = f'author:"{author_name}"'
        print(f"👤 Buscando publicações do autor: {author_name}")
        return self.search_by_query(query, max_results)

    def search_by_author_profile(self, author_name):
        """Busca usando perfil do autor (mais precisa)"""
        print(f"👤 Buscando perfil do autor: {author_name}")
        
        # Busca o perfil
        profile_params = {
            "api_key": self.api_key,
            "engine": "google_scholar_profiles",
            "mauthors": author_name
        }
        
        search = GoogleSearch(profile_params)
        profiles = search.get_dict()
        
        if 'error' in profiles:
            print(f"❌ Erro ao buscar perfil: {profiles['error']}")
            return []
        
        if 'profiles' not in profiles or not profiles['profiles']:
            print(f"❌ Perfil não encontrado para: {author_name}")
            return []
        
        # Pega o primeiro perfil
        author_profile = profiles['profiles'][0]
        author_id = author_profile['author_id']
        
        print(f"✅ Perfil encontrado: {author_profile['name']}")
        print(f"📍 Afiliação: {author_profile.get('affiliations', 'N/A')}")
        print(f"📊 Citações: {author_profile.get('cited_by', 'N/A')}")
        
        # Busca publicações do autor
        return self._get_author_publications(author_id)

    def _get_author_publications(self, author_id):
        """Pega publicações usando ID do autor"""
        params = {
            "api_key": self.api_key,
            "engine": "google_scholar_author",
            "author_id": author_id,
            "num": 100
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if 'error' in results:
            print(f"❌ Erro: {results['error']}")
            return []
        
        articles = results.get("articles", [])
        print(f"📚 Encontradas {len(articles)} publicações do autor")
        
        publications = []
        for article in articles:
            publications.append({
                "title": article.get("title", ""),
                "authors": article.get("authors", ""),
                "publication": article.get("publication", ""),
                "year": article.get("year"),
                "cited_by": article.get("cited_by", {}).get("value", 0),
                "link": article.get("link", ""),
                "citation_id": article.get("citation_id", ""),
                "result_type": "author_publication"
            })
        
        return publications

    def comprehensive_author_search(self, author_name):
        """Busca completa por autor - tenta perfil primeiro"""
        print(f"🎯 BUSCA COMPLETA POR AUTOR: {author_name}")
        print("=" * 60)
        
        # Método 1: Busca por perfil (mais precisa)
        publications = self.search_by_author_profile(author_name)
        
        if not publications:
            # Método 2: Busca por nome
            print("📋 Tentativa alternativa: busca por nome...")
            publications = self.search_by_author_name(author_name)
        
        if publications:
            # Organiza por ano
            publications.sort(key=lambda x: x.get('year') or 0, reverse=True)
            print(f"✅ Total encontrado: {len(publications)} publicações")
            self._show_author_summary(publications, author_name)
        else:
            print("❌ Nenhuma publicação encontrada")
        
        return publications

    def search_citations(self, query, max_results=3):
        """Busca citações para uma query"""
        print(f"📚 Buscando citações para: {query}")
        
        organic_results = self.search_by_query(query, max_results=max_results)
        
        if not organic_results:
            return []
        
        citations = []
        
        for i, result in enumerate(organic_results):
            result_id = result.get("result_id")
            if not result_id:
                continue
            
            print(f"  🔍 Citações para resultado {i+1}...")
            
            try:
                params = {
                    "api_key": self.api_key,
                    "engine": "google_scholar_cite",
                    "q": result_id
                }
                
                search = GoogleSearch(params)
                cite_results = search.get_dict()
                
                if 'error' in cite_results:
                    continue
                
                for citation in cite_results.get("citations", []):
                    citations.append({
                        "original_title": result.get("title"),
                        "citation_title": citation.get("title"),
                        "citation_snippet": citation.get("snippet")
                    })
                    
            except Exception as e:
                print(f"    ❌ Erro: {e}")
                continue
        
        return citations

    def _extract_result_data(self, result, page_number=1):
        """Extrai dados de um resultado de forma segura"""
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
        
        return {
            "page_number": page_number,
            "title": title,
            "authors": authors,
            "publication": pub_info,
            "year": year,
            "cited_by": cited_by_count,
            "link": link,
            "snippet": snippet,
            "result_id": result_id,
            "result_type": result_type,
            **file_info
        }

    def _extract_year(self, publication_info):
        """Extrai ano da publicação"""
        if not publication_info:
            return None
        match = re.search(r'\b(19|20)\d{2}\b', publication_info)
        return int(match.group()) if match else None

    def _show_author_summary(self, publications, author_name):
        """Mostra resumo das publicações do autor"""
        print(f"\n📊 RESUMO - {author_name.upper()}")
        print("=" * 40)
        
        # Estatísticas
        years = [p['year'] for p in publications if p['year']]
        if years:
            print(f"📅 Período: {min(years)} - {max(years)}")
        
        total_citations = sum(p.get('cited_by', 0) for p in publications)
        print(f"📈 Total de citações: {total_citations}")
        print(f"📚 Total de publicações: {len(publications)}")
        
        # Top 5 mais citadas
        top_cited = sorted(publications, key=lambda x: x.get('cited_by', 0), reverse=True)[:5]
        print(f"\n🏆 TOP 5 MAIS CITADAS:")
        for i, pub in enumerate(top_cited, 1):
            title = pub['title'][:60] + "..." if len(pub['title']) > 60 else pub['title']
            print(f"{i}. {title} ({pub.get('cited_by', 0)} citações)")

    def save_to_csv(self, data, filename_prefix, query=""):
        """Salva dados em CSV com timestamp"""
        if not data:
            print("❌ Nenhum dado para salvar")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_clean = query.replace(" ", "_").replace('"', '').lower()
        filename = f"{filename_prefix}_{query_clean}_{timestamp}.csv"
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"💾 Dados salvos em: {filename}")
        return filename

# Funções de conveniência para compatibilidade com seu código atual
def search_by_query(query, max_results=50):
    scraper = GoogleScholarScraper()
    return scraper.search_by_query(query, max_results)

def search_by_author(author_name):
    scraper = GoogleScholarScraper()
    return scraper.comprehensive_author_search(author_name)

def test_api():
    scraper = GoogleScholarScraper()
    return scraper.test_connection()

if __name__ == "__main__":
    print("🎯 GOOGLE SCHOLAR SCRAPER COMPLETO")
    print("=" * 50)
    
    scraper = GoogleScholarScraper()
    
    # Teste de conexão
    if not scraper.test_connection():
        print("❌ Falha na conexão. Verifique sua API Key.")
        exit(1)
    
    print("\n🚀 Escolha uma opção:")
    print("1. Busca por query")
    print("2. Busca por autor")
    print("3. Busca com citações")
    
    choice = input("Digite sua escolha (1-3): ").strip()
    
    if choice == "1":
        query = input("Digite a query de busca: ")
        results = scraper.search_by_query(query, max_results=20)
        scraper.save_to_csv(results, "query_results", query)
    
    elif choice == "2":
        author = input("Digite o nome do autor: ")
        results = scraper.comprehensive_author_search(author)
        scraper.save_to_csv(results, "author_publications", author)
    
    elif choice == "3":
        query = input("Digite a query para buscar citações: ")
        results = scraper.search_by_query(query, max_results=5)
        citations = scraper.search_citations(query, max_results=3)
        scraper.save_to_csv(results, "results_with_citations", query)
        scraper.save_to_csv(citations, "citations", query)
    
    else:
        print("❌ Opção inválida")