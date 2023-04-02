terraform {
  required_version = ">= 1.0"
  backend "gcs" {}
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  project     = var.project
  region      = var.region
  credentials = file(var.credentials)
}
