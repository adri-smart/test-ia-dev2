output "cloud_run_service_url" {
  description = "The URL of the deployed Cloud Run service."
  value       = google_cloud_run_v2_service.default.uri
}

output "bigquery_dataset_id" {
  description = "The ID of the BigQuery dataset."
  value       = google_bigquery_dataset.default.dataset_id
}

output "firestore_database_name" {
  description = "The name of the Firestore database."
  value       = google_firestore_database.database.name
}

output "backup_bucket_name" {
  description = "The name of the Cloud Storage bucket for backups."
  value       = google_storage_bucket.backups.name
}
