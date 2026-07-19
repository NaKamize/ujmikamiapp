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

variable "terraform_operator_principal_ids" {
  description = "Azure AD object IDs (human users and/or service principals) granted Key Vault Secrets Officer so they can manage secrets via Terraform. Fixed list, independent of whichever identity happens to be running a given plan/apply."
  type        = list(string)
  default = [
    "5731fd27-fb2a-4dd3-b4b5-e709cb8980b0",
    "4c0cd6ef-89ab-49f9-9184-1eed4afbb869",
  ]
}
