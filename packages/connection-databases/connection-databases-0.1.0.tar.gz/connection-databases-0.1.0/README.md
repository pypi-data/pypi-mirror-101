# connection

Package for establishing cenexion with the different databases to perform queries

## Features

- MySQL connection
- MongoDB connection
- Big Query connection

## Instalation
You can install this package using

```
pip install connection
```

## Usage
```
# MySQL
from connection.mysql import MySQL
MySQL(username, password, host)

# MongoDB
from connection.mongodb import MongoDB
MongoDB(username, password, host_string)

# Big Query
from connection.bigquery import BigQuery
BigQuery(bigquery_uri, credentials_path)
```