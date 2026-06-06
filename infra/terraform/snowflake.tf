# Arquivo: /infra/terraform/snowflake.tf

# 1. Motor de Processamento (Compute)
resource "snowflake_warehouse" "ecommerce_wh" {
  name           = "ECOMMERCE_WH"
  warehouse_size = "XSMALL"
  auto_suspend   = 60     # Desliga automaticamente após 60 segundos de inatividade para poupar créditos
  auto_resume    = true   # Liga automaticamente quando uma query for feita
}

# 2. Banco de Dados (Storage)
resource "snowflake_database" "ecommerce_db" {
  name = "ECOMMERCE_DB"
}

# 3. Camadas Lógicas (Arquitetura Medalhão)
resource "snowflake_schema" "bronze_schema" {
  database = snowflake_database.ecommerce_db.name
  name     = "BRONZE"
}

resource "snowflake_schema" "silver_schema" {
  database = snowflake_database.ecommerce_db.name
  name     = "SILVER"
}
