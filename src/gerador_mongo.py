from pymongo import MongoClient
from faker import Faker
import random
import os
from dotenv import load_dotenv

load_dotenv()


# Inicializa o gerador de dados falsos
fake = Faker("pt_BR")


# Lógica de Negócio e Inserção (NoSQL)
def obter_conexao_mongo():
    """Cria e retorna a conexão com a coleção 'produtos' no MongoDB local."""
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("MONGO_PORT")

    # A string de conexão usa os dados definidos no docker-compose.yml
    uri = f"mongodb://{user}:{password}@localhost:{port}/?authSource=admin"  # esse auth source admin serve pra dizer pro mongo procurar as variaveis no banco admin
    cliente = MongoClient(uri)
    banco = cliente["ecommerce_db"]
    return banco["produtos"]  # Retorna a Collection (equivalente a uma Tabela no SQL)


def gerar_produtos(qtd):
    """Gera uma lista de dicionários (documentos JSON) simulando produtos variados."""
    categorias = ["Eletrônicos", "Vestuário", "Casa", "Livros"]
    produtos = []

    for _ in range(qtd):
        categoria = random.choice(categorias)

        # Estrutura base comum a todos os produtos
        produto = {
            "nome_produto": fake.word().capitalize(),
            "categoria": categoria,
            "preco": round(random.uniform(15.0, 1500.0), 2),
            "estoque_disponivel": random.randint(0, 100),
            "especificacoes_tecnicas": {},  # Aqui mora o poder do NoSQL!
        }

        # Atributos dinâmicos baseados na categoria
        if categoria == "Eletrônicos":
            produto["especificacoes_tecnicas"]["voltagem"] = random.choice(
                ["110V", "220V", "Bivolt"]
            )
            produto["especificacoes_tecnicas"]["garantia_meses"] = random.choice(
                [12, 24, 36]
            )
        elif categoria == "Vestuário":
            produto["especificacoes_tecnicas"]["tamanho"] = random.choice(
                ["P", "M", "G", "GG"]
            )
            produto["especificacoes_tecnicas"]["cor"] = fake.safe_color_name()

        produtos.append(produto)

    return produtos


def popular_mongo():
    colecao = obter_conexao_mongo()

    try:
        # Limpeza opcional: Garante que não teremos dados duplicados se você rodar o script 2 vezes
        colecao.delete_many({})
        print("Coleção anterior limpa.")

        # Gera os dados
        print("Gerando catálogo de produtos (NoSQL)...")
        dados_produtos = gerar_produtos(50)

        # Insere os Produtos (Batch Insert / Insert Many)
        print("Inserindo produtos no MongoDB...")
        resultado = colecao.insert_many(dados_produtos)

        print(
            f"Carga NoSQL finalizada! {len(resultado.inserted_ids)} produtos inseridos com sucesso."
        )

    except Exception as e:
        print(f"Erro ao processar dados no MongoDB: {e}")


if __name__ == "__main__":
    popular_mongo()
