#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_query_field():
    print("🧪 Testando se o campo 'query' está sendo retornado corretamente...")
    
    api_url = 'http://localhost:8000/search/author/profile'
    
    # Perfil de teste
    profile_url = "https://scholar.google.com/citations?user=JicYPdAAAAAJ"  # Geoffrey Hinton
    
    params = {
        'query': 'Geoffrey Hinton',
        'platforms': 'scholar',
        'profile_url': profile_url,
        'export_excel': False,
        'max_publications': 20
    }
    
    print(f"📡 Fazendo requisição para: {api_url}")
    print(f"📋 Parâmetros: {params}")
    
    try:
        response = requests.get(api_url, params=params, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n✅ RESPOSTA RECEBIDA:")
            print(f"  Success: {data.get('success', False)}")
            print(f"  Message: {data.get('message', 'N/A')}")
            print(f"  Platform: {data.get('platform', 'N/A')}")
            
            # Verificar especificamente o campo query
            query_field = data.get('query', None)
            print(f"\n🔍 CAMPO QUERY:")
            print(f"  Valor: '{query_field}'")
            print(f"  Tipo: {type(query_field)}")
            print(f"  Vazio?: {not query_field}")
            
            # Verificar researcher_info
            if 'researcher_info' in data:
                researcher_name = data['researcher_info'].get('name', None)
                print(f"\n👤 RESEARCHER_INFO:")
                print(f"  Nome: '{researcher_name}'")
                
                # Verificar se o query corresponde ao nome
                if query_field and researcher_name:
                    if query_field == researcher_name:
                        print(f"  ✅ Query corresponde ao nome do pesquisador")
                    else:
                        print(f"  ⚠️ Query ({query_field}) != Nome ({researcher_name})")
                elif not query_field and researcher_name:
                    print(f"  ❌ Query vazio mas nome disponível!")
                elif query_field and not researcher_name:
                    print(f"  ⚠️ Query disponível mas nome vazio")
                else:
                    print(f"  ❌ Ambos vazios!")
            
            # Verificar se há dados para exportação
            has_publications = False
            pub_count = 0
            
            if 'data' in data and 'publications' in data['data']:
                publications = data['data']['publications']
                pub_count = len(publications)
                has_publications = pub_count > 0
            
            print(f"\n📚 DADOS PARA EXPORTAÇÃO:")
            print(f"  Publicações: {pub_count}")
            print(f"  Pode exportar?: {has_publications and bool(query_field)}")
            
            # Simular verificação do frontend
            print(f"\n🖥️ SIMULAÇÃO FRONTEND:")
            print(f"  Campo busca mostrará: '{query_field or '(vazio)'}'")
            print(f"  Botão export habilitado?: {has_publications and bool(query_field)}")
            
            if not query_field:
                print(f"  🚨 PROBLEMA: Campo query vazio impedirá exportação!")
            elif not has_publications:
                print(f"  🚨 PROBLEMA: Sem publicações impedirá exportação!")
            else:
                print(f"  ✅ Exportação deveria funcionar normalmente")
                
        else:
            print(f"❌ Erro HTTP {response.status_code}")
            print(f"Resposta: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    test_query_field()