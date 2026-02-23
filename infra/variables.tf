variable "project_name" {
  description = "The name of the project, used for naming resources."
  type        = string
  default     = "mall-plaza-manager"
}

variable "project_id" {
  description = "The GCP project ID to deploy resources into."
  type        = string
}

variable "environment" {
  description = "The deployment environment."
  type        = string
  default     = "dev"
}

variable "region" {
  description = "The GCP region for deployment."
  type        = string
  default     = "europe-west1"
}
