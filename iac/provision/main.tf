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

# Update your provider block (lines 23-25)
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
}

# Add this before the VM resource (before line 28)
resource "azurerm_virtual_network" "main" {
  name                = "carprice-vnet"
  address_space       = ["10.1.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_subnet" "main" {
  name                 = "carprice-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.1.1.0/24"]
}

resource "azurerm_network_interface" "main" {
  name                = "carprice-nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.resource_group_location
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
    public_key = file("~/.ssh/carprice_ssh.pub")
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
  kubernetes_version  = "1.30.2"

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
      key_data = file("~/.ssh/carprice_ssh.pub")
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

# Add this security rule to your NSG configuration
resource "azurerm_network_security_group" "main" {
    name                = "carprice-nsg"
    location            = azurerm_resource_group.rg.location
    resource_group_name = azurerm_resource_group.rg.name

    security_rule {
        name                       = "SSH"
        priority                   = 100
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "22"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }

    # New ICMP rule
    security_rule {
        name                       = "AllowICMP"
        priority                   = 110  # Must be higher than SSH rule
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Icmp"
        source_port_range          = "*"
        destination_port_range     = "*"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }
}

    resource "azurerm_subnet_network_security_group_association" "main" {
      subnet_id                 = azurerm_subnet.main.id
      network_security_group_id = azurerm_network_security_group.main.id
    }