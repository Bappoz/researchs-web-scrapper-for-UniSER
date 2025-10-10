"""
🗄️ MONGODB DATABASE MANAGER
Gerenciamento de banco de dados para pesquisas acadêmicas
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import motor.motor_asyncio
from pymongo import MongoClient
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class ResearchDatabase:
    """Gerenciador do banco de dados de pesquisas"""
    
    def __init__(self):
        self.mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/web-scraper-uniser')
        self.database_name = os.getenv('DATABASE_NAME', 'web-scraper-uniser')
        self.collection_name = os.getenv('COLLECTION_NAME', 'researchers-data')
        
        # Cliente síncrono para operações normais
        self.client = None
        self.db = None
        self.collection = None
        
        # Cliente assíncrono para uso com FastAPI
        self.async_client = None
        self.async_db = None
        self.async_collection = None
        
        print(f"📊 MongoDB configurado: {self.mongo_url}")
    
    def connect(self):
        """Conectar ao MongoDB (síncrono)"""
        try:
            self.client = MongoClient(self.mongo_url)
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            
            # Testar conexão
            self.client.admin.command('ping')
            print(f"✅ Conectado ao MongoDB: {self.database_name}.{self.collection_name}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao conectar MongoDB: {e}")
            return False
    
    async def connect_async(self):
        """Conectar ao MongoDB (assíncrono)"""
        try:
            self.async_client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_url)
            self.async_db = self.async_client[self.database_name]
            self.async_collection = self.async_db[self.collection_name]
            print(f"✅ Cliente assíncrono MongoDB configurado")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao configurar cliente assíncrono: {e}")
            return False
    
    def save_research_result(self, research_data: Dict[str, Any]) -> bool:
        """Salvar resultado de pesquisa no banco"""
        try:
            if not self.collection:
                if not self.connect():
                    return False
            
            # Preparar documento
            document = {
                "timestamp": datetime.now(timezone.utc),
                "query": research_data.get("query", ""),
                "platform": research_data.get("platform", ""),
                "search_type": research_data.get("search_type", ""),
                "researcher_info": research_data.get("researcher_info", {}),
                "total_publications": research_data.get("total_results", 0),
                "filtered_by_keywords": research_data.get("filtered_by_keywords", False),
                "original_total": research_data.get("original_total", 0),
                "publications": research_data.get("data", {}).get("publications", []),
                "execution_time": research_data.get("execution_time", 0),
                "metadata": {
                    "saved_at": datetime.now(timezone.utc).isoformat(),
                    "source": "web-scraper-api",
                    "version": "1.0"
                }
            }
            
            # Inserir no banco
            result = self.collection.insert_one(document)
            
            print(f"💾 Pesquisa salva no MongoDB: {result.inserted_id}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar no MongoDB: {e}")
            return False
    
    async def save_research_result_async(self, research_data: Dict[str, Any]) -> bool:
        """Salvar resultado de pesquisa no banco (assíncrono)"""
        try:
            if not self.async_collection:
                if not self.connect_async():
                    return False
            
            # Preparar documento
            document = {
                "timestamp": datetime.now(timezone.utc),
                "query": research_data.get("query", ""),
                "platform": research_data.get("platform", ""),
                "search_type": research_data.get("search_type", ""),
                "researcher_info": research_data.get("researcher_info", {}),
                "total_publications": research_data.get("total_results", 0),
                "filtered_by_keywords": research_data.get("filtered_by_keywords", False),
                "original_total": research_data.get("original_total", 0),
                "publications": research_data.get("data", {}).get("publications", []),
                "execution_time": research_data.get("execution_time", 0),
                "metadata": {
                    "saved_at": datetime.now(timezone.utc).isoformat(),
                    "source": "web-scraper-api",
                    "version": "1.0"
                }
            }
            
            # Inserir no banco
            result = await self.async_collection.insert_one(document)
            
            print(f"💾 Pesquisa salva no MongoDB (async): {result.inserted_id}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar no MongoDB (async): {e}")
            return False
    
    def get_all_keyword_filtered_research(self) -> List[Dict[str, Any]]:
        """Buscar todas as pesquisas filtradas por keywords"""
        try:
            if not self.collection:
                if not self.connect():
                    return []
            
            # Buscar apenas pesquisas com filtro de keywords
            cursor = self.collection.find(
                {"filtered_by_keywords": True},
                sort=[("timestamp", -1)]  # Mais recentes primeiro
            )
            
            results = list(cursor)
            print(f"📚 Encontradas {len(results)} pesquisas com filtro de keywords")
            
            return results
            
        except Exception as e:
            print(f"❌ Erro ao buscar dados do MongoDB: {e}")
            return []
    
    async def get_all_keyword_filtered_research_async(self) -> List[Dict[str, Any]]:
        """Buscar todas as pesquisas filtradas por keywords (versão assíncrona)"""
        try:
            if self.async_collection is None:
                if not await self.connect_async():
                    return []
            
            # Buscar apenas pesquisas com filtro de keywords
            cursor = self.async_collection.find(
                {"filtered_by_keywords": True},
                sort=[("timestamp", -1)]  # Mais recentes primeiro
            )
            
            results = []
            async for doc in cursor:
                results.append(doc)
            
            print(f"📚 Encontradas {len(results)} pesquisas com filtro de keywords")
            
            return results
            
        except Exception as e:
            print(f"❌ Erro ao buscar dados do MongoDB (async): {e}")
            return []
    
    def get_research_statistics(self) -> Dict[str, Any]:
        """Obter estatísticas gerais das pesquisas"""
        try:
            if not self.collection:
                if not self.connect():
                    return {}
            
            # Agregar estatísticas
            pipeline = [
                {
                    "$group": {
                        "_id": None,
                        "total_searches": {"$sum": 1},
                        "filtered_searches": {
                            "$sum": {"$cond": ["$filtered_by_keywords", 1, 0]}
                        },
                        "total_publications": {"$sum": "$total_publications"},
                        "platforms": {"$addToSet": "$platform"},
                        "latest_search": {"$max": "$timestamp"}
                    }
                }
            ]
            
            result = list(self.collection.aggregate(pipeline))
            
            if result:
                stats = result[0]
                stats.pop("_id", None)
                return stats
            
            return {}
            
        except Exception as e:
            print(f"❌ Erro ao obter estatísticas: {e}")
            return {}
    
    async def get_research_statistics_async(self) -> Dict[str, Any]:
        """Obter estatísticas gerais das pesquisas (versão assíncrona)"""
        try:
            if self.async_collection is None:
                if not await self.connect_async():
                    return {}
            
            # Agregar estatísticas
            pipeline = [
                {
                    "$group": {
                        "_id": None,
                        "total_searches": {"$sum": 1},
                        "filtered_searches": {
                            "$sum": {"$cond": ["$filtered_by_keywords", 1, 0]}
                        },
                        "total_publications": {"$sum": "$total_publications"},
                        "platforms": {"$addToSet": "$platform"},
                        "latest_search": {"$max": "$timestamp"}
                    }
                }
            ]
            
            result = []
            async for doc in self.async_collection.aggregate(pipeline):
                result.append(doc)
            
            if result:
                stats = result[0]
                stats.pop("_id", None)
                return stats
            
            return {}
            
        except Exception as e:
            print(f"❌ Erro ao obter estatísticas (async): {e}")
            return {}
    
    def close(self):
        """Fechar conexões"""
        if self.client:
            self.client.close()
        if self.async_client:
            self.async_client.close()
        print("🔒 Conexões MongoDB fechadas")

# Instância global
research_db = ResearchDatabase()