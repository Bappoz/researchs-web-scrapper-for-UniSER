#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_scholar_endpoint():
    print("🧪 Testando endpoint específico do Scholar...")
    
    # Parâmetros para teste
    url = 'http://localhost:8000/search/author/profile'
    params = {
        'query': 'Geoffrey Hinton',
        'platforms': 'scholar',
        'profile_url': 'https://scholar.google.com/citations?user=JicYPdAAAAAJ',
        'export_excel': False
    }
    
    print(f"Fazendo requisição para: {url}")
    print(f"Parâmetros: {params}")
    
    try:
        response = requests.get(url, params=params, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n✅ RESPOSTA COMPLETA DA API:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Verificar especificamente os valores
            if 'researcher_info' in data:
                info = data['researcher_info']
                print(f"\n🔍 ANÁLISE DOS VALORES:")
                print(f"Nome: {info.get('name', 'N/A')}")
                print(f"H-index: {info.get('h_index', 'N/A')}")
                print(f"Total Citations: {info.get('total_citations', 'N/A')}")
                print(f"Institution: {info.get('institution', 'N/A')}")
                
                # Verificar se h_index está com valor de citações
                h_index = info.get('h_index', '0')
                citations = info.get('total_citations', '0')
                
                try:
                    h_val = int(str(h_index).replace(',', ''))
                    cit_val = int(str(citations).replace(',', ''))
                    
                    print(f"\n📊 VALIDAÇÃO:")
                    print(f"H-index numérico: {h_val}")
                    print(f"Citações numéricas: {cit_val}")
                    
                    if h_val == cit_val:
                        print("❌ PROBLEMA DETECTADO: H-index igual às citações!")
                    elif h_val > 500:
                        print("❌ PROBLEMA: H-index muito alto (provavelmente confundido com citações)")
                    elif 1 <= h_val <= 500 and h_val < cit_val:
                        print("✅ H-index parece correto")
                    else:
                        print("⚠️ H-index pode ter problemas")
                        
                except Exception as e:
                    print(f"❌ Erro ao validar valores: {e}")
            
        else:
            print(f"❌ Erro HTTP {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_scholar_endpoint()