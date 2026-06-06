import psycopg2
from psycopg2 import extras
from faker import Faker
import random
import os
from dotenv import load_dotenv

load_dotenv()

# Inicializa o gerador de dados falsos com localização brasileira
fake = Faker("pt_BR")

# DDL (Data Definition Language) -O Schema

DDL_CLIENTES = """
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    estado VARCHAR(2) NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

DDL_COMPRAS = """
CREATE TABLE IF NOT EXISTS compras (
    id_compra SERIAL PRIMARY KEY,
    id_cliente INT REFERENCES clientes(id_cliente),
    valor_total DECIMAL(10, 2) NOT NULL,
    metodo_pagamento VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    data_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Lógica de Negócio e Inserção


def obter_conexao():
    """Cria e retorna a conexão com o PostgreSQL local via Docker."""
    return psycopg2.connect(
        host="localhost",  # Como o Python está rodando na sua máquina, acessamos via localhost
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def gerar_clientes(qtd):
    """Gera uma lista de tuplas contendo dados falsos de clientes."""
    return [(fake.name(), fake.unique.email(), fake.estado_sigla()) for _ in range(qtd)]


def gerar_compras(qtd, max_id_cliente):
    """Gera uma lista de tuplas contendo dados falsos de compras."""
    metodos = ["PIX", "Cartão de Crédito", "Boleto"]
    status = ["Aprovado", "Pendente", "Cancelado"]

    compras = []
    for _ in range(qtd):
        id_cliente = random.randint(1, max_id_cliente)
        valor = round(random.uniform(20.0, 5000.0), 2)
        pagamento = random.choice(metodos)
        stat = random.choice(status)
        compras.append((id_cliente, valor, pagamento, stat))

    return compras


def popular_banco():
    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        # Cria as tabelas
        print("Criando tabelas...")
        cursor.execute(DDL_CLIENTES)
        cursor.execute(DDL_COMPRAS)
        conexao.commit()

        # Gera os dados
        print("Gerando dados sintéticos...")
        dados_clientes = gerar_clientes(100)  # Gerando 100 clientes

        # Insere Clientes (Batch Insert)
        print("Inserindo clientes...")
        extras.execute_values(
            cursor,
            "INSERT INTO clientes (nome, email, estado) VALUES %s",
            dados_clientes,
        )
        conexao.commit()

        # Insere Compras (Batch Insert)
        print("Inserindo compras...")
        dados_compras = gerar_compras(300, 100)  # 300 compras diluídas em 100 clientes
        extras.execute_values(
            cursor,
            "INSERT INTO compras (id_cliente, valor_total, metodo_pagamento, status) VALUES %s",
            dados_compras,
        )
        conexao.commit()

        print("Carga inicial finalizada com sucesso!")

    except Exception as e:
        print(f"Erro ao processar dados: {e}")
        conexao.rollback()  #
    finally:
        cursor.close()
        conexao.close()


if __name__ == "__main__":
    popular_banco()
