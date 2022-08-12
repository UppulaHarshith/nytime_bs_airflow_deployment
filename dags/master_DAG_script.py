"""
DAG file for extracting best sellers and sending weekly emails

Author : Harshith Uppula
Date created: 08/09/2022
Date modified: 08/11/2022
"""

#import statements
import requests
from datetime import date, datetime, timedelta, timezone
from struct import Struct
from airflow import DAG
from airflow.models.variable import Variable
from airflow.utils import dates, timezone
from nytimes_bestsellers_extract import nytimes_api_trigger
from email_trigger import send_email
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

last_modified_old = Variable.get('last_modified_old', default_var="")

if last_modified_old == "":
    Variable.set('last_modified_old', "")


def get_bestsellers_xcom(**kwargs):
    """
        get final string of the bestsellers
    """
    xcom_pull_str, last_modified_new = kwargs["ti"].xcom_pull(
        dag_id = 'nytimes_bestsellers_extract',
        task_ids='extract_bestsellers',
        key='return_value')

    Variable.set('xcom_pull_str', str(xcom_pull_str))
    Variable.set('last_modified_new', str(last_modified_new))

DEFAULT_DAG_ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 4,
    'retry_delay': timedelta(seconds=20)
}


nytimes_bestsellers_extract = DAG(
    dag_id='nytimes_bestsellers_extract',
    catchup=False,
    start_date=dates.days_ago(1),
    schedule_interval="0 0 * * *",
    default_args=DEFAULT_DAG_ARGS,
    params={"name" : ["huppula2@gmail.com", "venkatsairao1@gmail.com"]}
)

# Dummy operator before starting the tasks
START_OP = DummyOperator(task_id="START",
                       dag=nytimes_bestsellers_extract)


# Task to extract bestsellers from Nytimes API
extract_bestsellers_from_API = PythonOperator(
    task_id='extract_bestsellers',
    python_callable=nytimes_api_trigger,
    provide_context=True,
    dag=nytimes_bestsellers_extract
)

# Get xcom pull string from extract_bestsellers_from_API function
get_xcom_string = PythonOperator(
    task_id="get_xcom_pull_str",
    python_callable=get_bestsellers_xcom,
    provide_context=True,
    dag=nytimes_bestsellers_extract
)

final_str = Variable.get('xcom_pull_str', default_var='empty_string')

# Task to trigger email_trigger.py
email_trigger = PythonOperator(
    task_id="weekly_email_trigger",
    python_callable=send_email,
    op_kwargs={'final_str' : final_str, 'receiver' : "{{ params.name}}" },
    provide_context=True
)

# Dummy operator after finishing the tasks
END_OP = DummyOperator(task_id="END",
                       dag=nytimes_bestsellers_extract)


START_OP.set_downstream(extract_bestsellers_from_API)
extract_bestsellers_from_API.set_downstream(get_xcom_string)

last_modified_new = Variable.get('last_modified_new', default_var='empty_string')
last_modified_old = Variable.get('last_modified_old', default_var='empty_string')


if  (last_modified_new != last_modified_old) :
    get_xcom_string.set_downstream(email_trigger)
    email_trigger.set_downstream(END_OP)
else :
    get_xcom_string.set_downstream(END_OP)

Variable.set('last_modified_old', str(last_modified_new))
