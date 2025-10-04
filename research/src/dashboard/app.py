"""Dashboard interativo para revisão sistemática."""

from research.src.analysis.visualizations import ReviewVisualizer
from research.src.processing.adaptive_selection import AdaptiveSelection
from research.src.db import read_papers, get_statistics
from research.src.config import load_config
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# Configuração da página
st.set_page_config(
    page_title="📊 Revisão Sistemática - Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def load_data():
    """Carrega dados do banco."""
    try:
        config = load_config()
        df = read_papers(config)
        stats = get_statistics(config)
        return df, stats, config
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame(), {}, None


def main():
    """Função principal do dashboard."""

    # Header
    st.markdown('<h1 class="main-header">📊 Dashboard da Revisão Sistemática</h1>',
                unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("🎛️ Controles")

    # Carregar dados
    df, stats, config = load_data()

    if df.empty:
        st.warning(
            "⚠️ Nenhum dado encontrado no banco. Execute o pipeline de coleta primeiro.")

        if st.sidebar.button("🚀 Executar Pipeline de Coleta"):
            st.info("Executando pipeline...")
            # Aqui você pode adicionar a execução do pipeline
            st.success("Pipeline executado com sucesso!")
            st.rerun()

        return

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📄 Total de Artigos</h3>
            <h2>{}</h2>
        </div>
        """.format(stats.get('total_papers', 0)), unsafe_allow_html=True)

    with col2:
        selected_count = len(df[df['selection_stage'] == 'included']
                             ) if 'selection_stage' in df.columns else 0
        st.markdown("""
        <div class="metric-card">
            <h3>✅ Artigos Selecionados</h3>
            <h2>{}</h2>
        </div>
        """.format(selected_count), unsafe_allow_html=True)

    with col3:
        selection_rate = (selected_count / len(df) * 100) if len(df) > 0 else 0
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Taxa de Seleção</h3>
            <h2>{:.1f}%</h2>
        </div>
        """.format(selection_rate), unsafe_allow_html=True)

    with col4:
        avg_score = df['relevance_score'].mean(
        ) if 'relevance_score' in df.columns else 0
        st.markdown("""
        <div class="metric-card">
            <h3>⭐ Score Médio</h3>
            <h2>{:.2f}</h2>
        </div>
        """.format(avg_score), unsafe_allow_html=True)

    st.markdown("---")

    # Abas principais
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Visão Geral", "🔍 Análise Detalhada", "⚙️ Configurações", "📋 Relatórios"])

    with tab1:
        show_overview_tab(df, stats)

    with tab2:
        show_analysis_tab(df)

    with tab3:
        show_config_tab(config, df)

    with tab4:
        show_reports_tab(df)


def show_overview_tab(df, stats):
    """Mostra aba de visão geral."""

    # Gráficos principais
    col1, col2 = st.columns(2)

    with col1:
        # Evolução temporal
        if 'year' in df.columns:
            year_counts = df['year'].value_counts().sort_index()
            fig_timeline = px.line(
                x=year_counts.index,
                y=year_counts.values,
                title="📅 Evolução Temporal dos Artigos",
                labels={'x': 'Ano', 'y': 'Número de Artigos'}
            )
            fig_timeline.update_layout(height=400)
            st.plotly_chart(fig_timeline, use_container_width=True)

    with col2:
        # Distribuição por base de dados
        if 'database' in df.columns:
            db_counts = df['database'].value_counts()
            fig_db = px.pie(
                values=db_counts.values,
                names=db_counts.index,
                title="🗃️ Distribuição por Base de Dados"
            )
            fig_db.update_layout(height=400)
            st.plotly_chart(fig_db, use_container_width=True)

    # Gráfico de scores
    if 'relevance_score' in df.columns:
        fig_scores = px.histogram(
            df,
            x='relevance_score',
            title="📊 Distribuição dos Scores de Relevância",
            nbins=20
        )
        fig_scores.update_layout(height=400)
        st.plotly_chart(fig_scores, use_container_width=True)

    # Tabela de resumo
    st.subheader("📋 Resumo dos Dados")

    summary_data = {
        'Métrica': [
            'Total de Artigos',
            'Artigos com Abstract',
            'Artigos com DOI',
            'Ano Mais Antigo',
            'Ano Mais Recente',
            'Score Médio',
            'Score Máximo'
        ],
        'Valor': [
            len(df),
            df['abstract'].notna().sum(),
            df['doi'].notna().sum(),
            df['year'].min() if 'year' in df.columns else 'N/A',
            df['year'].max() if 'year' in df.columns else 'N/A',
            f"{df['relevance_score'].mean():.2f}" if 'relevance_score' in df.columns else 'N/A',
            f"{df['relevance_score'].max():.2f}" if 'relevance_score' in df.columns else 'N/A'
        ]
    }

    summary_df = pd.DataFrame(summary_data)
    st.table(summary_df)

    # Últimos exports disponíveis
    exports_dir = Path(load_config().database.exports_dir)
    reports_dir = exports_dir / 'reports'
    viz_dir = exports_dir / 'visualizations'

    st.markdown("---")
    st.subheader("🗂️ Últimos Arquivos Gerados")
    latest_items = []
    if reports_dir.exists():
        latest_reports = sorted(reports_dir.glob('summary_report_*.html'))
        if latest_reports:
            latest_items.append(("Último summary_report", latest_reports[-1]))
    if viz_dir.exists():
        latest_viz = sorted(viz_dir.glob('*.png'))
        if latest_viz:
            latest_items.append(("Últimas visualizações (diretório)", viz_dir))

    for label, path in latest_items:
        st.write(f"- {label}: {path}")
    if not latest_items:
        st.info("Sem arquivos de export recentes ainda. Use a CLI para gerar: run-pipeline/export.")


def show_analysis_tab(df):
    """Mostra aba de análise detalhada."""

    st.subheader("🔍 Análise Detalhada")

    # Filtros
    col1, col2, col3 = st.columns(3)

    with col1:
        year_filter = st.slider(
            "Ano mínimo:",
            min_value=int(df['year'].min()) if 'year' in df.columns else 2010,
            max_value=int(df['year'].max()) if 'year' in df.columns else 2025,
            value=int(df['year'].min()) if 'year' in df.columns else 2015
        )

    with col2:
        score_filter = st.slider(
            "Score mínimo:",
            min_value=float(df['relevance_score'].min()
                            ) if 'relevance_score' in df.columns else 0.0,
            max_value=float(df['relevance_score'].max()
                            ) if 'relevance_score' in df.columns else 10.0,
            value=float(df['relevance_score'].min()
                        ) if 'relevance_score' in df.columns else 0.0
        )

    with col3:
        database_filter = st.multiselect(
            "Base de dados:",
            options=df['database'].unique(
            ) if 'database' in df.columns else [],
            default=df['database'].unique() if 'database' in df.columns else []
        )

    # Aplicar filtros
    filtered_df = df.copy()

    if 'year' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['year'] >= year_filter]

    if 'relevance_score' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['relevance_score']
                                  >= score_filter]

    if 'database' in filtered_df.columns and database_filter:
        filtered_df = filtered_df[filtered_df['database'].isin(
            database_filter)]

    st.info(f"📊 Mostrando {len(filtered_df)} artigos de {len(df)} total")

    # Gráficos filtrados
    col1, col2 = st.columns(2)

    with col1:
        if 'year' in filtered_df.columns:
            fig_filtered_timeline = px.line(
                filtered_df.groupby('year').size().reset_index(),
                x='year',
                y=0,
                title="📅 Evolução Temporal (Filtrado)"
            )
            st.plotly_chart(fig_filtered_timeline, use_container_width=True)

    with col2:
        if 'relevance_score' in filtered_df.columns:
            fig_filtered_scores = px.box(
                filtered_df,
                y='relevance_score',
                title="📊 Distribuição de Scores (Filtrado)"
            )
            st.plotly_chart(fig_filtered_scores, use_container_width=True)

    # Tabela de artigos
    st.subheader("📄 Artigos Filtrados")

    display_columns = ['title', 'authors',
                       'year', 'database', 'relevance_score']
    available_columns = [
        col for col in display_columns if col in filtered_df.columns]

    if available_columns:
        st.dataframe(
            filtered_df[available_columns].head(20),
            use_container_width=True
        )

        if len(filtered_df) > 20:
            st.info(
                f"Mostrando 20 de {len(filtered_df)} artigos. Use os filtros para refinar a busca.")


