import os
import pandas as pd

from sqlalchemy import create_engine, text
from vlgi_datasets.postgres_upsert_table import PostgresUpsertFactory

class Advisory:
    def __init__(self, connection):
        self.engine = create_engine(connection)
        self.CUSTOMERS_DB = os.environ.get("CUSTOMERS_DB")
        self.COLLABORATORS_DB = os.environ.get("COLLABORATORS_DB")
        self.CUSTOMERS_RULES_DB = os.environ.get("CUSTOMERS_RULES_DB")
        self.CONSTRAINT_CUSTOMERS_RULES = os.environ.get("CONSTRAINT_CUSTOMERS_RULES")

    def get_customers(self) -> pd.DataFrame:
        query = text(f"SELECT * FROM {self.CUSTOMERS_DB}")
        with self.engine.connect() as connection:
            customers = pd.read_sql(query, connection)
        return customers

    def get_collaborators(self) -> pd.DataFrame:
        query = text(f"SELECT * FROM {self.COLLABORATORS_DB}")
        with self.engine.connect() as connection:
            collaborators = pd.read_sql(query, connection)
        return collaborators

    def save_customers_collaborators(self, data: pd.DataFrame) -> None:
        upsert_method_factory = PostgresUpsertFactory()
        upsert_factor = upsert_method_factory.build(constraint=self.CONSTRAINT_CUSTOMERS_RULES, overwrite_columns=True)
        with self.engine.connect() as connection:
            data.to_sql(
                self.CUSTOMERS_RULES_DB,
                con=connection,
                if_exists="append",
                index=False,
                method=upsert_factor,
            )