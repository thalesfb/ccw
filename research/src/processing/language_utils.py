"""
Utilitários para detecção e processamento de idiomas.
"""

import logging
from typing import Optional, List, Union
import pandas as pd

logger = logging.getLogger(__name__)

try:
    from langdetect import detect, DetectorFactory
    from langdetect.lang_detect_exception import LangDetectException
    
    # Set seed for consistent results
    DetectorFactory.seed = 0
    LANGDETECT_AVAILABLE = True
except ImportError:
    logger.warning("langdetect not available. Install with: pip install langdetect")
    LANGDETECT_AVAILABLE = False


def detect_language(text: str) -> Optional[str]:
    """
    Detecta o idioma de um texto.
    
    Args:
        text: Texto para detectar idioma
        
    Returns:
        Código do idioma (ISO 639-1) ou None se não conseguir detectar
    """
    if not LANGDETECT_AVAILABLE or not text or len(text.strip()) < 10:
        return None
    
    try:
        # Remove caracteres especiais que podem atrapalhar detecção
        clean_text = text.strip()
        if len(clean_text) < 10:
            return None
            
        language = detect(clean_text)
        return language
    except (LangDetectException, Exception) as e:
        logger.debug(f"Could not detect language for text: {str(e)}")
        return None


def detect_language_from_fields(
    title: Optional[str] = None,
    abstract: Optional[str] = None,
    keywords: Optional[str] = None
) -> Optional[str]:
    """
    Detecta idioma usando múltiplos campos de texto.
    
    Args:
        title: Título do paper
        abstract: Resumo do paper
        keywords: Palavras-chave
        
    Returns:
        Código do idioma detectado ou None
    """
    # Tentar campos em ordem de prioridade
    texts_to_try = []
    
    if abstract and len(abstract.strip()) > 50:
        texts_to_try.append(abstract)
    
    if title and len(title.strip()) > 20:
        texts_to_try.append(title)
        
    if keywords and len(keywords.strip()) > 10:
        texts_to_try.append(keywords)
    
    # Combinar textos se forem curtos
    if not texts_to_try:
        combined = " ".join(filter(None, [title, abstract, keywords]))
        if combined.strip():
            texts_to_try.append(combined)
    
    for text in texts_to_try:
        lang = detect_language(text)
        if lang:
            return lang
    
    return None


def is_supported_language(language: str, supported_langs: List[str] = None) -> bool:
    """
    Verifica se o idioma é suportado.
    
    Args:
        language: Código do idioma
        supported_langs: Lista de idiomas suportados (default: ['en', 'pt'])
        
    Returns:
        True se o idioma é suportado
    """
    if supported_langs is None:
        supported_langs = ['en', 'pt']
    
    return language in supported_langs


def enhance_language_detection(df: pd.DataFrame) -> pd.DataFrame:
    """
    Melhora a detecção de idiomas em um DataFrame.
    
    Args:
        df: DataFrame com papers
        
    Returns:
        DataFrame com coluna 'language' preenchida
    """
    if not LANGDETECT_AVAILABLE:
        logger.warning("langdetect not available - skipping language detection")
        return df
    
    df = df.copy()
    
    # Criar coluna language se não existir
    if 'language' not in df.columns:
        df['language'] = None
    
    # Detectar idioma para papers sem language definido
    missing_language = df['language'].isna() | (df['language'] == '') | (df['language'] == 'unknown')
    papers_to_detect = df[missing_language]
    
    if len(papers_to_detect) == 0:
        logger.info("All papers already have language information")
        return df
    
    logger.info(f"Detecting language for {len(papers_to_detect)} papers")
    
    detected_languages = []
    for idx, row in papers_to_detect.iterrows():
        lang = detect_language_from_fields(
            title=row.get('title'),
            abstract=row.get('abstract'),
            keywords=row.get('keywords')
        )
        detected_languages.append(lang)
    
    # Atualizar DataFrame
    df.loc[missing_language, 'language'] = detected_languages
    
    # Estatísticas
    detected_count = sum(1 for lang in detected_languages if lang is not None)
    logger.info(f"Successfully detected language for {detected_count}/{len(papers_to_detect)} papers")
    
    if detected_count > 0:
        lang_counts = pd.Series(detected_languages).value_counts()
        logger.info(f"Detected languages: {dict(lang_counts)}")
    
    return df


def add_language_criteria(row: pd.Series, supported_langs: List[str] = None) -> List[str]:
    """
    Adiciona critérios de idioma baseado na detecção.
    
    Args:
        row: Linha do DataFrame
        supported_langs: Idiomas suportados
        
    Returns:
        Lista de critérios atendidos
    """
    if supported_langs is None:
        supported_langs = ['en', 'pt']
    
    criteria = []
    language = row.get('language')
    
    if language:
        if language in supported_langs:
            criteria.append(f'language_{language}')
        
        # Critério geral de idioma suportado
        if is_supported_language(language, supported_langs):
            criteria.append('supported_language')
    
    return criteria


# Mapeamento de códigos de idioma para nomes
LANGUAGE_NAMES = {
    'en': 'English',
    'pt': 'Portuguese', 
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ru': 'Russian',
    'ar': 'Arabic'
}


def get_language_name(code: str) -> str:
    """
    Retorna o nome do idioma a partir do código.
    
    Args:
        code: Código do idioma
        
    Returns:
        Nome do idioma ou o próprio código se não encontrado
    """
    return LANGUAGE_NAMES.get(code, code)