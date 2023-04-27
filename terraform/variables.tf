locals {
  data_lake_bucket     = "de-data-lake"
  container_repository = "de-container-repository"
}

variable "project" {
  description = "GCP Project ID"
  default     = "spry-alignment-375710" # replace with your project ID
  type        = string
}

variable "region" {
  description = "Region for GCP resources"
  default     = "australia-southeast2" # replace with your region
  type        = string
}

variable "storage_class" {
  description = "Bucket storage class type"
  default     = "STANDARD"
}

variable "bq_dataset_raw" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type        = string
  default     = "carbon_emissions_raw"
}

variable "credentials" {
  description = "Path to service-account-authkeys.json"
  type        = string
  default     = "~/.gc/spry-alignment.json" # replace with the path to your access keys file
}
