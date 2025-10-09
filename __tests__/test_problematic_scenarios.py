#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_problematic_scenario():
    print("🧪 Testando cenários problemáticos de H-index...")
    
    # Vamos testar se o problema pode estar na interface do usuário
    # Criando um cenário onde os valores poderiam ser confundidos
    
    api_url = 'http://localhost:8000/search/author/profile'
    
    # Teste com perfil diferente que pode ter valores problemáticos
    test_profiles = [
        {
            "name": "Teste com Geoffrey Hinton",
            "url": "https://scholar.google.com/citations?user=JicYPdAAAAAJ"
        },
        {
            "name": "Teste com Yann LeCun", 
            "url": "https://scholar.google.com/citations?user=WLN3QrAAAAAJ"
        }
    ]
    
    for profile in test_profiles:
        print(f"\n{'='*60}")
        print(f"TESTANDO: {profile['name']}")
        print(f"URL: {profile['url']}")
        print(f"{'='*60}")
        
        params = {
            'query': profile['name'],
            'platforms': 'scholar',
            'profile_url': profile['url'],
            'export_excel': False
        }
        
        try:
            print("📡 Fazendo requisição...")
            response = requests.get(api_url, params=params, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                
                print("✅ DADOS RECEBIDOS:")
                
                # Verificar estrutura researcher_info
                if 'researcher_info' in data:
                    info = data['researcher_info']
                    
                    name = info.get('name', 'N/A')
                    h_index = info.get('h_index', 'N/A')
                    citations = info.get('total_citations', 'N/A')
                    institution = info.get('institution', 'N/A')
                    
                    print(f"📋 RESULTADO:")
                    print(f"  Nome: {name}")
                    print(f"  H-index: {h_index}")
                    print(f"  Citações: {citations}")
                    print(f"  Instituição: {institution}")
                    
                    # Análise de possíveis problemas
                    print(f"\n🔍 ANÁLISE DE PROBLEMAS:")
                    
                    try:
                        h_val = int(str(h_index).replace(',', ''))
                        cit_val = int(str(citations).replace(',', ''))
                        
                        print(f"  H-index (número): {h_val:,}")
                        print(f"  Citações (número): {cit_val:,}")
                        print(f"  Razão H/Citações: {h_val/cit_val:.4f}")
                        
                        # Verificações de problemas
                        problems = []
                        
                        if h_val == cit_val:
                            problems.append("❌ H-index IGUAL às citações!")
                        
                        if h_val > 1000:
                            problems.append("❌ H-index MUITO ALTO (>1000)")
                        
                        if h_val > cit_val:
                            problems.append("❌ H-index MAIOR que citações")
                        
                        if h_val > cit_val * 0.1:
                            problems.append("⚠️ H-index suspeito (>10% das citações)")
                        
                        if str(h_index) == str(citations):
                            problems.append("❌ H-index STRING igual à citações STRING")
                        
                        if len(problems) > 0:
                            print(f"\n🚨 PROBLEMAS DETECTADOS:")
                            for problem in problems:
                                print(f"  {problem}")
                        else:
                            print(f"\n✅ H-index parece válido")
                            
                        # Verificar se pode haver confusão na interface
                        print(f"\n🎭 SIMULAÇÃO DE INTERFACE:")
                        print(f"  Como apareceria na tela:")
                        print(f"    H-Index: {h_index}")
                        print(f"    Citações: {citations}")
                        
                        if len(str(h_index)) == len(str(citations)):
                            print(f"  ⚠️ AVISO: Mesmo número de dígitos! Usuário pode confundir.")
                        
                    except Exception as e:
                        print(f"  ❌ Erro na análise numérica: {e}")
                
                else:
                    print("❌ researcher_info não encontrado!")
                    print(f"Chaves disponíveis: {list(data.keys())}")
            
            else:
                print(f"❌ Erro HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    test_problematic_scenario()