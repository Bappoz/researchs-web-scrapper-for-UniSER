"""
📚 MODELOS DE DADOS PARA LATTES E ORCID
========================================
Definição de estruturas JSON específicas para Lattes e ORCID
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date
from enum import Enum

class PlatformType(str, Enum):
    """Plataformas de busca disponíveis"""
    LATTES = "lattes"
    ORCID = "orcid"

class LattesSearchType(str, Enum):
    """Tipos de busca no Lattes"""
    NAME = "name"
    CPF = "cpf"
    INSTITUTION = "institution"
    AREA = "area"

class ORCIDSearchType(str, Enum):
    """Tipos de busca no ORCID"""
    NAME = "name"
    ORCID_ID = "orcid_id"
    EMAIL = "email"
    AFFILIATION = "affiliation"

# ==================== MODELOS LATTES ====================

class LattesEducation(BaseModel):
    """Formação acadêmica no Lattes"""
    level: str = Field(..., description="Nível (Graduação, Mestrado, Doutorado, etc.)")
    course: Optional[str] = Field(None, description="Nome do curso")
    institution: Optional[str] = Field(None, description="Instituição")
    year_start: Optional[int] = Field(None, description="Ano de início")
    year_end: Optional[int] = Field(None, description="Ano de conclusão")
    status: Optional[str] = Field(None, description="Status (Concluído, Em andamento)")

class LattesPublication(BaseModel):
    """Publicação no Lattes"""
    title: str = Field(..., description="Título da publicação")
    authors: Optional[str] = Field(None, description="Autores")
    journal: Optional[str] = Field(None, description="Revista/Periódico")
    year: Optional[int] = Field(None, description="Ano de publicação")
    volume: Optional[str] = Field(None, description="Volume")
    pages: Optional[str] = Field(None, description="Páginas")
    doi: Optional[str] = Field(None, description="DOI")
    cited_by: int = Field(default=0, description="Número de citações")
    issn: Optional[str] = Field(None, description="ISSN")
    publication_type: str = Field(default="article", description="Tipo de publicação")

class LattesProject(BaseModel):
    """Projeto de pesquisa no Lattes"""
    title: str = Field(..., description="Título do projeto")
    description: Optional[str] = Field(None, description="Descrição")
    year_start: Optional[int] = Field(None, description="Ano de início")
    year_end: Optional[int] = Field(None, description="Ano de fim")
    funding_agency: Optional[str] = Field(None, description="Agência financiadora")
    situation: Optional[str] = Field(None, description="Situação")

class LattesProfile(BaseModel):
    """Perfil completo do Lattes"""
    name: str = Field(..., description="Nome completo")
    lattes_id: Optional[str] = Field(None, description="ID do Lattes")
    cpf: Optional[str] = Field(None, description="CPF")
    orcid_id: Optional[str] = Field(None, description="ORCID ID")
    birth_date: Optional[date] = Field(None, description="Data de nascimento")
    nationality: Optional[str] = Field(None, description="Nacionalidade")
    
    # Informações profissionais
    current_institution: Optional[str] = Field(None, description="Instituição atual")
    current_position: Optional[str] = Field(None, description="Cargo atual")
    research_areas: List[str] = Field(default=[], description="Áreas de pesquisa")
    
    # Formação
    education: List[LattesEducation] = Field(default=[], description="Formação acadêmica")
    
    # Produção
    publications: List[LattesPublication] = Field(default=[], description="Publicações")
    projects: List[LattesProject] = Field(default=[], description="Projetos")
    
    # Estatísticas
    total_publications: int = Field(default=0, description="Total de publicações")
    total_projects: int = Field(default=0, description="Total de projetos")
    h_index: Optional[int] = Field(None, description="Índice H calculado")
    total_citations: Optional[int] = Field(None, description="Total de citações")
    last_update: Optional[datetime] = Field(None, description="Última atualização")

# ==================== MODELOS ORCID ====================

class ORCIDEmployment(BaseModel):
    """Emprego/Afiliação no ORCID"""
    organization: str = Field(..., description="Organização")
    role_title: Optional[str] = Field(None, description="Cargo")
    department: Optional[str] = Field(None, description="Departamento")
    start_date: Optional[date] = Field(None, description="Data de início")
    end_date: Optional[date] = Field(None, description="Data de fim")
    city: Optional[str] = Field(None, description="Cidade")
    country: Optional[str] = Field(None, description="País")

class ORCIDWork(BaseModel):
    """Trabalho/Publicação no ORCID"""
    title: str = Field(..., description="Título")
    journal_title: Optional[str] = Field(None, description="Nome da revista")
    type: Optional[str] = Field(None, description="Tipo de trabalho")
    publication_date: Optional[date] = Field(None, description="Data de publicação")
    external_ids: List[Dict[str, str]] = Field(default=[], description="IDs externos (DOI, PMID, etc.)")
    url: Optional[str] = Field(None, description="URL")
    citation_type: Optional[str] = Field(None, description="Tipo de citação")
    citation_value: Optional[str] = Field(None, description="Citação formatada")
    cited_by: int = Field(default=0, description="Número de citações")

class ORCIDEducation(BaseModel):
    """Educação no ORCID"""
    organization: str = Field(..., description="Instituição")
    degree: Optional[str] = Field(None, description="Grau/Título")
    start_date: Optional[date] = Field(None, description="Data de início")
    end_date: Optional[date] = Field(None, description="Data de conclusão")
    city: Optional[str] = Field(None, description="Cidade")
    country: Optional[str] = Field(None, description="País")

class ORCIDProfile(BaseModel):
    """Perfil completo do ORCID"""
    orcid_id: str = Field(..., description="ORCID ID")
    given_names: Optional[str] = Field(None, description="Nome")
    family_name: Optional[str] = Field(None, description="Sobrenome")
    credit_name: Optional[str] = Field(None, description="Nome para crédito")
    other_names: List[str] = Field(default=[], description="Outros nomes")
    
    # Informações pessoais
    biography: Optional[str] = Field(None, description="Biografia")
    researcher_urls: List[Dict[str, str]] = Field(default=[], description="URLs do pesquisador")
    emails: List[str] = Field(default=[], description="Emails")
    
    # Informações profissionais
    employments: List[ORCIDEmployment] = Field(default=[], description="Empregos/Afiliações")
    educations: List[ORCIDEducation] = Field(default=[], description="Educação")
    works: List[ORCIDWork] = Field(default=[], description="Trabalhos/Publicações")
    
    # Metadados
    creation_method: Optional[str] = Field(None, description="Método de criação")
    last_modified_date: Optional[datetime] = Field(None, description="Última modificação")
    claimed: bool = Field(default=True, description="Perfil reivindicado")
    verified_email: bool = Field(default=False, description="Email verificado")
    
    # Estatísticas calculadas
    total_works: int = Field(default=0, description="Total de trabalhos")
    h_index: Optional[int] = Field(None, description="Índice H calculado")
    total_citations: Optional[int] = Field(None, description="Total de citações")

# ==================== MODELOS DE BUSCA ====================

class AcademicSearchRequest(BaseModel):
    """Requisição de busca acadêmica"""
    query: str = Field(..., description="Termo de busca")
    platform: PlatformType = Field(..., description="Plataforma (lattes ou orcid)")
    search_type: Union[LattesSearchType, ORCIDSearchType] = Field(..., description="Tipo de busca")
    max_results: int = Field(default=20, ge=1, le=100, description="Máximo de resultados")
    include_publications: bool = Field(default=True, description="Incluir publicações")
    include_projects: bool = Field(default=True, description="Incluir projetos (Lattes)")
    save_csv: bool = Field(default=False, description="Salvar em CSV")

class AcademicSearchResponse(BaseModel):
    """Resposta da busca acadêmica"""
    success: bool = Field(..., description="Status da operação")
    message: str = Field(..., description="Mensagem de status")
    platform: PlatformType = Field(..., description="Plataforma utilizada")
    search_type: str = Field(..., description="Tipo de busca realizada")
    query: str = Field(..., description="Query utilizada")
    total_results: int = Field(..., description="Total de resultados encontrados")
    execution_time: float = Field(..., description="Tempo de execução em segundos")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da busca")
    
    # Dados específicos por plataforma
    lattes_profiles: Optional[List[LattesProfile]] = Field(None, description="Perfis do Lattes")
    orcid_profiles: Optional[List[ORCIDProfile]] = Field(None, description="Perfis do ORCID")
    
    # Estatísticas agregadas
    total_publications: int = Field(default=0, description="Total de publicações encontradas")
    total_projects: int = Field(default=0, description="Total de projetos encontrados")
    
    # Metadados
    csv_file: Optional[str] = Field(None, description="Nome do arquivo CSV gerado")
    data_sources: List[str] = Field(default=[], description="Fontes de dados utilizadas")

class AcademicSummary(BaseModel):
    """Resumo estatístico acadêmico"""
    researcher_name: str = Field(..., description="Nome do pesquisador")
    platforms_found: List[PlatformType] = Field(..., description="Plataformas onde foi encontrado")
    
    # Estatísticas gerais
    total_publications: int = Field(default=0, description="Total de publicações")
    total_projects: int = Field(default=0, description="Total de projetos")
    
    # Análise temporal
    publication_years: Dict[str, int] = Field(default={}, description="Publicações por ano")
    most_recent_publication: Optional[int] = Field(None, description="Ano da publicação mais recente")
    career_span: Optional[int] = Field(None, description="Duração da carreira (anos)")
    
    # Análise institucional
    institutions: List[str] = Field(default=[], description="Instituições associadas")
    research_areas: List[str] = Field(default=[], description="Áreas de pesquisa")
    
    # Comparação entre plataformas
    platform_comparison: Dict[str, Dict[str, Any]] = Field(default={}, description="Comparação entre plataformas")