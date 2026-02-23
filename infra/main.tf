# KAN-464: Basic infrastructure configuration for GCP
# This setup provisions resources based on the project's user stories.

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable necessary APIs for the project
resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "firestore.googleapis.com",
    "bigquery.googleapis.com",
    "cloudscheduler.googleapis.com",
    "cloudbuild.googleapis.com",
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "storage.googleapis.com"
  ])
  service                    = each.key
  disable_dependent_services = true
}

# KAN-536, KAN-537: Firestore Database for transactional data
resource "google_firestore_database" "database" {
  project                 = var.project_id
  name                    = "(default)"
  location_id             = var.region
  type                    = "FIRESTORE_NATIVE"
  delete_protection_state = "DELETE_PROTECTION_DISABLED" # For dev environment
  depends_on              = [google_project_service.apis]
}

# KAN-536, KAN-537: BigQuery for analytics and reporting
resource "google_bigquery_dataset" "default" {
  dataset_id                 = "mall_plaza_analytics"
  friendly_name              = "Mall Plaza Analytics"
  description                = "Dataset for analytics and reporting"
  location                   = var.region
  delete_contents_on_destroy = true # For dev environment
  depends_on                 = [google_project_service.apis]
}

# Placeholder for BigQuery tables. Schemas will be defined by the application.
# Example for 'modulos' table mentioned in KAN-536
resource "google_bigquery_table" "modulos" {
  dataset_id          = google_bigquery_dataset.default.dataset_id
  table_id            = "modulos"
  deletion_protection = false # For dev environment

  schema = <<EOF
[
  {"name": "id", "type": "STRING", "mode": "REQUIRED"},
  {"name": "nombre", "type": "STRING", "mode": "NULLABLE"},
  {"name": "piso", "type": "INTEGER", "mode": "NULLABLE"},
  {"name": "centroComercialId", "type": "STRING", "mode": "NULLABLE"},
  {"name": "dimensiones", "type": "STRING", "mode": "NULLABLE"},
  {"name": "estado", "type": "STRING", "mode": "NULLABLE"},
  {"name": "is_active", "type": "BOOLEAN", "mode": "NULLABLE", "description": "Used for soft deletes from Firestore"},
  {"name": "timestamp", "type": "TIMESTAMP", "mode": "NULLABLE"}
]
EOF
}

# KAN-509, KAN-551: Cloud Run service for the backend API
resource "google_cloud_run_v2_service" "default" {
  name     = "api-${var.project_name}-${var.environment}"
  location = var.region

  template {
    containers {
      image = "gcr.io/cloud-run/placeholder" # Placeholder image
      ports {
        container_port = 8080
      }
    }
  }
  depends_on = [google_project_service.apis]
}

# Allow unauthenticated access to Cloud Run for now (for easy testing)
resource "google_cloud_run_v2_service_iam_binding" "allow_unauthenticated" {
  project  = google_cloud_run_v2_service.default.project
  location = google_cloud_run_v2_service.default.location
  name     = google_cloud_run_v2_service.default.name
  role     = "roles/run.invoker"
  members = [
    "allUsers",
  ]
}

# Service account for the scheduler to invoke Cloud Run
resource "google_service_account" "scheduler_invoker" {
  account_id   = "scheduler-invoker-${var.environment}"
  display_name = "Service Account for Cloud Scheduler to invoke Cloud Run"
}

resource "google_project_iam_member" "scheduler_run_invoker" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.scheduler_invoker.email}"
}

# KAN-517: Cloud Scheduler for inactivity checks
resource "google_cloud_scheduler_job" "inactivity_check" {
  name        = "inactivity-check-${var.environment}"
  description = "Checks for inactive shopping centers"
  schedule    = "0 2 * * *" # Every day at 2 AM
  time_zone   = "UTC"

  http_target {
    http_method = "POST"
    uri         = "${google_cloud_run_v2_service.default.uri}/tasks/check-inactivity"
    # OIDC token is needed for secure invocation
    oidc_token {
      service_account_email = google_service_account.scheduler_invoker.email
    }
  }
  depends_on = [google_project_service.apis, google_project_iam_member.scheduler_run_invoker]
}

# KAN-554, KAN-555: Cloud Storage bucket for backups
resource "google_storage_bucket" "backups" {
  name          = "${var.project_id}-backups-${var.environment}"
  location      = var.region
  force_destroy = true # For dev environment

  # KAN-554, KAN-555: Configure retention policy
  retention_policy {
    retention_period = 7776000 # 90 days in seconds
  }
  depends_on = [google_project_service.apis]
}
