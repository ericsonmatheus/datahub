import pandas as pd
from sqlalchemy import create_engine, text
from vlgi_datasets.postgres_upsert_table import PostgresUpsertFactory

class Advisory:
    def __init__(self, connection):
        self.engine = create_engine(connection)
    
    def get_customers(self):
        query = text("""
            SELECT * FROM customers
        """)
        with self.engine.connect() as connection:
            customers = pd.read_sql(query, connection)
        return customers

    def get_collaborators(self):
        query = text("""
            SELECT * FROM collaborators
        """)
        with self.engine.connect() as connection:
            collaborators = pd.read_sql(query, connection)
        return collaborators

    def save_customers_collaborators(self, data: pd.DataFrame):
        upsert_method_factory = PostgresUpsertFactory()
        upsert_factor = upsert_method_factory.build(constraint="unique_customer_collaborator", overwrite_columns=True)
        with self.engine.connect() as connection:
            data.to_sql(
                "customers_collaborators",
                con=connection,
                if_exists="append",
                index=False,
                method=upsert_factor,
            )