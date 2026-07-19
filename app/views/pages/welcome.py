"""Página de bienvenida con estilo visual más llamativo."""

import streamlit as st


def render_welcome_page() -> None:
    """Muestra una pantalla de bienvenida elegante con acción hacia los datos."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #0f172a 0%, #2563eb 50%, #06b6d4 100%);
                    padding: 32px; border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.25);">
            <h1 style="color:white; margin:0; font-size:48px;">✨ Dashboard de Ventas</h1>
            <p style="color:#e2e8f0; font-size:20px; margin-top:10px;">Explora tus datos con una experiencia visual más moderna y atractiva.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 0.8])
    with col1:
        st.markdown(
            """
            <div style="background:#111827; padding:20px; border-radius:18px; border:1px solid #374151;">
                <h3 style="color:white; margin-top:0">¿Listo para ver los datos?</h3>
                <p style="color:#cbd5e1">Esta propuesta usa un diseño más dinámico, con una transición visual hacia una vista especial de análisis.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        if st.button("🚀 Ver datos", use_container_width=True):
            st.session_state["show_data_page"] = True
            st.rerun()

    if st.session_state.get("show_data_page"):
        st.success("Abriendo la vista de datos...")
