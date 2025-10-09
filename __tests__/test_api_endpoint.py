#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_api_endpoint():
    print("Testando endpoint /search/author/profile...")
    
    # Parâmetros para teste
    url = 'http://localhost:8000/search/author/profile'
    params = {
        'query': 'Geoffrey Hinton',
        'platforms': 'scholar',
        'profile_url': 'https://scholar.google.com/citations?user=JicYPdAAAAAJ',
        'export_excel': False
    }
    
    print(f"URL: {url}")
    print(f"Parâmetros: {params}")
    
    try:
        response = requests.get(url, params=params, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Resposta da API:")
            
            # Verificar se há dados em researcher_info
            if 'researcher_info' in data and data['researcher_info']:
                result = data['researcher_info']
                print(f"Nome: {result.get('name', 'N/A')}")
                print(f"H-index: {result.get('h_index', 'N/A')}")
                print(f"Citations: {result.get('total_citations', 'N/A')}")
                print(f"Institution: {result.get('institution', 'N/A')}")
                print(f"Platform: {data.get('platform', 'N/A')}")
                
                if result.get('h_index') and result.get('h_index') != '0':
                    print("🎯 H-index extraído via API com sucesso!")
                    return True
                else:
                    print("❌ H-index não encontrado via API")
                    return False
            elif 'results' in data and data['results']:
                result = data['results'][0]
                print(f"Nome: {result.get('name', 'N/A')}")
                print(f"H-index: {result.get('h_index', 'N/A')}")
                print(f"Citations: {result.get('total_citations', 'N/A')}")
                print(f"Affiliation: {result.get('affiliation', 'N/A')}")
                print(f"Platform: {result.get('platform', 'N/A')}")
                
                if result.get('h_index') and result.get('h_index') != '0':
                    print("🎯 H-index extraído via API com sucesso!")
                    return True
                else:
                    print("❌ H-index não encontrado via API")
                    return False
            else:
                print("❌ Nenhum resultado encontrado")
                print(f"Resposta completa: {json.dumps(data, indent=2)}")
                return False
        else:
            print(f"❌ Erro HTTP {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Servidor não está rodando. Por favor, inicie a API primeiro.")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    success = test_api_endpoint()
    if success:
        print("\n🎉 API está funcionando corretamente!")
    else:
        print("\n💡 API precisa ser iniciada ou há algum problema.")