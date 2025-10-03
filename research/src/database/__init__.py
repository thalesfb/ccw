"""Database module for systematic review."""

from .manager import DatabaseManager
from .schema import PaperRecord

__all__ = ["DatabaseManager", "PaperRecord"]
