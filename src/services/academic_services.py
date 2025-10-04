"""
🔍 SERVIÇOS PARA BUSCA LATTES E ORCID
=====================================
Camada de serviço para operações de busca acadêmica
"""

import os
import re
import time
import requests
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv

from ..models.academic_models import (
    LattesProfile, LattesPublication, LattesProject, LattesEducation,
    ORCIDProfile, ORCIDWork, ORCIDEmployment, ORCIDEducation,
    PlatformType, LattesSearchType, ORCIDSearchType,
    AcademicSummary
)

# Carregar variáveis de ambiente
env_path = os.path.join(os.path.dirname(__file__), 'scraper', '.env')
load_dotenv(env_path)

class LattesService:
    """Serviço para busca na Plataforma Lattes"""
    
    def __init__(self):
        self.base_url = "http://buscatextual.cnpq.br/buscatextual"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.request_count = 0
    
    def search_by_name(self, name: str, max_results: int = 20) -> List[LattesProfile]:
        """Busca por nome no Lattes"""
        try:
            print(f"🔍 Buscando no Lattes: {name}")
            print("📝 NOTA: Sistema do Lattes com instabilidade, usando dados de demonstração")
            
            # Usar dados simulados enquanto resolve problemas do Lattes
            return self._create_demo_lattes_profiles(name, max_results)
            
            # TODO: Reativar quando resolver problemas de conectividade do Lattes
            # Código de busca real comentado temporariamente
            """
            # Múltiplas URLs para testar (sistema do Lattes mudou recentemente)
            urls_to_try = [
                # Busca POST (método correto)
                (f"{self.base_url}/buscatextual/busca.do", {
                    'metodo': 'buscar',
                    'textoBusca': name,
                    'buscarDoutores': '1',
                    'buscarDemais': '1',
                    'submit': 'Buscar'
                }, 'POST'),
                # Busca GET alternativa
                (f"{self.base_url}/buscatextual/busca.do", {
                    'metodo': 'buscar',
                    'textoBusca': name,
                    'tipoConsulta': 'PESSOA'
                }, 'GET'),
                # URL antiga
                (f"{self.base_url}/buscatextual/visualizacv.do", {
                    'metodo': 'apresentar',
                    'modoIndAdhoc': '1',
                    'textoBusca': name,
                    'assunto': 'buscarCurriculoCompleto'
                }, 'GET'),
            ]
            
            print(f"🔍 Buscando no Lattes: {name}")
            print(f"🔄 Testando {len(urls_to_try)} combinações de URL/parâmetros...")
            
            success_response = None
            for i, url_data in enumerate(urls_to_try):
                if len(url_data) == 3:
                    search_url, params, method = url_data
                else:
                    search_url, params = url_data
                    method = 'GET'
                    
                print(f"\n🌐 Tentativa {i+1}: {search_url} ({method})")
                print(f"📋 Parâmetros: {params}")
                
                try:
                    if method == 'POST':
                        response = self.session.post(search_url, data=params, timeout=30)
                    else:
                        response = self.session.get(search_url, params=params, timeout=30)
                    self.request_count += 1
                    
                    print(f"📊 Status: {response.status_code}")
                    print(f"📏 Tamanho: {len(response.content)} bytes")
                    
                    if response.status_code == 200:
                        # Verificar se não é uma página de erro ou formulário de busca
                        page_text = response.text.lower()
                        if ('error report' not in page_text and 
                            'exception' not in page_text and
                            'curriculum' in page_text and  # Deve ter conteúdo de currículo
                            len(response.content) > 50000):  # Deve ser uma página com conteúdo substancial
                            print("✅ Resposta válida encontrada!")
                            success_response = response
                            break
                        else:
                            print("⚠️ Página de busca/erro retornada, tentando próxima...")
                    else:
                        print(f"⚠️ Status {response.status_code}, tentando próxima...")
                        
                except Exception as e:
                    print(f"❌ Erro na tentativa: {e}")
                    continue
            
            if not success_response:
                print("❌ Todas as tentativas falharam, usando dados simulados para demonstração")
                # Retornar dados simulados para demonstração
                return self._create_demo_lattes_profiles(name, max_results)
            
            response = success_response
            
            # Debug da resposta - VERSÃO MELHORADA
            soup = BeautifulSoup(response.content, 'html.parser')
            
            print(f"📄 Título da página: {soup.title.string if soup.title else 'Sem título'}")
            print(f"� Tamanho do conteúdo: {len(response.content)} bytes")
            
            # Análise detalhada da estrutura HTML
            print("\n🔍 ANÁLISE DA ESTRUTURA HTML:")
            
            # Verificar divs com possíveis classes de resultado
            possible_classes = ['resultado', 'busca-resultado', 'resultado-busca', 'item-resultado', 'search-result']
            for cls in possible_classes:
                elements = soup.find_all('div', class_=cls)
                if elements:
                    print(f"📋 Encontradas {len(elements)} divs com classe '{cls}'")
            
            # Verificar tabelas
            tables = soup.find_all('table')
            print(f"📊 Encontradas {len(tables)} tabelas")
            
            # Verificar links para currículos
            cv_links = soup.find_all('a', href=re.compile(r'(visualizacv\.do|curriculo\.do).*id='))
            print(f"🔗 Encontrados {len(cv_links)} links para currículos")
            
            # Verificar formulários (pode estar em página de busca)
            forms = soup.find_all('form')
            print(f"📝 Encontrados {len(forms)} formulários")
            
            # Verificar se há mensagens de erro ou "nenhum resultado"
            no_results_texts = ['nenhum resultado', 'não encontrado', 'sem resultados', 'no results']
            page_text = soup.get_text().lower()
            for text in no_results_texts:
                if text in page_text:
                    print(f"⚠️ Encontrada mensagem: '{text}'")
            
            # Salvar HTML para análise (apenas os primeiros 2000 chars)
            html_sample = str(soup)[:2000]
            print(f"\n📄 AMOSTRA DO HTML (primeiros 2000 chars):")
            print("=" * 60)
            print(html_sample)
            print("=" * 60)
            
            # Verificar se chegamos na página certa
            if 'lattes' not in page_text:
                print("⚠️ ATENÇÃO: Não parece ser uma página do Lattes!")
            if 'busca' not in page_text and 'search' not in page_text:
                print("⚠️ ATENÇÃO: Não parece ser uma página de busca!")
            
            print(f"\n🎯 Iniciando extração de perfis...")
            profiles = self._extract_lattes_profiles(soup, max_results)
            
            print(f"✅ Encontrados {len(profiles)} perfis no Lattes")
            return profiles
            """
            
        except Exception as e:
            print(f"❌ Erro na busca Lattes: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_full_profile(self, lattes_id: str) -> Optional[LattesProfile]:
        """Obtém perfil completo do Lattes"""
        try:
            cv_url = f"{self.base_url}/visualizacv.do"
            params = {'id': lattes_id}
            
            print(f"📋 Carregando perfil completo: {lattes_id}")
            response = self.session.get(cv_url, params=params, timeout=30)
            self.request_count += 1
            
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            profile = self._parse_full_lattes_profile(soup, lattes_id)
            
            return profile
            
        except Exception as e:
            print(f"❌ Erro ao carregar perfil: {e}")
            return None
    
    def _extract_lattes_profiles(self, soup: BeautifulSoup, max_results: int) -> List[LattesProfile]:
        """Extrai perfis básicos da página de busca - VERSÃO MELHORADA"""
        profiles = []
        
        print("🔍 Iniciando extração de perfis...")
        
        # Múltiplas estratégias de busca
        result_elements = []
        
        # Estratégia 1: Divs com classe resultado
        result_divs = soup.find_all('div', class_=['resultado', 'busca-resultado', 'resultado-busca'])
        if result_divs:
            result_elements = result_divs
            print(f"📋 Estratégia 1: {len(result_divs)} divs encontradas")
        
        # Estratégia 2: Tabelas de resultados
        if not result_elements:
            result_tables = soup.find_all('table', class_=['resultado', 'resultado-busca'])
            if result_tables:
                for table in result_tables:
                    result_elements.extend(table.find_all('tr'))
                print(f"📋 Estratégia 2: {len(result_elements)} linhas de tabela")
        
        # Estratégia 3: Links para currículos
        if not result_elements:
            cv_links = soup.find_all('a', href=re.compile(r'visualizacv\.do.*id='))
            result_elements = [link.parent for link in cv_links if link.parent]
            print(f"📋 Estratégia 3: {len(result_elements)} links de CV")
        
        # Estratégia 4: Busca por padrões de nome
        if not result_elements:
            # Busca por qualquer link ou texto que pareça ser um nome
            all_links = soup.find_all('a')
            for link in all_links:
                if link.get('href') and 'id=' in link.get('href', ''):
                    result_elements.append(link.parent or link)
            print(f"📋 Estratégia 4: {len(result_elements)} elementos com links")
        
        print(f"🎯 Total de elementos para processar: {len(result_elements)}")
        
        processed = 0
        for i, element in enumerate(result_elements[:max_results * 3]):  # Processar mais elementos
            try:
                print(f"🔄 Processando elemento {i+1}...")
                
                # Busca nome - múltiplas estratégias
                name = None
                name_element = None
                
                # Procurar link com href contendo 'id='
                cv_link = element.find('a', href=re.compile(r'id='))
                if cv_link:
                    name = cv_link.get_text(strip=True)
                    name_element = cv_link
                    print(f"✅ Nome encontrado via link CV: {name}")
                
                # Se não encontrou, buscar outros elementos
                if not name:
                    for tag in ['a', 'strong', 'b', 'h3', 'h4']:
                        elem = element.find(tag)
                        if elem and elem.get_text(strip=True):
                            name = elem.get_text(strip=True)
                            name_element = elem
                            print(f"✅ Nome encontrado via {tag}: {name}")
                            break
                
                if not name or len(name) < 3:
                    print(f"⚠️ Nome inválido ou muito curto: {name}")
                    continue
                
                # Extrair ID do Lattes
                lattes_id = None
                if name_element:
                    link = name_element.get('href', '')
                    if 'id=' in link:
                        lattes_id = link.split('id=')[1].split('&')[0]
                        print(f"🆔 ID encontrado: {lattes_id}")
                
                # Buscar informações adicionais no texto do elemento
                element_text = element.get_text()
                
                # Instituição
                institution = None
                for pattern in [r'[Ii]nstituição:?\s*([^;\n]+)', r'[Uu]niversidade\s+([^;\n]+)', r'[Ii]nstituto\s+([^;\n]+)']:
                    match = re.search(pattern, element_text)
                    if match:
                        institution = match.group(1).strip()
                        break
                
                # Área de pesquisa
                area = None
                for pattern in [r'[Áá]rea:?\s*([^;\n]+)', r'[Pp]esquisa:?\s*([^;\n]+)']:
                    match = re.search(pattern, element_text)
                    if match:
                        area = match.group(1).strip()
                        break
                
                # Criar perfil
                profile = LattesProfile(
                    name=name,
                    lattes_id=lattes_id,
                    current_institution=institution,
                    research_areas=[area] if area else [],
                    summary=element_text[:200] if element_text else None  # Resumo dos primeiros 200 chars
                )
                
                profiles.append(profile)
                processed += 1
                print(f"✅ Perfil {processed} criado: {name}")
                
                if len(profiles) >= max_results:
                    break
                
            except Exception as e:
                print(f"⚠️ Erro ao processar elemento {i+1}: {e}")
                continue
        
        print(f"🎯 Extração concluída: {len(profiles)} perfis válidos de {processed} processados")
        return profiles
    
    def _create_demo_lattes_profiles(self, name: str, max_results: int) -> List[LattesProfile]:
        """Cria perfis de demonstração quando a busca real falha"""
        print(f"🎭 Criando dados de demonstração para '{name}'...")
        
        demo_profiles = []
        base_names = [
            f"{name} (Prof. Dr.)",
            f"{name} Silva",
            f"{name} Santos",
            f"{name} Junior",
            f"{name} Neto"
        ]
        
        institutions = [
            "Universidade de São Paulo (USP)",
            "Universidade Federal do Rio de Janeiro (UFRJ)",
            "Universidade Estadual de Campinas (UNICAMP)",
            "Universidade Federal de Minas Gerais (UFMG)",
            "Pontifícia Universidade Católica de São Paulo (PUC-SP)"
        ]
        
        research_areas = [
            ["Inteligência Artificial", "Machine Learning"],
            ["Engenharia de Software", "Sistemas Distribuídos"],
            ["Bioinformática", "Biologia Computacional"],
            ["Redes de Computadores", "Segurança da Informação"],
            ["Banco de Dados", "Big Data"]
        ]
        
        for i in range(min(max_results, len(base_names))):
            profile = LattesProfile(
                name=base_names[i],
                lattes_id=f"demo_{i+1}_{hash(name) % 10000}",
                current_institution=institutions[i],
                research_areas=research_areas[i],
                summary=f"Pesquisador na área de {research_areas[i][0]}, com experiência em {research_areas[i][1]}. Perfil demonstrativo para testes do sistema.",
                total_citations=50 + (i * 25),
                h_index=5 + i,
                publications_count=15 + (i * 10)
            )
            demo_profiles.append(profile)
            print(f"🎭 Perfil demo criado: {profile.name}")
        
        print(f"✅ {len(demo_profiles)} perfis de demonstração criados")
        return demo_profiles
    
    def _parse_full_lattes_profile(self, soup: BeautifulSoup, lattes_id: str) -> LattesProfile:
        """Parse completo do currículo Lattes"""
        
        # Informações básicas
        name = self._extract_text_by_selector(soup, 'h2.nome') or "Nome não encontrado"
        
        # Dados pessoais
        birth_date = self._extract_date_by_pattern(soup, r'nascimento:?\s*(\d{2}/\d{2}/\d{4})')
        nationality = self._extract_text_by_pattern(soup, r'nacionalidade:?\s*([^;]+)')
        
        # ORCID
        orcid_id = self._extract_text_by_pattern(soup, r'ORCID.*?(\d{4}-\d{4}-\d{4}-\d{3}[\dX])')
        
        # Instituição atual
        current_institution = self._extract_text_by_pattern(soup, r'Instituição:?\s*([^;]+)')
        current_position = self._extract_text_by_pattern(soup, r'Cargo:?\s*([^;]+)')
        
        # Áreas de pesquisa
        research_areas = self._extract_research_areas(soup)
        
        # Formação acadêmica
        education = self._extract_education(soup)
        
        # Publicações
        publications = self._extract_publications(soup)
        
        # Projetos
        projects = self._extract_projects(soup)
        
        profile = LattesProfile(
            name=name,
            lattes_id=lattes_id,
            orcid_id=orcid_id,
            birth_date=birth_date,
            nationality=nationality,
            current_institution=current_institution,
            current_position=current_position,
            research_areas=research_areas,
            education=education,
            publications=publications,
            projects=projects,
            total_publications=len(publications),
            total_projects=len(projects),
            last_update=datetime.now()
        )
        
        return profile
    
    def _extract_education(self, soup: BeautifulSoup) -> List[LattesEducation]:
        """Extrai formação acadêmica"""
        education_list = []
        
        # Busca seções de formação
        education_sections = soup.find_all('div', class_='formacao') or soup.find_all('tr', class_='formacao')
        
        for section in education_sections:
            try:
                level = self._extract_text_by_pattern(section, r'(Graduação|Mestrado|Doutorado|Pós-doutorado)')
                course = self._extract_text_by_pattern(section, r'Curso:?\s*([^;]+)')
                institution = self._extract_text_by_pattern(section, r'Instituição:?\s*([^;]+)')
                
                # Anos
                year_match = re.search(r'(\d{4})\s*-\s*(\d{4})', section.get_text())
                year_start = int(year_match.group(1)) if year_match else None
                year_end = int(year_match.group(2)) if year_match else None
                
                if level:
                    education = LattesEducation(
                        level=level,
                        course=course,
                        institution=institution,
                        year_start=year_start,
                        year_end=year_end
                    )
                    education_list.append(education)
                    
            except Exception as e:
                continue
        
        return education_list
    
    def _extract_publications(self, soup: BeautifulSoup) -> List[LattesPublication]:
        """Extrai publicações"""
        publications = []
        
        # Busca seções de publicações
        pub_sections = soup.find_all('div', class_='artigo') or soup.find_all('li', class_='artigo')
        
        for section in pub_sections:
            try:
                text = section.get_text()
                
                # Título (geralmente em negrito ou primeira linha)
                title_element = section.find('strong') or section.find('b')
                title = title_element.get_text(strip=True) if title_element else ""
                
                # Autores
                authors = self._extract_text_by_pattern(section, r'Autores?:?\s*([^;]+)')
                
                # Revista
                journal = self._extract_text_by_pattern(section, r'(?:Periódico|Revista):?\s*([^;]+)')
                
                # Ano
                year_match = re.search(r'\b(19|20)\d{2}\b', text)
                year = int(year_match.group()) if year_match else None
                
                # DOI
                doi = self._extract_text_by_pattern(section, r'DOI:?\s*([^;\s]+)')
                
                if title:
                    publication = LattesPublication(
                        title=title,
                        authors=authors,
                        journal=journal,
                        year=year,
                        doi=doi
                    )
                    publications.append(publication)
                    
            except Exception as e:
                continue
        
        return publications
    
    def _extract_projects(self, soup: BeautifulSoup) -> List[LattesProject]:
        """Extrai projetos de pesquisa"""
        projects = []
        
        # Busca seções de projetos
        project_sections = soup.find_all('div', class_='projeto') or soup.find_all('li', class_='projeto')
        
        for section in project_sections:
            try:
                title_element = section.find('strong') or section.find('b')
                title = title_element.get_text(strip=True) if title_element else ""
                
                description = self._extract_text_by_pattern(section, r'Descrição:?\s*([^;]+)')
                funding_agency = self._extract_text_by_pattern(section, r'(?:Financiadora|Agência):?\s*([^;]+)')
                
                # Anos do projeto
                year_match = re.search(r'(\d{4})\s*-\s*(\d{4})', section.get_text())
                year_start = int(year_match.group(1)) if year_match else None
                year_end = int(year_match.group(2)) if year_match else None
                
                if title:
                    project = LattesProject(
                        title=title,
                        description=description,
                        year_start=year_start,
                        year_end=year_end,
                        funding_agency=funding_agency
                    )
                    projects.append(project)
                    
            except Exception as e:
                continue
        
        return projects
    
    def _extract_research_areas(self, soup: BeautifulSoup) -> List[str]:
        """Extrai áreas de pesquisa"""
        areas = []
        
        # Busca seções de áreas de atuação
        area_sections = soup.find_all('div', class_='area') or soup.find_all('li', class_='area')
        
        for section in area_sections:
            area_text = section.get_text(strip=True)
            if area_text:
                areas.append(area_text)
        
        return areas
    
    def _extract_text_by_pattern(self, element, pattern: str) -> Optional[str]:
        """Extrai texto usando regex"""
        try:
            text = element.get_text() if hasattr(element, 'get_text') else str(element)
            match = re.search(pattern, text, re.IGNORECASE)
            return match.group(1).strip() if match else None
        except:
            return None
    
    def _extract_text_by_selector(self, soup: BeautifulSoup, selector: str) -> Optional[str]:
        """Extrai texto usando seletor CSS"""
        try:
            element = soup.select_one(selector)
            return element.get_text(strip=True) if element else None
        except:
            return None
    
    def _extract_date_by_pattern(self, soup: BeautifulSoup, pattern: str) -> Optional[date]:
        """Extrai data usando regex"""
        try:
            text = soup.get_text()
            match = re.search(pattern, text)
            if match:
                date_str = match.group(1)
                return datetime.strptime(date_str, '%d/%m/%Y').date()
            return None
        except:
            return None

    def search_by_research_area(self, area: str, max_results: int = 20) -> List[LattesProfile]:
        """Busca pesquisadores por área de pesquisa"""
        try:
            # Por simplicidade, usar busca por nome mas filtrar por área
            profiles = self.search_by_name(area, max_results * 2)  # Buscar mais para filtrar
            
            # Filtrar profiles que tenham a área nas research_areas
            filtered_profiles = []
            for profile in profiles:
                if any(area.lower() in research_area.lower() for research_area in profile.research_areas):
                    filtered_profiles.append(profile)
                    if len(filtered_profiles) >= max_results:
                        break
            
            return filtered_profiles
        except Exception as e:
            print(f"Erro na busca por área: {e}")
            return []

    def get_profile_by_id(self, lattes_id: str) -> Optional[LattesProfile]:
        """Busca perfil específico pelo ID do Lattes"""
        try:
            url = f"{self.base_url}/visualizacv.do?metodo=apresentar&id={lattes_id}"
            
            response = self.session.get(url, timeout=10)
            self.request_count += 1
            
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrair dados básicos
            name = soup.find('h2', class_='nome')
            name = name.get_text().strip() if name else "Nome não encontrado"
            
            # Tentar extrair outras informações (implementação simplificada)
            profile = LattesProfile(
                name=name,
                lattes_id=lattes_id,
                current_institution="",
                current_position="",
                research_areas=[],
                education=[],
                publications=[],
                projects=[],
                total_publications=0,
                total_projects=0
            )
            
            return profile
            
        except Exception as e:
            print(f"Erro ao buscar perfil {lattes_id}: {e}")
            return None

class ORCIDService:
    """Serviço para busca no ORCID"""
    
    def __init__(self):
        self.base_url = "https://pub.orcid.org/v3.0"
        self.search_url = "https://pub.orcid.org/v3.0/search"
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 Academic Research Tool'
        })
        self.request_count = 0
    
    def search_by_name(self, name: str, max_results: int = 20) -> List[ORCIDProfile]:
        """Busca por nome no ORCID"""
        try:
            # Query de busca
            query = f'given-names:"{name.split()[0]}"'
            if len(name.split()) > 1:
                query += f' AND family-name:"{name.split()[-1]}"'
            
            params = {
                'q': query,
                'rows': min(max_results, 200),  # ORCID API limit
                'start': 0
            }
            
            print(f"🔍 Buscando no ORCID: {name}")
            response = self.session.get(self.search_url, params=params, timeout=30)
            self.request_count += 1
            
            if response.status_code != 200:
                raise Exception(f"Erro na busca ORCID: Status {response.status_code}")
            
            data = response.json()
            profiles = self._process_orcid_search_results(data, max_results)
            
            print(f"✅ Encontrados {len(profiles)} perfis no ORCID")
            return profiles
            
        except Exception as e:
            print(f"❌ Erro na busca ORCID: {e}")
            return []
    
    def get_full_profile(self, orcid_id: str) -> Optional[ORCIDProfile]:
        """Obtém perfil completo do ORCID"""
        try:
            # Remove URL prefix if present
            orcid_id = orcid_id.replace('https://orcid.org/', '')
            
            profile_url = f"{self.base_url}/{orcid_id}/record"
            
            print(f"📋 Carregando perfil ORCID: {orcid_id}")
            response = self.session.get(profile_url, timeout=30)
            self.request_count += 1
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            profile = self._parse_full_orcid_profile(data, orcid_id)
            
            return profile
            
        except Exception as e:
            print(f"❌ Erro ao carregar perfil ORCID: {e}")
            return None
    
    def _process_orcid_search_results(self, data: Dict, max_results: int) -> List[ORCIDProfile]:
        """Processa resultados de busca do ORCID"""
        profiles = []
        
        results = data.get('result', [])
        
        for result in results[:max_results]:
            try:
                orcid_id = result.get('orcid-identifier', {}).get('path', '')
                
                if orcid_id:
                    # Busca perfil completo
                    full_profile = self.get_full_profile(orcid_id)
                    if full_profile:
                        profiles.append(full_profile)
                
                # Rate limiting
                time.sleep(0.1)
                
            except Exception as e:
                print(f"⚠️ Erro ao processar resultado ORCID: {e}")
                continue
        
        return profiles
    
    def _parse_full_orcid_profile(self, data: Dict, orcid_id: str) -> ORCIDProfile:
        """Parse completo do perfil ORCID com logs de debug"""
        
        print(f"🔍 ORCID DEBUG - Processando perfil {orcid_id}")
        
        # Verificação de segurança
        if not data or not isinstance(data, dict):
            print(f"⚠️ Dados ORCID inválidos para {orcid_id}")
            return self._create_basic_orcid_profile(orcid_id)
        
        try:
            person = data.get('person', {}) or {}
            activities = data.get('activities-summary', {}) or {}
            
            print(f"🔍 ORCID DEBUG - Person data: {bool(person)}")
            print(f"🔍 ORCID DEBUG - Activities data: {bool(activities)}")
            
            # Informações pessoais básicas
            name = person.get('name') or {}
            given_names = self._safe_extract(name, ['given-names', 'value'])
            family_name = self._safe_extract(name, ['family-name', 'value'])
            credit_name = self._safe_extract(name, ['credit-name', 'value'])
            
            # Nome para exibição
            display_name = credit_name or f"{given_names or ''} {family_name or ''}".strip() or f"ORCID User {orcid_id[:8]}"
            
            print(f"🔍 ORCID DEBUG - Nome extraído: {display_name}")
            
            # Biografia
            biography = self._safe_extract(person, ['biography', 'content']) or ""
            
            # Outros nomes
            other_names = []
            other_names_data = person.get('other-names', {}) or {}
            if other_names_data.get('other-name'):
                for other_name in other_names_data['other-name']:
                    if other_name and other_name.get('content'):
                        other_names.append(other_name['content'])
            
            # URLs do pesquisador
            researcher_urls = []
            urls_data = person.get('researcher-urls', {}) or {}
            if urls_data.get('researcher-url'):
                for url_item in urls_data['researcher-url']:
                    if url_item and url_item.get('url', {}).get('value'):
                        researcher_urls.append({
                            'name': url_item.get('url-name', 'Website'),
                            'url': url_item['url']['value']
                        })
            
            # Emails (simplificado)
            emails = []
            emails_data = person.get('emails', {}) or {}
            if emails_data.get('email'):
                for email_item in emails_data['email']:
                    if email_item and email_item.get('email'):
                        emails.append(email_item['email'])
            
            # Empregos/Afiliações (simplificado)
            employments = self._extract_orcid_employments_simple(activities.get('employments', {}) or {})
            
            # Educação (simplificado)  
            educations = self._extract_orcid_educations_simple(activities.get('educations', {}) or {})
            
            # Trabalhos/Publicações (simplificado)
            works = self._extract_orcid_works_simple(activities.get('works', {}) or {})
            
            print(f"✅ ORCID DEBUG - Perfil processado: {display_name} ({len(employments)} empregos, {len(works)} trabalhos)")
            
            profile = ORCIDProfile(
                orcid_id=orcid_id,
                given_names=given_names or "",
                family_name=family_name or "",
                credit_name=credit_name or "",
                other_names=other_names,
                biography=biography,
                researcher_urls=researcher_urls,
                emails=emails,
                employments=employments,
                educations=educations,
                works=works,
                last_modified_date=datetime.now()
            )
            
            return profile
            
        except Exception as e:
            print(f"❌ Erro ao processar perfil ORCID {orcid_id}: {e}")
            return self._create_basic_orcid_profile(orcid_id)
    
    def _safe_extract(self, data: Dict, path: List[str]):
        """Extração segura de dados aninhados"""
        try:
            result = data
            for key in path:
                result = result.get(key)
                if result is None:
                    return None
            return result
        except:
            return None
    
    def _create_basic_orcid_profile(self, orcid_id: str) -> ORCIDProfile:
        """Cria perfil ORCID básico quando há erro no processamento"""
        return ORCIDProfile(
            orcid_id=orcid_id,
            given_names="",
            family_name="",
            credit_name=f"ORCID User {orcid_id[:8]}",
            other_names=[],
            biography="Perfil ORCID disponível",
            researcher_urls=[],
            emails=[],
            employments=[],
            educations=[],
            works=[],
            last_modified_date=datetime.now()
        )
        if emails_data.get('email'):
            for email in emails_data['email']:
                if email and email.get('email'):
                    emails.append(email['email'])
        
        # URLs
        researcher_urls = []
        urls_data = person.get('researcher-urls', {}) or {}
        if urls_data.get('researcher-url'):
            for url_data in urls_data['researcher-url']:
                if url_data and url_data.get('url') and url_data['url'].get('value'):
                    researcher_urls.append({
                        'name': url_data.get('url-name', ''),
                        'url': url_data['url']['value']
                    })
        
        # Empregos
        employments = self._extract_orcid_employments(activities.get('employments', {}) or {})
        
        # Educação
        educations = self._extract_orcid_educations(activities.get('educations', {}) or {})
        
        # Trabalhos/Publicações
        works = self._extract_orcid_works(activities.get('works', {}) or {})
        
        profile = ORCIDProfile(
            orcid_id=orcid_id,
            given_names=given_names or "",
            family_name=family_name or "",
            credit_name=credit_name or "",
            other_names=other_names,
            biography=biography,
            researcher_urls=researcher_urls,
            emails=emails,
            employments=employments,
            educations=educations,
            works=works,
            last_modified_date=datetime.now()
        )
        
        return profile
    
    def _extract_orcid_employments(self, employments_data: Dict) -> List[ORCIDEmployment]:
        """Extrai empregos do ORCID"""
        employments = []
        
        for group in employments_data.get('affiliation-group', []):
            for summary in group.get('summaries', []):
                emp_data = summary.get('employment-summary', {})
                
                org = emp_data.get('organization', {})
                organization = org.get('name', '')
                
                role_title = emp_data.get('role-title', '')
                department = emp_data.get('department-name', '')
                
                # Datas
                start_date = self._extract_orcid_date(emp_data.get('start-date'))
                end_date = self._extract_orcid_date(emp_data.get('end-date'))
                
                city = org.get('address', {}).get('city', '')
                country = org.get('address', {}).get('country', '')
                
                employment = ORCIDEmployment(
                    organization=organization,
                    role_title=role_title,
                    department=department,
                    start_date=start_date,
                    end_date=end_date,
                    city=city,
                    country=country
                )
                employments.append(employment)
        
        return employments
    
    def _extract_orcid_educations(self, educations_data: Dict) -> List[ORCIDEducation]:
        """Extrai educação do ORCID"""
        educations = []
        
        for group in educations_data.get('affiliation-group', []):
            for summary in group.get('summaries', []):
                edu_data = summary.get('education-summary', {})
                
                org = edu_data.get('organization', {})
                organization = org.get('name', '')
                
                degree = edu_data.get('role-title', '')
                
                # Datas
                start_date = self._extract_orcid_date(edu_data.get('start-date'))
                end_date = self._extract_orcid_date(edu_data.get('end-date'))
                
                city = org.get('address', {}).get('city', '')
                country = org.get('address', {}).get('country', '')
                
                education = ORCIDEducation(
                    organization=organization,
                    degree=degree,
                    start_date=start_date,
                    end_date=end_date,
                    city=city,
                    country=country
                )
                educations.append(education)
        
        return educations
    
    def _extract_orcid_works(self, works_data: Dict) -> List[ORCIDWork]:
        """Extrai trabalhos/publicações do ORCID"""
        works = []
        
        for group in works_data.get('group', []):
            for summary in group.get('work-summary', []):
                title_data = summary.get('title', {})
                title = title_data.get('title', {}).get('value', '') if title_data else ''
                
                journal_title = summary.get('journal-title', {}).get('value') if summary.get('journal-title') else None
                work_type = summary.get('type', '')
                
                # Data de publicação
                pub_date = self._extract_orcid_date(summary.get('publication-date'))
                
                # IDs externos
                external_ids = []
                for ext_id in summary.get('external-ids', {}).get('external-id', []):
                    external_ids.append({
                        'type': ext_id.get('external-id-type', ''),
                        'value': ext_id.get('external-id-value', '')
                    })
                
                url = summary.get('url', {}).get('value') if summary.get('url') else None
                
                work = ORCIDWork(
                    title=title,
                    journal_title=journal_title,
                    type=work_type,
                    publication_date=pub_date,
                    external_ids=external_ids,
                    url=url
                )
                works.append(work)
        
        return works

    def _extract_orcid_employments_simple(self, employments_data: Dict) -> List[ORCIDEmployment]:
        """Extração simplificada de empregos do ORCID"""
        employments = []
        try:
            for group in employments_data.get('affiliation-group', []):
                for summary in group.get('summaries', []):
                    emp_data = summary.get('employment-summary', {})
                    
                    org = emp_data.get('organization', {})
                    organization = org.get('name', 'Organização não informada')
                    role_title = emp_data.get('role-title', '')
                    
                    employment = ORCIDEmployment(
                        organization=organization,
                        role_title=role_title,
                        department="",
                        start_date=None,
                        end_date=None,
                        city="",
                        country=""
                    )
                    employments.append(employment)
        except Exception as e:
            print(f"⚠️ Erro ao extrair empregos ORCID: {e}")
        
        return employments

    def _extract_orcid_educations_simple(self, educations_data: Dict) -> List[ORCIDEducation]:
        """Extração simplificada de educação do ORCID"""
        educations = []
        try:
            for group in educations_data.get('affiliation-group', []):
                for summary in group.get('summaries', []):
                    edu_data = summary.get('education-summary', {})
                    
                    org = edu_data.get('organization', {})
                    organization = org.get('name', 'Instituição não informada')
                    degree = edu_data.get('role-title', '')
                    
                    education = ORCIDEducation(
                        organization=organization,
                        degree=degree,
                        department="",
                        start_date=None,
                        end_date=None,
                        city="",
                        country=""
                    )
                    educations.append(education)
        except Exception as e:
            print(f"⚠️ Erro ao extrair educação ORCID: {e}")
        
        return educations

    def _extract_orcid_works_simple(self, works_data: Dict) -> List[ORCIDWork]:
        """Extração simplificada de trabalhos do ORCID"""
        works = []
        try:
            for group in works_data.get('group', []):
                for summary in group.get('work-summary', []):
                    title_data = summary.get('title', {})
                    title = title_data.get('title', {}).get('value', 'Título não disponível')
                    
                    work_type = summary.get('type', 'publication')
                    journal = summary.get('journal-title', {}).get('value', '') if summary.get('journal-title') else ''
                    
                    work = ORCIDWork(
                        title=title,
                        journal_title=journal,
                        type=work_type,
                        publication_date=None,
                        external_ids=[],
                        url=""
                    )
                    works.append(work)
        except Exception as e:
            print(f"⚠️ Erro ao extrair trabalhos ORCID: {e}")
        
        return works

    def search_by_research_area(self, area: str, max_results: int = 20) -> List[ORCIDProfile]:
        """Busca pesquisadores por área de pesquisa"""
        try:
            # ORCID permite busca por keyword nos works
            params = {
                'q': f'keyword:"{area}"',
                'start': 0,
                'rows': min(max_results, 200)
            }
            
            response = self.session.get(self.search_url, params=params, timeout=10)
            self.request_count += 1
            
            if response.status_code != 200:
                return []
                
            data = response.json()
            profiles = []
            
            results = data.get('result', [])
            for result in results[:max_results]:
                orcid_id = result.get('orcid-identifier', {}).get('path', '')
                if orcid_id:
                    profile = self.get_profile_by_id(orcid_id)
                    if profile:
                        profiles.append(profile)
                        
            return profiles
            
        except Exception as e:
            print(f"Erro na busca ORCID por área: {e}")
            return []

    def get_profile_by_id(self, orcid_id: str) -> Optional[ORCIDProfile]:
        """Busca perfil específico pelo ORCID ID"""
        try:
            # Remove URL prefix if present
            orcid_id = orcid_id.replace('https://orcid.org/', '')
            
            profile_url = f"{self.base_url}/{orcid_id}/record"
            
            response = self.session.get(profile_url, timeout=10)
            self.request_count += 1
            
            if response.status_code != 200:
                return None
                
            data = response.json()
            
            # Usar o método existente de parse
            profile = self._parse_full_orcid_profile(data, orcid_id)
            
            return profile
            
        except Exception as e:
            print(f"Erro ao buscar perfil ORCID {orcid_id}: {e}")
            return None

    def search_works_by_keyword(self, keyword: str, max_results: int = 20) -> List[Dict]:
        """Busca trabalhos por palavra-chave"""
        try:
            params = {
                'q': f'text:"{keyword}"',
                'start': 0,
                'rows': min(max_results, 200)
            }
            
            response = self.session.get(self.search_url, params=params, timeout=10)
            self.request_count += 1
            
            if response.status_code != 200:
                return []
                
            data = response.json()
            works = []
            
            results = data.get('result', [])
            for result in results:
                work_info = {
                    'title': 'ORCID Search Result',
                    'authors': [f"{result.get('given-names', '')} {result.get('family-names', '')}".strip()],
                    'orcid_id': result.get('orcid-identifier', {}).get('path', ''),
                    'relevance_score': result.get('relevancy-score', {}).get('value', 0)
                }
                works.append(work_info)
                    
            return works
            
        except Exception as e:
            print(f"Erro na busca de trabalhos ORCID: {e}")
            return []
    
    def _extract_orcid_date(self, date_data: Optional[Dict]) -> Optional[date]:
        """Extrai data do formato ORCID"""
        if not date_data:
            return None
        
        try:
            year = date_data.get('year', {}).get('value')
            month = date_data.get('month', {}).get('value', 1)
            day = date_data.get('day', {}).get('value', 1)
            
            if year:
                return date(int(year), int(month), int(day))
            return None
        except:
            return None

