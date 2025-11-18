"""
Sistema de Cache SQLite para APIs de Pesquisa Acadêmica.

Este módulo implementa um cache persistente usando SQLite para armazenar
resultados de consultas às APIs de bases de dados acadêmicas, substituindo
o sistema anterior baseado em arquivos JSON.
"""

import sqlite3
import json
import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """Estrutura de entrada do cache."""
    query_hash: str
    api_source: str
    query_text: str
    response_data: str  # JSON serializado
    created_at: datetime
    expires_at: Optional[datetime]
    hit_count: int = 0
    last_accessed: Optional[datetime] = None


class SQLiteAPICache:
    """
    Cache SQLite para resultados de APIs de pesquisa acadêmica.
    
    Características:
    - Armazenamento persistente em SQLite
    - Expiração configurável por API
    - Compressão de dados grandes
    - Métricas de uso
    - Limpeza automática
    """
    
    def __init__(self, db_path: str = "research/cache/api_cache.sqlite"):
        """
        Inicializa o cache SQLite.
        
        Args:
            db_path: Caminho para o arquivo de banco SQLite
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configurações de expiração por API (em horas)
        self.expiration_config = {
            'semantic_scholar': 24 * 7,  # 7 dias
            'openalex': 24 * 7,          # 7 dias
            'crossref': 24 * 14,         # 14 dias (mais estável)
            'core': 24 * 3,              # 3 dias (menos estável)
        }
        
        self._init_database()
        logger.info(f"Cache SQLite inicializado: {self.db_path}")
    
    def _init_database(self):
        """Inicializa o esquema do banco de dados."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS api_cache (
                    query_hash TEXT PRIMARY KEY,
                    api_source TEXT NOT NULL,
                    query_text TEXT NOT NULL,
                    response_data TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    expires_at TIMESTAMP,
                    hit_count INTEGER DEFAULT 0,
                    last_accessed TIMESTAMP,
                    data_size INTEGER
                )
            """)
            
            # Criar índices separadamente
            conn.execute("CREATE INDEX IF NOT EXISTS idx_api_source ON api_cache(api_source)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON api_cache(created_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_expires_at ON api_cache(expires_at)")
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache_stats (
                    api_source TEXT PRIMARY KEY,
                    total_queries INTEGER DEFAULT 0,
                    cache_hits INTEGER DEFAULT 0,
                    cache_misses INTEGER DEFAULT 0,
                    total_size_bytes INTEGER DEFAULT 0,
                    last_cleanup TIMESTAMP
                )
            """)
            
            # Inicializar estatísticas se não existem
            for api in self.expiration_config.keys():
                conn.execute("""
                    INSERT OR IGNORE INTO cache_stats (api_source)
                    VALUES (?)
                """, (api,))
            
            conn.commit()
    
    def _generate_hash(self, query: str, api_source: str) -> str:
        """Gera hash único para query + API."""
        combined = f"{api_source}:{query}"
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def get(self, query: str, api_source: str) -> Optional[List[Dict[str, Any]]]:
        """
        Recupera dados do cache.
        
        Args:
            query: Texto da consulta
            api_source: Nome da API fonte
            
        Returns:
            Dados em cache ou None se não encontrado/expirado
        """
        query_hash = self._generate_hash(query, api_source)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Buscar entrada no cache
            cursor.execute("""
                SELECT * FROM api_cache 
                WHERE query_hash = ? AND api_source = ?
            """, (query_hash, api_source))
            
            row = cursor.fetchone()
            if not row:
                self._update_stats(conn, api_source, cache_miss=True)
                return None
            
            # Verificar expiração
            if row['expires_at']:
                expires_at = datetime.fromisoformat(row['expires_at'])
                if datetime.now() > expires_at:
                    logger.debug(f"Cache expirado para {api_source}:{query[:50]}")
                    # Remover entrada expirada
                    cursor.execute("DELETE FROM api_cache WHERE query_hash = ?", (query_hash,))
                    conn.commit()
                    self._update_stats(conn, api_source, cache_miss=True)
                    return None
            
            # Atualizar estatísticas de acesso
            cursor.execute("""
                UPDATE api_cache 
                SET hit_count = hit_count + 1, last_accessed = ?
                WHERE query_hash = ?
            """, (datetime.now().isoformat(), query_hash))
            
            self._update_stats(conn, api_source, cache_hit=True)
            conn.commit()
            
            # Deserializar dados
            try:
                data = json.loads(row['response_data'])
                logger.debug(f"Cache hit para {api_source}:{query[:50]}")
                return data
            except json.JSONDecodeError as e:
                logger.error(f"Erro ao deserializar cache: {e}")
                # Remover entrada corrompida
                cursor.execute("DELETE FROM api_cache WHERE query_hash = ?", (query_hash,))
                conn.commit()
                return None
    
    def set(self, query: str, api_source: str, data: List[Dict[str, Any]]) -> bool:
        """
        Armazena dados no cache.
        
        Args:
            query: Texto da consulta
            api_source: Nome da API fonte
            data: Dados para armazenar
            
        Returns:
            True se armazenado com sucesso
        """
        if not data:
            return False
            
        query_hash = self._generate_hash(query, api_source)
        
        try:
            # Serializar dados
            response_data = json.dumps(data, ensure_ascii=False)
            data_size = len(response_data.encode())
            
            # Calcular expiração
            expiration_hours = self.expiration_config.get(api_source, 24)
            expires_at = datetime.now() + timedelta(hours=expiration_hours)
            
            with sqlite3.connect(self.db_path) as conn:
                # Inserir ou atualizar entrada
                conn.execute("""
                    INSERT OR REPLACE INTO api_cache
                    (query_hash, api_source, query_text, response_data, 
                     created_at, expires_at, data_size)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    query_hash, api_source, query, response_data,
                    datetime.now().isoformat(), expires_at.isoformat(), data_size
                ))
                
                # Atualizar estatísticas
                conn.execute("""
                    UPDATE cache_stats 
                    SET total_queries = total_queries + 1,
                        total_size_bytes = (
                            SELECT COALESCE(SUM(data_size), 0) 
                            FROM api_cache 
                            WHERE api_source = ?
                        )
                    WHERE api_source = ?
                """, (api_source, api_source))
                
                conn.commit()
                
            logger.debug(f"Dados armazenados no cache: {api_source}:{query[:50]} ({data_size} bytes)")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao armazenar no cache: {e}")
            return False
    
    def _update_stats(self, conn: sqlite3.Connection, api_source: str, 
                     cache_hit: bool = False, cache_miss: bool = False):
        """Atualiza estatísticas de uso do cache."""
        if cache_hit:
            conn.execute("""
                UPDATE cache_stats 
                SET cache_hits = cache_hits + 1
                WHERE api_source = ?
            """, (api_source,))
        elif cache_miss:
            conn.execute("""
                UPDATE cache_stats 
                SET cache_misses = cache_misses + 1
                WHERE api_source = ?
            """, (api_source,))
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do cache.
        
        Returns:
            Dicionário com estatísticas por API e totais
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Estatísticas por API
            cursor.execute("SELECT * FROM cache_stats")
            api_stats = {row['api_source']: dict(row) for row in cursor.fetchall()}
            
            # Estatísticas gerais
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_entries,
                    SUM(data_size) as total_size,
                    SUM(hit_count) as total_hits,
                    COUNT(CASE WHEN expires_at < ? THEN 1 END) as expired_entries
                FROM api_cache
            """, (datetime.now().isoformat(),))
            
            general_stats = dict(cursor.fetchone())
            
            # Taxa de hit por API
            for api, stats in api_stats.items():
                total = stats['cache_hits'] + stats['cache_misses']
                stats['hit_rate'] = stats['cache_hits'] / total if total > 0 else 0.0
            
            return {
                'apis': api_stats,
                'general': general_stats,
                'db_size_mb': self.db_path.stat().st_size / (1024 * 1024) if self.db_path.exists() else 0
            }
    
    def cleanup_expired(self) -> int:
        """
        Remove entradas expiradas do cache.
        
        Returns:
            Número de entradas removidas
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Contar entradas expiradas
            cursor.execute("""
                SELECT COUNT(*) FROM api_cache 
                WHERE expires_at < ?
            """, (datetime.now().isoformat(),))
            
            count = cursor.fetchone()[0]
            
            # Remover entradas expiradas
            cursor.execute("""
                DELETE FROM api_cache 
                WHERE expires_at < ?
            """, (datetime.now().isoformat(),))
            
            # Atualizar estatísticas de tamanho
            for api in self.expiration_config.keys():
                cursor.execute("""
                    UPDATE cache_stats 
                    SET total_size_bytes = (
                        SELECT COALESCE(SUM(data_size), 0) 
                        FROM api_cache 
                        WHERE api_source = ?
                    ),
                    last_cleanup = ?
                    WHERE api_source = ?
                """, (api, datetime.now().isoformat(), api))
            
            conn.commit()
            
        if count > 0:
            logger.info(f"Removidas {count} entradas expiradas do cache")
        
        return count
    
    def clear_api_cache(self, api_source: str) -> int:
        """
        Remove todas as entradas de uma API específica.
        
        Args:
            api_source: Nome da API
            
        Returns:
            Número de entradas removidas
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM api_cache WHERE api_source = ?", (api_source,))
            count = cursor.fetchone()[0]
            
            cursor.execute("DELETE FROM api_cache WHERE api_source = ?", (api_source,))
            
            # Resetar estatísticas
            cursor.execute("""
                UPDATE cache_stats 
                SET cache_hits = 0, cache_misses = 0, total_size_bytes = 0
                WHERE api_source = ?
            """, (api_source,))
            
            conn.commit()
            
        logger.info(f"Cache limpo para {api_source}: {count} entradas removidas")
        return count
    
    def clear_all(self) -> int:
        """
        Remove todas as entradas do cache.
        
        Returns:
            Número de entradas removidas
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM api_cache")
            count = cursor.fetchone()[0]
            
            cursor.execute("DELETE FROM api_cache")
            cursor.execute("""
                UPDATE cache_stats 
                SET cache_hits = 0, cache_misses = 0, total_size_bytes = 0
            """)
            
            conn.commit()
            
        logger.info(f"Cache completamente limpo: {count} entradas removidas")
        return count
    
    def vacuum(self):
        """Otimiza o banco de dados SQLite."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("VACUUM")
            conn.commit()
        
        logger.info("Banco de dados otimizado (VACUUM)")


