"""Módulo de acceso a datos para Supabase.

Este archivo encapsula la conexión y las consultas a la base de datos.
Se usa un patrón modelo para separar la lógica de acceso a datos del resto
 de la aplicación.

Ejemplo de configuración con Streamlit Secrets:

[secrets]
[supabase]
url = "https://tu-proyecto.supabase.co"
anon_key = "tu-clave-anon"
"""

import os
import tomllib
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st
from supabase import Client, create_client


def _read_local_secrets() -> dict:
    """Lee secretos desde el archivo local de Streamlit si está disponible."""
    secrets_path = Path(__file__).resolve().parents[2] / ".streamlit" / "secrets.toml"
    if not secrets_path.exists():
        return {}

    with secrets_path.open("rb") as file_handle:
        return tomllib.load(file_handle)


def _get_secret_value(section: str, key: str, env_key: Optional[str] = None) -> Optional[str]:
    """Lee un valor desde Streamlit Secrets, variables de entorno o un archivo local."""
    try:
        if hasattr(st, "secrets"):
            section_values = st.secrets.get(section, {})
            if isinstance(section_values, dict) and key in section_values:
                return str(section_values[key])
    except Exception:
        pass

    if env_key:
        env_value = os.getenv(env_key)
        if env_value:
            return env_value

    env_value = os.getenv(f"{section.upper()}_{key.upper()}")
    if env_value:
        return env_value

    local_secrets = _read_local_secrets()
    section_values = local_secrets.get(section, {})
    if isinstance(section_values, dict):
        value = section_values.get(key)
        if value:
            return str(value)

    return None


def get_supabase_client() -> Client:
    """Crea y devuelve un cliente de Supabase configurado de forma segura."""
    supabase_url = _get_secret_value("supabase", "url", "SUPABASE_URL")
    supabase_key = _get_secret_value("supabase", "anon_key", "SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError(
            "No se encontraron las credenciales de Supabase. "
            "Define st.secrets['supabase']['url'] y st.secrets['supabase']['anon_key'] "
            "o las variables de entorno SUPABASE_URL/SUPABASE_ANON_KEY."
        )

    return create_client(supabase_url, supabase_key)


def fetch_table_as_dataframe(table_name: str, limit: int = 100, columns: str = "*") -> pd.DataFrame:
    """Obtiene filas de una tabla y las devuelve como un DataFrame de pandas."""
    client = get_supabase_client()
    response = client.table(table_name).select(columns).limit(limit).execute()

    data = getattr(response, "data", None)
    if not data:
        return pd.DataFrame()

    return pd.DataFrame(data)


def fetch_sales_data(limit: int = 100) -> pd.DataFrame:
    """Ejemplo educativo para consultar la vista 'ventas' y devolver un DataFrame."""
    return fetch_table_as_dataframe("ventas", limit=limit)
