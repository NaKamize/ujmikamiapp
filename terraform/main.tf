resource "azurerm_resource_group" "resource_groups-ujmikamiapp20" {
  location = "westeurope"
  name     = "ujmikamiapp2"
}
resource "azurerm_container_app" "container_apps-ujmikamiapp_env0" {
  container_app_environment_id = azurerm_container_app_environment.managed_environments-ujmikamiapp_env_env0.id
  max_inactive_revisions       = 100
  name                         = "ujmikamiapp-env"
  resource_group_name          = azurerm_resource_group.resource_groups-ujmikamiapp20.name
  revision_mode                = "Single"
  workload_profile_name        = "Consumption"
  identity {
    type = "SystemAssigned"
  }
  ingress {
    client_certificate_mode = "ignore"
    external_enabled        = true
    target_port             = 8000
    cors {
      allowed_headers = ["Content-Type", "Authorization"]
      allowed_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
      allowed_origins = ["*"]
    }
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }
  registry {
    password_secret_name = "ujmikamiacrazurecrio-ujmikamiacr"
    server               = "ujmikamiacr.azurecr.io"
    username             = "ujmikamiacr"
  }
  secret {
    name                = "ujmikamiacrazurecrio-ujmikamiacr"
    key_vault_secret_id = azurerm_key_vault_secret.acr_admin_password.versionless_id
    identity            = "System"
  }
  secret {
    name                = "django-secret-key"
    key_vault_secret_id = azurerm_key_vault_secret.django_secret_key.versionless_id
    identity            = "System"
  }
  secret {
    name                = "database-url"
    key_vault_secret_id = azurerm_key_vault_secret.database_url.versionless_id
    identity            = "System"
  }
  secret {
    name                = "storage-account-key"
    key_vault_secret_id = azurerm_key_vault_secret.storage_account_key.versionless_id
    identity            = "System"
  }
  template {
    container {
      cpu    = 0.5
      image  = "ujmikamiacr.azurecr.io/backend-hotfix:neon-cutover"
      memory = "1Gi"
      name   = "ujmikamiapp-env"
      env {
        name  = "ALLOWED_HOSTS"
        value = "localhost,127.0.0.1,ujmikamiapp-env.kindbush-72762bde.westus2.azurecontainerapps.io"
      }
      env {
        name  = "CORS_ALLOWED_ORIGINS"
        value = "http://localhost:3000,http://127.0.0.1:3000,https://zealous-bay-04c9a6603.7.azurestaticapps.net"
      }
      env {
        name        = "DATABASE_URL"
        secret_name = "database-url"
      }
      env {
        name        = "SECRET_KEY"
        secret_name = "django-secret-key"
      }
      env {
        name  = "DEBUG"
        value = "False"
      }
      env {
        name  = "PRODUCTION"
        value = "true"
      }
      env {
        name  = "AZURE_ACCOUNT_NAME"
        value = "ujmikamiblob"
      }
      env {
        name        = "AZURE_ACCOUNT_KEY"
        secret_name = "storage-account-key"
      }
      liveness_probe {
        initial_delay = 0
        port          = 8000
        timeout       = 5
        transport     = "TCP"
      }
      readiness_probe {
        failure_count_threshold = 48
        interval_seconds        = 5
        port                    = 8000
        success_count_threshold = 1
        timeout                 = 5
        transport               = "TCP"
      }
      startup_probe {
        failure_count_threshold = 240
        initial_delay           = 1
        interval_seconds        = 1
        port                    = 8000
        timeout                 = 3
        transport               = "TCP"
      }
    }
    http_scale_rule {
      concurrent_requests = "10"
      name                = "http-scaler"
    }
  }

  lifecycle {
    ignore_changes = [template[0].container[0].image]
  }
}
resource "azurerm_container_app_environment" "managed_environments-ujmikamiapp_env_env0" {
  location                   = "westus2"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.workspaces-workspace_ujmikamiapp2_hm_um0.id
  name                       = "ujmikamiapp-env-env"
  resource_group_name        = azurerm_resource_group.resource_groups-ujmikamiapp20.name
  workload_profile {
    name                  = "Consumption"
    workload_profile_type = "Consumption"
  }
}
resource "azurerm_container_registry" "registries-ujmikamiacr0" {
  admin_enabled       = true
  location            = "westeurope"
  name                = "ujmikamiacr"
  resource_group_name = azurerm_resource_group.resource_groups-ujmikamiapp20.name
  sku                 = "Standard"
}
resource "azurerm_log_analytics_workspace" "workspaces-workspace_ujmikamiapp2_hm_um0" {
  location            = "westus2"
  name                = "workspace-ujmikamiapp2HmUM"
  resource_group_name = azurerm_resource_group.resource_groups-ujmikamiapp20.name

  lifecycle {
    ignore_changes = [local_authentication_enabled]
  }
}
resource "azurerm_storage_account" "storage_accounts-ujmikamiblob0" {
  account_replication_type = "LRS"
  account_tier             = "Standard"
  location                 = "westeurope"
  name                     = "ujmikamiblob"
  resource_group_name      = azurerm_resource_group.resource_groups-ujmikamiapp20.name
}
resource "azurerm_storage_container" "containers-media0" {
  container_access_type = "blob"
  name                  = "media"
  storage_account_id    = "/subscriptions/ffaa5a63-e63d-498f-9747-c1deed636ef4/resourceGroups/ujmikamiapp2/providers/Microsoft.Storage/storageAccounts/ujmikamiblob"
  depends_on = []
}
resource "azurerm_storage_container" "containers-static0" {
  container_access_type = "blob"
  name                  = "static"
  storage_account_id    = "/subscriptions/ffaa5a63-e63d-498f-9747-c1deed636ef4/resourceGroups/ujmikamiapp2/providers/Microsoft.Storage/storageAccounts/ujmikamiblob"
  depends_on = []
}
resource "azurerm_storage_account_queue_properties" "queue_services-default0" {
  storage_account_id = azurerm_storage_account.storage_accounts-ujmikamiblob0.id
  hour_metrics {
    version = "1.0"
  }
  logging {
    delete  = false
    read    = false
    version = "1.0"
    write   = false
  }
  minute_metrics {
    version = "1.0"
  }
}
resource "azurerm_static_web_app" "static_sites-ujmikamiapp0" {
  location          = "westeurope"
  name              = "ujmikamiapp"
  repository_branch = "main"
  repository_url    = "https://github.com/NaKamize/ujmikamiapp"
  repository_token    = "unmanaged-see-lifecycle-block"
  resource_group_name = azurerm_resource_group.resource_groups-ujmikamiapp20.name

  lifecycle {
    ignore_changes = [repository_token, repository_branch, repository_url]
  }
}