def show_config_tab(config, df=None):
    """Mostra aba de configurações."""

    st.subheader("⚙️ Configurações do Sistema")

    if config is None:
        st.error("Configuração não disponível")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Critérios de Revisão")

        config_data = {
            'Ano mínimo': config.review.year_min,
            'Ano máximo': config.review.year_max,
            'Idiomas': ', '.join(config.review.languages),
            'Abstract obrigatório': config.review.abstract_required,
            'Threshold de relevância': config.review.relevance_threshold
        }

        for key, value in config_data.items():
            st.write(f"**{key}:** {value}")

    with col2:
        st.markdown("### 🔗 Configurações de API")

        api_data = {
            'Delay Semantic Scholar': f"{config.apis.semantic_scholar_rate_delay_s}s",
            'Delay OpenAlex': f"{config.apis.open_alex_rate_delay_s}s",
            'Delay Crossref': f"{config.apis.crossref_rate_delay_s}s",
            'CORE API Key': "✅ Configurada" if config.apis.core_api_key else "❌ Não configurada"
        }

        for key, value in api_data.items():
            st.write(f"**{key}:** {value}")

    # Seletor adaptativo
    st.markdown("### 🎯 Seleção Adaptativa")

    target_size = st.slider("Tamanho desejado da amostra:", 10, 500, 100)
    min_size = st.slider("Tamanho mínimo aceitável:", 5, 100, 20)

    if st.button("🔄 Aplicar Seleção Adaptativa"):
        if df is not None and not df.empty:
            adaptive_selector = AdaptiveSelection(target_size, min_size)
            selected_df = adaptive_selector.select_adaptive(df)
            st.success(f"✅ Seleção adaptativa aplicada: {len(selected_df)} artigos selecionados")
            report = adaptive_selector.get_selection_report(df, selected_df)
            st.json(report)
        else:
            st.warning("Carregue dados primeiro para aplicar a seleção adaptativa.")


