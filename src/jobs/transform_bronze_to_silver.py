from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def main():
    print("Iniciando Job de Transformação (Bronze -> Silver)...")

    spark = SparkSession.builder.appName("Bronze_to_Silver").getOrCreate()

    # 1. Lê a Camada Bronze
    df = spark.read.parquet("/opt/airflow/data/bronze/clientes")

    # 2. Transformação (Limpeza)
    # Exemplo: remover e-mails nulos e padronizar nomes para maiúsculas
    df_silver = (
        df.filter(F.col("email").isNotNull())
        .withColumn("nome", F.upper(F.col("nome")))
        .withColumn("data_processamento", F.current_timestamp())
    )

    # 3. Salva na Camada Silver
    output_path = "/opt/airflow/data/silver/clientes"
    df_silver.write.mode("overwrite").parquet(output_path)

    print(f"Dados refinados salvos em: {output_path}")
    df_silver.show(5)

    spark.stop()
    print("Job finalizado.")


if __name__ == "__main__":
    main()
