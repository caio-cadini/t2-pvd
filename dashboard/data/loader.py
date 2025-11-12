import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
FILE_PATH = BASE_DIR / "datasets" / "GLP" / "glp-2025-01.csv"

def load_data():
    df = pd.read_csv(FILE_PATH, sep=None, engine="python", encoding="utf-8-sig")

    df.columns = df.columns.str.replace("\ufeff", "", regex=False).str.strip()

    df = df.rename(columns={
        "Regiao - Sigla": "regiao",
        "Estado - Sigla": "uf",
        "Municipio": "municipio",
        "Revenda": "revenda",
        "Produto": "produto",
        "Data da Coleta": "data_coleta",
        "Valor de Venda": "valor_venda",
        "Valor de Compra": "valor_compra",
        "Bandeira": "bandeira",
    })

    df["data_coleta"] = pd.to_datetime(df["data_coleta"], format="%d/%m/%Y", errors="coerce")

    df["valor_venda"] = (
        df["valor_venda"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    df["bandeira"] = df["bandeira"].fillna("Não informada")
    df["regiao"] = df["regiao"].fillna("Não informada")

    return df
