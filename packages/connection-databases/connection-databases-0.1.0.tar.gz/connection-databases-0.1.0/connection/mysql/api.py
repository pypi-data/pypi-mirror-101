from urllib.parse import quote

import pandas as pd
from sqlalchemy import create_engine


class MySQL(object):
    """Class to query MySQL database"""

    def __init__(self, username, password, host):
        self.host = host
        self.username = username
        # torna "/ " em caracter
        self.password = quote(password, safe="!~*'();/?:@&=+$,#")

    def __engine_mysql(self, schema):
        """Private function to create the connection engine"""
        engine = create_engine(
            f'mysql+pymysql://{self.username}:{self.password}@{self.host}/{schema}')

        return engine

    def select_query(self, query, schema):
        """Queries the database and returns a Dataframe

        Parameters
        ----------
        query : str
            query to be passed on to the database

        schema : str
            Schema in which the tables are located

        Returns
        -------
        pandas DataFrame
        """
        # connection engine
        engine = MySQL.__engine_mysql(self, schema)

        with engine.connect() as conn:
            df_raw = pd.read_sql(query, conn)

        return df_raw
