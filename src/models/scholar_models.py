"""
📚 MODELOS DE DADOS PARA API GOOGLE SCHOLAR
===========================================
Definição de estruturas JSON para requests e responses
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SearchType(str, Enum):
    """Tipos de pesquisa disponíveis"""
    QUERY = "query"
    AUTHOR = "author"
    CITATIONS = "citations"

class SearchRequest(BaseModel):
    """Modelo para requisições de busca"""
    query: str = Field(..., description="Termo de busca ou nome do autor")
    search_type: SearchType = Field(default=SearchType.QUERY, description="Tipo de busca")
    max_results: int = Field(default=20, ge=1, le=100, description="Máximo de resultados")
    max_pages: int = Field(default=3, ge=1, le=10, description="Máximo de páginas")
    save_csv: bool = Field(default=False, description="Salvar em CSV")

class PublicationData(BaseModel):
    """Modelo para dados de uma publicação"""
    title: str = Field(..., description="Título da publicação")
    authors: Optional[str] = Field(None, description="Autores")
    publication: Optional[str] = Field(None, description="Informações da publicação")
    year: Optional[int] = Field(None, description="Ano de publicação")
    cited_by: int = Field(default=0, description="Número de citações")
    link: Optional[str] = Field(None, description="Link para a publicação")
    snippet: Optional[str] = Field(None, description="Trecho da publicação")
    result_id: Optional[str] = Field(None, description="ID do resultado")
    result_type: Optional[str] = Field(None, description="Tipo do resultado")
    page_number: int = Field(default=1, description="Número da página")
    file_title: Optional[str] = Field(None, description="Título do arquivo")
    file_link: Optional[str] = Field(None, description="Link do arquivo")
    file_format: Optional[str] = Field(None, description="Formato do arquivo")

class AuthorProfile(BaseModel):
    """Modelo para perfil do autor"""
    name: str = Field(..., description="Nome do autor")
    author_id: str = Field(..., description="ID do autor no Google Scholar")
    affiliations: Optional[str] = Field(None, description="Afiliações")
    cited_by: Optional[int] = Field(None, description="Total de citações")
    email_domain: Optional[str] = Field(None, description="Domínio do email")
    interests: Optional[List[str]] = Field(None, description="Áreas de interesse")

class AuthorSummary(BaseModel):
    """Modelo para resumo estatístico do autor"""
    author_name: str = Field(..., description="Nome do autor")
    total_publications: int = Field(..., description="Total de publicações")
    total_citations: int = Field(..., description="Total de citações")
    year_range: Optional[Dict[str, int]] = Field(None, description="Período de publicações")
    top_cited: List[Dict[str, Any]] = Field(default=[], description="Top 5 mais citadas")
    publications_by_year: Optional[Dict[str, int]] = Field(None, description="Publicações por ano")

class CitationData(BaseModel):
    """Modelo para dados de citação"""
    original_title: str = Field(..., description="Título original")
    citation_title: str = Field(..., description="Título da citação")
    citation_snippet: Optional[str] = Field(None, description="Trecho da citação")

class SearchResponse(BaseModel):
    """Modelo para resposta da busca"""
    success: bool = Field(..., description="Status da operação")
    message: str = Field(..., description="Mensagem de status")
    search_type: SearchType = Field(..., description="Tipo de busca realizada")
    query: str = Field(..., description="Query utilizada")
    total_results: int = Field(..., description="Total de resultados encontrados")
    execution_time: float = Field(..., description="Tempo de execução em segundos")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da busca")
    
    # Dados específicos por tipo de busca
    publications: Optional[List[PublicationData]] = Field(None, description="Lista de publicações")
    author_profile: Optional[AuthorProfile] = Field(None, description="Perfil do autor")
    author_summary: Optional[AuthorSummary] = Field(None, description="Resumo do autor")
    citations: Optional[List[CitationData]] = Field(None, description="Lista de citações")
    
    # Metadados
    csv_file: Optional[str] = Field(None, description="Nome do arquivo CSV gerado")
    api_calls_used: int = Field(default=1, description="Número de chamadas API utilizadas")

class ErrorResponse(BaseModel):
    """Modelo para resposta de erro"""
    success: bool = Field(default=False, description="Status da operação")
    error: str = Field(..., description="Mensagem de erro")
    error_code: str = Field(..., description="Código do erro")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp do erro")

class HealthResponse(BaseModel):
    """Modelo para health check"""
    status: str = Field(..., description="Status da API")
    api_key_valid: bool = Field(..., description="Validade da API key")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp do health check")
    version: str = Field(default="1.0.0", description="Versão da API")