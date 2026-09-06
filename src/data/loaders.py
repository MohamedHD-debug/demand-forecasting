import os
import pandas as pd

# Fichiers disponibles dans data/processed/ 
PARQUET_FILES = {
    "df_bornes": "df_bornes.parquet",
    "df_left": "df_left.parquet",
    "df_price_cat": "df_price_cat.parquet",
    "full": "full.parquet",
    "test": "test.parquet",
    "test_fe": "test_fe.parquet",
    "train": "train.parquet",
    "train_fe": "train_fe.parquet",
}


def get_processed_dir(project_root: str) -> str:
    return os.path.join(project_root, "data", "processed")


def load_parquet(project_root: str, name: str) -> pd.DataFrame:

    if name not in PARQUET_FILES:
        raise ValueError(
            f"'{name}' inconnu. Noms disponibles : {list(PARQUET_FILES.keys())}"
        )
    path = os.path.join(get_processed_dir(project_root), PARQUET_FILES[name])
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fichier introuvable : {path}")
    return pd.read_parquet(path)


def load_many(project_root: str, names: list[str]) -> dict[str, pd.DataFrame]:
    
    return {name: load_parquet(project_root, name) for name in names}