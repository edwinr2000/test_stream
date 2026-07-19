"""Vista visualmente más atractiva para mostrar datos de ventas en Streamlit."""

import pandas as pd
import streamlit as st

from app.controllers.controller import build_sales_summary


def _find_column(columns: pd.Index, candidates: list[str]) -> str | None:
    """Busca una columna compatible a partir de varias alternativas posibles."""
    normalized = {col.lower(): col for col in columns}
    for candidate in candidates:
        if candidate in normalized:
            return normalized[candidate]
    return None


def _render_overview(df: pd.DataFrame) -> None:
    """Renderiza una vista tipo dashboard con métricas y gráficos dinámicos."""
    st.header("Resumen ejecutivo")
    summary = build_sales_summary(df)

    st.markdown(
        "<div style='background:linear-gradient(90deg,#0f172a,#2563eb);padding:16px;border-radius:12px;color:white;'>"
        "<h3 style='margin:0'>Panel en vivo de ventas</h3>"
        "<p style='margin:4px 0 0 0'>Observa el comportamiento de tus datos con una interfaz más cercana a un tablero empresarial.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Registros", f"{summary['registros']}")
    col2.metric("💰 Total", f"${summary['total']:,.2f}")
    col3.metric("📈 Promedio", f"${summary['promedio']:,.2f}")

    date_column = _find_column(df.columns, ["created_at", "fecha", "date", "fecha_venta"])
    value_column = _find_column(df.columns, ["total", "monto", "importe", "valor", "ventas", "precio"])
    category_column = _find_column(df.columns, ["producto", "categoria", "category", "producto_nombre", "cliente"])

    chart_col1, chart_col2 = st.columns(2)

    if date_column and value_column:
        monthly_data = df.copy()
        monthly_data[date_column] = pd.to_datetime(monthly_data[date_column], errors="coerce")
        monthly_data = monthly_data.dropna(subset=[date_column, value_column])
        monthly_data = monthly_data.set_index(date_column).resample("M").sum(numeric_only=True)
        with chart_col1:
            st.subheader("Evolución mensual")
            st.line_chart(monthly_data[[value_column]])

    if category_column and value_column:
        grouped = df.groupby(category_column, dropna=False)[value_column].sum().sort_values(ascending=False).head(8)
        with chart_col2:
            st.subheader("Top por categoría")
            st.bar_chart(grouped)

    st.divider()
    st.subheader("Vista rápida")
    st.dataframe(df.head(12), use_container_width=True, hide_index=True)


def _apply_expression_filter(df: pd.DataFrame, expression: str) -> pd.DataFrame:
    """Filtra el DataFrame usando expresiones del tipo columna = valor."""
    if not expression or "=" not in expression:
        return df

    left, right = [part.strip() for part in expression.split("=", 1)]
    if not left or not right:
        return df

    column_name = None
    normalized_columns = {col.lower(): col for col in df.columns}
    if left.lower() in normalized_columns:
        column_name = normalized_columns[left.lower()]

    if not column_name:
        return df

    value = right.strip().strip("\"'")
    try:
        return df[df[column_name].astype(str).str.lower() == value.lower()]
    except Exception:
        return df


def _render_detail(df: pd.DataFrame) -> None:
    """Renderiza una tabla detallada con filtros y contexto visual."""
    st.header("Detalle operativo")

    if df.empty:
        st.info("No hay datos disponibles para mostrar.")
        return

    st.caption("Puedes escribir filtros como: ciudad_tienda = Cali, genero = M o categoria = Electrónica")
    filter_expression = st.text_input("🔎 Filtrar por columna = valor")
    filtered_df = _apply_expression_filter(df, filter_expression)

    if filter_expression and filtered_df.empty:
        st.info("No se encontraron resultados para esa condición.")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)


def _render_insights(df: pd.DataFrame) -> None:
    """Renderiza insights y recomendaciones más atractivas."""
    st.header("Insights de negocio")

    if df.empty:
        st.info("Aún no hay datos suficientes para generar insights.")
        return

    value_column = _find_column(df.columns, ["total", "monto", "importe", "valor", "ventas", "precio"])
    category_column = _find_column(df.columns, ["producto", "categoria", "category", "producto_nombre", "cliente"])

    st.success("En esta app, podras ver datos de prueba extraídos de Supabase y visualizados con Streamlit. Puedes explorar métricas, gráficos y detalles de ventas.")

    if category_column and value_column:
        top_group = df.groupby(category_column, dropna=False)[value_column].sum().sort_values(ascending=False).head(3)
        st.subheader("Categorías más relevantes")
        st.bar_chart(top_group)

    with st.expander("💡 Notas equipo"):
        st.markdown("Esta aplicación es una prueba de concepto desarrollada con Streamlit y Supabase.")
        st.markdown("El objetivo es demostrar cómo una aplicación web puede conectarse a una base de datos y consultar información en tiempo real.")
        st.markdown("A partir de este ejemplo, pueden experimentar agregando filtros, gráficos y nuevas funcionalidades.")
        st.markdown("La aplicación puede utilizarse como punto de partida para construir sus propios proyectos.")
        st.markdown("Saludos y feliz aprendizaje! 🚀")
        st.markdown("Edwin Oswaldo Torres Rincón")



def render_sales_dashboard(df: pd.DataFrame) -> None:
    """Renderiza un dashboard con varias páginas y mejor experiencia visual."""
    st.title("📊 Dashboard de Ventas")
    st.caption("Aplicación educativa con Streamlit, MVC y Supabase")

    if df.empty:
        st.info("No hay datos disponibles en este momento.")
        return

    page = st.sidebar.radio("🧭 Navegación", ["Resumen", "Detalle", "Insights"], index=0)

    if page == "Resumen":
        _render_overview(df)
    elif page == "Detalle":
        _render_detail(df)
    else:
        _render_insights(df)
