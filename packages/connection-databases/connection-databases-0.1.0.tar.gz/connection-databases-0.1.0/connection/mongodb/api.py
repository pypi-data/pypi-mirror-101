from urllib.parse import quote

import pandas as pd
from pymongo import MongoClient


class MongoDB(object):
    """Class to query the MongoDB database through pipelines"""

    def __init__(self, username, password, host_string):
        self.username = username
        # torna "/ " em caracter
        self.password = quote(password, safe="!~*'();/?:@&=+$,#")
        self.host_string = quote(host_string, safe="!~*'();/?:@&=+$,#")

    def __client(self):
        """Private function to create the mongodb client"""
        client = MongoClient(
            f'mongodb+srv://{self.username}:{self.password}@{self.host_string}')

        return client

    def select_pipeline(self, database, collection, pipeline):
        """

        Parameters
        ----------
        database : str
           Database to be connected

        collection : str
            Collection in which you want to make the query

        pipeline : list
            Agregation pipeline  (Mongo)

        Returns
        -------
        pandas DataFrame
        """
        client = MongoDB.__client(self)

        db = client[database]
        col = db[collection]

        results = col.aggregate(pipeline)
        df_raw = pd.DataFrame(results)

        return df_raw
