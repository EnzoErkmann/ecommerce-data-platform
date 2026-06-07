import os
import sys
from pyspark.sql import SparkSession


def main():
    print("Iniciando Job de Carga para o BigQuery (Modo Direct)...")

    project_id = os.getenv("GCP_PROJECT_ID")
    dataset = os.getenv("GCP_DATASET")
    key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not all([project_id, dataset, key_path]):
        print("ERRO: Variáveis de ambiente obrigatórias não estão definidas.")
        sys.exit(1)

    # 1. Usamos APENAS o conector do BigQuery (adeus, conflito de JARs!)
    spark = (
        SparkSession.builder.appName("Load_to_BigQuery")
        .config(
            "spark.jars.packages",
            "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.30.0",
        )
        .getOrCreate()
    )

    # 2. Autenticação pura do BigQuery
    spark.conf.set("google.cloud.auth.service.account.json.keyfile", key_path)

    try:
        df = spark.read.parquet("/opt/airflow/data/silver/clientes")
        print(
            "Dados da Silver lidos com sucesso. Iniciando escrita DIRETA no BigQuery..."
        )

        # 3. O Pulo do Gato: writeMethod("direct")
        df.write.format("bigquery").option(
            "table", f"{project_id}.{dataset}.clientes"
        ).option("writeMethod", "direct").mode("overwrite").save()

        print("Carga concluída com sucesso no BigQuery!")
    except Exception as e:
        print(f"Falha na carga: {e}")
        sys.exit(1)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
