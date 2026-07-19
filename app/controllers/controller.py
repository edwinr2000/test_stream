"""Controlador para preparar los datos que consumirá la interfaz.

Este módulo transforma los datos crudos recibidos desde el modelo para
hacerlos más fáciles de visualizar y analizar.
"""

from typing import Optional

import pandas as pd


def _find_column(columns: pd.Index, candidates: list[str]) -> Optional[str]:
    """Busca una columna compatible a partir de varias alternativas posibles."""
    normalized = {col.lower(): col for col in columns}
    for candidate in candidates:
        if candidate in normalized:
            return normalized[candidate]
    return None


def prepare_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una copia limpia de los datos de ventas para la UI."""
    if df.empty:
        return df.copy()

    prepared_df = df.copy()
    prepared_df.columns = [str(col).lower() for col in prepared_df.columns]

    date_column = _find_column(prepared_df.columns, ["created_at", "fecha", "date", "fecha_venta", "fecha_venta"])
    if date_column:
        prepared_df[date_column] = pd.to_datetime(prepared_df[date_column], errors="coerce")

    numeric_column = _find_column(prepared_df.columns, ["total", "monto", "importe", "valor", "ventas", "precio"])
    if numeric_column:
        prepared_df[numeric_column] = pd.to_numeric(prepared_df[numeric_column], errors="coerce")

    return prepared_df


def build_sales_summary(df: pd.DataFrame) -> dict[str, float | int]:
    """Construye métricas simples de resumen para la vista."""
    if df.empty:
        return {"registros": 0, "total": 0, "promedio": 0}

    metric_column = _find_column(df.columns, ["total", "monto", "importe", "valor", "ventas", "precio"])
    if metric_column:
        total_value = float(df[metric_column].sum())
        average_value = float(df[metric_column].mean())
    else:
        total_value = float(len(df))
        average_value = float(len(df))

    return {
        "registros": int(len(df)),
        "total": total_value,
        "promedio": average_value,
    }
