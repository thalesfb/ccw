"""Script de debug para analisar estágios PRISMA no banco."""
import sqlite3
from pathlib import Path

db_path = Path("research/systematic_review.db")

if not db_path.exists():
    print(f"❌ Banco não encontrado: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("="*80)
print("DIAGNÓSTICO DOS ESTÁGIOS PRISMA")
print("="*80)

# Total de registros
cursor.execute("SELECT COUNT(*) FROM papers")
total = cursor.fetchone()[0]
print(f"\n📊 Total de registros: {total}")

# Distribuição por selection_stage
print("\n🔍 Distribuição por selection_stage:")
cursor.execute("""
    SELECT selection_stage, COUNT(*) as count
    FROM papers
    GROUP BY selection_stage
    ORDER BY count DESC
""")
for stage, count in cursor.fetchall():
    print(f"  {stage or 'NULL'}: {count}")

# Distribuição por status
print("\n📋 Distribuição por status:")
cursor.execute("""
    SELECT status, COUNT(*) as count
    FROM papers
    GROUP BY status
    ORDER BY count DESC
""")
for status, count in cursor.fetchall():
    print(f"  {status or 'NULL'}: {count}")

# Cruzamento selection_stage x status
print("\n🔀 Cruzamento selection_stage x status:")
cursor.execute("""
    SELECT 
        selection_stage,
        status,
        COUNT(*) as count
    FROM papers
    GROUP BY selection_stage, status
    ORDER BY selection_stage, status
""")
for stage, status, count in cursor.fetchall():
    print(f"  {stage or 'NULL'} / {status or 'NULL'}: {count}")

# Exclusion reasons
print("\n❌ Motivos de exclusão (top 10):")
cursor.execute("""
    SELECT 
        exclusion_reason,
        COUNT(*) as count
    FROM papers
    WHERE exclusion_reason IS NOT NULL
    GROUP BY exclusion_reason
    ORDER BY count DESC
    LIMIT 10
""")
for reason, count in cursor.fetchall():
    print(f"  {reason}: {count}")

# Amostra de registros
print("\n📝 Amostra de 5 registros:")
cursor.execute("""
    SELECT 
        id,
        title,
        selection_stage,
        status,
        exclusion_reason
    FROM papers
    LIMIT 5
""")
for row in cursor.fetchall():
    paper_id, title, stage, status, reason = row
    title_short = (title[:50] + '...') if title and len(title) > 50 else title
    print(f"\n  ID: {paper_id}")
    print(f"  Título: {title_short}")
    print(f"  Estágio: {stage or 'NULL'}")
    print(f"  Status: {status or 'NULL'}")
    print(f"  Exclusão: {reason or 'N/A'}")

conn.close()
print("\n" + "="*80)
