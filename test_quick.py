#!/usr/bin/env python3
"""
🚀 TESTE RÁPIDO DA INTEGRAÇÃO ESCAVADOR
======================================
Execute este script para testar rapidamente a nova funcionalidade
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def quick_test():
    """Teste rápido e simples"""
    print("\n🧪 TESTE RÁPIDO - ESCAVADOR + GOOGLE SCHOLAR")
    print("=" * 60)
    
    # Pedir nome ao usuário
    nome = input("\n👤 Digite o nome de um pesquisador brasileiro: ").strip()
    
    if not nome:
        print("❌ Nome vazio! Usando exemplo...")
        nome = "Carlos Silva"
    
    print(f"\n🔍 Buscando dados para: {nome}")
    print("-" * 60)
    
    # Importar serviços
    try:
        from services.services import GoogleScholarService
        print("✅ Módulo GoogleScholarService importado")
    except Exception as e:
        print(f"❌ Erro ao importar serviço: {e}")
        return 1
    
    # Criar serviço
    service = GoogleScholarService()
    
    # Testar Google Scholar
    print("\n1️⃣ GOOGLE SCHOLAR:")
    print("-" * 40)
    try:
        author_profile, publications = service.search_by_author_profile(nome)
        
        if author_profile:
            print(f"✅ Nome: {author_profile.name}")
            print(f"📚 Publicações: {len(publications)}")
            print(f"📊 H-index: {author_profile.h_index if hasattr(author_profile, 'h_index') else 'N/A'}")
            print(f"📈 Citações: {author_profile.cited_by if hasattr(author_profile, 'cited_by') else 'N/A'}")
        else:
            print("⚠️ Perfil não encontrado no Google Scholar")
            
    except Exception as e:
        print(f"❌ Erro no Google Scholar: {e}")
    
    # Testar Escavador
    print("\n2️⃣ ESCAVADOR (Resumo do Lattes):")
    print("-" * 40)
    try:
        lattes_summary = service.get_lattes_summary_via_escavador(nome)
        
        if lattes_summary and lattes_summary.get('success'):
            print(f"✅ Nome: {lattes_summary.get('name')}")
            print(f"🏢 Instituição: {lattes_summary.get('institution')}")
            print(f"📚 Área: {lattes_summary.get('area')}")
            print(f"📝 Resumo: {lattes_summary.get('summary', '')[:150]}...")
            print(f"🔗 Lattes URL: {lattes_summary.get('lattes_url') or 'N/A'}")
        else:
            print("⚠️ Resumo não encontrado no Escavador")
            print(f"   Mensagem: {lattes_summary.get('summary', 'N/A')}")
            
    except Exception as e:
        print(f"❌ Erro no Escavador: {e}")
    
    # Resultado Final
    print("\n" + "=" * 60)
    print("✅ TESTE CONCLUÍDO!")
    print("\nAgora você pode:")
    print("1. Iniciar o backend: python src/api.py")
    print("2. Iniciar o frontend: cd frontend && npm run dev")
    print("3. Acessar: http://localhost:5173")
    print("4. Buscar por qualquer pesquisador!")
    print("=" * 60 + "\n")
    
    return 0

if __name__ == "__main__":
    try:
        exit(quick_test())
    except KeyboardInterrupt:
        print("\n\n⚠️ Teste cancelado pelo usuário")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        exit(1)
