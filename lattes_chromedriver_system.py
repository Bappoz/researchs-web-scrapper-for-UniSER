"""
🤖 SISTEMA CHROMEDRIVER PARA LATTES
===================================

Sistema completo de automação para scraping do Lattes
usando ChromeDriver para resolver CAPTCHA e extrair dados.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from bs4 import BeautifulSoup
from typing import Dict, List, Optional

class LattesAutomation:
    """Automação completa do Lattes com ChromeDriver"""
    
    def __init__(self, headless: bool = False):
        """
        Inicializa o sistema de automação
        
        Args:
            headless: Se True, executa sem interface gráfica
        """
        self.driver = None
        self.headless = headless
        
    def setup_driver(self):
        """Configura e inicializa o ChromeDriver"""
        print("🚀 Inicializando ChromeDriver...")
        
        try:
            # Configurar opções do Chrome
            options = webdriver.ChromeOptions()
            
            if self.headless:
                options.add_argument("--headless")
            
            # Configurações para evitar detecção
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # User agent real
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            # Configurar service
            service = Service(ChromeDriverManager().install())
            
            # Inicializar driver
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Executar script para evitar detecção
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ ChromeDriver configurado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao configurar ChromeDriver: {str(e)}")
            return False
    
    def access_lattes_profile(self, lattes_id: str) -> bool:
        """
        Acessa o perfil do Lattes
        
        Args:
            lattes_id: ID do currículo Lattes
            
        Returns:
            True se conseguir acessar, False caso contrário
        """
        if not self.driver:
            if not self.setup_driver():
                return False
        
        try:
            # URL do perfil
            url = f"http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id={lattes_id}"
            
            print(f"🌐 Acessando: {url}")
            self.driver.get(url)
            
            # Aguardar carregamento
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao acessar perfil: {str(e)}")
            return False
    
    def detect_captcha(self) -> bool:
        """
        Detecta se há CAPTCHA na página
        
        Returns:
            True se houver CAPTCHA, False caso contrário
        """
        try:
            # Verificar diferentes indicadores de CAPTCHA
            captcha_indicators = [
                "captcha",
                "recaptcha",
                "Confirme que você não é um robô",
                "I'm not a robot",
                "Verificação de segurança"
            ]
            
            page_source = self.driver.page_source.lower()
            
            for indicator in captcha_indicators:
                if indicator.lower() in page_source:
                    print(f"🔒 CAPTCHA detectado: {indicator}")
                    return True
            
            # Verificar elementos específicos do CAPTCHA
            captcha_elements = [
                (By.ID, "captcha"),
                (By.CLASS_NAME, "g-recaptcha"),
                (By.XPATH, "//iframe[contains(@src, 'recaptcha')]")
            ]
            
            for by, value in captcha_elements:
                try:
                    if self.driver.find_element(by, value):
                        print("🔒 CAPTCHA detectado por elemento!")
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Erro ao detectar CAPTCHA: {str(e)}")
            return False
    
    def wait_for_captcha_resolution(self, max_wait: int = 300) -> bool:
        """
        Aguarda resolução manual do CAPTCHA
        
        Args:
            max_wait: Tempo máximo de espera em segundos
            
        Returns:
            True se CAPTCHA foi resolvido, False se timeout
        """
        print("👆 Resolva o CAPTCHA na janela do Chrome")
        print("⏳ Sistema aguardará automaticamente...")
        
        start_time = time.time()
        check_count = 0
        
        while time.time() - start_time < max_wait:
            check_count += 1
            print(f"⏳ Aguardando... ({check_count}/{max_wait//20})")
            
            time.sleep(20)  # Verificar a cada 20 segundos
            
            # Verificar se CAPTCHA foi resolvido
            if not self.detect_captcha():              # Verificar se perfil carregou
                if self.is_profile_loaded():
                    print("✅ PERFIL CARREGADO!")
                    return True
            
        print("⏰ Timeout aguardando resolução do CAPTCHA")
        return False
    
    def is_profile_loaded(self) -> bool:
        """
        Verifica se o perfil foi carregado corretamente
        
        Returns:
            True se perfil carregou, False caso contrário
        """
        try:
            # Verificar indicadores de perfil carregado
            profile_indicators = [
                "Currículo do Sistema de Currículos Lattes",
                "dados gerais",
                "formação acadêmica",
                "Última atualização"
            ]
            
            page_source = self.driver.page_source.lower()
            
            for indicator in profile_indicators:
                if indicator.lower() in page_source:
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Erro ao verificar perfil: {str(e)}")
            return False
    
    def extract_profile_data(self) -> Dict:
        """
        Extrai dados do perfil Lattes usando métodos robustos
        
        Returns:
            Dicionário com dados do perfil
        """
        try:
            print("🔍 Extraindo dados do perfil...")
            
            # Obter HTML da página
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extrair dados
            profile_data = {
                'name': self._extract_name(soup),
                'institution': self._extract_institution(soup),
                'last_update': self._extract_last_update(soup),
                'publications': self._extract_publications(soup),
                'lattes_url': self.driver.current_url
            }
            
            return profile_data
            
        except Exception as e:
            print(f"❌ Erro na extração: {str(e)}")
            return {}
    
    def _extract_name(self, soup: BeautifulSoup) -> str:
        """Extrai nome do pesquisador"""
        try:
            # Tentar diferentes seletores para o nome
            name_selectors = [
                'title',
                'h1',
                '.nome-pesquisador',
                '.dadosGerais h1'
            ]
            
            for selector in name_selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text().strip()
                    
                    # Extrair nome do título se necessário
                    if "Currículo do Sistema de Currículos Lattes" in text:
                        match = re.search(r'\((.*?)\)', text)
                        if match:
                            return match.group(1).strip()
                    elif text and len(text) > 3:
                        return text
            
            return "Nome não encontrado"
            
        except Exception as e:
            print(f"❌ Erro ao extrair nome: {str(e)}")
            return "Erro na extração do nome"
    
    def _extract_institution(self, soup: BeautifulSoup) -> str:
        """Extrai instituição atual"""
        try:
            # Procurar por diferentes padrões de instituição
            institution_patterns = [
                r'Vinculo.*?instituicional.*?:(.*?)(?:\n|<)',
                r'instituição.*?:(.*?)(?:\n|<)',
                r'Endereço.*?Profissional.*?:(.*?)(?:\n|<)'
            ]
            
            page_text = soup.get_text()
            
            for pattern in institution_patterns:
                match = re.search(pattern, page_text, re.IGNORECASE | re.DOTALL)
                if match:
                    institution = match.group(1).strip()
                    if len(institution) > 5:
                        return institution
            
            return "Instituição não informada"
            
        except Exception as e:
            print(f"❌ Erro ao extrair instituição: {str(e)}")
            return "Erro na extração da instituição"
    
    def _extract_last_update(self, soup: BeautifulSoup) -> str:
        """Extrai data da última atualização"""
        try:
            # Procurar padrões de data de atualização
            update_patterns = [
                r'última.*?atualização.*?do.*?currículo.*?em.*?(\d{2}/\d{2}/\d{4})',
                r'atualizado.*?em.*?(\d{2}/\d{2}/\d{4})',
                r'(\d{2}/\d{2}/\d{4})'
            ]
            
            page_text = soup.get_text()
            
            for pattern in update_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                if matches:
                    return matches[-1]  # Última data encontrada
            
            return "Data não encontrada"
            
        except Exception as e:
            print(f"❌ Erro ao extrair data: {str(e)}")
            return "Erro na extração da data"
    
    def _extract_publications(self, soup: BeautifulSoup) -> List[Dict]:
        """Extrai publicações"""
        try:
            publications = []
            
            # Procurar seções de publicações
            publication_sections = soup.find_all(['div', 'section'], 
                                                class_=re.compile(r'(artigo|trabalho|publicacao)', re.I))
            
            if not publication_sections:
                # Procurar por texto de publicações
                pub_texts = soup.find_all(text=re.compile(r'(Artigo|Trabalho|Publicação)', re.I))
                for text in pub_texts[:10]:  # Limitar a 10 publicações
                    parent = text.parent
                    if parent:
                        publications.append({
                            'title': parent.get_text().strip()[:100],
                            'year': 'N/A',
                            'type': 'Publicação'
                        })
            
            return publications
            
        except Exception as e:
            print(f"❌ Erro ao extrair publicações: {str(e)}")
            return []
    
    def close(self):
        """Fecha o ChromeDriver"""
        if self.driver:
            self.driver.quit()
            print("🔒 ChromeDriver fechado")

def extract_lattes_with_automation(lattes_id: str, headless: bool = False) -> Dict:
    """
    Função principal para extrair dados do Lattes com automação
    
    Args:
        lattes_id: ID do currículo Lattes
        headless: Se True, executa sem interface gráfica
        
    Returns:
        Dicionário com dados extraídos
    """
    automation = LattesAutomation(headless=headless)
    
    try:
        # Acessar perfil
        if not automation.access_lattes_profile(lattes_id):
            return {'error': 'Não foi possível acessar o perfil'}
        
        # Verificar CAPTCHA
        if automation.detect_captcha():
            if not headless:
                # Aguardar resolução manual
                if not automation.wait_for_captcha_resolution():
                    return {'error': 'CAPTCHA não foi resolvido a tempo'}
            else:
                return {'error': 'CAPTCHA detectado - modo headless não suportado'}
        
        # Extrair dados
        profile_data = automation.extract_profile_data()
        
        if profile_data:
            print("🎉 Extração concluída com sucesso!")
            return profile_data
        else:
            return {'error': 'Não foi possível extrair dados do perfil'}
    
    except Exception as e:
        return {'error': f'Erro na automação: {str(e)}'}
    
    finally:
        automation.close()

# Teste rápido
if __name__ == "__main__":
    print("🤖 SISTEMA CHROMEDRIVER PARA LATTES")
    print("=" * 50)
    
    # ID de teste
    test_id = "K4247989Z2"  # Nicolle Zimmermann
    
    print(f"🎯 Testando com ID: {test_id}")
    
    result = extract_lattes_with_automation(test_id, headless=False)
    
    if 'error' not in result:
        print("\n✅ SUCESSO!")
        print(f"👤 Nome: {result.get('name', 'N/A')}")
        print(f"🏛️ Instituição: {result.get('institution', 'N/A')}")
        print(f"📅 Última Atualização: {result.get('last_update', 'N/A')}")
        print(f"📚 Publicações: {len(result.get('publications', []))}")
    else:
        print(f"\n❌ ERRO: {result['error']}")