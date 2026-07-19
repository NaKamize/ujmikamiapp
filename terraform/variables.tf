variable "mysql_admin_password" {
  description = "Existing admin password for the ujmikami-db MySQL Flexible Server."
  type        = string
  sensitive   = true
}

variable "django_secret_key" {
  description = "Django SECRET_KEY for production (TF_VAR_django_secret_key)."
  type        = string
  sensitive   = true
}
