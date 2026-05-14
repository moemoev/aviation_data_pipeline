import pandas as pd

from sqlalchemy import create_engine
from plugins.utils.paths import transformed_file
from plugins.utils.file_io import read_parquet

def load_files(run_id, conn_db: str):

    path = transformed_file(run_id=run_id)
    data = read_parquet(path)

    engine = create_engine(conn_db)
    data.to_sql("data", con=engine, index=False, if_exists="replace")