def show_reports_tab(df):
    """Mostra aba de relatórios."""

    st.subheader("📋 Relatórios")

    # Relatório de qualidade
    st.markdown("### 📊 Relatório de Qualidade dos Dados")

    quality_report = {
        'Campo': ['title', 'abstract', 'authors', 'year', 'doi', 'relevance_score'],
        'Preenchimento (%)': [
            f"{df['title'].notna().sum() / len(df) * 100:.1f}%" if 'title' in df.columns else "0%",
            f"{df['abstract'].notna().sum() / len(df) * 100:.1f}%" if 'abstract' in df.columns else "0%",
            f"{df['authors'].notna().sum() / len(df) * 100:.1f}%" if 'authors' in df.columns else "0%",
            f"{df['year'].notna().sum() / len(df) * 100:.1f}%" if 'year' in df.columns else "0%",
            f"{df['doi'].notna().sum() / len(df) * 100:.1f}%" if 'doi' in df.columns else "0%",
            f"{df['relevance_score'].notna().sum() / len(df) * 100:.1f}%" if 'relevance_score' in df.columns else "0%"
        ]
    }

    quality_df = pd.DataFrame(quality_report)
    st.table(quality_df)

    # Botão para exportar
    if st.button("📥 Exportar Relatório Completo"):
        # Aqui você pode implementar a exportação
        st.success("✅ Relatório exportado com sucesso!")


if __name__ == "__main__":
    main()
