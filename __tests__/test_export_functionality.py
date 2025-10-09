#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_export_functionality():
    print("🧪 Testando funcionalidade completa de exportação...")
    
    api_url = 'http://localhost:8000/search/author/profile'
    
    # Perfil de teste
    profile_url = "https://scholar.google.com/citations?user=JicYPdAAAAAJ"  # Geoffrey Hinton
    
    print("📚 PASSO 1: Busca normal (sem export)")
    params = {
        'query': 'Geoffrey Hinton',
        'platforms': 'scholar',
        'profile_url': profile_url,
        'export_excel': False,
        'max_publications': 20
    }
    
    try:
        response = requests.get(api_url, params=params, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"  ✅ Busca normal funcionou")
            print(f"  Query: '{data.get('query', 'VAZIO!')}'")
            print(f"  Nome: '{data.get('researcher_info', {}).get('name', 'VAZIO!')}'")
            print(f"  Publicações: {len(data.get('data', {}).get('publications', []))}")
            
            # Simular o que o frontend faria
            query_field = data.get('query', '')
            has_publications = len(data.get('data', {}).get('publications', [])) > 0
            
            print(f"\n🖥️ VALIDAÇÃO FRONTEND:")
            print(f"  Campo query preenchido?: {bool(query_field)}")
            print(f"  Tem publicações?: {has_publications}")
            print(f"  Exportação permitida?: {bool(query_field) and has_publications}")
            
            if not query_field:
                print(f"  ❌ PROBLEMA: Query vazio impedirá exportação!")
                return False
            
            print(f"\n📤 PASSO 2: Teste de exportação")
            params['export_excel'] = True
            
            response = requests.get(api_url, params=params, timeout=120)
            
            if response.status_code == 200:
                export_data = response.json()
                
                has_excel_file = 'excel_file' in export_data
                excel_filename = export_data.get('excel_file', 'N/A')
                
                print(f"  ✅ Requisição de export funcionou")
                print(f"  Tem arquivo Excel?: {has_excel_file}")
                print(f"  Nome do arquivo: {excel_filename}")
                
                if has_excel_file:
                    print(f"  🎉 EXPORTAÇÃO DEVERIA FUNCIONAR!")
                    return True
                else:
                    print(f"  ❌ PROBLEMA: Arquivo Excel não foi gerado")
                    print(f"  Resposta completa: {json.dumps(export_data, indent=2)}")
                    return False
            else:
                print(f"  ❌ Erro na exportação: HTTP {response.status_code}")
                return False
                
        else:
            print(f"❌ Erro na busca normal: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

if __name__ == "__main__":
    success = test_export_functionality()
    if success:
        print(f"\n🎉 TESTE PASSOU! Exportação deveria funcionar.")
    else:
        print(f"\n💥 TESTE FALHOU! Há problemas na exportação.")