## Here I build a DAG pipeline in Apache Airflow 
## using Python operators then visualize it in the Airflow UI
## and then troubleshoot errors in the DAG.
## The premise of this project is that I have been tasked to develop the 'Book of the Day' 
## feature where a random book is selected as book of  the day and displayed on a website.

## I use the Open Library Web APIs (books, authors, and covers APIs)
## to fetch information about a random book, authors, and book covers.

## This project was completed during week 4 of 'Source Systems, Data Ingestion, and Pipelines'
## a certification course taught by Joe Reis (author: Fundamentals of Data Engineering). 



import datetime as dt
import json
import logging
from random import randint

import boto3
import requests
from airflow import DAG
from airflow.operators.dummy import EmptyOperator
from airflow.operators.python import PythonOperator


RAW_DATA_BUCKET = "de-c2w4lab1-851725230964-us-east-1-raw-data"


client = boto3.client("s3")


logger = logging.getLogger()
logger.setLevel("INFO")

# define directed acyclic graph
with DAG(
    dag_id="book_of_the_day",

    start_date=dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=7),

    
    schedule="@daily",

    catchup=True,
) as dag:


    start_task = EmptyOperator(task_id="start")



    def get_random_book(**context):
        
      
        random_book_id = randint(10001, 21000000)

        # use previously obtained random number to get an Open Library work
        # ID:
        book_id = f"works/OL{random_book_id}W"
        logger.info(f"SELECTED BOOK ID: {book_id}")

        # make a call to the Open Library works API to retrieve information
        # about the book with the given ID:
        response = requests.get(
            f"https://openlibrary.org/works/{book_id}.json"
        )

        assert response.status_code == 200, response.reason

       # raise an assertion error so that Airflow retries the task:
        assert "title" in response.json()

     
        file_name = f"initial_info_{context['ds']}.json"

        logger.info(f"Saving file: {file_name}")
    
    
        # call the `put_object` method of the boto3 client by passing the
        # raw Data Bucket constant to the Bucket parameter, and the content of the
        # API response to the Body parameter with the code `response.content`
         client.put_object(
            Bucket=RAW_DATA_BUCKET,
            Key=f"books/{context['ds']}/{file_name}",
            Body=response.content,
      
        logger.info(f"File: {file_name} saved successfully")

    # define the task that fetches the initial information about a random book
    # and stores it in S3:
    get_book_task = PythonOperator(
        task_id="get_random_book",
      
        # pass `get_random_book` function defined above
        python_callable=get_random_book,    
        
        retries=5,  # retry the task in case we get a resource with no title
        retry_delay=dt.timedelta(seconds=1),
    )



    def get_initial_info_dict(date: str):
        """
        Fetches the contents of the initial information file for the given date
        as a Python dictionary.
        """
 
        initial_info_file_name = f"initial_info_{date}.json"

        logger.info(f"Reading the file: {initial_info_file_name}")

      
        initial_info_file = client.get_object(
            Bucket=RAW_DATA_BUCKET,
            Key=f"books/{date}/{initial_info_file_name}",
        )

        
        logger.info(f"File read: {initial_info_file_name}")

        assert (
            initial_info_file is not None
        ), f"The file {RAW_DATA_BUCKET}/books/{date}/{initial_info_file_name} does not exist"

        initial_info_string = initial_info_file["Body"].read()
 

        initial_info = json.loads(initial_info_string)

        return initial_info


    def get_author_names(**context):
        
      
        initial_info = get_initial_info_dict(context["ds"])
       

        author_names = []

      
        for author in initial_info.get("authors", []):
            author_key = author["author"]["key"]  # API call suffix
            response = requests.get(
                f"https://openlibrary.org{author_key}.json"
            )
            author_names.append(response.json()["name"])

      
        author_names_string = json.dumps(author_names)

        author_file_name = f"author_names_{context['ds']}.json"

        logger.info(f"Saving file: {author_file_name}")

     
        # call the `put_object` method of the boto3 client by passing the
        # Raw Data Bucket name to the Bucket parameter, and 
        # the author_names_string to the Body parameter
        client.put_object(
            Bucket=RAW_DATA_BUCKET,
            Key=f"authors/{context['ds']}/{author_file_name}",
            Body=author_names_string,
        )


        logger.info(f"File: {author_file_name} saved")

    
    get_authors_task = PythonOperator(
        task_id="get_authors",
        
      
        # pass `get_author_names` to the `python_callabes` parameter
        python_callable=get_author_names,
 
        
    )

  

    def get_cover(**context):


        # read initial information about the book selected for the
        # corresponding day using the `get_initial_info_dict` function.
        initial_info = get_initial_info_dict(context["ds"])
     
        if "covers" in initial_info:
            # get first cover ID from the list 
            cover_id = initial_info["covers"][0]

            response = requests.get(
                f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
            )

            cover_file_name = f"cover_{context['ds']}.jpg"

            logger.info(f"Saving File: {cover_file_name}")
            
         
              client.put_object(
                Bucket=RAW_DATA_BUCKET,
                Key=f"covers/{context['ds']}/{cover_file_name}",
                Body=response.content,
            )
      
            
            logger.info(f"File: {cover_file_name} saved")

    get_cover_task = PythonOperator(
        task_id="get_cover",
        
      
        python_callable=get_cover,

    )


    def save_final_book_record(**context):
        
    
        initial_info = get_initial_info_dict(context["ds"])

        # read information about the authors as list of strings:
        authors_file_name = f"author_names_{context['ds']}.json"
        authors_object = client.get_object(
            Bucket=RAW_DATA_BUCKET,
            Key=f"authors/{context['ds']}/{authors_file_name}",
        )
        assert authors_object is not None

        authors = json.loads(authors_object["Body"].read())

        # create book record
        book_record_dict = {
            "title": initial_info["title"],
            "authors": authors,
        }

        # if there is a cover in the initial info
        if "covers" in initial_info:
            cover_filename = f"cover_{context['ds']}.jpg"

            book_record_dict[
                "cover_uri"
            ] = f"s3://{RAW_DATA_BUCKET}/covers/{context['ds']}/{cover_filename}"

        # serialize as JSON string
        book_record_json = json.dumps(book_record_dict)


        book_record_file_name = f"book_record_{context['ds']}.json"
        
   
        # call the `put_object` method of the boto3 client by passing the
        # Raw Data Bucket name to the Bucket parameter, and the 
        # `book_record_json` to the Body parameter
         client.put_object(
            Bucket=RAW_DATA_BUCKET,
            Key=f"book_records/{context['ds']}/{book_record_file_name}",
            Body=book_record_json,
        )
   

    save_final_book_record_task = PythonOperator(
        task_id="save_final_book_record",
        

        python_callable=save_final_book_record,
    )



    def clean_up_intermediate_info(**context):
        # delete initial information file of the logical date by using the
        # `delete_object` method of the boto3 client by passing the bucket
        # name and Key with the path to the object:
        initial_info_file_name = f"initial_info_{context['ds']}.json"

        client.delete_object(
            Bucket=RAW_DATA_BUCKET,
            Key=f"books/{context['ds']}/{initial_info_file_name}",
        )

        
        authors_file_name = f"author_names_{context['ds']}.json"
        

        # delete the authors' names file of the logical date by using the
        # `delete_object` method of the boto3 client by passing the bucket
        # name and Key with the path to the object:
         client.delete_object(
            Bucket=RAW_DATA_BUCKET,
            Key=f"authors/{context['ds']}/{authors_file_name}",
        )




    cleanup_task = PythonOperator(
        task_id="cleanup",
        

        python_callable=clean_up_intermediate_info,

    )

 
    end_task = EmptyOperator(task_id="end")
   


    # define task dependencies to obtain the desired
    # DAG:
     start_task >> get_book_task
    get_book_task >> [get_authors_task, get_cover_task]
    [get_authors_task, get_cover_task] >> save_final_book_record_task
    save_final_book_record_task >> cleanup_task
    cleanup_task >> end_task





///////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////




## Here is a simple DAG which emphasizes Airflow best practices 

"""
DAG Task Descriptions:

1. start: An empty task marking the start of the DAG, executed with DummyOperator. It doesn't perform any operations but creates a task instance in the Airflow metadata database.

2. extract_load_orders: Extracts data from the `orders` table and loads it into the bronze zone in the S3 bucket at:
   s3://<BUCKET_NAME>/bronze/orders/YYYY/MM/DD/
   Implemented using SqlToS3Operator, an Amazon transfer operator to copy data from SQL to S3.

3. transform_orders: Transforms data extracted from the `orders` table and loads it into the silver zone in the S3 bucket at:
   s3://<BUCKET_NAME>/silver/orders/YYYY/MM/DD/
   The transformation drops null records and duplicate rows. Executed using PythonOperator with the `drop_nas_and_duplicates` function.

4. notification: Simulates a notification task by printing the number of rows in the transformed data. Executed using PythonOperator with the `notify_valid_records` function.

5. end: An empty task marking the end of the DAG, executed with DummyOperator.
"""

import datetime as dt
import re
import pandas as pd
from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.transfers.sql_to_s3 import SqlToS3Operator
from airflow.utils.context import Context

S3_URI_PATTERN = r"^s3://[a-zA-Z0-9.\-_]+(/[a-zA-Z0-9.\-_]+)*$"

def drop_nas_and_duplicates(
    source_bucket: str,
    source_key: str,
    target_key: str,
    target_bucket: str = "",
    **context: Context,
):
    if not target_bucket:
        target_bucket = source_bucket

    source_s3_uri = f"s3://{source_bucket}/{source_key}"
    target_s3_uri = f"s3://{target_bucket}/{target_key}"

    assert re.match(S3_URI_PATTERN, source_s3_uri)
    assert re.match(S3_URI_PATTERN, target_s3_uri)

    df = pd.read_csv(source_s3_uri)
    df = df.dropna()
    df = df.drop_duplicates()
    df.to_csv(target_s3_uri, index=False)

    num_valid_records = len(df)
    context["ti"].xcom_push(key="valid_records", value=num_valid_records)

def notify_valid_records(table: str, **context: Context):
    task_id = f"transform_{table}"
    valid_records = context["ti"].xcom_pull(task_ids=task_id, key="valid_records")
    print(f"Number of valid records in table {table}: {valid_records}")

with DAG(
    dag_id="simple_dag",
    schedule="@daily",
    start_date=dt.datetime(year=2024, month=12, day=16),
    catchup=False,
) as dag:
    partition_date = '{{ macros.ds_format(ds, "%Y-%m-%d", "%Y/%m/%d") }}'

    start_task = DummyOperator(task_id="start")

    extract_and_load_task = SqlToS3Operator(
        task_id="extract_and_load_orders",
        sql_conn_id="mysql_connection",
        query="SELECT * FROM orders;",
        s3_bucket=Variable.get("s3_bucket"),
        s3_key=f"bronze/{partition_date}/orders.csv",
        replace=True,
    )

    transform_task = PythonOperator(
        task_id="transform_orders",
        python_callable=drop_nas_and_duplicates,
        provide_context=True,
        op_kwargs={
            "source_bucket": Variable.get("s3_bucket_name"),
            "source_key": f"bronze/{partition_date}/orders.csv",
            "target_key": f"silver/{partition_date}/orders.csv",
        },
    )

    notification_task = PythonOperator(
        task_id="notification",
        python_callable=notify_valid_records,
        provide_context=True,
        op_kwargs={"table": "orders"},
    )

    end_task = DummyOperator(task_id="end")

    start_task >> extract_and_load_task >> transform_task >> notification_task >> end_task






///////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////




## Finally, here is a DAG with grouped tasks 
# Comments on task behavior:
# start: is an empty task marking the start of the DAG. It doesn't include any behavior.
# extract_load_<table>: extracts data from the table <table> and loads it into the S3 bucket (Raw Data Bucket).
#                       The destination path is s3://<BUCKET_NAME>/bronze/<table>/YYYY/MM/DD/.
#                       You will execute this task using the SqlToS3Operator.
# transform_<table>: transforms the data extracted from the table <table> and loads it into another zone of the S3 bucket.
#                    The destination path is s3://<BUCKET_NAME>/silver/<table>/YYYY/MM/DD/.
#                    The transformation also consists of dropping the null records and duplicate rows.
#                    You will also use a PythonOperator which will call the drop_nas_and_duplicates function.


import datetime as dt
import re
import pandas as pd
from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.transfers.sql_to_s3 import SqlToS3Operator
from airflow.utils.context import Context
from airflow.utils.task_group import TaskGroup

S3_URI_PATTERN = r"^s3://[a-zA-Z0-9.\-_]+(/[a-zA-Z0-9.\-_]+)*$"
tables = ["payments", "customers", "products"]

def drop_nas_and_duplicates(
    source_bucket: str,
    source_key: str,
    target_key: str,
    target_bucket: str = "",
    **context: Context,
):
    if not target_bucket:
        target_bucket = source_bucket

    source_s3_uri = f"s3://{source_bucket}/{source_key}"
    target_s3_uri = f"s3://{target_bucket}/{target_key}"

    assert re.match(S3_URI_PATTERN, source_s3_uri)
    assert re.match(S3_URI_PATTERN, target_s3_uri)

    df = pd.read_csv(source_s3_uri)

    df = df.dropna()
    df = df.drop_duplicates()

    df.to_csv(target_s3_uri)

    num_valid_records = len(df)
    context["ti"].xcom_push(key="valid_records", value=num_valid_records)

def notify_valid_records(tables: list[str], **context: Context):
    for table in tables:
        task_id = f"transform_{table}"
        task_id = f"{table}.{task_id}" if len(tables) > 1 else task_id
        
        valid_records = context["ti"].xcom_pull(
            task_ids=[task_id], key="valid_records"
        )

        print(f"Number of valid records in table {table}: {valid_records}")


with DAG(
    dag_id="grouped_tasks_dag",
    schedule="@daily",
    start_date=dt.datetime(year=2024, month=4, day=1),
    catchup=False,
) as dag:
    partition_date = '{{ macros.ds_format(ds, "%Y-%m-%d", "%Y/%m/%d") }}'

    start_task = DummyOperator(task_id="start")

    task_group = []
    for table in tables:
        with TaskGroup(table) as etl_tg:
            
            extract_load_task = SqlToS3Operator(
                task_id=f"extract_load_{table}",
                sql_conn_id="mysql_connection",
                query=f"SELECT * FROM {table};",
                s3_bucket=Variable.get("s3_bucket"),
                s3_key=f"bronze/{partition_date}/{table}.csv",
                replace=True,
            )

            transform_task = PythonOperator(
                task_id=f"transform_{table}",
                python_callable=drop_nas_and_duplicates,
                provide_context=True,
                op_kwargs={
                    "source_bucket": Variable.get("s3_bucket"),
                    "source_key": f"bronze/{partition_date}/{table}.csv",
                    "target_key": f"silver/{partition_date}/{table}.csv",
                },
            )
            
            extract_load_task >> transform_task
            task_group.append(etl_tg)

    notification_task = PythonOperator(
        task_id="notification",
        python_callable=notify_valid_records, 
        provide_context=True,
        op_kwargs={"tables": tables}, 
    )

    end_task = DummyOperator(task_id="end")

    start_task >> task_group >> notification_task >> end_task

