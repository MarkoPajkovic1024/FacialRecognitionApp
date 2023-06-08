variable "prefix" {
  default = "paad"
}

variable "project" {
  default = "patients-app-api-devops"
}

variable "contact" {
  default = "sahara.sheikholeslami@gmail.com"
}

variable "db_username" {
  description = "Username for the RDS Postgres instance"
}

variable "db_password" {
  description = "Password for the RDS postgres instance"
}

variable "bastion_key_name" {
  default = "patients-app-api-devops-bastion"
}

variable "ecr_image_api" {
  description = "ECR Image for API"
  default     = "595592471409.dkr.ecr.us-east-1.amazonaws.com/patients-app-api-devops:latest"
}

variable "ecr_image_proxy" {
  description = "ECR Image for API"
  default     = "595592471409.dkr.ecr.us-east-1.amazonaws.com/patients-app-api-proxy:latest"
}

variable "django_secret_key" {
  description = "Secret key for Django app"
}

variable "dns_zone_name" {
  description = "Domain name"
  default     = "rostro-authentication.com"
}

variable "subdomain" {
  description = "Subdomain per environment"
  type        = map(string)
  default = {
    production = "api"
    staging    = "api.staging"
    dev        = "api.dev"
  }
}
