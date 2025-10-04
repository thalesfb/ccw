"""Script para análise visual das imagens PRISMA geradas."""
from pathlib import Path

viz_dir = Path("research/exports/visualizations")

print("="*80)
print("ANÁLISE DAS VISUALIZAÇÕES PRISMA")
print("="*80)

images = list(viz_dir.glob("*.png"))

for img in sorted(images):
    size = img.stat().st_size / 1024  # KB
    print(f"\n📊 {img.name}")
    print(f"   Tamanho: {size:.1f} KB")
    print(f"   Caminho: {img}")

print("\n" + "="*80)
print("RESUMO DOS NÚMEROS ESPERADOS:")
print("="*80)
print("""
FUNIL DE SELEÇÃO:
- Identificação: 11.966 papers
- Triagem: 11.966 papers (todos passaram)
- Elegibilidade: 0 papers (nenhum passou sem ser excluído)
- Incluídos: 41 papers

FLUXO PRISMA:
- Identificados: 11.966
- Sem duplicatas: 11.966
- Selecionados para triagem: 11.966
- Excluídos na triagem: 0
- Avaliados para elegibilidade: 0 (os que passaram elegibilidade sem exclusão)
- Excluídos na elegibilidade: 11.925
- Incluídos: 41

NOTA: O banco atual tem apenas dois estágios finais:
- eligibility/excluded: 11.925 (baixo score de relevância)
- included/included: 41

Isso significa que todos os papers foram processados, mas a maioria
foi excluída na fase de elegibilidade por não atingir o score mínimo.
""")

print("\n" + "="*80)
print("Para visualizar as imagens, abra:")
print(f"  file:///{viz_dir.absolute()}/selection_funnel.png")
print(f"  file:///{viz_dir.absolute()}/prisma_flow.png")
print("="*80)
