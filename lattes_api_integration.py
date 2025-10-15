"""
🔧 INTEGRAÇÃO CHROMEDRIVER COM API LATTES
========================================

Sistema integrado para usar ChromeDriver na API do Lattes
com fallback automático quando há CAPTCHA.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lattes_chromedriver_system import extract_lattes_with_automation
from typing import Dict, Optional
import requests
from bs4 import BeautifulSoup
import time

class LattesScraperWithAutomation:
    """Scraper do Lattes com fallback para ChromeDriver"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_profile(self, lattes_id: str, use_automation: bool = False) -> Dict:
        """
        Extrai perfil do Lattes com fallback automático
        
        Args:
            lattes_id: ID do currículo Lattes
            use_automation: Se True, força uso do ChromeDriver
            
        Returns:
            Dicionário com dados do perfil
        """
        
        # Tentar método direto primeiro (se não forçar automação)
        if not use_automation:
            print("🚀 Tentando extração direta...")
            direct_result = self._extract_direct(lattes_id)
            
            if direct_result and 'error' not in direct_result:
                print("✅ Extração direta bem-sucedida!")
                return direct_result
            elif direct_result and 'captcha' in direct_result.get('error', '').lower():
                print("🔒 CAPTCHA detectado - usando ChromeDriver...")
            else:
                print("⚠️ Falha na extração direta - tentando ChromeDriver...")
        
        # Usar ChromeDriver como fallback ou método principal
        print("🤖 Usando ChromeDriver para automação...")
        automation_result = extract_lattes_with_automation(lattes_id, headless=False)
        
        if 'error' not in automation_result:
            # Converter para formato padrão da API
            return self._normalize_automation_result(automation_result)
        else:
            return {
                'error': 'Falha na extração automatizada',
                'details': automation_result.get('error', 'Erro desconhecido'),
                'suggestion': 'Verifique se o ID do Lattes está correto e se o CAPTCHA foi resolvido'
            }
    
    def _extract_direct(self, lattes_id: str) -> Dict:
        """Tentativa de extração direta (sem ChromeDriver)"""
        try:
            url = f"http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id={lattes_id}"
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                return {'error': f'HTTP {response.status_code}'}
            
            # Verificar CAPTCHA
            if self._has_captcha(response.text):
                return {'error': 'CAPTCHA detectado - necessária automação'}
            
            # Tentar extrair dados
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Verificar se perfil carregou
            if not self._is_profile_valid(soup):
                return {'error': 'Perfil não encontrado ou inacessível'}
            
            # Extrair dados básicos
            return {
                'name': self._extract_name_simple(soup),
                'institution': 'Não extraído (método direto)',
                'last_update': self._extract_date_simple(soup),
                'publications': [],
                'lattes_url': url,
                'method': 'direct'
            }
            
        except Exception as e:
            return {'error': f'Erro na extração direta: {str(e)}'}
    
    def _has_captcha(self, html: str) -> bool:
        """Verifica se há CAPTCHA na resposta"""
        captcha_indicators = [
            'captcha', 'recaptcha', 'verificação', 'robô', 'robot'
        ]
        
        html_lower = html.lower()
        return any(indicator in html_lower for indicator in captcha_indicators)
    
    def _is_profile_valid(self, soup: BeautifulSoup) -> bool:
        """Verifica se é um perfil válido"""
        indicators = [
            'currículo do sistema de currículos lattes',
            'dados gerais', 'formação acadêmica'
        ]
        
        text = soup.get_text().lower()
        return any(indicator in text for indicator in indicators)
    
    def _extract_name_simple(self, soup: BeautifulSoup) -> str:
        """Extração simples do nome"""
        try:
            title = soup.find('title')
            if title:
                text = title.get_text()
                if '(' in text and ')' in text:
                    import re
                    match = re.search(r'\((.*?)\)', text)
                    if match:
                        return match.group(1).strip()
            return "Nome não extraído"
        except:
            return "Erro na extração do nome"
    
    def _extract_date_simple(self, soup: BeautifulSoup) -> str:
        """Extração simples da data"""
        try:
            import re
            text = soup.get_text()
            dates = re.findall(r'\d{2}/\d{2}/\d{4}', text)
            return dates[-1] if dates else "Data não encontrada"
        except:
            return "Erro na extração da data"
    
    def _normalize_automation_result(self, result: Dict) -> Dict:
        """Normaliza resultado da automação para formato da API"""
        publications = result.get('publications', [])
        
        return {
            'success': True,
            'name': result.get('name', 'Nome não encontrado'),
            'institution': result.get('institution', 'Instituição não informada'),
            'last_update': result.get('last_update', 'Data não encontrada'),
            'lattes_url': result.get('lattes_url', ''),
            'total_publications': len(publications),
            'publications': publications,
            'method': 'automation',
            'message': 'Dados extraídos com sucesso usando ChromeDriver'
        }

# Função de teste
def test_integration():
    """Testa a integração completa"""
    print("🧪 TESTE DE INTEGRAÇÃO CHROMEDRIVER + API")
    print("=" * 60)
    
    scraper = LattesScraperWithAutomation()
    
    # Teste com ID conhecido
    test_id = "K4247989Z2"
    print(f"🎯 Testando ID: {test_id}")
    
    # Testar método direto primeiro
    print("\n1️⃣ TESTE MÉTODO DIRETO:")
    result_direct = scraper.extract_profile(test_id, use_automation=False)
    
    if 'error' in result_direct:
        print(f"❌ Método direto falhou: {result_direct['error']}")
        print("🤖 Tentando com ChromeDriver...")
        
        # Testar com automação
        print("\n2️⃣ TESTE COM CHROMEDRIVER:")
        result_auto = scraper.extract_profile(test_id, use_automation=True)
        
        if 'error' not in result_auto:
            print("✅ ChromeDriver funcionou!")
            print(f"👤 Nome: {result_auto.get('name', 'N/A')}")
            print(f"📅 Atualização: {result_auto.get('last_update', 'N/A')}")
        else:
            print(f"❌ ChromeDriver também falhou: {result_auto.get('error', 'N/A')}")
    else:
        print("✅ Método direto funcionou!")
        print(f"👤 Nome: {result_direct.get('name', 'N/A')}")

if __name__ == "__main__":
    test_integration()