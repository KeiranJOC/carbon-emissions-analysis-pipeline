resource "google_storage_bucket" "data-lake-bucket" {
  name                        = "${local.data_lake_bucket}_${var.project}" # Concatenating DL bucket & Project name for unique naming
  location                    = var.region
  storage_class               = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // days
    }
  }

  force_destroy = true
}

resource "google_artifact_registry_repository" "de-container-repository" {
  location      = var.region
  repository_id = local.container_repository
  description   = "Repository to store Docker containers"
  format        = "DOCKER"
}