#!/usr/bin/env python3
"""
Healthcheck para o Web Scraper UniSER
Verifica se a API está funcionando corretamente
"""

import sys
import requests
import json
from typing import Dict, Any

def check_api_health() -> Dict[str, Any]:
    """Verifica se a API está saudável"""
    try:
        # Verificar endpoint básico
        response = requests.get("http://localhost:8000/", timeout=10)
        
        if response.status_code == 200:
            return {
                "status": "healthy",
                "api": "online",
                "message": "API está funcionando corretamente"
            }
        else:
            return {
                "status": "unhealthy", 
                "api": "error",
                "message": f"API retornou status {response.status_code}"
            }
            
    except requests.exceptions.ConnectionError:
        return {
            "status": "unhealthy",
            "api": "offline", 
            "message": "Não foi possível conectar à API"
        }
    except requests.exceptions.Timeout:
        return {
            "status": "unhealthy",
            "api": "timeout",
            "message": "API não respondeu em tempo hábil"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "api": "error",
            "message": f"Erro inesperado: {str(e)}"
        }

def check_mongodb_health() -> Dict[str, Any]:
    """Verifica se o MongoDB está acessível"""
    try:
        # Tentar acessar endpoint de health do MongoDB via API
        response = requests.get("http://localhost:8000/health/db", timeout=10)
        
        if response.status_code == 200:
            return {
                "status": "healthy",
                "database": "online",
                "message": "MongoDB está acessível"
            }
        else:
            return {
                "status": "unhealthy",
                "database": "error", 
                "message": "MongoDB não está acessível"
            }
            
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "message": f"Erro ao verificar MongoDB: {str(e)}"
        }

def main():
    """Função principal do healthcheck"""
    print("🔍 Verificando saúde do Web Scraper UniSER...")
    
    # Verificar API
    api_health = check_api_health()
    print(f"API: {api_health['message']}")
    
    # Verificar MongoDB
    db_health = check_mongodb_health()
    print(f"MongoDB: {db_health['message']}")
    
    # Determinar status geral
    if api_health["status"] == "healthy" and db_health["status"] == "healthy":
        print("✅ Sistema está saudável!")
        sys.exit(0)
    else:
        print("❌ Sistema apresenta problemas!")
        sys.exit(1)

if __name__ == "__main__":
    main()