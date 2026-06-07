from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Configurações padrão da DAG
default_args = {
    "owner": "engenheiro_dados",
    "depends_on_past": False,
    "start_date": datetime(2026, 6, 7),
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Definição da DAG
with DAG(
    "processamento_vendas_dag",
    default_args=default_args,
    description="Pipeline de extração do Postgres para Parquet",
    schedule_interval="@daily",
    catchup=False,
) as dag:
    # Esses coisos aqui são basicamente os arquivos que vão rodar e em baixo a ordem
    # A Task que dispara o job PySpark de extranção
    # Usa o BashOperator para chamar o Python exatamente como você fez no terminal
    extract_task = BashOperator(
        task_id="extract_clientes_to_bronze",
        bash_command="python /opt/airflow/jobs/extract_postgres.py",
    )
    # A Task que dispara o job PySpark bronze -> silver
    transform_task = BashOperator(
        task_id="transform_silver",
        bash_command="python /opt/airflow/jobs/transform_bronze_to_silver.py",
    )

    load_task = BashOperator(
        task_id="load_to_bigquery",
        bash_command="python /opt/airflow/jobs/load_to_bigquery.py",
    )
    # Definição da ordem de execução dos de cima
    extract_task >> transform_task >> load_task
