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
            'Link da Publicação'
        ]
        
        # Escrever cabeçalhos
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, formats['header'])
        
        # Configurar larguras das colunas
        column_widths = [20, 12, 50, 30, 8, 10, 12, 40]
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
            
            # Link da publicação (se existir)
            if pub_data['link']:
                worksheet.write_url(row, 7, pub_data['link'], formats['link'], 'Ver Publicação')
            else:
                worksheet.write(row, 7, 'Link não disponível', data_format)
            
            row += 1
        
        # Aplicar filtro automático
        if row > 1:
            worksheet.autofilter(0, 0, row - 1, len(headers) - 1)
        
        # Congelar painel no cabeçalho
        worksheet.freeze_panes(1, 0)
        
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
                    
                    # Se há publicações associadas ao perfil
                    if 'publications' in platform_data:
                        for pub in platform_data['publications']:
                            pub_info = self._extract_publication_info(pub, platform_name, platform_data, author_name, h_index)
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
                            'link': profile.get('lattes_url', '')
                        })
                
                # Perfis ORCID
                elif 'orcid_profiles' in platform_data:
                    for profile in platform_data['orcid_profiles']:
                        given_names = profile.get('given_names', '')
                        family_name = profile.get('family_name', '')
                        author_name = f"{given_names} {family_name}".strip()
                        
                        publications.append({
                            'autor_principal': author_name,
                            'plataforma': platform_name,
                            'titulo': f'Perfil ORCID - {author_name}',
                            'todos_autores': author_name,
                            'ano': '',
                            'citacoes': 0,  # ORCID não fornece citações diretamente
                            'h_index': profile.get('h_index', 0),
                            'link': f"https://orcid.org/{profile.get('orcid_id', '')}"
                        })
        
        return publications
    
    def _extract_publication_info(self, pub, platform_name, platform_data, author_name=None, h_index=None):
        """Extrai informações de uma publicação específica"""
        # Determinar autor principal
        if author_name:
            main_author = author_name
            author_h_index = h_index or 0
        else:
            # Extrair primeiro autor da lista de autores
            all_authors = pub.get('authors', '')
            main_author = all_authors.split(',')[0].strip() if all_authors else 'Autor não identificado'
            
            # Tentar obter H-Index do perfil do autor se disponível
            author_h_index = 0
            if platform_data.get('author_profile'):
                author_h_index = platform_data['author_profile'].get('h_index', 0)
        
        return {
            'autor_principal': main_author,
            'plataforma': platform_name,
            'titulo': pub.get('title', 'Título não disponível'),
            'todos_autores': pub.get('authors', ''),
            'ano': pub.get('year', ''),
            'citacoes': pub.get('cited_by', 0),
            'h_index': author_h_index,
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
    
    def _create_summary_sheet(self, workbook, search_data, formats):
        """Cria aba de resumo da pesquisa"""
        worksheet = workbook.add_worksheet('Resumo da Pesquisa')
        
        # Título
        worksheet.merge_range(0, 0, 0, 3, 'RELATÓRIO DE PESQUISA ACADÊMICA', formats['header'])
        
        # Informações da pesquisa
        row = 2
        info_data = [
            ['Consulta realizada:', search_data.get('query', 'N/A')],
            ['Tipo de busca:', search_data.get('search_type', 'N/A')],
            ['Data/Hora:', datetime.now().strftime('%d/%m/%Y %H:%M:%S')],
            ['Plataformas consultadas:', ', '.join(search_data.get('platforms', []))],
            ['Total de publicações encontradas:', len(self._extract_all_publications(search_data))],
            ['Tempo de execução:', f"{search_data.get('execution_time', 0):.2f} segundos"]
# Fim do arquivo