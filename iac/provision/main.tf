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

resource "azurerm_linux_virtual_machine" "main" {
  name                  = "carprice-vm"
  location              = azurerm_resource_group.rg.location
  resource_group_name   = azurerm_resource_group.rg.name
  size                  = "Standard_B2s"
  admin_username        = var.username
  network_interface_ids = [azurerm_network_interface.main.id]

  admin_ssh_key {
    username   = var.username
    public_key = azapi_resource_action.ssh_public_key_gen_vm.output.publicKey
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "carprice-aks"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "carpriceaks"
  kubernetes_version  = "1.26"

  default_node_pool {
    name       = "default"
    node_count = var.node_count
    vm_size    = "Standard_DS2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  linux_profile {
    admin_username = var.username

    ssh_key {
      key_data = azapi_resource_action.ssh_public_key_gen_aks.output.publicKey
    }
  }

  network_profile {
    network_plugin = "azure"
    network_policy = "azure"
    service_cidr   = "10.0.0.0/16"
    dns_service_ip = "10.0.0.10"
    load_balancer_sku = "standard"
  }
}