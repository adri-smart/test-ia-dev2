variable "project_name" {
  description = "The name of the project."
  type        = string
  default     = "kan463-agent"
}

variable "environment" {
  description = "The deployment environment."
  type        = string
  default     = "dev"
}

variable "location" {
  description = "The Azure region for deployment."
  type        = string
  default     = "West Europe"
}
