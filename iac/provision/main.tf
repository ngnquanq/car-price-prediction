# Define the provider and the required version
terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.80.0" // Provider version
    }
  }
  required_version = "1.10.5" // Terraform version
}

# Define the provider configuration
provider "google" {
  project     = var.project_id
  region      = var.region
  zone        = var.zone
}

# Define the google storage resource
# resource "google_storage_bucket" "static" {
#   name          = var.bucket
#   location      = var.region

#   # Enable bucket level access
#   uniform_bucket_level_access = true
# }

# Define the google compute instance resource
resource "google_compute_instance" "vm_instance" {
  name         = "terraform-instance"
  machine_type = var.gce_machine_type
  zone         = var.zone

  // This instances use ubuntu image
  boot_disk {
    initialize_params {
      image = "projects/ubuntu-os-cloud/global/images/ubuntu-2204-jammy-v20230727"
    }
  }
}
