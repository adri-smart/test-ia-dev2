output "cloud_run_service_url" {
  description = "La URL del servicio de Cloud Run desplegado."
  value       = google_cloud_run_v2_service.backend_api.uri
}

output "redis_instance_host" {
  description = "El host de la instancia de Redis."
  value       = google_redis_instance.cache.host
}
