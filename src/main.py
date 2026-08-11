from etl.extract import load_raw_data
from etl.transform import build_item, build_dim_date, build_fact_sales, build_price, build_store
from etl.load import get_engine, load_DB

def main() :
    #extracting
    sales, calendar, prices = load_raw_data()

    #transforming
    item = build_item(sales)
    store = build_store(sales)
    dim_date = build_dim_date(calendar)
    price = build_price(prices, calendar, item, store)
    fact_sales = build_fact_sales(sales, dim_date, item, store)

    #loading
    engine = get_engine()
    load_DB(engine, dim_date, item, store, price, fact_sales)

if __name__ == "__main__" :
    main()