#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import os

def test_export_with_data():
    print("🧪 Testando exportação com dados corrigidos...")
    
    api_url = 'http://localhost:8000/search/author/profile'
    profile_url = "https://scholar.google.com/citations?user=JicYPdAAAAAJ"  # Geoffrey Hinton
    
    params = {
        'query': 'Geoffrey Hinton',
        'platforms': 'scholar',
        'profile_url': profile_url,
        'export_excel': True,  # EXPORT DIRETO
        'max_publications': 10  # 10 publicações para teste
    }
    
    try:
        print("📤 Fazendo requisição com export_excel=True...")
        response = requests.get(api_url, params=params, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Resposta recebida!")
            print(f"Success: {data.get('success')}")
            print(f"Publicações: {len(data.get('data', {}).get('publications', []))}")
            
            # Verificar se arquivo Excel foi gerado
            excel_file = data.get('excel_file')
            export_error = data.get('export_error')
            
            if excel_file:
                print(f"🎉 ARQUIVO EXCEL GERADO: {excel_file}")
                
                # Verificar se arquivo existe
                export_path = f"exports/{excel_file}"
                if os.path.exists(export_path):
                    file_size = os.path.getsize(export_path)
                    print(f"📁 Arquivo existe: {export_path}")
                    print(f"📏 Tamanho: {file_size} bytes")
                    
                    if file_size > 1024:  # Mais de 1KB
                        print("✅ ARQUIVO TEM CONTEÚDO!")
                        return True
                    else:
                        print("⚠️ Arquivo muito pequeno, pode estar vazio")
                        return False
                else:
                    print(f"❌ Arquivo não encontrado: {export_path}")
                    return False
                    
            elif export_error:
                print(f"❌ ERRO NA EXPORTAÇÃO: {export_error}")
                return False
            else:
                print("❌ Arquivo Excel não foi gerado e nenhum erro reportado")
                return False
                
        else:
            print(f"❌ Erro na API: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    success = test_export_with_data()
    if success:
        print("\n🎉 EXPORTAÇÃO FUNCIONANDO COM DADOS!")
    else:
        print("\n💥 EXPORTAÇÃO AINDA TEM PROBLEMAS")