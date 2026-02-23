variable "project_name" {
  description = "El nombre del proyecto, usado para nombrar recursos."
  type        = string
  default     = "customer-analysis-agent"
}

variable "project_id" {
  description = "El ID del proyecto de GCP donde se desplegarán los recursos."
  type        = string
}

variable "environment" {
  description = "El entorno de despliegue."
  type        = string
  default     = "dev"
}

variable "region" {
  description = "La región de GCP para el despliegue."
  type        = string
  default     = "europe-west1"
}
