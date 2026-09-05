import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import io


load_dotenv()
DB_USER = os.getenv("POSTGRES_USER","forecaster")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD","forecaster_pass")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB","demand_db")

def get_engine():
    connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_string)

def fast_load(df, table_name, engine):
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)
    
    raw_conn = engine.raw_connection()
    cursor = raw_conn.cursor()
    cursor.copy_expert(
        f"COPY {table_name} ({', '.join(df.columns)}) FROM STDIN WITH CSV",
        buffer
    )
    raw_conn.commit()
    cursor.close()
    raw_conn.close()

def fast_load_chunked(df, table_name, engine, chunk_size=1_000_000):
    total = len(df)
    for start in range(0, total, chunk_size):
        end = min(start + chunk_size, total)
        chunk = df.iloc[start:end]
        
        buffer = io.StringIO()
        chunk.to_csv(buffer, index=False, header=False)
        buffer.seek(0)
        
        raw_conn = engine.raw_connection()
        cursor = raw_conn.cursor()
        cursor.copy_expert(
            f"COPY {table_name} ({', '.join(chunk.columns)}) FROM STDIN WITH CSV",
            buffer
        )
        raw_conn.commit()
        cursor.close()
        raw_conn.close()
        
        print(f"Chargé {end}/{total} lignes")

def load_DB(engine, dim_date: pd.DataFrame, item: pd.DataFrame, store: pd.DataFrame, price: pd.DataFrame, fact_sales: pd.DataFrame) :
    item.to_sql('item', engine, if_exists='append', index=False)
    store.to_sql('store', engine, if_exists='append', index=False)
    dim_date.to_sql('dim_date', engine, if_exists='append', index=False)
    fast_load(price, 'price', engine)
    fast_load_chunked(fact_sales, 'fact_sales', engine)