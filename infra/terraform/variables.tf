# Arquivo atualizado: /infra/terraform/variables.tf
variable "project_id" {
  type        = string
  description = "ID do projeto no Google Cloud"
}

variable "region" {
  type        = string
  description = "Região principal dos recursos"
}

variable "snowflake_user" {
  type        = string
  description = "Usuário do Snowflake"
}

variable "snowflake_password" {
  type        = string
  description = "Senha do Snowflake"
  sensitive   = true
}

variable "snowflake_organization_name" {
  type        = string
  description = "Nome da organização no Snowflake"
}

variable "snowflake_account_name" {
  type        = string
  description = "Nome da conta no Snowflake"
}
