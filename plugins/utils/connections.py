import os

def get_postgres_conn_str() -> str:
    #note: revisit and handle errors , malformed string will fail , missing values are not caught
    """
    create connection string for postgres db
    :return:
    """
    return (
        f"postgresql+psycopg2://"
        f"{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:"
        f"{os.getenv('POSTGRES_PORT')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )

