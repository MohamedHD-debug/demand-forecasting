import pandas as pd


def add_lag_features(df: pd.DataFrame, group_cols: list[str], target_col: str) -> pd.DataFrame:
    """
    Ajoute lag_1 et lag_7 sur target_col, groupé par group_cols.
    Doit être appelé sur train+test concaténés (pas seulement train)
    pour éviter les NaN en début de test.
    """
    df = df.sort_values(group_cols + ['la_date'])
    df['lag_1'] = df.groupby(group_cols)[target_col].shift(1)
    df['lag_7'] = df.groupby(group_cols)[target_col].shift(7)
    return df


def add_rolling_mean(df: pd.DataFrame, group_cols: list[str], target_col: str, window: int = 7) -> pd.DataFrame:
    """
    Ajoute une moyenne mobile décalée (shift avant rolling pour éviter la fuite temporelle).
    """
    df[f'rolling_mean_{window}'] = (
        df.groupby(group_cols)[target_col]
        .transform(lambda x: x.shift(1).rolling(window=window).mean())
    )
    return df