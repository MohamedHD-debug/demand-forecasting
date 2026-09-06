import lightgbm as lgb
import pandas as pd


def prepare_features(df: pd.DataFrame, features: list[str], cat_features: list[str]) -> pd.DataFrame:
    """Type les colonnes catégorielles pour LightGBM."""
    X = df[features].copy()
    for col in cat_features:
        X[col] = X[col].astype('category')
    return X


def train_lgbm(X_train: pd.DataFrame, y_train: pd.Series, cat_features: list[str],
                alpha: float = 0.63, n_estimators: int = 100, random_state: int = 42) -> lgb.LGBMRegressor:
    """Entraîne le modèle LightGBM avec objectif quantile (correction du biais Q4)."""
    model = lgb.LGBMRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        objective='quantile',
        alpha=alpha
    )
    model.fit(X_train, y_train, categorical_feature=cat_features)
    return model