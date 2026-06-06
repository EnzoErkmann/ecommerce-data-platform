# E-Commerce Real-Time Data Platform (Projeto de Engenharia de Dados)

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)
![Docker](https://img.shields.io/badge/Docker_Compose-Infrastructure-2496ED?style=for-the-badge&logo=docker)
![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-Streaming-black?style=for-the-badge&logo=apachekafka)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Relational_DB-4169E1?style=for-the-badge&logo=postgresql)
![MongoDB](https://img.shields.io/badge/MongoDB-NoSQL_Document-47A248?style=for-the-badge&logo=mongodb)
![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=for-the-badge&logo=terraform)

## 📌 Visão Geral do Projeto
Este repositório armazena o **Projeto Eng Dados - 1**, uma plataforma de dados híbrida (Local + Cloud) focada em processamento **Batch e Streaming** para o ecossistema de um E-commerce. O objetivo principal deste projeto é demonstrar senioridade, visão de arquitetura End-to-End e o domínio das melhores práticas de engenharia de software aplicadas a dados.

Em vez de importar arquivos `.csv` estáticos e irrealistas, a plataforma gera seus próprios dados sintéticos de forma massiva e contínua, simulando o comportamento de usuários reais em produção (transações, catálogos flexíveis e eventos de navegação).

---

## 🏛️ Arquitetura e Decisões Técnicas

A fundação local do ecossistema foi projetada para simular três paradigmas distintos de origens de dados de mercado:

* **Dados Estruturados (PostgreSQL):** Atua como o banco transacional central. Armazena dados que exigem consistência ACID rigorosa, como o cadastro de `clientes` e registros de `compras`.
* **Dados Semi-Estruturados / Documentais (MongoDB):** Atua como o catálogo de `produtos`. Utiliza o paradigma NoSQL *Schema-less* para suportar especificações técnicas altamente variadas de produtos convivendo na mesma coleção sem o desperdício de colunas nulas.
* **Dados em Streaming / Tempo Real (Apache Kafka):** Atua como o sistema nervoso da plataforma. Captura de forma contínua o *Clickstream* (telemetria de navegação e cliques dos usuários no site), ordenando os eventos cronologicamente por cliente através de chaves de partição hashing.

---

## 📂 Estrutura do Repositório

O projeto adota o princípio de *Separation of Concerns* (Separação de Responsabilidades), garantindo um repositório limpo, escalável e de fácil manutenção:

```text
ecommerce-data-platform/
├── .github/workflows/    # Esteiras automatizadas de CI/CD (Fase 5)
├── infra/                # IaC: Configurações Docker Compose e arquivos Terraform (.tf)
├── src/                  # Scripts Python (Geradores sintéticos, jobs Spark, produtores Kafka)
├── dags/                 # Pipelines de orquestração do Apache Airflow
├── dbt/                  # Camada de Analytics Engineering (Transformações lógicas)
├── tests/                # Malha de testes unitários e de integração com pytest
├── .env                  # Variáveis de ambiente locais (Ignorado pelo Git por segurança)
├── .env.example          # Modelo de configuração de credenciais públicas
├── .gitignore            # Filtro de blindagem de arquivos para o Git
├── .pre-commit-config.yaml # Manual de instruções de qualidade e linters locais
└── requirements.txt      # Gerenciamento estrito de dependências raízes

## Governança e CI/CD Locais

A qualidade do código e a segurança da informação são tratadas como prioridades absolutas desde a linha zero do desenvolvimento:

### 1. Git Hooks e Qualidade de Estilo (PEP-8)
O projeto utiliza a biblioteca pre-commit acoplada aos ganchos nativos do Git (.git/hooks). Toda vez que um comando git commit é disparado, uma esteira de validação local é executada automaticamente:
* **trailing-whitespace & end-of-file-fixer:** Limpam espaços em branco inúteis e garantem a quebra de linha padrão POSIX no fim dos arquivos.
* **check-added-large-files:** Trava de segurança que impede o commit acidental de arquivos brutos pesados (como logs ou datasets), mantendo o repositório leve.
* **Ruff:** Linter e formatador de código Python de alta performance. Garante de forma estrita que todo o código escrito siga as boas práticas da PEP-8 antes de subir para o GitHub Actions.

### 2. Blindagem de Credenciais e Segurança (.env)
Seguindo o padrão de mercado para repositórios públicos, nenhuma credencial de acesso ou senha foi deixada como hardcoded code.
* Os parâmetros de autenticação foram isolados na raiz em um arquivo .env.
* O arquivo .gitignore foi configurado na raiz para garantir que senhas locais e ambientes virtuais nunca vazem para a nuvem.
* O docker-compose.yml consome essas variáveis dinamicamente via interpolação (${VARIAVEL}), e os scripts Python realizam a leitura segura utilizando a biblioteca python-dotenv.

---

## Como Executar o Projeto Localmente

### Pré-requisitos
* Python 3.10 ou superior
* Docker e Docker Desktop ativos
* Git

### Passo a Passo

1. **Clone o repositório para a sua máquina host:**
   ```bash
   git clone [https://github.com/seu-usuario/ecommerce-data-platform.git](https://github.com/seu-usuario/ecommerce-data-platform.git)
   cd ecommerce-data-platform

depois ei continuo o README...
