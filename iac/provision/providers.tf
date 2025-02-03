terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "3.80.0"
    }
    azapi = {
      source = "hashicorp/azapi"
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
  required_versions = "1.10.5"
}

provider "azurerm" {
  # Configuration options
  features {}
}