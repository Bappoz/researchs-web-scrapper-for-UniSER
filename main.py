#!/usr/bin/env python3
"""
🚀 PONTO DE ENTRADA PRINCIPAL DA API - VERSÃO MODULAR
Executa a API Real de Scraping com arquitetura separada
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    try:
        import fastapi
        import uvicorn
        import pydantic
        import requests
        import bs4
        print("✅ Todas as dependências estão instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("📦 Execute: pip install -r requirements.txt")
        return False

def main():
    """Função principal"""
    print("🔥 INICIALIZANDO API REAL DE SCRAPING - VERSÃO MODULAR")
    print("=" * 60)
    
    # Verificar dependências
    if not check_dependencies():
        return
    
    # Importar a aplicação
    try:
        from src.api import app
        print("✅ Aplicação carregada com sucesso!")
    except ImportError as e:
        print(f"❌ Erro ao carregar aplicação: {e}")
        print("💡 Certifique-se de que está no diretório correto do projeto")
        return
    
    # Configuração do servidor
    print("\n🚀 Iniciando servidor...")
    print("📍 API: http://localhost:8000")
    print("📖 Documentação: http://localhost:8000/docs")
    print("📋 Endpoints Lattes: http://localhost:8000/api/lattes/")
    print("📋 Endpoints ORCID: http://localhost:8000/api/orcid/")
    print("🔄 Pressione CTRL+C para parar")
    print("=" * 60)
    
    # Executar servidor
    import uvicorn
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"]
    )

if __name__ == "__main__":
    main()