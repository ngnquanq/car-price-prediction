terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "4.17.0"
    }
    azapi = {
      source = "Azure/azapi"
      version = "~>1.5"
    }
    random = {
      source = "hashicorp/random"
      version = "~>3.0"
    }
    time = {
      source  = "hashicorp/time"
      version = "0.9.1"
    }
  }
  required_version = "1.10.5"
}

provider "azurerm" {
  # Configuration options
  features {}
}