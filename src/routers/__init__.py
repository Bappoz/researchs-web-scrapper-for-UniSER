"""
Módulo API separado para endpoints do Lattes e ORCID
"""

try:
    from .lattes_api import lattes_router
    from .orcid_api import orcid_router
    __all__ = ['lattes_router', 'orcid_router']
except ImportError:
    # Routers não disponíveis
    pass