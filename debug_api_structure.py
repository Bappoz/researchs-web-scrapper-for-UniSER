#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def debug_api_response():
    print("🔍 Investigando estrutura de dados da API...")
    
    api_url = 'http://localhost:8000/search/author/profile'
    profile_url = "https://scholar.google.com/citations?user=JicYPdAAAAAJ"  # Geoffrey Hinton
    
    params = {
        'query': 'Geoffrey Hinton',
        'platforms': 'scholar',
        'profile_url': profile_url,
        'export_excel': False,
        'max_publications': 5  # Só 5 para debug
    }
    
    try:
        response = requests.get(api_url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            print("📋 ESTRUTURA DOS DADOS DA API:")
            print("="*50)
            
            print(f"🔑 Chaves principais: {list(data.keys())}")
            print(f"✅ Success: {data.get('success')}")
            print(f"🏷️ Platform: {data.get('platform')}")
            print(f"🔍 Search Type: {data.get('search_type')}")
            print(f"❓ Query: {data.get('query')}")
            
            if 'researcher_info' in data:
                print(f"\n👤 RESEARCHER INFO:")
                researcher = data['researcher_info']
                for key, value in researcher.items():
                    print(f"  {key}: {value}")
            
            if 'data' in data and 'publications' in data['data']:
                pubs = data['data']['publications']
                print(f"\n📚 PUBLICAÇÕES: {len(pubs)} encontradas")
                
                if pubs:
                    print("\n📖 PRIMEIRA PUBLICAÇÃO:")
                    first_pub = pubs[0]
                    for key, value in first_pub.items():
                        print(f"  {key}: {value}")
                        
            print(f"\n🗂️ ESTRUTURA COMPLETA (para debug):")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:2000] + "..." if len(str(data)) > 2000 else json.dumps(data, indent=2, ensure_ascii=False))
            
        else:
            print(f"❌ Erro na API: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    debug_api_response()