# Função de conveniência para migração do cache JSON
def migrate_json_cache_to_sqlite(json_cache_dir: str, sqlite_cache: SQLiteAPICache) -> int:
    """
    Migra cache de arquivos JSON para SQLite.
    
    Args:
        json_cache_dir: Diretório com arquivos JSON do cache antigo
        sqlite_cache: Instância do cache SQLite
        
    Returns:
        Número de arquivos migrados
    """
    json_dir = Path(json_cache_dir)
    if not json_dir.exists():
        logger.warning(f"Diretório de cache JSON não encontrado: {json_dir}")
        return 0
    
    migrated = 0
    
    # Mapear diretórios para nomes de API
    api_mapping = {
        'semanticscholar': 'semantic_scholar',
        'openalex': 'openalex', 
        'crossref': 'crossref',
        'robustcore': 'core'
    }
    
    for api_dir in json_dir.iterdir():
        if not api_dir.is_dir() or api_dir.name not in api_mapping:
            continue
            
        api_name = api_mapping[api_dir.name]
        logger.info(f"Migrando cache de {api_name}...")
        
        for json_file in api_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Tentar extrair query do hash (limitação do sistema antigo)
                query_hash = json_file.stem
                dummy_query = f"migrated_{query_hash}"
                
                # Armazenar no SQLite
                if sqlite_cache.set(dummy_query, api_name, data):
                    migrated += 1
                    
            except Exception as e:
                logger.error(f"Erro ao migrar {json_file}: {e}")
    
    logger.info(f"Migração concluída: {migrated} arquivos migrados")
    return migrated


if __name__ == "__main__":
    # Teste básico do sistema
    cache = SQLiteAPICache("research/cache/api_cache.sqlite")
    
    # Teste de armazenamento e recuperação
    test_data = [
        {"title": "Test Paper 1", "authors": ["Author 1"], "year": 2023},
        {"title": "Test Paper 2", "authors": ["Author 2"], "year": 2024}
    ]
    
    cache.set("test query", "semantic_scholar", test_data)
    retrieved = cache.get("test query", "semantic_scholar")
    
    print("Teste básico:", "✅ PASSOU" if retrieved == test_data else "❌ FALHOU")
    print("Estatísticas:", cache.get_stats())