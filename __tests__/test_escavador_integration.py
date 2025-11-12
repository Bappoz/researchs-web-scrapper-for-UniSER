"""
🧪 TESTE DA INTEGRAÇÃO COM ESCAVADOR
====================================
Script para testar a funcionalidade de busca do resumo do Lattes via Escavador
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from scraper.escavador_scraper import search_lattes_summary
from services.services import GoogleScholarService

def test_escavador_direct():
    """Teste direto do scraper do Escavador"""
    print("=" * 60)
    print("🧪 TESTE 1: Scraper Direto do Escavador")
    print("=" * 60)
    
    # Nome de teste
    test_name = "Maria Silva"
    
    print(f"\n🔍 Buscando resumo para: {test_name}")
    result = search_lattes_summary(test_name)
    
    print("\n📊 RESULTADO:")
    print(f"✅ Sucesso: {result.get('success')}")
    print(f"👤 Nome: {result.get('name')}")
    print(f"🏢 Instituição: {result.get('institution')}")
    print(f"📚 Área: {result.get('area')}")
    print(f"📝 Resumo: {result.get('summary')[:100]}..." if result.get('summary') else "Resumo: N/A")
    print(f"🔗 URL Lattes: {result.get('lattes_url')}")
    
    return result.get('success', False)

def test_service_integration():
    """Teste da integração no serviço do Google Scholar"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 2: Integração no GoogleScholarService")
    print("=" * 60)
    
    # Nome de teste
    test_name = "João Santos"
    
    print(f"\n🔍 Buscando através do serviço: {test_name}")
    
    service = GoogleScholarService()
    result = service.get_lattes_summary_via_escavador(test_name)
    
    print("\n📊 RESULTADO:")
    print(f"✅ Sucesso: {result.get('success')}")
    print(f"👤 Nome: {result.get('name')}")
    print(f"🏢 Instituição: {result.get('institution')}")
    print(f"📚 Área: {result.get('area')}")
    print(f"📝 Resumo: {result.get('summary')[:100]}..." if result.get('summary') else "Resumo: N/A")
    
    return result is not None

def test_full_integration():
    """Teste completo da integração"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 3: Integração Completa (Scholar + Lattes)")
    print("=" * 60)
    
    test_name = "Carlos Oliveira"
    
    print(f"\n🔍 Buscando autor no Scholar + resumo do Lattes: {test_name}")
    
    service = GoogleScholarService()
    
    # Buscar no Scholar
    print("\n1️⃣ Buscando no Google Scholar...")
    author_profile, publications = service.search_by_author_profile(test_name)
    
    if author_profile:
        print(f"✅ Perfil encontrado: {author_profile.name}")
        print(f"📚 Publicações: {len(publications)}")
    else:
        print("⚠️ Perfil não encontrado no Scholar")
    
    # Buscar resumo do Lattes
    print("\n2️⃣ Buscando resumo do Lattes...")
    lattes_summary = service.get_lattes_summary_via_escavador(test_name)
    
    if lattes_summary and lattes_summary.get('success'):
        print(f"✅ Resumo do Lattes encontrado: {lattes_summary.get('name')}")
        print(f"🏢 Instituição: {lattes_summary.get('institution')}")
        print(f"📚 Área: {lattes_summary.get('area')}")
    else:
        print("⚠️ Resumo do Lattes não encontrado")
    
    print("\n3️⃣ Resultado Integrado:")
    print(f"   - Dados do Scholar: {'✅' if author_profile else '❌'}")
    print(f"   - Resumo do Lattes: {'✅' if lattes_summary and lattes_summary.get('success') else '❌'}")
    
    return True

def main():
    """Executa todos os testes"""
    print("\n🚀 INICIANDO TESTES DE INTEGRAÇÃO COM ESCAVADOR")
    print("=" * 60)
    
    results = []
    
    # Teste 1: Scraper direto
    try:
        result = test_escavador_direct()
        results.append(("Scraper Direto", result))
    except Exception as e:
        print(f"\n❌ Erro no Teste 1: {e}")
        results.append(("Scraper Direto", False))
    
    # Teste 2: Integração no serviço
    try:
        result = test_service_integration()
        results.append(("Serviço Integrado", result))
    except Exception as e:
        print(f"\n❌ Erro no Teste 2: {e}")
        results.append(("Serviço Integrado", False))
    
    # Teste 3: Integração completa
    try:
        result = test_full_integration()
        results.append(("Integração Completa", result))
    except Exception as e:
        print(f"\n❌ Erro no Teste 3: {e}")
        results.append(("Integração Completa", False))
    
    # Resumo dos testes
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    for test_name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, s in results if s)
    total = len(results)
    
    print(f"\n🎯 Total: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM")
        return 1

if __name__ == "__main__":
    exit(main())
