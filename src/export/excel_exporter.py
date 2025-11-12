"""
Sistema de Exportação Excel Profissional
Formato: Uma linha por publicação com todas as informações relevantes
"""

import os
import pandas as pd
import xlsxwriter
from typing import List, Dict, Any, Optional
from datetime import datetime
import re

# Palavras-chave para filtragem de publicações relacionadas ao envelhecimento
KEYWORDS = [
    # Institucional
    'UniSER', 'UnB',

    # População Alvo (Português, Inglês, Espanhol)
    'idoso', 'idosa', 'idosos', 'pessoa idosa', 'terceira idade', 'melhor idade', 'longevo',
    'elderly', 'older adult', 'senior', 'aged', 'third age', 'long-lived',
    'anciano', 'persona mayor', 'adulto mayor', 'tercera edad',

    # Processo Biológico/Social
    'envelhecimento', 'envelhecer', 'longevidade',
    'aging', 'ageing', 'longevity',
    'envejecimiento', 'envejecer', 'longevidad',
    'senescência', 'senescente', 'senescence', 'senescent', 'senescencia',
    'senilidade', 'senility',

    # Áreas de Estudo
    'gerontologia', 'gerontológico', 'gerontology', 'gerontological', 'gerontología',
    'geriatria', 'geriátrico', 'geriatrics', 'geriatric', 'geriatría',

    # Saúde e Bem-Estar
    'qualidade de vida', 'bem-estar',
    'quality of life', 'well-being', 'wellness',
    'calidad de vida', 'bienestar',
    'saúde do idoso', 'elderly health', 'senior health', 'salud del adulto mayor',
    'autonomia', 'capacidade funcional', 'autonomy', 'functional capacity',

    # Educação e Sociedade
    'educação permanente', 'educação continuada', 'lifelong learning', 'continuing education', 'educación permanente',
    'inclusão social', 'inclusão digital', 'social inclusion', 'digital inclusion', 'inclusión social',
    'universidade aberta', 'open university'
]

