"""Private, domain-scoped views over canonical Knowledge Atlas notes."""

from .catalog import Catalog, DOMAINS, build_index

__all__ = ["Catalog", "DOMAINS", "build_index"]
