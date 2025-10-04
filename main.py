#!/usr/bin/env python3
"""
🚀 INICIALIZADOR DA API GOOGLE SCHOLAR
======================================
Script para iniciar a API REST
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    try:
        import fastapi
        import uvicorn
        import pydantic
        from serpapi import GoogleSearch
        print("✅ Todas as dependências estão instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        return False

def install_dependencies():
    """Instala as dependências"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements-api.txt"
        ])
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def check_env_file():
    """Verifica se o arquivo .env existe"""
    env_path = Path("src/scraper/.env")
    if env_path.exists():
        print("✅ Arquivo .env encontrado")
        return True
    else:
        print("❌ Arquivo .env não encontrado em src/scraper/.env")
        print("📝 Crie um arquivo .env com sua API_KEY do SerpAPI")
        return False

def start_api():
    """Inicia a API"""
    print("🚀 Iniciando API Google Scholar...")
    print("📍 API estará disponível em: http://localhost:8000")
    print("📚 Documentação em: http://localhost:8000/docs")
    print("🔄 Redoc em: http://localhost:8000/redoc")
    print("\n" + "="*50)
    
    os.chdir("src")
    subprocess.run([
        sys.executable, "-m", "uvicorn", "api:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])

def main():
    """Função principal"""
    print("🎓 GOOGLE SCHOLAR API STARTER")
    print("="*40)
    
    # Verificar arquivo .env
    if not check_env_file():
        return
    
    # Verificar dependências
    if not check_dependencies():
        print("\n📦 Instalando dependências...")
        if not install_dependencies():
            return
    
    # Iniciar API
    start_api()

if __name__ == "__main__":
    main()