class ProfessionalExcelExporter:
    """Exportador profissional focado em publicações por linha"""
    
    def __init__(self):
        self.export_dir = "exports"
        self._ensure_export_dir()
    
    def _ensure_export_dir(self):
        """Garante que o diretório de exportação existe"""
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
    
    def export_research_data(
        self, 
        search_data: Dict[str, Any], 
        filename_prefix: str = "pesquisa_academica"
    ) -> str:
        """
        Exporta dados de pesquisa em formato profissional
        Uma linha por publicação encontrada
        """
        
        # Gerar nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_clean = re.sub(r'[^\w\-_]', '_', search_data.get('query', 'pesquisa'))[:30]
        filename = f"{filename_prefix}_{query_clean}_{timestamp}.xlsx"
        filepath = os.path.join(self.export_dir, filename)
        
        # Criar workbook
        workbook = xlsxwriter.Workbook(filepath)
        
        # Definir formatos profissionais
        formats = self._create_professional_formats(workbook)
        
        # Criar aba principal com todas as publicações
        self._create_publications_sheet(workbook, search_data, formats)
        
        # Criar aba de resumo
        self._create_summary_sheet(workbook, search_data, formats)
        
        workbook.close()
        return filename
    
    def _find_keywords_in_publication(self, publication: Dict[str, Any]) -> List[str]:
        """
        Encontra palavras-chave relacionadas ao envelhecimento em uma publicação
        
        Args:
            publication: Dicionário com dados da publicação
            
        Returns:
            Lista de palavras-chave encontradas
        """
        found_keywords = []
        
        # Campos de texto para pesquisar
        text_fields = [
            publication.get('title', ''),
            publication.get('authors', ''),
            publication.get('publication', ''),
            publication.get('snippet', ''),
            publication.get('abstract', '')  # Caso tenha resumo
        ]
        
        # Juntar todos os textos em uma string única
        full_text = ' '.join(text_fields).lower()
        
        # Buscar cada palavra-chave
        for keyword in KEYWORDS:
            keyword_lower = keyword.lower()
            
            # Busca por palavra completa (evita falsos positivos)
            # Usando regex para garantir que seja uma palavra completa
            pattern = r'\b' + re.escape(keyword_lower) + r'\b'
            
            if re.search(pattern, full_text):
                found_keywords.append(keyword)
        
        return found_keywords
    
    def _filter_publications_by_keywords(self, publications: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filtra publicações que contêm pelo menos uma palavra-chave relacionada ao envelhecimento
        
        Args:
            publications: Lista de publicações
            
        Returns:
            Lista de publicações filtradas com keywords encontradas
        """
        filtered_publications = []
        
        for pub in publications:
            keywords_found = self._find_keywords_in_publication(pub)
            
            if keywords_found:  # Se encontrou pelo menos uma keyword
                # Adicionar as keywords encontradas ao dicionário da publicação
                pub_with_keywords = pub.copy()
                pub_with_keywords['keywords_found'] = keywords_found
                pub_with_keywords['keywords_text'] = '; '.join(keywords_found)
                filtered_publications.append(pub_with_keywords)
        
        return filtered_publications
    
    def _create_professional_formats(self, workbook):
        """Cria formatos profissionais para o Excel"""
        return {
            'header': workbook.add_format({
                'bold': True,
                'font_size': 12,
                'bg_color': '#2F4F4F',
                'font_color': 'white',
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'text_wrap': True
            }),
            'data': workbook.add_format({
                'font_size': 10,
                'valign': 'top',
                'border': 1,
                'text_wrap': True
            }),
            'data_alt': workbook.add_format({
                'font_size': 10,
                'valign': 'top',
                'border': 1,
                'text_wrap': True,
                'bg_color': '#F8F8F8'
            }),
            'number': workbook.add_format({
                'font_size': 10,
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'num_format': '#,##0'
            }),
            'year': workbook.add_format({
                'font_size': 10,
                'align': 'center',
                'valign': 'vcenter',
                'border': 1
            }),
            'link': workbook.add_format({
                'font_size': 10,
                'font_color': 'blue',
                'underline': 1,
                'valign': 'top',
                'border': 1,
                'text_wrap': True
            }),
            'platform': workbook.add_format({
                'font_size': 10,
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'bold': True
            })
        }
    
    def _create_publications_sheet(self, workbook, search_data, formats):
        """Cria aba principal com todas as publicações (uma por linha)"""
        worksheet = workbook.add_worksheet('Publicações')
        
        # Definir cabeçalhos
        headers = [
            'Autor Principal',
            'Plataforma',
            'Título da Publicação', 
            'Todos os Autores',
            'Ano',
            'Citações',
            'H-Index do Autor',
            'i10-Index do Autor',
            'Link da Publicação'
        ]
        
        # Escrever cabeçalhos
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, formats['header'])
        
        # Configurar larguras das colunas
        column_widths = [20, 12, 50, 30, 8, 10, 12, 12, 40]
        for i, width in enumerate(column_widths):
            worksheet.set_column(i, i, width)
        
        # Extrair e escrever dados das publicações
        row = 1
        publications_data = self._extract_all_publications(search_data)
        
        for pub_data in publications_data:
            # Alternar cor de fundo para melhor legibilidade
            data_format = formats['data_alt'] if row % 2 == 0 else formats['data']
            
            # Escrever dados da publicação
            worksheet.write(row, 0, pub_data['autor_principal'], data_format)
            worksheet.write(row, 1, pub_data['plataforma'], formats['platform'])
            worksheet.write(row, 2, pub_data['titulo'], data_format)
            worksheet.write(row, 3, pub_data['todos_autores'], data_format)
            worksheet.write(row, 4, pub_data['ano'], formats['year'])
            worksheet.write(row, 5, pub_data['citacoes'], formats['number'])
            worksheet.write(row, 6, pub_data['h_index'], formats['number'])
            worksheet.write(row, 7, pub_data['i10_index'], formats['number'])
            
            # Link da publicação (se existir)
            if pub_data['link']:
                worksheet.write_url(row, 8, pub_data['link'], formats['link'], 'Ver Publicação')
            else:
                worksheet.write(row, 8, 'Link não disponível', data_format)
            
            row += 1
        
        # Aplicar filtro automático
        if row > 1:
            worksheet.autofilter(0, 0, row - 1, len(headers) - 1)
        
        # Congelar painel no cabeçalho
        worksheet.freeze_panes(1, 0)
        
        return worksheet
    
    def export_api_data(self, api_response: Dict[str, Any], filename_prefix: str = "pesquisa_academica", filter_by_keywords: bool = True) -> str:
        """
        Exporta dados da nossa API diretamente para Excel
        Formato específico para nossa estrutura de dados
        
        Args:
            api_response: Resposta da API com dados das publicações
            filename_prefix: Prefixo do nome do arquivo
            filter_by_keywords: Se True, filtra apenas publicações com keywords relacionadas ao envelhecimento
        """
        
        # Filtrar publicações por keywords se solicitado
        if filter_by_keywords:
            publications = api_response.get('data', {}).get('publications', [])
            filtered_publications = self._filter_publications_by_keywords(publications)
            
            # Criar uma cópia da resposta com publicações filtradas
            filtered_response = api_response.copy()
            filtered_response['data'] = {'publications': filtered_publications}
            filtered_response['total_results'] = len(filtered_publications)
            filtered_response['filtered_by_keywords'] = True
            
            api_data = filtered_response
        else:
            api_data = api_response
        
        # Gerar nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_clean = re.sub(r'[^\w\-_]', '_', api_data.get('query', 'pesquisa'))[:30]
        
        if filter_by_keywords:
            filename = f"{filename_prefix}_filtered_{query_clean}_{timestamp}.xlsx"
        else:
            filename = f"{filename_prefix}_{query_clean}_{timestamp}.xlsx"
            
        filepath = os.path.join(self.export_dir, filename)
        
        # Criar workbook
        workbook = xlsxwriter.Workbook(filepath)
        
        # Definir formatos profissionais
        formats = self._create_professional_formats(workbook)
        
        # Criar aba principal com todas as publicações
        self._create_api_publications_sheet(workbook, api_data, formats, filter_by_keywords)
        
        # Criar aba de resumo
        self._create_api_summary_sheet(workbook, api_data, formats)
        
        workbook.close()
        return filename
    
    def _create_api_publications_sheet(self, workbook, api_response, formats, filter_by_keywords=False):
        """Cria aba principal com publicações da nossa API"""
        worksheet = workbook.add_worksheet('Publicações')
        
        # Definir cabeçalhos (incluindo coluna de keywords se filtrado)
        headers = [
            'Título da Publicação',
            'Autores',
            'Publicação/Venue',
            'Ano',
            'Citações',
            'Plataforma',
            'Tipo',
            'Link'
        ]
        
        # Adicionar coluna de keywords se filtrado
        if filter_by_keywords:
            headers.append('Keywords Encontradas')
        
        # Adicionar colunas de resumo do Lattes se disponível
        lattes_summary = api_response.get('data', {}).get('lattes_summary')
        if lattes_summary and lattes_summary.get('success'):
            headers.extend([
                'Instituição (Lattes)',
                'Área (Lattes)',
                'Resumo (Lattes)'
            ])
        
        # Escrever cabeçalhos
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, formats['header'])
        
        # Configurar larguras das colunas
        column_widths = [50, 30, 25, 8, 10, 12, 12, 40]  # Base
        if filter_by_keywords:
            column_widths.append(30)  # Keywords
        if lattes_summary and lattes_summary.get('success'):
            column_widths.extend([25, 20, 60])  # Instituição, Área, Resumo do Lattes
        
        for i, width in enumerate(column_widths):
            worksheet.set_column(i, i, width)
        
        # Extrair e escrever dados das publicações
        row = 1
        publications = api_response.get('data', {}).get('publications', [])
        
        for pub in publications:
            # Alternar cor de fundo para melhor legibilidade
            data_format = formats['data_alt'] if row % 2 == 0 else formats['data']
            
            # Escrever dados da publicação
            worksheet.write(row, 0, pub.get('title', 'Título não disponível'), data_format)
            worksheet.write(row, 1, pub.get('authors', 'Autores não disponíveis'), data_format)
            worksheet.write(row, 2, pub.get('publication', 'Venue não disponível'), data_format)
            worksheet.write(row, 3, pub.get('year', ''), formats['year'])
            worksheet.write(row, 4, pub.get('cited_by', 0), formats['number'])
            worksheet.write(row, 5, pub.get('platform', api_response.get('platform', '')), formats['platform'])
            worksheet.write(row, 6, pub.get('type', 'article'), data_format)
            
            # Link da publicação (se existir)
            link = pub.get('link', '')
            if link and link != 'N/A':
                worksheet.write_url(row, 7, link, formats['link'], 'Ver Publicação')
            else:
                worksheet.write(row, 7, 'Link não disponível', data_format)
            
            # Keywords encontradas (se filtrado por keywords)
            col_offset = 8
            if filter_by_keywords:
                keywords_text = pub.get('keywords_text', '')
                worksheet.write(row, col_offset, keywords_text, data_format)
                col_offset += 1
            
            # Dados do Lattes (se disponível) - mesmo valor para todas as linhas
            if lattes_summary and lattes_summary.get('success'):
                worksheet.write(row, col_offset, lattes_summary.get('institution', ''), data_format)
                worksheet.write(row, col_offset + 1, lattes_summary.get('area', ''), data_format)
                worksheet.write(row, col_offset + 2, lattes_summary.get('summary', ''), data_format)
            
            row += 1
        
        # Aplicar filtro automático
        if row > 1:
            worksheet.autofilter(0, 0, row - 1, len(headers) - 1)
        
        # Congelar painel no cabeçalho
        worksheet.freeze_panes(1, 0)
        
        return worksheet
    
    def _create_api_summary_sheet(self, workbook, api_response, formats):
        """Cria aba de resumo para dados da nossa API"""
        worksheet = workbook.add_worksheet('Resumo')
        
        # Título da planilha
        worksheet.merge_range(0, 0, 0, 7, 'RELATÓRIO DE PESQUISA ACADÊMICA', formats['header'])
        
        row = 2
        
        # Informações gerais da pesquisa em formato horizontal
        general_headers = ['Consulta', 'Plataforma', 'Tipo de Busca', 'Total de Resultados', 'Data/Hora', 'Filtrado por Keywords', 'Total Original']
        
        # Escrever cabeçalhos
        for col, header in enumerate(general_headers):
            worksheet.write(row, col, header, formats['header'])
        
        row += 1
        
        # Escrever dados gerais
        general_data = [
            api_response.get('query', ''),
            api_response.get('platform', ''),
            api_response.get('search_type', ''),
            api_response.get('total_results', 0),
            datetime.now().strftime('%d/%m/%Y %H:%M'),
            'Sim' if api_response.get('filtered_by_keywords', False) else 'Não',
            api_response.get('original_total', api_response.get('total_results', 0))
        ]
        
        for col, data in enumerate(general_data):
            worksheet.write(row, col, str(data), formats['data'])
        
        row += 3
        
        # Informações do pesquisador em formato horizontal (se disponível)
        researcher_info = api_response.get('researcher_info', {})
        if researcher_info:
            worksheet.write(row, 0, 'INFORMAÇÕES DO PESQUISADOR:', formats['header'])
            row += 1
            
            # Cabeçalhos do pesquisador
            researcher_headers = ['Nome', 'Instituição', 'H-Index', 'i10-Index', 'Total de Citações', 'Áreas de Pesquisa', 'Última Atualização']
            
            for col, header in enumerate(researcher_headers):
                worksheet.write(row, col, header, formats['header'])
            
            row += 1
            
            # Dados do pesquisador
            researcher_data = [
                researcher_info.get('name', 'N/A'),
                researcher_info.get('institution', 'N/A'),
                researcher_info.get('h_index', 'N/A'),
                researcher_info.get('i10_index', 'N/A'),
                researcher_info.get('total_citations', 'N/A'),
                ', '.join(researcher_info.get('research_areas', [])) if isinstance(researcher_info.get('research_areas'), list) else str(researcher_info.get('research_areas', 'N/A')),
                researcher_info.get('last_update', 'N/A')
            ]
            
            for col, data in enumerate(researcher_data):
                worksheet.write(row, col, str(data), formats['data'])
            
            row += 2
        
        # Informações do Lattes via Escavador (se disponível)
        lattes_summary = api_response.get('data', {}).get('lattes_summary')
        if lattes_summary and lattes_summary.get('success'):
            worksheet.write(row, 0, 'RESUMO DO LATTES (VIA ESCAVADOR):', formats['header'])
            row += 1
            
            # Cabeçalhos do Lattes
            lattes_headers = ['Nome', 'Instituição', 'Área', 'Resumo', 'Link Lattes']
            
            for col, header in enumerate(lattes_headers):
                worksheet.write(row, col, header, formats['header'])
            
            row += 1
            
            # Dados do Lattes
            lattes_data = [
                lattes_summary.get('name', 'N/A'),
                lattes_summary.get('institution', 'N/A'),
                lattes_summary.get('area', 'N/A'),
                lattes_summary.get('summary', 'N/A'),
                lattes_summary.get('lattes_url', 'N/A')
            ]
            
            for col, data in enumerate(lattes_data):
                if col == 4 and data != 'N/A' and data:  # Link do Lattes
                    worksheet.write_url(row, col, data, formats['link'], 'Acessar Lattes')
                else:
                    worksheet.write(row, col, str(data), formats['data'])
        
        # Configurar larguras das colunas
        for col in range(8):
            worksheet.set_column(col, col, 15)
        
        # Ajustar algumas colunas específicas
        worksheet.set_column(0, 0, 25)  # Consulta/Nome
        worksheet.set_column(1, 1, 30)  # Plataforma/Instituição
        worksheet.set_column(3, 3, 60)  # Resumo do Lattes (mais largo)
        worksheet.set_column(4, 4, 18)  # Data/Áreas de Pesquisa
        
        return worksheet
    
    def _extract_all_publications(self, search_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extrai todas as publicações de todas as plataformas"""
        publications = []
        
        # Obter dados por plataforma
        results_by_platform = search_data.get('results_by_platform', {})
        
        for platform, platform_data in results_by_platform.items():
            platform_name = self._get_platform_display_name(platform)
            
            # Processar publicações desta plataforma
            if isinstance(platform_data, dict):
                # Google Scholar - publicações diretas
                if 'publications' in platform_data:
                    for pub in platform_data['publications']:
                        pub_info = self._extract_publication_info(pub, platform_name, platform_data)
                        publications.append(pub_info)
                
                # Perfil de autor com publicações
                elif 'author_profile' in platform_data and platform_data['author_profile']:
                    author_profile = platform_data['author_profile']
                    author_name = author_profile.get('name', 'Autor não identificado')
                    h_index = author_profile.get('h_index', 0)
                    i10_index = author_profile.get('i10_index', 0)
                    
                    # Se há publicações associadas ao perfil
                    if 'publications' in platform_data:
                        for pub in platform_data['publications']:
                            pub_info = self._extract_publication_info(pub, platform_name, platform_data, author_name, h_index, i10_index)
                            publications.append(pub_info)
                    else:
                        # Criar entrada para o perfil mesmo sem publicações específicas
                        publications.append({
                            'autor_principal': author_name,
                            'plataforma': platform_name,
                            'titulo': f'Perfil de {author_name}',
                            'todos_autores': author_name,
                            'ano': '',
                            'citacoes': author_profile.get('cited_by', 0),
                            'h_index': h_index,
                            'i10_index': i10_index,
                            'link': ''
                        })
                
                # Perfis Lattes
                elif 'lattes_profiles' in platform_data:
                    for profile in platform_data['lattes_profiles']:
                        author_name = profile.get('name', 'Autor não identificado')
                        publications.append({
                            'autor_principal': author_name,
                            'plataforma': platform_name,
                            'titulo': f'Perfil Lattes - {author_name}',
                            'todos_autores': author_name,
                            'ano': '',
                            'citacoes': profile.get('total_citations', 0),
                            'h_index': profile.get('h_index', 0),
                            'i10_index': profile.get('i10_index', 0),
                            'link': profile.get('lattes_url', '')
                        })
                
                # Perfis ORCID - tratar tanto orcid_profile (singular) quanto orcid_profiles (plural)
                elif 'orcid_profiles' in platform_data:
                    for profile in platform_data['orcid_profiles']:
                        given_names = profile.get('given_names', '')
                        family_name = profile.get('family_name', '')
                        author_name = f"{given_names} {family_name}".strip()
                        
                        # Processar publicações do perfil ORCID se existirem
                        works = profile.get('works', [])
                        if works:
                            for work in works:
                                publications.append({
                                    'autor_principal': author_name,
                                    'plataforma': platform_name,
                                    'titulo': work.get('title', 'Título não disponível'),
                                    'todos_autores': author_name,
                                    'ano': self._extract_year_from_orcid_date(work.get('publication_date')),
                                    'citacoes': work.get('cited_by', 0),
                                    'h_index': profile.get('h_index', 0),
                                    'i10_index': profile.get('i10_index', 0),
                                    'link': work.get('url', f"https://orcid.org/{profile.get('orcid_id', '')}")
                                })
                        else:
                            # Se não há publicações, criar entrada para o perfil
                            publications.append({
                                'autor_principal': author_name,
                                'plataforma': platform_name,
                                'titulo': f'Perfil ORCID - {author_name}',
                                'todos_autores': author_name,
                                'ano': '',
                                'citacoes': profile.get('total_citations', 0),
                                'h_index': profile.get('h_index', 0),
                                'i10_index': profile.get('i10_index', 0),
                                'link': f"https://orcid.org/{profile.get('orcid_id', '')}"
                            })
                
                # Perfil ORCID singular (busca por URL direta)
                elif 'orcid_profile' in platform_data:
                    profile = platform_data['orcid_profile']
                    if profile:
                        given_names = profile.get('given_names', '')
                        family_name = profile.get('family_name', '')
                        author_name = f"{given_names} {family_name}".strip()
                        
                        # Processar publicações do perfil ORCID se existirem
                        works = profile.get('works', [])
                        if works:
                            for work in works:
                                publications.append({
                                    'autor_principal': author_name,
                                    'plataforma': platform_name,
                                    'titulo': work.get('title', 'Título não disponível'),
                                    'todos_autores': author_name,
                                    'ano': self._extract_year_from_orcid_date(work.get('publication_date')),
                                    'citacoes': work.get('cited_by', 0),
                                    'h_index': profile.get('h_index', 0),
                                    'i10_index': profile.get('i10_index', 0),
                                    'link': work.get('url', f"https://orcid.org/{profile.get('orcid_id', '')}")
                                })
                        else:
                            # Se não há publicações, criar entrada para o perfil
                            publications.append({
                                'autor_principal': author_name,
                                'plataforma': platform_name,
                                'titulo': f'Perfil ORCID - {author_name}',
                                'todos_autores': author_name,
                                'ano': '',
                                'citacoes': profile.get('total_citations', 0),
                                'h_index': profile.get('h_index', 0),
                                'i10_index': profile.get('i10_index', 0),
                                'link': f"https://orcid.org/{profile.get('orcid_id', '')}"
                            })
        
        return publications
    
    def _extract_publication_info(self, pub, platform_name, platform_data, author_name=None, h_index=None, i10_index=None):
        """Extrai informações de uma publicação específica"""
        # Determinar autor principal
        if author_name:
            main_author = author_name
            author_h_index = h_index or 0
            author_i10_index = i10_index or 0
        else:
            # Extrair primeiro autor da lista de autores
            all_authors = pub.get('authors', '')
            main_author = all_authors.split(',')[0].strip() if all_authors else 'Autor não identificado'
            
            # Tentar obter H-Index e i10-Index do perfil do autor se disponível
            author_h_index = 0
            author_i10_index = 0
            if platform_data.get('author_profile'):
                author_h_index = platform_data['author_profile'].get('h_index', 0)
                author_i10_index = platform_data['author_profile'].get('i10_index', 0)
        
        return {
            'autor_principal': main_author,
            'plataforma': platform_name,
            'titulo': pub.get('title', 'Título não disponível'),
            'todos_autores': pub.get('authors', ''),
            'ano': pub.get('year', ''),
            'citacoes': pub.get('cited_by', 0),
            'h_index': author_h_index,
            'i10_index': author_i10_index,
            'link': pub.get('link', '')
        }
    
    def _get_platform_display_name(self, platform: str) -> str:
        """Converte nome da plataforma para exibição"""
        platform_names = {
            'scholar': 'Google Scholar',
            'lattes': 'Plataforma Lattes',
            'orcid': 'ORCID'
        }
        return platform_names.get(platform.lower(), platform.title())
    
    def _extract_year_from_orcid_date(self, publication_date):
        """Extrai ano da data de publicação do ORCID"""
        if not publication_date:
            return ''
        
        # ORCID pode retornar datas em vários formatos
        if isinstance(publication_date, dict):
            year = publication_date.get('year')
            if year:
                return str(year.get('value', '')) if isinstance(year, dict) else str(year)
        elif isinstance(publication_date, str):
            # Tentar extrair ano de string (formato YYYY-MM-DD ou similar)
            import re
            year_match = re.search(r'\b(19|20)\d{2}\b', publication_date)
            if year_match:
                return year_match.group()
        
        return ''
    
    def _create_summary_sheet(self, workbook, search_data, formats):
        """Cria aba de resumo da pesquisa"""
        worksheet = workbook.add_worksheet('Resumo da Pesquisa')
        
        # Título
        worksheet.merge_range(0, 0, 0, 5, 'RELATÓRIO DE PESQUISA ACADÊMICA', formats['header'])
        
        # Informações da pesquisa em formato horizontal
        row = 2
        
        # Cabeçalhos
        headers = ['Consulta', 'Tipo de Busca', 'Data/Hora', 'Plataformas', 'Total Publicações', 'Tempo Execução (s)']
        
        for col, header in enumerate(headers):
            worksheet.write(row, col, header, formats['header'])
        
        row += 1
        
        # Dados
        data = [
            search_data.get('query', 'N/A'),
            search_data.get('search_type', 'N/A'),
            datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            ', '.join(search_data.get('platforms', [])),
            len(self._extract_all_publications(search_data)),
            str(search_data.get('execution_time', '0'))
        ]
        
        for col, value in enumerate(data):
            worksheet.write(row, col, str(value), formats['data'])
        
        # Configurar larguras das colunas
        for col in range(6):
            worksheet.set_column(col, col, 15)
        
        # Ajustar colunas específicas
        worksheet.set_column(0, 0, 25)  # Consulta
        worksheet.set_column(2, 2, 18)  # Data/Hora
        worksheet.set_column(3, 3, 20)  # Plataformas
        
        return worksheet

# Função principal para compatibilidade
def export_research_to_excel(search_data: Dict[str, Any], filename_prefix: str = "pesquisa") -> str:
    """Função principal de exportação"""
    exporter = ProfessionalExcelExporter()
    return exporter.export_research_data(search_data, filename_prefix)