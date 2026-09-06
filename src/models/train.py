import lightgbm as lgb
import pandas as pd


def prepare_features(df: pd.DataFrame, features: list[str], cat_features: list[str]) -> pd.DataFrame:
    """Type les colonnes catégorielles pour LightGBM."""
    X = df[features].copy()
    for col in cat_features:
        X[col] = X[col].astype('category')
    return X


def train_lgbm(
    X_train, y_train, cat_features, alpha=0.63, n_estimators=100, random_state=42, objective='quantile',):
    model = lgb.LGBMRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        objective=objective,
        alpha=alpha,
    )
    model.fit(X_train, y_train, categorical_feature=cat_features)
    return model