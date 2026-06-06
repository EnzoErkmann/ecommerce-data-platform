from confluent_kafka import Producer
from faker import Faker
import json
import time
import random
import uuid
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

# Inicializa o gerador de dados falsos com localização brasileira

fake = Faker("pt_BR")

# Configuração do Produtor Kafka

# O bootstrap.servers aponta para o Listener externo que foi configurado  no docker-compose
KAFKA_CONFIG = {
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    "client.id": "gerador-clickstream-local",
}

TOPICO = "ecommerce_clickstream"


def delivery_report(err, msg):
    """Callback (Retorno) chamado quando a mensagem é entregue ou falha."""
    if err is not None:
        print(f"Erro ao entregar mensagem: {err}")
    else:
        print(
            f"Evento entregue: Tópico {msg.topic()} | Partição {msg.partition()} | Offset {msg.offset()}"
        )


def gerar_evento_navegacao():
    """Gera um dicionário simulando uma ação de um usuário no site."""
    tipos_evento = [
        "view_homepage",
        "view_product",
        "add_to_cart",
        "remove_from_cart",
        "checkout_started",
    ]

    evento = {
        "id_evento": str(uuid.uuid4()),
        "id_cliente": random.randint(1, 100),  # Reaproveita os IDs gerados no Postgres
        "id_produto": random.randint(1, 50)
        if random.random() > 0.3
        else None,  # Alguns eventos não têm produto associado
        "tipo_evento": random.choice(tipos_evento),
        "plataforma": random.choice(["Web", "iOS", "Android"]),
        "timestamp": datetime.now(timezone.utc).isoformat(),  # Padrão UTC
    }
    return evento


def iniciar_streaming():
    produtor = Producer(KAFKA_CONFIG)
    print(
        f"Iniciando transmissão de eventos para o tópico '{TOPICO}'... Pressione Ctrl+C para parar."
    )

    try:
        while True:
            evento = gerar_evento_navegacao()

            # Serialização: O Kafka só entende BYTES. Precisamos converter o dicionário Python para JSON, e depois para Bytes (utf-8)
            evento_json = json.dumps(evento).encode("utf-8")

            # Produz a mensagem no Kafka
            produtor.produce(
                topic=TOPICO,
                key=str(evento["id_cliente"]).encode(
                    "utf-8"
                ),  # A chave garante que cliques do mesmo cliente caiam na mesma partição
                value=evento_json,
                callback=delivery_report,
            )

            # O poll() serve pro produtor processar os callbacks de sucesso/erro
            produtor.poll(0)

            # Simula o tempo de navegação de um usuário real (entre 0.5 e 2 segundos)
            time.sleep(random.uniform(0.5, 2.0))

    except KeyboardInterrupt:
        print("\nTransmissão interrompida pelo usuário.")
    finally:
        # Garante que todas as mensagens que estão na memória RAM sejam enviadas antes do script desligar
        print("Limpando buffer do Kafka (Flush)...")
        produtor.flush()
        print("Finalizado com sucesso.")


if __name__ == "__main__":
    iniciar_streaming()
