data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "main" {
  name                       = "ujmikami-kv"
  location                   = azurerm_resource_group.resource_groups-ujmikamiapp20.location
  resource_group_name        = azurerm_resource_group.resource_groups-ujmikamiapp20.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  rbac_authorization_enabled = true
  soft_delete_retention_days = 7
  purge_protection_enabled = false
}

resource "azurerm_role_assignment" "terraform_secrets_officer" {
  for_each             = toset(var.terraform_operator_principal_ids)
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = each.value
}

resource "azurerm_role_assignment" "container_app_secrets_user" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id          = azurerm_container_app.container_apps-ujmikamiapp_env0.identity[0].principal_id
}

resource "azurerm_key_vault_secret" "django_secret_key" {
  name         = "django-secret-key"
  value        = var.django_secret_key
  key_vault_id = azurerm_key_vault.main.id
  depends_on   = [azurerm_role_assignment.terraform_secrets_officer]
}

resource "azurerm_key_vault_secret" "mysql_database_url" {
  name         = "mysql-database-url"
  value        = "mysql://nakamize:${var.mysql_admin_password}@ujmikami-db.mysql.database.azure.com:3306/ujmikamiapp"
  key_vault_id = azurerm_key_vault.main.id
  depends_on   = [azurerm_role_assignment.terraform_secrets_officer]
}

resource "azurerm_key_vault_secret" "acr_admin_password" {
  name         = "acr-admin-password"
  value        = azurerm_container_registry.registries-ujmikamiacr0.admin_password
  key_vault_id = azurerm_key_vault.main.id
  depends_on   = [azurerm_role_assignment.terraform_secrets_officer]
}

resource "azurerm_key_vault_secret" "storage_account_key" {
  name         = "storage-account-key"
  value        = azurerm_storage_account.storage_accounts-ujmikamiblob0.primary_access_key
  key_vault_id = azurerm_key_vault.main.id
  depends_on   = [azurerm_role_assignment.terraform_secrets_officer]
}
