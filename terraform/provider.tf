provider "azurerm" {
  features {
  }
  subscription_id = "ffaa5a63-e63d-498f-9747-c1deed636ef4"
  environment     = "public"
  use_msi         = false
  # use_cli defaults to true (local az login) and use_oidc defaults to false;
  # CI overrides the latter via the ARM_USE_OIDC=true env var, so neither is
  # hardcoded here.
  resource_provider_registrations = "none"
}
