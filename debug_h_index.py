#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.api import ScholarExtractor
import time
import requests
from bs4 import BeautifulSoup

def debug_h_index_extraction():
    print("🔍 Debug detalhado da extração do H-index...")
    
    # URL de teste - perfil público do Google Scholar
    scholar_url = 'https://scholar.google.com/citations?user=JicYPdAAAAAJ'
    
    print(f"URL de teste: {scholar_url}")
    
    extractor = ScholarExtractor()
    
    try:
        print("Fazendo requisição direta para o Google Scholar...")
        time.sleep(3)
        
        response = extractor.session.get(scholar_url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print("\n🔍 ANÁLISE DETALHADA DA ESTRUTURA HTML:")
        
        # 1. Verificar elementos de estatísticas
        stats_elements = soup.select('.gsc_rsb_std')
        print(f"\n📊 Elementos .gsc_rsb_std encontrados: {len(stats_elements)}")
        for i, elem in enumerate(stats_elements):
            value = elem.get_text(strip=True)
            print(f"  Posição {i}: '{value}'")
        
        # 2. Verificar estrutura de tabela completa
        print(f"\n📋 ESTRUTURA DA TABELA DE ESTATÍSTICAS:")
        table_rows = soup.select('.gsc_rsb_st')
        print(f"Linhas da tabela encontradas: {len(table_rows)}")
        
        for i, row in enumerate(table_rows):
            cells = row.select('td')
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True)
                all_value = cells[1].get_text(strip=True)
                since_2019 = cells[2].get_text(strip=True) if len(cells) > 2 else "N/A"
                print(f"  Linha {i}: {label} | Total: {all_value} | Desde 2019: {since_2019}")
        
        # 3. Verificar especificamente por h-index
        print(f"\n🎯 BUSCA ESPECÍFICA POR H-INDEX:")
        h_index_found = False
        
        # Procurar por texto que contenha "h-index"
        for element in soup.find_all(text=lambda text: text and 'h-index' in text.lower()):
            parent = element.parent
            print(f"  Texto encontrado: '{element.strip()}'")
            print(f"  Elemento pai: {parent.name if parent else 'None'}")
            
            # Tentar encontrar o valor associado
            if parent:
                # Procurar no próximo elemento
                next_elem = parent.find_next('.gsc_rsb_std')
                if next_elem:
                    value = next_elem.get_text(strip=True)
                    print(f"  Valor associado: '{value}'")
                    h_index_found = True
        
        # 4. Tentar estratégia baseada na posição conhecida
        print(f"\n🎲 ESTRATÉGIA BASEADA EM POSIÇÃO:")
        if len(stats_elements) >= 3:
            # No Google Scholar, normalmente:
            # Posição 0: Citações total
            # Posição 1: Citações desde 2019  
            # Posição 2: h-index total
            # Posição 3: h-index desde 2019
            citations_total = stats_elements[0].get_text(strip=True)
            citations_2019 = stats_elements[1].get_text(strip=True) if len(stats_elements) > 1 else "N/A"
            h_index_total = stats_elements[2].get_text(strip=True) if len(stats_elements) > 2 else "N/A"
            h_index_2019 = stats_elements[3].get_text(strip=True) if len(stats_elements) > 3 else "N/A"
            
            print(f"  Citações total: {citations_total}")
            print(f"  Citações desde 2019: {citations_2019}")
            print(f"  H-index total: {h_index_total}")
            print(f"  H-index desde 2019: {h_index_2019}")
            
            # Validar se o h-index faz sentido
            try:
                h_val = int(h_index_total.replace(',', ''))
                cit_val = int(citations_total.replace(',', ''))
                
                if 1 <= h_val <= 500 and h_val < cit_val:
                    print(f"  ✅ H-index válido identificado: {h_index_total}")
                else:
                    print(f"  ❌ H-index inválido: {h_index_total} (muito grande ou pequeno)")
            except:
                print(f"  ❌ Erro ao validar H-index: {h_index_total}")
        
        # 5. Testar o método atual
        print(f"\n🧪 TESTANDO MÉTODO ATUAL:")
        h_index_result = extractor._extract_h_index(soup)
        print(f"Resultado do método atual: '{h_index_result}'")
        
    except Exception as e:
        print(f"❌ Erro durante debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_h_index_extraction()