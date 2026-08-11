import pandas as pd

def load_raw_data(data_dir="data/raw"):
    sales = pd.read_csv(f"{data_dir}/sales_train_validation.csv")
    calendar = pd.read_csv(f"{data_dir}/calendar.csv")
    prices = pd.read_csv(f"{data_dir}/sell_prices.csv")
    return sales, calendar, prices