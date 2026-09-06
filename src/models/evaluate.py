import pandas as pd


def wape(y_true: pd.Series, y_pred: pd.Series) -> float:
    """
    Weighted Absolute Percentage Error.
    """

    return (y_true - y_pred).abs().sum() / y_true.sum()

def mase(mae_model: float, naive_scale: float) -> float:
    """
    Mean Absolute Scaled Error.
    """
    return mae_model / naive_scale