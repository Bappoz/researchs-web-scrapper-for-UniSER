"""
MONGODB DATABASE MANAGER
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
        self.mongo_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
        self.database_name = os.getenv('MONGODB_DATABASE', 'web-scraper-uniser')
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
            if self.collection is None:  # Corrigido para comparação explícita
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
            if self.async_collection is None:
                if not await self.connect_async():
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
    
    async def get_all_scholar_research_async(self) -> List[Dict[str, Any]]:
        """Buscar todas as pesquisas do Scholar (com ou sem filtro de keywords)"""
        try:
            if self.async_collection is None:
                if not await self.connect_async():
                    return []
            
            # Buscar todas as pesquisas do Scholar
            cursor = self.async_collection.find(
                {"platform": "scholar"},
                sort=[("timestamp", -1)]  # Mais recentes primeiro
            )
            
            results = []
            async for doc in cursor:
                results.append(doc)
            
            print(f"📚 Encontradas {len(results)} pesquisas do Scholar")
            
            return results
            
        except Exception as e:
            print(f"❌ Erro ao buscar dados do Scholar no MongoDB (async): {e}")
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
    
    async def get_all_unique_researchers_async(self) -> List[Dict[str, Any]]:
        """Obter todos os pesquisadores únicos com seus dados agregados"""
        try:
            if self.async_collection is None:
                if not await self.connect_async():
                    return []
            
            # Agregar pesquisadores únicos
            pipeline = [
                {
                    "$group": {
                        "_id": "$researcher_info.name",
                        "name": {"$first": "$researcher_info.name"},
                        "institution": {"$first": "$researcher_info.institution"},
                        "email": {"$first": "$researcher_info.email"},
                        "h_index": {"$first": "$researcher_info.h_index"},
                        "i10_index": {"$first": "$researcher_info.i10_index"},
                        "total_citations": {"$first": "$researcher_info.total_citations"},
                        "lattes_summary": {"$first": "$researcher_info.lattes_summary"},
                        "lattes_institution": {"$first": "$researcher_info.lattes_institution"},
                        "lattes_area": {"$first": "$researcher_info.lattes_area"},
                        "lattes_url": {"$first": "$researcher_info.lattes_url"},
                        "research_areas": {"$first": "$researcher_info.research_areas"},
                        "total_publications": {"$sum": "$total_publications"},
                        "searches": {"$sum": 1},
                        "last_search": {"$max": "$timestamp"}
                    }
                },
                {
                    "$sort": {"last_search": -1}
                }
            ]
            
            researchers = []
            async for doc in self.async_collection.aggregate(pipeline):
                # Converter _id para string para JSON serialization
                doc["id"] = str(doc["_id"]) if doc.get("_id") else ""
                doc.pop("_id", None)
                researchers.append(doc)
            
            print(f"👥 Encontrados {len(researchers)} pesquisadores únicos")
            return researchers
            
        except Exception as e:
            print(f"❌ Erro ao obter pesquisadores únicos (async): {e}")
            return []
    
    async def delete_researcher_async(self, researcher_id: str) -> Dict[str, Any]:
        """Deletar um pesquisador específico e todas as suas publicações"""
        try:
            if self.async_collection is None:
                if not await self.connect_async():
                    return {"deleted_publications": 0}
            
            # Deletar todas as buscas deste pesquisador
            result = await self.async_collection.delete_many({
                "researcher_info.name": researcher_id
            })
            
            print(f"🗑️ Deletadas {result.deleted_count} buscas do pesquisador: {researcher_id}")
            return {"deleted_publications": result.deleted_count}
            
        except Exception as e:
            print(f"❌ Erro ao deletar pesquisador (async): {e}")
            raise
    
    async def clear_all_data_async(self) -> Dict[str, Any]:
        """Limpar todos os dados do banco (USE COM CUIDADO!)"""
        try:
            if self.async_collection is None:
                if not await self.connect_async():
                    return {"deleted_count": 0}
            
            # Deletar todos os documentos
            result = await self.async_collection.delete_many({})
            
            print(f"🗑️ Banco de dados limpo! {result.deleted_count} documentos deletados")
            return {"deleted_count": result.deleted_count}
            
        except Exception as e:
            print(f"❌ Erro ao limpar banco de dados (async): {e}")
            raise
    
    def close(self):
        """Fechar conexões"""
        if self.client:
            self.client.close()
        if self.async_client:
            self.async_client.close()
        print("🔒 Conexões MongoDB fechadas")

# Instância global
research_db = ResearchDatabase()