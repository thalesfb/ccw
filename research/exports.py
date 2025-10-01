"""
Export module for generating reports and spreadsheets.
"""
import os
import logging
from datetime import datetime
import pandas as pd


class ExportManager:
    """Manager for exporting systematic review results."""
    
    def __init__(self, export_dir: str = "research/exports"):
        """
        Initialize export manager.
        
        Args:
            export_dir: Directory for export files
        """
        self.export_dir = export_dir
        self.logger = logging.getLogger("export")
        os.makedirs(export_dir, exist_ok=True)
    
    def export_to_excel(
        self,
        df: pd.DataFrame,
        filename: str = None
    ) -> str:
        """
        Export DataFrame to Excel file.
        
        Args:
            df: DataFrame to export
            filename: Optional filename (auto-generated if None)
            
        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"systematic_review_{timestamp}.xlsx"
        
        filepath = os.path.join(self.export_dir, filename)
        
        # Create Excel writer with multiple sheets
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name='Papers', index=False)
            
            # Summary sheet
            summary_data = {
                'Metric': [
                    'Total Papers',
                    'Unique Databases',
                    'Year Range',
                    'Open Access Papers',
                    'Export Date'
                ],
                'Value': [
                    len(df),
                    df['database'].nunique() if 'database' in df.columns else 0,
                    f"{df['year'].min()}-{df['year'].max()}" if 'year' in df.columns else 'N/A',
                    df['is_open_access'].sum() if 'is_open_access' in df.columns else 0,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        self.logger.info(f"Exported {len(df)} papers to {filepath}")
        return filepath
    
    def export_to_csv(
        self,
        df: pd.DataFrame,
        filename: str = None
    ) -> str:
        """
        Export DataFrame to CSV file.
        
        Args:
            df: DataFrame to export
            filename: Optional filename (auto-generated if None)
            
        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"systematic_review_{timestamp}.csv"
        
        filepath = os.path.join(self.export_dir, filename)
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        self.logger.info(f"Exported {len(df)} papers to {filepath}")
        return filepath
    
    def generate_summary_report(self, df: pd.DataFrame) -> str:
        """
        Generate a summary report of the systematic review.
        
        Args:
            df: DataFrame with papers
            
        Returns:
            Path to report file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_report_{timestamp}.txt"
        filepath = os.path.join(self.export_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("SYSTEMATIC REVIEW SUMMARY REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Basic statistics
            f.write("BASIC STATISTICS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Papers: {len(df)}\n")
            
            if 'database' in df.columns:
                f.write(f"\nPapers by Database:\n")
                for db, count in df['database'].value_counts().items():
                    f.write(f"  - {db}: {count}\n")
            
            if 'year' in df.columns and not df['year'].isnull().all():
                f.write(f"\nYear Range: {df['year'].min():.0f} - {df['year'].max():.0f}\n")
                f.write(f"\nPapers by Year:\n")
                for year, count in df['year'].value_counts().sort_index().items():
                    f.write(f"  - {int(year)}: {count}\n")
            
            if 'is_open_access' in df.columns:
                oa_count = df['is_open_access'].sum()
                f.write(f"\nOpen Access Papers: {oa_count} ({oa_count/len(df)*100:.1f}%)\n")
            
            f.write("\n" + "=" * 80 + "\n")
        
        self.logger.info(f"Generated summary report at {filepath}")
        return filepath
