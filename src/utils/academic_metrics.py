"""
📊 UTILITÁRIOS DE CÁLCULO DE MÉTRICAS ACADÊMICAS
==============================================
Funções para cálculo de índices H, i10 e outras métricas
"""

from typing import List, Dict, Any, Optional, Tuple
import logging

def calculate_h_index(publications: List[Dict[str, Any]]) -> int:
    """
    Calcula o índice H baseado nas publicações e suas citações
    
    O índice H é o maior número h tal que o pesquisador tenha h publicações
    com pelo menos h citações cada.
    
    Args:
        publications: Lista de publicações com campo 'cited_by'
        
    Returns:
        int: Valor do índice H
    """
    if not publications:
        return 0
    
    # Extrair número de citações de cada publicação
    citations = []
    for pub in publications:
        cited_by = pub.get('cited_by', 0)
        # Garantir que é um número válido
        if isinstance(cited_by, (int, float)) and cited_by >= 0:
            citations.append(int(cited_by))
        else:
            citations.append(0)
    
    # Ordenar em ordem decrescente
    citations.sort(reverse=True)
    
    # Calcular índice H
    h_index = 0
    for i, citation_count in enumerate(citations, 1):
        if citation_count >= i:
            h_index = i
        else:
            break
    
    return h_index

def calculate_i10_index(publications: List[Dict[str, Any]]) -> int:
    """
    Calcula o índice i10 (número de publicações com pelo menos 10 citações)
    
    Args:
        publications: Lista de publicações com campo 'cited_by'
        
    Returns:
        int: Valor do índice i10
    """
    if not publications:
        return 0
    
    count = 0
    for pub in publications:
        cited_by = pub.get('cited_by', 0)
        if isinstance(cited_by, (int, float)) and cited_by >= 10:
            count += 1
    
    return count

def calculate_total_citations(publications: List[Dict[str, Any]]) -> int:
    """
    Calcula o total de citações de todas as publicações
    
    Args:
        publications: Lista de publicações com campo 'cited_by'
        
    Returns:
        int: Total de citações
    """
    if not publications:
        return 0
    
    total = 0
    for pub in publications:
        cited_by = pub.get('cited_by', 0)
        if isinstance(cited_by, (int, float)) and cited_by >= 0:
            total += int(cited_by)
    
    return total

def get_top_cited_publications(publications: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
    """
    Retorna as top N publicações mais citadas
    
    Args:
        publications: Lista de publicações
        top_n: Número de publicações para retornar
        
    Returns:
        List[Dict]: Lista das publicações mais citadas
    """
    if not publications:
        return []
    
    # Filtrar e ordenar por citações
    valid_pubs = []
    for pub in publications:
        cited_by = pub.get('cited_by', 0)
        if isinstance(cited_by, (int, float)) and cited_by >= 0:
            pub_copy = pub.copy()
            pub_copy['cited_by'] = int(cited_by)
            valid_pubs.append(pub_copy)
    
    # Ordenar por citações (decrescente)
    valid_pubs.sort(key=lambda x: x['cited_by'], reverse=True)
    
    return valid_pubs[:top_n]

def calculate_academic_metrics(publications: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calcula todas as métricas acadêmicas de uma vez
    
    Args:
        publications: Lista de publicações com campos necessários
        
    Returns:
        Dict: Dicionário com todas as métricas calculadas
    """
    try:
        h_index = calculate_h_index(publications)
        i10_index = calculate_i10_index(publications)
        total_citations = calculate_total_citations(publications)
        top_cited = get_top_cited_publications(publications, 5)
        
        # Análise temporal
        years = []
        for pub in publications:
            year = pub.get('year')
            if isinstance(year, (int, float)) and year > 1900:
                years.append(int(year))
        
        year_range = {}
        if years:
            year_range = {
                "min": min(years),
                "max": max(years),
                "span": max(years) - min(years) + 1 if years else 0
            }
        
        # Publicações por ano
        publications_by_year = {}
        for year in years:
            publications_by_year[str(year)] = publications_by_year.get(str(year), 0) + 1
        
        return {
            "h_index": h_index,
            "i10_index": i10_index,
            "total_citations": total_citations,
            "total_publications": len(publications),
            "top_cited": top_cited,
            "year_range": year_range,
            "publications_by_year": publications_by_year,
            "avg_citations": round(total_citations / len(publications), 2) if publications else 0
        }
        
    except Exception as e:
        logging.error(f"Erro ao calcular métricas acadêmicas: {str(e)}")
        return {
            "h_index": 0,
            "i10_index": 0,
            "total_citations": 0,
            "total_publications": len(publications),
            "top_cited": [],
            "year_range": {},
            "publications_by_year": {},
            "avg_citations": 0,
            "error": str(e)
        }

def format_metrics_summary(metrics: Dict[str, Any], author_name: str) -> str:
    """
    Formata um resumo das métricas para exibição
    
    Args:
        metrics: Dicionário com métricas calculadas
        author_name: Nome do autor
        
    Returns:
        str: Resumo formatado
    """
    summary = f"""
📊 MÉTRICAS ACADÊMICAS - {author_name.upper()}
===============================================

📈 ÍNDICES:
• Índice H: {metrics.get('h_index', 0)}
• Índice i10: {metrics.get('i10_index', 0)}

📚 PUBLICAÇÕES:
• Total: {metrics.get('total_publications', 0)}
• Citações: {metrics.get('total_citations', 0)}
• Média de citações: {metrics.get('avg_citations', 0)}

📅 PERÍODO:
• Primeiro trabalho: {metrics.get('year_range', {}).get('min', 'N/A')}
• Último trabalho: {metrics.get('year_range', {}).get('max', 'N/A')}
• Duração da carreira: {metrics.get('year_range', {}).get('span', 0)} anos

🏆 TOP 3 MAIS CITADAS:
"""
    
    top_cited = metrics.get('top_cited', [])[:3]
    for i, pub in enumerate(top_cited, 1):
        title = pub.get('title', 'Título não disponível')[:60]
        citations = pub.get('cited_by', 0)
        year = pub.get('year', 'N/A')
        summary += f"  {i}. {title}... ({year}) - {citations} citações\n"
    
    return summary