class AcademicResearchService:
    """Serviço unificado para pesquisa acadêmica"""
    
    def __init__(self):
        self.lattes_service = LattesService()
        self.orcid_service = ORCIDService()
    
    def comprehensive_search(self, researcher_name: str, max_results: int = 20) -> Tuple[List[LattesProfile], List[ORCIDProfile], AcademicSummary]:
        """Busca completa em todas as plataformas"""
        print(f"🎯 BUSCA ACADÊMICA COMPLETA: {researcher_name}")
        print("=" * 60)
        
        # Busca no Lattes
        lattes_profiles = self.lattes_service.search_by_name(researcher_name, max_results)
        
        # Busca no ORCID
        orcid_profiles = self.orcid_service.search_by_name(researcher_name, max_results)
        
        # Gera resumo
        summary = self._generate_academic_summary(researcher_name, lattes_profiles, orcid_profiles)
        
        return lattes_profiles, orcid_profiles, summary
    
    def _generate_academic_summary(self, researcher_name: str, lattes_profiles: List[LattesProfile], orcid_profiles: List[ORCIDProfile]) -> AcademicSummary:
        """Gera resumo acadêmico unificado"""
        
        platforms_found = []
        if lattes_profiles:
            platforms_found.append(PlatformType.LATTES)
        if orcid_profiles:
            platforms_found.append(PlatformType.ORCID)
        
        # Estatísticas agregadas
        total_publications = sum(p.total_publications for p in lattes_profiles)
        total_publications += sum(len(p.works) for p in orcid_profiles)
        
        total_projects = sum(p.total_projects for p in lattes_profiles)
        
        # Instituições
        institutions = []
        for profile in lattes_profiles:
            if profile.current_institution:
                institutions.append(profile.current_institution)
        
        for profile in orcid_profiles:
            for emp in profile.employments:
                institutions.append(emp.organization)
        
        institutions = list(set(institutions))  # Remove duplicatas
        
        # Áreas de pesquisa
        research_areas = []
        for profile in lattes_profiles:
            research_areas.extend(profile.research_areas)
        
        research_areas = list(set(research_areas))  # Remove duplicatas
        
        # Comparação entre plataformas
        platform_comparison = {
            "lattes": {
                "profiles_found": len(lattes_profiles),
                "total_publications": sum(p.total_publications for p in lattes_profiles),
                "total_projects": sum(p.total_projects for p in lattes_profiles)
            },
            "orcid": {
                "profiles_found": len(orcid_profiles),
                "total_works": sum(len(p.works) for p in orcid_profiles),
                "total_employments": sum(len(p.employments) for p in orcid_profiles)
            }
        }
        
        summary = AcademicSummary(
            researcher_name=researcher_name,
            platforms_found=platforms_found,
            total_publications=total_publications,
            total_projects=total_projects,
            institutions=institutions,
            research_areas=research_areas,
            platform_comparison=platform_comparison
        )
        
        return summary
    
    def save_to_csv(self, lattes_profiles: List[LattesProfile], orcid_profiles: List[ORCIDProfile], researcher_name: str) -> str:
        """Salva dados em CSV"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"academic_research_{researcher_name.replace(' ', '_').lower()}_{timestamp}.csv"
        
        # Combina dados de ambas as plataformas
        combined_data = []
        
        # Dados do Lattes
        for profile in lattes_profiles:
            combined_data.append({
                "platform": "Lattes",
                "name": profile.name,
                "id": profile.lattes_id,
                "institution": profile.current_institution,
                "position": profile.current_position,
                "total_publications": profile.total_publications,
                "total_projects": profile.total_projects,
                "research_areas": "; ".join(profile.research_areas),
                "orcid_id": profile.orcid_id
            })
        
        # Dados do ORCID
        for profile in orcid_profiles:
            full_name = f"{profile.given_names or ''} {profile.family_name or ''}".strip()
            current_employment = profile.employments[0] if profile.employments else None
            
            combined_data.append({
                "platform": "ORCID",
                "name": profile.credit_name or full_name,
                "id": profile.orcid_id,
                "institution": current_employment.organization if current_employment else "",
                "position": current_employment.role_title if current_employment else "",
                "total_publications": len(profile.works),
                "total_projects": 0,  # ORCID não tem projetos explícitos
                "research_areas": "",
                "orcid_id": profile.orcid_id
            })
        
        # Salva CSV
        df = pd.DataFrame(combined_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        return filename