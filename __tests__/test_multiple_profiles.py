#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_multiple_profiles():
    print("🧪 Testando múltiplos perfis do Scholar...")
    
    # URLs de teste diferentes
    test_profiles = [
        {
            "name": "Geoffrey Hinton", 
            "url": "https://scholar.google.com/citations?user=JicYPdAAAAAJ"
        },
        {
            "name": "Yann LeCun", 
            "url": "https://scholar.google.com/citations?user=WLN3QrAAAAAJ"
        },
        {
            "name": "Andrew Ng", 
            "url": "https://scholar.google.com/citations?user=mG4imMEAAAAJ"
        }
    ]
    
    api_url = 'http://localhost:8000/search/author/profile'
    
    for i, profile in enumerate(test_profiles):
        print(f"\n{'='*50}")
        print(f"TESTE {i+1}: {profile['name']}")
        print(f"URL: {profile['url']}")
        print(f"{'='*50}")
        
        params = {
            'query': profile['name'],
            'platforms': 'scholar',
            'profile_url': profile['url'],
            'export_excel': False
        }
        
        try:
            response = requests.get(api_url, params=params, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'researcher_info' in data:
                    info = data['researcher_info']
                    name = info.get('name', 'N/A')
                    h_index = info.get('h_index', 'N/A')
                    citations = info.get('total_citations', 'N/A')
                    institution = info.get('institution', 'N/A')
                    
                    print(f"✅ RESULTADO:")
                    print(f"  Nome: {name}")
                    print(f"  H-index: {h_index}")
                    print(f"  Citações: {citations}")
                    print(f"  Instituição: {institution}")
                    
                    # Análise de problemas
                    try:
                        h_val = int(str(h_index).replace(',', ''))
                        cit_val = int(str(citations).replace(',', ''))
                        
                        print(f"\n  📊 ANÁLISE:")
                        print(f"  H-index numérico: {h_val}")
                        print(f"  Citações numéricas: {cit_val}")
                        
                        if h_val == cit_val:
                            print("  ❌ PROBLEMA: H-index igual às citações!")
                        elif h_val > 500:
                            print("  ❌ PROBLEMA: H-index muito alto (> 500)")
                        elif h_val > cit_val:
                            print("  ❌ PROBLEMA: H-index maior que citações")
                        elif h_val < 1:
                            print("  ⚠️ AVISO: H-index muito baixo")
                        elif 1 <= h_val <= 500 and h_val < cit_val:
                            print("  ✅ H-index parece válido")
                        else:
                            print("  ⚠️ H-index pode ter problemas")
                            
                    except Exception as e:
                        print(f"  ❌ Erro na análise: {e}")
                else:
                    print("❌ researcher_info não encontrado na resposta")
                    
            else:
                print(f"❌ Erro HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
        
        # Aguardar entre requisições
        if i < len(test_profiles) - 1:
            print("\nAguardando para próxima requisição...")
            import time
            time.sleep(5)

if __name__ == "__main__":
    test_multiple_profiles()