terraform {
  backend "azurerm" {
    resource_group_name  = "ujmikamiapp2"
    storage_account_name = "ujmikamitfstate"
    container_name       = "tfstate"
    key                  = "ujmikamiapp.tfstate"
    use_azuread_auth     = true
  }

  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "4.80.0"

    }
  }
}
