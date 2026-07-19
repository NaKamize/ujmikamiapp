variable "mysql_admin_password" {
  description = "Existing admin password for the ujmikami-db MySQL Flexible Server (Azure never exposes this back via the API, so it must be supplied — set via TF_VAR_mysql_admin_password)."
  type        = string
  sensitive   = true
}

variable "django_secret_key" {
  description = "Django SECRET_KEY for production (set via TF_VAR_django_secret_key)."
  type        = string
  sensitive   = true
}
