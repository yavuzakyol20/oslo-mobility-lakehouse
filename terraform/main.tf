terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}

  storage_use_azuread = true
}
resource "azurerm_resource_group" "main" {
  name     = "rg-oslo-mobility-lakehouse"
  location = "norwayeast"

  tags = {
    project     = "oslo-mobility-lakehouse"
    environment = "dev"
    managed_by  = "terraform"
  }
}

resource "azurerm_storage_account" "lakehouse" {
  name                            = "oslomobilitylakehouse"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  account_kind                    = "StorageV2"
  is_hns_enabled                  = true
  allow_nested_items_to_be_public = false
  min_tls_version                 = "TLS1_0"

  tags = {
    project     = "oslo-mobility-lakehouse"
    environment = "dev"
    managed_by  = "terraform"
  }
}

resource "azurerm_container_registry" "main" {
  name                = "acroslomobilitylakehouse"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
  admin_enabled       = false

  tags = {
    project     = "oslo-mobility-lakehouse"
    environment = "dev"
    managed_by  = "terraform"
  }
}
