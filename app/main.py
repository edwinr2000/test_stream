"""Punto de entrada principal de la aplicación Streamlit.

Este archivo orquesta el flujo MVC:
1. El modelo obtiene los datos desde Supabase.
2. El controlador prepara los datos para la vista.
3. La vista los muestra en la interfaz.
"""

import streamlit as st

from app.controllers.controller import prepare_sales_data
from app.models.db import fetch_sales_data
from app.views.dashboard import render_sales_dashboard
from app.views.pages.data_view import render_data_page
from app.views.pages.welcome import render_welcome_page


def main() -> None:
    """Función principal que ejecuta la aplicación."""
    st.set_page_config(page_title="Streamlit + Supabase", page_icon="📊", layout="wide")

    if "show_data_page" not in st.session_state:
        st.session_state["show_data_page"] = False

    try:
        raw_df = fetch_sales_data(limit=200)
        prepared_df = prepare_sales_data(raw_df)
    except Exception as exc:
        st.error(f"No fue posible cargar los datos: {exc}")
        prepared_df = None

    if prepared_df is not None and st.session_state.get("show_data_page"):
        render_data_page(prepared_df)
    else:
        render_welcome_page()
        if prepared_df is not None:
            st.divider()
            render_sales_dashboard(prepared_df)


if __name__ == "__main__":
    main()
