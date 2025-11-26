
import json
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

import requests
from unittest.mock import patch, MagicMock

"""Tests for DeepReviewAnalyzer.

Import path adjusted to be robust whether pytest is invoked from the
`research/` directory (where `pytest.ini` sets `pythonpath=src`) or from
the repository root (where `research/src` is not automatically on
PYTHONPATH). Using the explicit `research.src` package path aligns with
other test modules (e.g. `test_prisma_stages.py`).
"""

try:
    from research.src.analysis.deep_review_analysis import DeepReviewAnalyzer
except ModuleNotFoundError:
    # Fallback for running from research/ directory
    from src.analysis.deep_review_analysis import DeepReviewAnalyzer

class TestDeepReviewAnalyzer(unittest.TestCase):
    # Determine correct module path for mocks
    try:
        from research.src.analysis import deep_review_analysis
        MODULE_PATH = 'research.src.analysis.deep_review_analysis'
    except ModuleNotFoundError:
        from src.analysis import deep_review_analysis
        MODULE_PATH = 'src.analysis.deep_review_analysis'

    def setUp(self):
        """Configura um banco de dados em memória para os testes."""
        temp_db = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
        temp_db.close()
        self.db_path = temp_db.name
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Criar a tabela 'papers'
        self.cursor.execute("""
            CREATE TABLE papers (
                id INTEGER PRIMARY KEY,
                doi TEXT,
                title TEXT,
                selection_stage TEXT,
                is_duplicate BOOLEAN,
                open_access_pdf TEXT,
                relevance_score REAL,
                citation_count INTEGER
            )
        """)

        # Inserir dados de teste
        self.papers_data = [
            (1, '10.1000/included', 'Paper com PDF', 'included', 0, 'http://example.com/pdf1', 8.5, 10),
            (2, '10.1000/excluded', 'Paper Excluído', 'screening_excluded', 0, None, 4.0, 5),
            (3, '10.1000/duplicate', 'Paper Duplicado', 'included', 1, 'http://example.com/pdf2', 7.0, 12),
            (4, '10.1000/no_pdf', 'Paper sem PDF', 'included', None, None, 9.0, 20)
        ]
        self.cursor.executemany(
            "INSERT INTO papers VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            self.papers_data
        )
        self.conn.commit()

        # Configurar o analisador
        self.analyzer = DeepReviewAnalyzer(db_path=self.db_path)
        self.output_dir = Path("./test_output")
        self.analyzer.output_dir = self.output_dir
        self.output_dir.mkdir(exist_ok=True)

    def tearDown(self):
        """Fecha a conexão com o banco e limpa os arquivos de saída."""
        self.conn.close()
        # Force garbage collection to release any SQLite connections
        import gc
        gc.collect()
        # Limpar todos os arquivos gerados no diretório de teste
        for f in self.output_dir.glob('*'):
            if f.is_file():
                f.unlink()
        if self.output_dir.exists():
            self.output_dir.rmdir()
        # On Windows, retry removal with a small delay if needed
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except PermissionError:
                import time
                time.sleep(0.2)
                try:
                    os.remove(self.db_path)
                except PermissionError:
                    # If still locked, log and skip
                    import warnings
                    warnings.warn(f"Could not remove {self.db_path} - file still locked")

    def test_load_included_papers_excludes_duplicates(self):
        """Verifica se 'load_included_papers' carrega apenas papers válidos."""
        loaded_papers = self.analyzer.load_included_papers()
        self.assertEqual(len(loaded_papers), 2)
        loaded_dois = {p['doi'] for p in loaded_papers}
        self.assertIn('10.1000/included', loaded_dois)
        self.assertIn('10.1000/no_pdf', loaded_dois)
        self.assertNotIn('10.1000/duplicate', loaded_dois)

    @patch('PyPDF2.PdfReader')
    @patch(f'{MODULE_PATH}.requests.get')
    def test_fetch_full_text_successful_extraction(self, mock_requests_get, mock_pdf_reader):
        """
        Testa a extração de texto bem-sucedida, simulando o download de um PDF.
        """
        # Configurar o mock da resposta HTTP
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'fake pdf content'
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response

        # Configurar o mock do leitor de PDF
        mock_pdf_instance = MagicMock()
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Este é o texto extraído."
        mock_pdf_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_pdf_instance

        # Executar a função
        self.analyzer.load_included_papers()
        self.analyzer.fetch_full_text()

        # Verificar se o texto foi adicionado ao paper
        paper_com_pdf = next(p for p in self.analyzer.papers if p['doi'] == '10.1000/included')
        self.assertEqual(paper_com_pdf['full_text'], "Este é o texto extraído.")

        # Verificar se o paper sem link de PDF não tem texto
        paper_sem_pdf = next(p for p in self.analyzer.papers if p['doi'] == '10.1000/no_pdf')
        self.assertIsNone(paper_sem_pdf['full_text'])
        
        # Verificar o cache
        cache_file = self.output_dir / "full_texts_cache.json"
        self.assertTrue(cache_file.exists())
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
            self.assertIn('10.1000/included', cache_data)
            self.assertEqual(cache_data['10.1000/included'], "Este é o texto extraído.")

    @patch(f'{MODULE_PATH}.requests.get')
    def test_fetch_full_text_download_fails(self, mock_requests_get):
        """Testa o comportamento quando o download do PDF falha."""
        # Configurar o mock para simular uma falha de requisição
        mock_requests_get.side_effect = requests.exceptions.RequestException("Falha na conexão")

        self.analyzer.load_included_papers()
        self.analyzer.fetch_full_text()

        paper_com_pdf = next(p for p in self.analyzer.papers if p['doi'] == '10.1000/included')
        self.assertIsNone(paper_com_pdf['full_text'])

    def test_run_full_analysis_generates_correct_report(self):
        """
        Testa o fluxo completo e verifica se o relatório reflete o resultado da extração.
        """
        # Para este teste, vamos simular que nenhum texto foi extraído
        with patch(f'{self.MODULE_PATH}.DeepReviewAnalyzer.fetch_full_text', return_value=[]):
            results = self.analyzer.run_full_analysis()

            self.assertEqual(results['total_papers'], 2)
            self.assertEqual(results['successful_extractions'], 0)

            report_file = Path(results['report_file'])
            self.assertTrue(report_file.exists())

            with open(report_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Verificações mais flexíveis para evitar falhas por pequenas variações de formatação
                import re
                # Procurar a contagem de extrações bem-sucedidas como '0 (0.0%)'
                self.assertIsNotNone(
                    re.search(r"extra(ç|c)\w*\s+bem-?sucedidas?.*0\s*\(0\.0%\)", content, flags=re.IGNORECASE | re.DOTALL),
                    "Relatório não contém a contagem de extrações bem-sucedidas esperada"
                )
                # Procurar indicador de falha (permitindo variações)
                self.assertTrue(
                    re.search(r"Falha|Failure|❌", content, flags=re.IGNORECASE) is not None,
                    "Relatório não indica falha na extração"
                )


if __name__ == '__main__':
    unittest.main()
