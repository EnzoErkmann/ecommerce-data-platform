# Arquivo: infra/terraform/providers.tf

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.87"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Modificação aqui: Agora passamos os argumentos via variáveis controladas do TF
provider "snowflake" {
  user              = var.snowflake_user
  password          = var.snowflake_password
  account_name      = var.snowflake_account_name
  organization_name = var.snowflake_organization_name
  role              = "ACCOUNTADMIN"
}
