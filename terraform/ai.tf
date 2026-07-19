resource "azurerm_cognitive_account" "openai" {
  name                  = "ujmikami-openai"
  location              = "westeurope"
  resource_group_name   = azurerm_resource_group.resource_groups-ujmikamiapp20.name
  kind                  = "OpenAI"
  sku_name              = "S0"
  custom_subdomain_name = "ujmikami-openai"
}

resource "azurerm_cognitive_deployment" "chat_model" {
  name                 = "gpt-5.4-mini"
  cognitive_account_id = azurerm_cognitive_account.openai.id

  model {
    format  = "OpenAI"
    name    = "gpt-5.4-mini"
    version = "2026-03-17"
  }

  sku {
    name     = "GlobalStandard"
    capacity = 10
  }
}

resource "azurerm_container_app" "fastapi_ai" {
  name                         = "ujmikami-ai"
  container_app_environment_id = azurerm_container_app_environment.managed_environments-ujmikamiapp_env_env0.id
  resource_group_name          = azurerm_resource_group.resource_groups-ujmikamiapp20.name
  revision_mode                = "Single"
  workload_profile_name        = "Consumption"

  ingress {
    external_enabled = true
    target_port      = 8000
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  registry {
    server               = "ujmikamiacr.azurecr.io"
    username             = "ujmikamiacr"
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.registries-ujmikamiacr0.admin_password
  }
  secret {
    name  = "azure-openai-api-key"
    value = azurerm_cognitive_account.openai.primary_access_key
  }

  template {
    min_replicas = 0
    max_replicas = 1

    container {
      name   = "fastapi-ai"
      image  = "ujmikamiacr.azurecr.io/fastapi-ai:latest"
      cpu    = 1.0
      memory = "2Gi"

      env {
        name  = "LLM_PROVIDER"
        value = "azure_openai"
      }
      env {
        name  = "AZURE_OPENAI_ENDPOINT"
        value = azurerm_cognitive_account.openai.endpoint
      }
      env {
        name        = "AZURE_OPENAI_API_KEY"
        secret_name = "azure-openai-api-key"
      }
      env {
        name  = "AZURE_OPENAI_DEPLOYMENT"
        value = azurerm_cognitive_deployment.chat_model.name
      }
      env {
        name  = "CHROMA_MODE"
        value = "embedded"
      }
      env {
        name  = "ANONYMIZED_TELEMETRY"
        value = "FALSE"
      }
      env {
        name  = "CORS_ALLOWED_ORIGINS"
        value = "https://zealous-bay-04c9a6603.7.azurestaticapps.net,http://localhost:3000"
      }
    }
  }

  lifecycle {
    ignore_changes = [template[0].container[0].image]
  }
}
