import os
import sys
from pyspark.sql import SparkSession


def main():
    print("Iniciando o Job de Extração do PostgreSQL...")

    # Coleta de variáveis de ambiente
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")

    # Validação rigorosa (Fail-Fast)
    if not db_user or not db_password or not db_name:
        print("[ERRO FATAL] Credenciais de banco de dados não encontradas no ambiente.")
        sys.exit(1)

    # Inicializa a Spark Session
    spark = (
        SparkSession.builder.appName("Extract_Postgres_Bronze")
        .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0")
        .getOrCreate()
    )

    db_host = "pg_transacional"
    db_port = "5432"
    table_name = "clientes"

    jdbc_url = f"jdbc:postgresql://{db_host}:{db_port}/{db_name}"

    try:
        # Extração dos dados
        df = (
            spark.read.format("jdbc")
            .option("url", jdbc_url)
            .option("dbtable", table_name)
            .option("user", db_user)
            .option("password", db_password)
            .option("driver", "org.postgresql.Driver")
            .load()
        )

        # Salvando na camada Bronze em Parquet
        output_path = "/opt/airflow/data/bronze/clientes"
        df.write.mode("overwrite").parquet(output_path)

        print(f"Dados extraídos e salvos em: {output_path}")
        df.show(5)

    except Exception as e:
        print(f"[ERRO] Falha na execução: {e}")

    finally:
        spark.stop()
        print("Job finalizado.")


if __name__ == "__main__":
    main()
