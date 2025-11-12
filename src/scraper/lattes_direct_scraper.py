"""
🇧🇷 SCRAPER DIRETO DO LATTES
============================
Busca informações diretamente da plataforma Lattes usando busca por nome
Usa requests apenas, sem BeautifulSoup para evitar dependências
"""

import requests
from typing import Dict, Any, Optional, List
import time
import random
import re
import urllib.parse

class LattesDirectScraper:
    """Scraper para buscar informações diretamente da Plataforma Lattes"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://buscatextual.cnpq.br/',
        })
        self.base_url = "http://buscatextual.cnpq.br/buscatextual/busca.do"
    
    def search_by_name(self, name: str) -> Dict[str, Any]:
        """
        Busca um pesquisador no Lattes por nome
        
        Args:
            name: Nome do pesquisador
            
        Returns:
            Dict com informações do currículo Lattes
        """
        print(f"🔍 Buscando no Lattes: {name}")
        
        try:
            # Parâmetros de busca do Lattes
            params = {
                'metodo': 'apresentar',
                'asg_contexto': 'buscaTextual',
                'asg_nome': name,
                'asg_uf': '',
                'asg_pais': '',
                'asg_local': '',
                'asg_cidade': '',
                'asg_logradouro': '',
                'asg_instituicao': '',
                'asg_filtro': 'on',
                'asg_popup': 'false',
                'asg_popup_titulo': '',
                'flagBuscaFonetica': 'false',
                'asg_criterio': '1',  # Busca por nome
                'asg_repositorio': '',
            }
            
            # Delay para evitar bloqueio
            time.sleep(random.uniform(1, 3))
            
            print(f"📡 Acessando Plataforma Lattes...")
            response = self.session.get(self.base_url, params=params, timeout=20)
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"⚠️ Status code não é 200")
                return self._create_empty_result(name)
            
            html = response.text
            
            # Extrair dados usando regex
            profile_data = self._extract_from_html(html, name)
            
            if profile_data.get('success'):
                print(f"✅ Perfil Lattes encontrado!")
                print(f"   Nome: {profile_data.get('name')}")
                print(f"   Instituição: {profile_data.get('institution')}")
                print(f"   URL: {profile_data.get('lattes_url')}")
            else:
                print(f"⚠️ Perfil não encontrado")
                
            return profile_data
            
        except Exception as e:
            print(f"❌ Erro ao buscar no Lattes: {e}")
            import traceback
            traceback.print_exc()
            return self._create_empty_result(name)
    
    def _extract_from_html(self, html: str, original_name: str) -> Dict[str, Any]:
        """Extrai dados do HTML usando regex"""
        try:
            # Procurar por ID do currículo Lattes
            id_match = re.search(r'id=([A-Z0-9]+)', html)
            if not id_match:
                # Tentar outro padrão
                id_match = re.search(r'idcnpq=([A-Z0-9]+)', html)
            
            if not id_match:
                print("⚠️ ID do currículo não encontrado no HTML")
                return self._create_empty_result(original_name)
            
            lattes_id = id_match.group(1)
            lattes_url = f"http://lattes.cnpq.br/{lattes_id}"
            
            print(f"✅ ID encontrado: {lattes_id}")
            
            # Extrair nome (geralmente vem em tags <b> ou <strong>)
            name_match = re.search(r'<(?:b|strong)>([^<]+)</(?:b|strong)>', html)
            name = name_match.group(1).strip() if name_match else original_name
            
            # Extrair instituição
            institution = self._extract_institution_from_text(html)
            
            # Extrair área
            area = self._extract_area_from_text(html)
            
            # Criar resumo
            summary = f"Pesquisador(a) da {institution} na área de {area}"
            
            return {
                "success": True,
                "name": name,
                "summary": summary,
                "institution": institution,
                "area": area,
                "lattes_url": lattes_url,
                "source": "lattes_direct"
            }
            
        except Exception as e:
            print(f"⚠️ Erro ao extrair dados do HTML: {e}")
            import traceback
            traceback.print_exc()
            return self._create_empty_result(original_name)
    
    def _extract_institution_from_text(self, text: str) -> str:
        """Extrai a instituição do texto HTML"""
        try:
            # Procurar por universidade ou instituto com padrões mais flexíveis
            patterns = [
                # Universidades completas
                r'>(Universidade[^<]{5,100}?)<',
                r'\s(Universidade[^\n<>]{5,100}?)\s*[<\n]',
                # Siglas conhecidas
                r'\b(UNESP[^<\n]{0,60}?)\s*[<\n]',
                r'\b(USP[^<\n]{0,60}?)\s*[<\n]',
                r'\b(UNICAMP[^<\n]{0,60}?)\s*[<\n]',
                r'\b(UFRJ[^<\n]{0,60}?)\s*[<\n]',
                r'\b(UFMG[^<\n]{0,60}?)\s*[<\n]',
                r'\b(UnB[^<\n]{0,60}?)\s*[<\n]',
                r'\b(UFSC[^<\n]{0,60}?)\s*[<\n]',
                r'\b(UFRGS[^<\n]{0,60}?)\s*[<\n]',
                # Institutos e Faculdades
                r'>(Instituto[^<]{5,80}?)<',
                r'>(Faculdade[^<]{5,80}?)<',
                # Padrão genérico para qualquer instituição após "de" ou similar
                r'(?:Instituição|Vinculação|Afiliação)[:\s]+([^<\n]{10,100}?)[<\n]',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    inst = match.strip()
                    # Limpar tags HTML residuais
                    inst = re.sub(r'<[^>]+>', '', inst)
                    # Limpar espaços extras
                    inst = re.sub(r'\s+', ' ', inst)
                    # Se encontrou algo significativo, retornar
                    if len(inst) > 5:
                        return inst
            
            return "Instituição não especificada"
        except Exception as e:
            print(f"⚠️ Erro ao extrair instituição: {e}")
            return "Instituição não especificada"
    
    def _extract_area_from_text(self, text: str) -> str:
        """Extrai a área de atuação do texto HTML"""
        try:
            # Procurar por grandes áreas do conhecimento
            areas = [
                'Ciências da Saúde', 'Ciências Biológicas', 'Ciências Exatas',
                'Engenharias', 'Ciências Humanas', 'Ciências Sociais',
                'Linguística', 'Letras', 'Artes', 'Ciências Agrárias',
                'Medicina', 'Odontologia', 'Farmácia', 'Enfermagem'
            ]
            
            for area in areas:
                if area.lower() in text.lower():
                    return area
            
            return "Área não especificada"
        except:
            return "Área não especificada"
    
    def _create_empty_result(self, name: str) -> Dict[str, Any]:
        """Cria um resultado vazio quando não há dados"""
        return {
            "success": False,
            "name": name,
            "summary": "Não encontrado na Plataforma Lattes",
            "institution": "Instituição não especificada",
            "area": "Área não especificada",
            "lattes_url": None,
            "source": "lattes_direct"
        }


# Instância global
lattes_direct_scraper = LattesDirectScraper()


# Função de conveniência
def search_lattes_by_name(name: str) -> Dict[str, Any]:
    """Função de conveniência para buscar no Lattes por nome"""
    return lattes_direct_scraper.search_by_name(name)


if __name__ == "__main__":
    # Teste
    print("🧪 Testando Lattes Direct Scraper")
    print("=" * 50)
    
    test_name = input("Digite o nome do pesquisador: ")
    result = search_lattes_by_name(test_name)
    
    print("\n📊 Resultado:")
    print(f"Sucesso: {result.get('success')}")
    print(f"Nome: {result.get('name')}")
    print(f"Resumo: {result.get('summary')}")
    print(f"Instituição: {result.get('institution')}")
    print(f"Área: {result.get('area')}")
    print(f"URL Lattes: {result.get('lattes_url')}")
