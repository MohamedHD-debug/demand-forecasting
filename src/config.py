import os

# --- Chemins ---
PROJECT_ROOT = r"c:\Users\admin\demand-forecasting"
DATA_PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
MODEL_DIR = os.path.join(PROJECT_ROOT, "models")

# --- Split temporel ---
CUTOFF_DATE = "2016-03-05"  

# --- Features du modèle ---
FEATURES = [
    "lag_1", "lag_7", "rolling_mean_7", "price", "prix_connu",
    "categorie", "jour_semaine_num", "is_weekend", "is_holiday",
]
CAT_FEATURES = ["categorie", "jour_semaine_num", "is_weekend", "is_holiday"]
TARGET = "quantite"

# --- Hyperparamètres du modèle retenu ---
MODEL_PARAMS = {
    "n_estimators": 100,
    "random_state": 42,
    "alpha": 0.63,
}
MODEL_FILENAME = "lgbm_m6_quantile_alpha063.pkl"

# --- Critères de validation ---
WAPE_THRESHOLD = 0.70          # "prêt à déployer" : WAPE global sous ce seuil
WAPE_PER_CATEGORY_MAX = 1.0    # aucune catégorie ne doit dépasser ce WAPE
BACKTEST_MAX_DEGRADATION = 0.15  # dégradation max tolérée entre fenêtres de backtesting

# --- Fenêtres de backtesting multi-périodes ---
BACKTEST_WINDOWS = [
    ("2016-01-15", "2016-03-05"),
    ("2016-02-01", "2016-03-22"),
    ("2016-03-05", "2016-04-24"),
]