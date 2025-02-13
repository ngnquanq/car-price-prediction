# Generate SSH key pairs for Azure VM and AKS
resource "random_pet" "ssh_key_name_vm" {
  prefix    = "vm-ssh"
  separator = ""
}

resource "random_pet" "ssh_key_name_aks" {
  prefix    = "aks-ssh"
  separator = ""
}

# Azure VM SSH key pair generation
resource "azapi_resource_action" "ssh_public_key_gen_vm" {
  type        = "Microsoft.Compute/sshPublicKeys@2022-11-01"
  resource_id = azapi_resource.ssh_public_key_vm.id
  action      = "generateKeyPair"
  method      = "POST"

  response_export_values = ["publicKey", "privateKey"]
}

resource "azapi_resource" "ssh_public_key_vm" {
  type      = "Microsoft.Compute/sshPublicKeys@2022-11-01"
  name      = random_pet.ssh_key_name_vm.id
  location  = azurerm_resource_group.rg.location
  parent_id = azurerm_resource_group.rg.id
}

# AKS SSH key pair generation
resource "azapi_resource_action" "ssh_public_key_gen_aks" {
  type        = "Microsoft.Compute/sshPublicKeys@2022-11-01"
  resource_id = azapi_resource.ssh_public_key_aks.id
  action      = "generateKeyPair"
  method      = "POST"

  response_export_values = ["publicKey", "privateKey"]
}
# AKS SSH key pair generation
resource "azapi_resource" "ssh_public_key_aks" {
  type      = "Microsoft.Compute/sshPublicKeys@2022-11-01"
  name      = random_pet.ssh_key_name_aks.id
  location  = azurerm_resource_group.rg.location
  parent_id = azurerm_resource_group.rg.id
}

# Outputs for both key pairs
output "vm_key_data" {
  value = azapi_resource_action.ssh_public_key_gen_vm.output.publicKey
}
output "aks_key_data" {
  value = azapi_resource_action.ssh_public_key_gen_aks.output.publicKey
}