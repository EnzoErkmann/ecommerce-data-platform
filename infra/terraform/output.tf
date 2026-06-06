# Arquivo: /infra/terraform/outputs.tf
output "bronze_dataset_id" {
  description = "ID do Dataset da Camada Bronze no BigQuery"
  value       = google_bigquery_dataset.bronze_ecommerce.dataset_id
}

output "silver_dataset_id" {
  description = "ID do Dataset da Camada Silver no BigQuery"
  value       = google_bigquery_dataset.silver_ecommerce.dataset_id
}

output "gcp_project" {
  description = "Projeto do GCP onde a infraestrutura foi provisionada"
  value       = var.project_id
}
