# KAN-464: Configuración de infraestructura base para GCP
# Esta configuración provisiona recursos para el Agente Conversacional de Análisis de Clientes.

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

# Habilitar las APIs necesarias para el proyecto
resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",        # Cloud Run
    "redis.googleapis.com",      # Memorystore for Redis
    "cloudbuild.googleapis.com", # Cloud Build para CI/CD
    "iam.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudresourcemanager.googleapis.com"
  ])
  service                    = each.key
  disable_dependent_services = true
}

# Servicio de Cloud Run para la API del backend
resource "google_cloud_run_v2_service" "backend_api" {
  name     = "api-${var.project_name}-${var.environment}"
  location = var.region

  template {
    containers {
      image = "gcr.io/${var.project_id}/${var.project_name}-api:latest" # Imagen de ejemplo
      ports {
        container_port = 5000 # Puerto de Flask
      }
      env {
        name  = "REDIS_HOST"
        value = google_redis_instance.cache.host
      }
      env {
        name  = "REDIS_PORT"
        value = google_redis_instance.cache.port
      }
    }
  }
  depends_on = [google_project_service.apis]
}

# Permitir acceso no autenticado a Cloud Run para pruebas fáciles
resource "google_cloud_run_v2_service_iam_binding" "allow_unauthenticated" {
  project  = google_cloud_run_v2_service.backend_api.project
  location = google_cloud_run_v2_service.backend_api.location
  name     = google_cloud_run_v2_service.backend_api.name
  role     = "roles/run.invoker"
  members = [
    "allUsers",
  ]
}

# KAN-490: Instancia de Redis (Memorystore) para la caché
resource "google_redis_instance" "cache" {
  name           = "redis-cache-${var.environment}"
  tier           = "BASIC"
  memory_size_gb = 1
  location_id    = "${var.region}-a"
  
  depends_on = [google_project_service.apis]
}
