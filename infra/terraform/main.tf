resource "google_bigquery_dataset" "bronze_ecommerce" {
  dataset_id                  = "bronze_ecommerce"
  friendly_name               = "Bronze E-commerce Dataset"
  description                 = "Dataset Raw (Bruto) para receber os dados do PostgreSQL, MongoDB e Kafka via Spark"
  location                    = var.region
  delete_contents_on_destroy  = true
}

resource "google_bigquery_dataset" "silver_ecommerce" {
  dataset_id                  = "silver_ecommerce"
  friendly_name               = "Silver E-commerce Dataset"
  description                 = "Dataset tratado e modelado via dbt"
  location                    = var.region
  delete_contents_on_destroy  = true
}
