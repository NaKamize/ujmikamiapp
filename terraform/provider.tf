provider "azurerm" {
  features {
  }
  subscription_id = "ffaa5a63-e63d-498f-9747-c1deed636ef4"
  environment     = "public"
  use_msi         = false
  resource_provider_registrations = "none"
}
