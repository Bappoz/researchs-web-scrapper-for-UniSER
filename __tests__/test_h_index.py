#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.api import ScholarExtractor
import time

def test_scholar_h_index():
    print("Testando extração de H-index do Google Scholar...")
    
    # URL de teste - perfil público do Google Scholar
    scholar_url = 'https://scholar.google.com/citations?user=JicYPdAAAAAJ'
    
    print(f"URL de teste: {scholar_url}")
    
    extractor = ScholarExtractor()
    
    try:
        print("Fazendo requisição para o Google Scholar...")
        result = extractor.extract_profile(scholar_url)
        
        if result and result.get('success'):
            print("✅ Resultado da busca:")
            print(f"Nome: {result.get('name', 'N/A')}")
            print(f"H-index: {result.get('h_index', 'N/A')}")
            print(f"Citations: {result.get('total_citations', 'N/A')}")
            print(f"Affiliation: {result.get('affiliation', 'N/A')}")
            print(f"Total Publications: {result.get('total_publications', 'N/A')}")
            
            if result.get('h_index') and result.get('h_index') != '0':
                print("✅ H-index extraído com sucesso!")
                return True
            else:
                print("❌ H-index não foi extraído corretamente")
                return False
        else:
            print("❌ Nenhum resultado encontrado ou erro:")
            print(f"Resultado: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante extração: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_scholar_h_index()
    if success:
        print("\n🎉 Teste concluído com sucesso! H-index foi extraído corretamente.")
    else:
        print("\n💡 Teste indicou que o H-index precisa de ajustes na extração.")