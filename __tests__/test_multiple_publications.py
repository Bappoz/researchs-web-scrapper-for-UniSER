#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_multiple_publications():
    print("🧪 Testando extração de múltiplas publicações...")
    
    api_url = 'http://localhost:8000/search/author/profile'
    
    # Perfil de teste
    profile_url = "https://scholar.google.com/citations?user=JicYPdAAAAAJ"  # Geoffrey Hinton
    
    # Testar diferentes números de publicações
    test_cases = [
        {"name": "Teste 20 publicações", "max_pubs": 20},
        {"name": "Teste 40 publicações", "max_pubs": 40},
        {"name": "Teste 60 publicações", "max_pubs": 60},
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n{'='*60}")
        print(f"CASO {i+1}: {test_case['name']} ({test_case['max_pubs']} publicações)")
        print(f"{'='*60}")
        
        params = {
            'query': 'Geoffrey Hinton',
            'platforms': 'scholar',
            'profile_url': profile_url,
            'export_excel': False,
            'max_publications': test_case['max_pubs']
        }
        
        print(f"📚 Solicitando {test_case['max_pubs']} publicações...")
        
        try:
            response = requests.get(api_url, params=params, timeout=120)  # Timeout maior
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success') and 'data' in data and 'publications' in data['data']:
                    publications = data['data']['publications']
                    pub_count = len(publications)
                    
                    print(f"✅ RESULTADO:")
                    print(f"  Publicações retornadas: {pub_count}")
                    print(f"  Publicações solicitadas: {test_case['max_pubs']}")
                    print(f"  Total no campo: {data.get('total_results', 'N/A')}")
                    
                    # Verificar se obteve mais do que as 20 padrão
                    if pub_count > 20:
                        print(f"  🎉 SUCESSO: Obteve mais que 20 publicações!")
                    elif pub_count == 20 and test_case['max_pubs'] > 20:
                        print(f"  ⚠️ POSSÍVEL PROBLEMA: Deveria ter mais que 20")
                    else:
                        print(f"  ✅ Resultado dentro do esperado")
                    
                    # Mostrar algumas publicações
                    print(f"\n  📋 PRIMEIRAS 5 PUBLICAÇÕES:")
                    for j, pub in enumerate(publications[:5]):
                        year = pub.get('year', 'N/A')
                        citations = pub.get('citations', 0)
                        title = pub.get('title', 'Sem título')[:60] + "..."
                        print(f"    {j+1}. {title} ({year}) - {citations} citações")
                    
                    if pub_count > 5:
                        print(f"    ... e mais {pub_count - 5} publicações")
                    
                    # Verificar informações do pesquisador
                    if 'researcher_info' in data:
                        info = data['researcher_info']
                        print(f"\n  👤 PESQUISADOR:")
                        print(f"    Nome: {info.get('name', 'N/A')}")
                        print(f"    H-index: {info.get('h_index', 'N/A')}")
                        print(f"    Citações: {info.get('total_citations', 'N/A')}")
                
                else:
                    print("❌ Estrutura de resposta inesperada")
                    print(f"Chaves disponíveis: {list(data.keys())}")
                    
            else:
                print(f"❌ Erro HTTP {response.status_code}")
                print(f"Resposta: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
        
        # Aguardar entre testes para evitar bloqueio
        if i < len(test_cases) - 1:
            print("\nAguardando para próximo teste...")
            import time
            time.sleep(10)
    
    print(f"\n{'='*60}")
    print("🏁 TESTES CONCLUÍDOS")
    print(f"{'='*60}")

if __name__ == "__main__":
    test_multiple_publications()