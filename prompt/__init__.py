# prompt/__init__.py

from .ocm import OCM_KIND_CLUSTER_ACCESS
from .ocm import OCM_BASIC_KNOWLEDGE

__all__ = [name for name in globals() if not name.startswith("_")]
