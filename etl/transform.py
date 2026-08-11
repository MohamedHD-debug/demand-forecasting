import pandas as pd

def build_item(sales: pd.DataFrame) -> pd.DataFrame:

    item = sales[['item_id', 'dept_id', 'cat_id']].drop_duplicates()
    item = item.reset_index(drop=True)
    item['id'] = item.index + 1
    item = item.rename(columns={'cat_id': 'categorie', 'dept_id': 'departement'})

    return item

def build_store(sales: pd.DataFrame) -> pd.DataFrame:

    store = sales[['store_id', 'state_id']].drop_duplicates()
    store = store.reset_index(drop=True)
    store['id'] = store.index + 1
    store = store.rename(columns={'state_id': 'etat'})

    return store

def build_dim_date(calendar: pd.DataFrame) -> pd.DataFrame:

    dim_date = calendar[['date','d','weekday']].copy()
    dim_date['is_weekend'] = [1 if c == 1 or c == 2 else 0 for c in calendar['wday']]
    dim_date['is_holiday'] = [1 if pd.notna(c) else 0 for c in calendar['event_name_1']]
    dim_date.rename(columns={
        'date':'la_date',
        'd':'date_id',
        'weekday':'jour_de_semaine'
    },inplace=True)
    dim_date = dim_date.reset_index(drop=True)
    dim_date['id'] = dim_date.index + 1

    dim_date['is_weekend'] = dim_date['is_weekend'].astype(bool)
    dim_date['is_holiday'] = dim_date['is_holiday'].astype(bool)

    return dim_date

def build_price(prices: pd.DataFrame, calendar: pd.DataFrame, item: pd.DataFrame, store: pd.DataFrame) -> pd.DataFrame:

    c_from = calendar[['date','wm_yr_wk']].drop_duplicates(subset="wm_yr_wk")
    c_from.rename(columns={
        'date':'valid_from'
    },inplace=True)
    c_to = calendar[['date','wm_yr_wk']].drop_duplicates(subset="wm_yr_wk")
    c_to['date'] = c_to['date'].shift(-1)
    c_to.rename(columns={
        'date':'valid_to'
    },inplace=True)
    price = prices.merge(c_from, on='wm_yr_wk', how='left')
    price = price.merge(c_to, on='wm_yr_wk', how='left')
    price = price.drop(columns=['wm_yr_wk'])
    price = price.rename(columns={'sell_price': 'price'})

    mapping_item = item.set_index("item_id")['id']
    price['item_id'] = price['item_id'].map(mapping_item)
    mapping_store = store.set_index("store_id")['id']
    price['store_id'] = price['store_id'].map(mapping_store)

    return price

def build_fact_sales(sales: pd.DataFrame, dim_date: pd.DataFrame, item: pd.DataFrame, store: pd.DataFrame) -> pd.DataFrame:

    fact_sales = sales.melt(
    id_vars=['item_id', 'store_id'],
    value_vars=[col for col in sales.columns if col.startswith('d_')],
    var_name='date_id',
    value_name='quantite'
    )
    fact_sales = fact_sales.merge(dim_date, on='date_id', how='left')

    mapping_item = item.set_index("item_id")['id']
    fact_sales['item_id'] = fact_sales['item_id'].map(mapping_item)
    mapping_store = store.set_index("store_id")['id']
    fact_sales['store_id'] = fact_sales['store_id'].map(mapping_store)
    mapping_date = dim_date.set_index('date_id')['id']
    fact_sales['date_id'] = fact_sales['date_id'].map(mapping_date)

    fact_sales = fact_sales.drop(columns=['la_date', 'jour_de_semaine', 'is_weekend', 'is_holiday'])

    return fact_sales