# Arquivo atualizado: /infra/terraform/variables.tf
variable "project_id" {
  type        = string
  description = "ID do projeto no Google Cloud"
}

variable "region" {
  type        = string
  description = "Região principal dos recursos"
}
