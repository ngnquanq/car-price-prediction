variable "project_id" {
  type        = string
  default     = ""
  description = "The ID of the project to host the server"
}


variable "region" {
  type        = string
  default     = "asia-southeast1"
  description = "The region to host the server"
}

variable "zone" {
  type        = string
  default     = "asia-southeast1-a"
  description = "THe zone within the region to deploy the cluster"
}

variable "service_account_email" {
  type        = string
  default     = "nhatquangdata2011@gmail.com"
  description = "The service account email to use for the server"
}

variable "gce_machine_type" {
  type        = string
  default     = "e2-micro"
  description = "The machine type to use for the server"
}