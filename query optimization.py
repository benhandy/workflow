"""
I use a Amazon Redshift database that leverages columnar storage, 
and an Amazon RDS (Relational Database Service) PostgreSQL data that leverages row-oriented storage.

To assess the execution time of the analytical queries, I work with a benchmarking dataset 
and run 5 analytical queries to query the data from each store.

"""


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

""" 
    Here is the env file which includes endpoints and connection 
    information for both the Redshift and Postgresql databases

RDSDBHOST=de-c3w3lab1-rds.cz6m82e4wt2x.us-east-1.rds.amazonaws.com
RDSDBPORT=5432
RDSDBNAME=dev
RDSDBUSER=postgresuser
RDSDBPASSWORD=adminpwrd
REDSHIFTDBHOST=redshiftcluster-9bnjth01mfim.coo7fo01pnn3.us-east-1.redshift.amazonaws.com
REDSHIFTDBPORT=5439
REDSHIFTDBNAME=dev
REDSHIFTDBUSER=defaultuser
REDSHIFTDBPASSWORD=Defaultuserpwrd1234+

"""

load_dotenv('./src/env', override=True)

REDSHIFTDBHOST = os.getenv('REDSHIFTDBHOST')
REDSHIFTDBPORT = int(os.getenv('REDSHIFTDBPORT'))
REDSHIFTDBNAME = os.getenv('REDSHIFTDBNAME')
REDSHIFTDBUSER = os.getenv('REDSHIFTDBUSER')
REDSHIFTDBPASSWORD = os.getenv('REDSHIFTDBPASSWORD')

# creating connection string

redshift_connection_url = f'redshift+psycopg2://{REDSHIFTDBUSER}:{REDSHIFTDBPASSWORD}@{REDSHIFTDBHOST}:{REDSHIFTDBPORT}/{REDSHIFTDBNAME}'
print(redshift_connection_url)

"""
Printed connection string: 

redshift+psycopg2://defaultuser:Defaultuserpwrd1234+@redshiftcluster-9bnjth01mfim.coo7fo01pnn3.us-east-1.redshift.amazonaws.com:5439/dev

"""
# connecting to redshift cluster 
%sql {redshift_connection_url}

# disable caching results
%sql SET enable_result_cache_for_session TO off;


    ///////////////////////////////////////////////////////////////////
//////////////////////////////////////////////

    
%%sql
SELECT  distinct tablename
FROM PG_TABLE_DEF
WHERE schemaname='public'
;


%%sql
SELECT  *
FROM PG_TABLE_DEF
WHERE schemaname='public'
AND tablename='lineitem'
;


"""

In the CTE: I need to add the order keys that I want to inspect into the IN operator. Specifically, I'll include the order keys 1552449, 13620130, and 45619461.
In the SELECT statement: I will select the necessary columns from each table. Specifically:
l_orderkey and l_partkey from the lineitemorders CTE.
p_name from the part table.
c_custkey from the customer table.
o_orderstatus and o_orderdate from the orders table.
n_name from the nation table.
r_name from the region table.
Join Statements: I will perform 5 joins:
I will join the part table on the p_partkey column and the l_partkey column from the lineitemorders CTE.
Then, I'll join the orders table on the l_orderkey column and the o_orderkey column from the orders table.
Next, I'll join the customer table on the c_custkey column and the o_custkey column from the orders table.
I'll then join the nation table on the n_nationkey column and the c_nationkey column from the customer table.
Finally, I'll join the region table on the r_regionkey column and the n_regionkey column from the nation table.

"""


%%timeit -n1 -r1
raw_sql_statement =     
    WITH lineitemorders AS (
        SELECT *
        FROM public.lineitem
        WHERE l_orderkey IN (1552449, 13620130, 45619461)
    )
    
    SELECT DISTINCT 
        lio.l_orderkey, 
        lio.l_partkey, 
        pt.p_name, 
        ctr.c_custkey, 
        ord.o_orderstatus, 
        ord.o_orderdate, 
        ntn.n_name, 
        rgn.r_name
    FROM lineitemorders lio
    JOIN public.part pt ON pt.p_partkey = lio.l_partkey
    JOIN public.orders ord ON lio.l_orderkey = ord.o_orderkey
    JOIN public.customer ctr ON ctr.c_custkey = ord.o_custkey
    JOIN public.nation ntn ON ntn.n_nationkey = ctr.c_nationkey
    JOIN public.region rgn ON rgn.r_regionkey = ntn.n_regionkey;


sql_statement = format_query(query=raw_sql_statement)

%sql {sql_statement}



"""

Create a CTE (Common Table Expression) called avg_balance_middle_east. In this CTE, I will:
Compute the average account balance (AVG()) of customers (c_acctbal) from the customer table.
Join the nation table on n_nationkey and c_nationkey to connect the customer data with the nation information.
Join the region table on r_regionkey and n_regionkey to associate the nation data with the region.
Filter by the region name 'MIDDLE EAST' in the region table.
In the main query:
I will select the count of distinct customers (COUNT(DISTINCT c.c_custkey)) whose account balance is greater than the average balance computed in the CTE.
I need to join the nation and region tables again on the same columns (n_nationkey and c_nationkey for nation; r_regionkey and n_regionkey for region).
I will apply two filters:
The region should be 'MIDDLE EAST'.
The customer’s account balance (c_acctbal) should be greater than the avg_balance computed in the CTE. 
I’ll need to use a subquery to extract the avg_balance from the CTE and apply it in the filter.


"""



%%timeit -n1 -r1
WITH avg_balance_middle_east AS (
    SELECT 
        AVG(c_acctbal) AS avg_balance
    FROM customer c
    JOIN nation n ON c.c_nationkey = n.n_nationkey
    JOIN region r ON n.n_regionkey = r.r_regionkey
    WHERE r.r_name = 'MIDDLE EAST'
)
SELECT 
    COUNT(DISTINCT c.c_custkey) AS num_customers_above_avg_balance
FROM customer c
JOIN nation n ON c.c_nationkey = n.n_nationkey
JOIN region r ON n.n_regionkey = r.r_regionkey
WHERE r.r_name = 'MIDDLE EAST'
  AND c.c_acctbal > (SELECT avg_balance FROM avg_balance_middle_east);



