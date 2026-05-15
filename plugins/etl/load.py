from sqlalchemy import create_engine
import pandas as pd
from plugins.utils.paths import transformed_file
from plugins.utils.connections import get_postgres_conn_str
from plugins.utils.file_io import read_parquet

def load_files(run_id):

    path = transformed_file(run_id=run_id)
    data = read_parquet(path)


    engine = create_engine(get_postgres_conn_str())
    data.to_sql("data",schema="raw_layer", con=engine, index=False, if_exists="replace")

def load_data(schema: str,data: pd.DataFrame):
    engine = create_engine(get_postgres_conn_str())
    data.to_sql("data",schema=schema, con=engine, index=False, if_exists="replace")