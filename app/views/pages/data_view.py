"""Página dedicada a mostrar los datos con estilo visual más llamativo."""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def _find_numeric_column(df: pd.DataFrame) -> str | None:
    """Busca una columna numérica útil entre las columnas del DataFrame."""
    candidates = [
        "total_neto",
        "total_bruto",
        "total_descuento",
        "precio_unitario",
        "cantidad",
        "total",
        "monto",
        "importe",
        "valor",
        "ventas",
        "precio",
    ]
    lowered_columns = {col.lower(): col for col in df.columns}
    for candidate in candidates:
        if candidate in lowered_columns:
            return lowered_columns[candidate]
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            return column
    return None


def render_data_page(df: pd.DataFrame) -> None:
    """Muestra una vista dedicada con gráfico y acceso de regreso."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #111827 0%, #1d4ed8 100%);
                    padding: 24px; border-radius: 20px; color:white;">
            <h2 style="margin:0">📈 Vista de datos premium</h2>
            <p style="margin:6px 0 0 0">Aquí se presenta una experiencia visual más impactante para tus estudiantes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⬅ Volver al inicio"):
        st.session_state["show_data_page"] = False
        st.rerun()

    if df.empty:
        st.info("No hay datos disponibles para mostrar.")
        return

    value_column = _find_numeric_column(df)
    if value_column is None:
        st.warning("No se encontró una columna numérica para graficar.")
        st.dataframe(df.head(15), use_container_width=True, hide_index=True)
        return

    chart_df = df[[value_column]].copy()
    chart_df = chart_df.fillna(0)
    chart_df = chart_df.head(30)

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(chart_df[value_column].values, color="#22c55e", linewidth=2.8)
    ax.fill_between(range(len(chart_df)), chart_df[value_column].values, color="#22c55e", alpha=0.18)
    ax.set_facecolor("#0f172a")
    fig.patch.set_facecolor("#0f172a")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title("Tendencia de los valores", color="white", fontsize=14)
    ax.set_xlabel("Registro", color="white")
    ax.set_ylabel("Valor", color="white")

    st.pyplot(fig)

    st.subheader("Tabla de muestra")
    st.dataframe(df.head(20), use_container_width=True, hide_index=True)
