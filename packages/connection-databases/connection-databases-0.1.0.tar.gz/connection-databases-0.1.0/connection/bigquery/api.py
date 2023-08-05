import os
import pandas as pd
from sqlalchemy import create_engine


class BigQuery(object):
    """Class to perform queries in Bigquery"""

    def __init__(self, bigquery_uri, credentials_path):
        self.bigquery_uri = bigquery_uri
        self.credentials_path = credentials_path

    def __engine_bigquery(self):
        """Private function to create the connection engine"""

        engine = create_engine(
            self.bigquery_uri,
            credentials_path=self.credentials_path
        )

        return engine

    def select_query(self, query):
        """Queries the database and returns a Dataframe

        Parameters
        ----------
        query : str
            query to be passed on to the database

        Returns
        -------
        pandas DataFrame
        """
        # connection engine
        engine = BigQuery.__engine_bigquery(self)

        rows = engine.execute(query).fetchall()
        df_raw = pd.DataFrame(rows)
        df_raw.columns = engine.execute(query).keys()

        return df_raw
