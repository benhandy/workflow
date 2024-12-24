## I use a Amazon Redshift database that leverages columnar storage, and an Amazon RDS (Relational Database Service) PostgreSQL data that leverages row-oriented storage
## To assess the execution time of the analytical queries, I work with a benchmarking dataset and run 5 analytical queries to query the data from each store 


import os 
import random
import time
import uuid
import sqlparse

from datetime import datetime, timedelta

from dotenv import load_dotenv
from faker import Faker

# loading SQL module 
%load_ext sql]

def format_query(query: str='', path: str =None) -> str:
    """Takes a query or a .sql file and adds 
    a comment with a random ID to avoid DB caching

    Arguments:
        query (str): SQL query
    
        path (str): Path to .sql file with one query

    Returns:
        str: Formatted query with comment
    
    """
    raw_uuid = str(uuid.uuid4()).replace('-', '')
    query_uuid = f'view{raw_uuid}' 
    
    if path:
        with open(path, 'r') as file:
            sql_commands = sqlparse.split(file.read())
            query = sql_commands[0]
    
    query = query.replace(';', '')
    sql_command = f"/* Query ID {query_uuid} */{query};"    
    
    return sql_command

