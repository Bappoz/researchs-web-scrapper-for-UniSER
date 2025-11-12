"""
🔍 SCRAPER DO ESCAVADOR
=======================
Scraper para buscar resumo do Lattes via Escavador
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
import time
import random

class EscavadorScraper:
    """Scraper para buscar resumo do currículo Lattes via Escavador"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
    
    def search_profile_summary(self, name: str) -> Dict[str, Any]:
        """
        Busca o resumo do perfil Lattes via Escavador
        
        Args:
            name: Nome do pesquisador
            
        Returns:
            Dict com informações do resumo do perfil
        """
        print(f"🔍 Buscando resumo do Lattes via Escavador para: {name}")
        
        try:
            # URL CORRETA do Escavador para buscar currículos Lattes
            search_url = "https://www.escavador.com/sobre"
            params = {
                'q': name
            }
            
            # Delay aleatório para evitar bloqueio
            time.sleep(random.uniform(2, 4))
            
            # Fazer requisição de busca
            print(f"📡 Acessando Escavador: {search_url}")
            response = self.session.get(search_url, params=params, timeout=20)
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"⚠️ Status code não é 200: {response.status_code}")
                return self._create_empty_result(name)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Estratégia: buscar elementos que contenham o nome e informações acadêmicas
            # O Escavador geralmente mostra cards com informações resumidas
            
            # Buscar qualquer menção ao currículo Lattes na página
            page_text = soup.get_text()
            
            # Verificar se encontrou algo relacionado ao Lattes
            if 'lattes' in page_text.lower() or 'currículo' in page_text.lower():
                print("✅ Página contém referência a Lattes/Currículo")
                
                # Extrair informações básicas
                summary_data = self._extract_from_page(soup, name)
                
                if summary_data.get('success'):
                    print(f"✅ Resumo encontrado para: {summary_data.get('name', name)}")
                    return summary_data
            else:
                print("⚠️ Nenhuma referência a Lattes encontrada na página")
            
            # Se não encontrou nada, retornar resultado vazio
            return self._create_empty_result(name)
            
        except requests.exceptions.Timeout:
            print("⚠️ Timeout ao acessar Escavador")
            return self._create_empty_result(name)
        except Exception as e:
            print(f"❌ Erro ao buscar no Escavador: {e}")
            import traceback
            traceback.print_exc()
            return self._create_empty_result(name)
    
    def _find_first_lattes_result(self, soup: BeautifulSoup) -> Optional[BeautifulSoup]:
        """Encontra o primeiro resultado de Lattes na página"""
        try:
            # Procurar por diferentes possíveis seletores do Escavador
            # (baseado em análise de páginas do Escavador)
            
            # Tentar encontrar cards de resultado
            result_cards = soup.find_all('div', class_=['resultado', 'card-resultado', 'resultado-pessoa'])
            
            for card in result_cards:
                # Verificar se é resultado de Lattes
                text = card.get_text().lower()
                if 'lattes' in text or 'cnpq' in text or 'currículo' in text:
                    return card
            
            # Alternativa: procurar por links de Lattes
            lattes_links = soup.find_all('a', href=lambda x: x and 'lattes' in x.lower())
            if lattes_links:
                # Pegar o container pai do link
                return lattes_links[0].find_parent(['div', 'article', 'section'])
            
            return None
            
        except Exception as e:
            print(f"⚠️ Erro ao procurar resultado: {e}")
            return None
    
    def _extract_from_page(self, soup: BeautifulSoup, original_name: str) -> Dict[str, Any]:
        """Extrai informações gerais da página inteira do Escavador"""
        try:
            page_text = soup.get_text(separator=' ', strip=True)
            
            # Buscar por padrões comuns
            name = original_name
            summary = "Informações disponíveis no Escavador"
            institution = "Não especificada"
            area = "Não especificada"
            lattes_url = None
            
            # Tentar encontrar URL do Lattes
            lattes_links = soup.find_all('a', href=True)
            for link in lattes_links:
                href = link.get('href', '')
                if 'lattes.cnpq.br' in href or 'buscatextual.cnpq.br' in href:
                    lattes_url = href
                    break
            
            # Buscar por universidade no texto
            import re
            univ_match = re.search(r'(Universidade[^.,;\n]{0,80})', page_text, re.IGNORECASE)
            if univ_match:
                institution = univ_match.group(1).strip()
            
            # Se encontrou pelo menos a URL do Lattes, considerar sucesso
            if lattes_url:
                print(f"✅ URL do Lattes encontrada: {lattes_url}")
                
                # Extrair um trecho relevante como resumo
                # Procurar por seções que contenham informações acadêmicas
                academic_keywords = ['pesquisador', 'professor', 'doutor', 'mestre', 'graduação', 'pós-graduação', 'pesquisa']
                for keyword in academic_keywords:
                    if keyword in page_text.lower():
                        # Extrair contexto ao redor da palavra-chave
                        idx = page_text.lower().find(keyword)
                        start = max(0, idx - 100)
                        end = min(len(page_text), idx + 400)
                        summary = page_text[start:end].strip()
                        if len(summary) > 50:
                            break
                
                return {
                    "success": True,
                    "name": name,
                    "summary": summary,
                    "institution": institution,
                    "area": area,
                    "lattes_url": lattes_url,
                    "source": "escavador"
                }
            
            # Se não encontrou URL mas tem menção a Lattes, retornar informação básica
            if 'lattes' in page_text.lower():
                return {
                    "success": True,
                    "name": name,
                    "summary": "Perfil encontrado no Escavador com referência ao Lattes",
                    "institution": institution,
                    "area": area,
                    "lattes_url": None,
                    "source": "escavador"
                }
            
            return self._create_empty_result(original_name)
            
        except Exception as e:
            print(f"⚠️ Erro ao extrair da página: {e}")
            import traceback
            traceback.print_exc()
            return self._create_empty_result(original_name)
    
    def _extract_summary_from_result(self, result_element: BeautifulSoup, original_name: str) -> Dict[str, Any]:
        """Extrai informações do resumo do resultado"""
        try:
            # Extrair nome
            name = self._extract_name(result_element) or original_name
            
            # Extrair resumo/descrição
            summary = self._extract_summary_text(result_element)
            
            # Extrair instituição
            institution = self._extract_institution(result_element)
            
            # Extrair área de atuação
            area = self._extract_area(result_element)
            
            # Extrair link do Lattes (se disponível)
            lattes_url = self._extract_lattes_url(result_element)
            
            return {
                "success": True,
                "name": name,
                "summary": summary,
                "institution": institution,
                "area": area,
                "lattes_url": lattes_url,
                "source": "escavador"
            }
            
        except Exception as e:
            print(f"⚠️ Erro ao extrair dados do resumo: {e}")
            return self._create_empty_result(original_name)
    
    def _extract_name(self, element: BeautifulSoup) -> Optional[str]:
        """Extrai o nome do pesquisador"""
        try:
            # Tentar diferentes seletores comuns
            name_selectors = [
                ('h2', {}),
                ('h3', {}),
                ('div', {'class': 'nome'}),
                ('span', {'class': 'nome'}),
                ('a', {'class': 'titulo'})
            ]
            
            for tag, attrs in name_selectors:
                name_elem = element.find(tag, attrs)
                if name_elem:
                    name = name_elem.get_text(strip=True)
                    if name and len(name) > 3:
                        return name
            
            return None
            
        except Exception:
            return None
    
    def _extract_summary_text(self, element: BeautifulSoup) -> str:
        """Extrai o texto do resumo"""
        try:
            # Procurar por elementos que contenham resumo/descrição
            summary_selectors = [
                ('div', {'class': ['resumo', 'descricao', 'texto']}),
                ('p', {'class': ['resumo', 'descricao']}),
                ('div', {'class': 'card-body'}),
            ]
            
            for tag, attrs in summary_selectors:
                summary_elem = element.find(tag, attrs)
                if summary_elem:
                    text = summary_elem.get_text(strip=True)
                    if text and len(text) > 20:
                        return text
            
            # Se não encontrou, pegar todo o texto do elemento (limitado)
            all_text = element.get_text(separator=' ', strip=True)
            if all_text:
                # Limitar a 500 caracteres para não pegar informações demais
                return all_text[:500] + ('...' if len(all_text) > 500 else '')
            
            return "Resumo não disponível"
            
        except Exception:
            return "Resumo não disponível"
    
    def _extract_institution(self, element: BeautifulSoup) -> str:
        """Extrai a instituição"""
        try:
            # Procurar por elementos de instituição
            inst_selectors = [
                ('div', {'class': ['instituicao', 'afiliacao']}),
                ('span', {'class': ['instituicao', 'afiliacao']}),
            ]
            
            for tag, attrs in inst_selectors:
                inst_elem = element.find(tag, attrs)
                if inst_elem:
                    return inst_elem.get_text(strip=True)
            
            # Tentar encontrar no texto
            text = element.get_text()
            if 'Universidade' in text:
                # Extrair primeira ocorrência de universidade
                import re
                match = re.search(r'Universidade[^.;,\n]{0,100}', text)
                if match:
                    return match.group(0).strip()
            
            return "Instituição não informada"
            
        except Exception:
            return "Instituição não informada"
    
    def _extract_area(self, element: BeautifulSoup) -> str:
        """Extrai a área de atuação"""
        try:
            # Procurar por elementos de área
            area_selectors = [
                ('div', {'class': ['area', 'especialidade']}),
                ('span', {'class': ['area', 'especialidade']}),
            ]
            
            for tag, attrs in area_selectors:
                area_elem = element.find(tag, attrs)
                if area_elem:
                    return area_elem.get_text(strip=True)
            
            return "Área não informada"
            
        except Exception:
            return "Área não informada"
    
    def _extract_lattes_url(self, element: BeautifulSoup) -> Optional[str]:
        """Extrai o URL do Lattes se disponível"""
        try:
            # Procurar por links do Lattes
            links = element.find_all('a', href=True)
            
            for link in links:
                href = link.get('href', '')
                if 'lattes.cnpq.br' in href or 'buscatextual.cnpq.br' in href:
                    return href
            
            return None
            
        except Exception:
            return None
    
    def _create_empty_result(self, name: str) -> Dict[str, Any]:
        """Cria um resultado vazio quando não há dados"""
        return {
            "success": False,
            "name": name,
            "summary": "Resumo não encontrado no Escavador",
            "institution": "Instituição não informada",
            "area": "Área não informada",
            "lattes_url": None,
            "source": "escavador"
        }


# Instância global para uso fácil
escavador_scraper = EscavadorScraper()


# Função de conveniência
def search_lattes_summary(name: str) -> Dict[str, Any]:
    """Função de conveniência para buscar resumo do Lattes via Escavador"""
    return escavador_scraper.search_profile_summary(name)


if __name__ == "__main__":
    # Teste
    print("🧪 Testando Escavador Scraper")
    print("=" * 50)
    
    test_name = input("Digite o nome do pesquisador: ")
    result = search_lattes_summary(test_name)
    
    print("\n📊 Resultado:")
    print(f"Nome: {result.get('name')}")
    print(f"Resumo: {result.get('summary')}")
    print(f"Instituição: {result.get('institution')}")
    print(f"Área: {result.get('area')}")
    print(f"URL Lattes: {result.get('lattes_url')}")
