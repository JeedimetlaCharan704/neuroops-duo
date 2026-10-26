# ==============================================================================
# Terraform IaC: Google Cloud Run Service with Low-Carbon Configuration
# ==============================================================================

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
  default     = "gitlab-transcend-prod"
}

variable "region" {
  description = "Google Cloud Region (Defaults to lowest-carbon region: europe-north1)"
  type        = string
  default     = "europe-north1"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Cloud Run Service Definition
resource "google_cloud_run_service" "omnipay_gateway" {
  name     = "omnipay-gateway"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/omnipay-gateway:latest"
        resources {
          limits = {
            memory = "512Mi"
            cpu    = "1000m"
          }
        }
        env {
          name  = "DEPLOYED_REGION"
          value = var.region
        }
        env {
          name  = "CARBON_INTENSITY_GCO2_KWH"
          value = "28.4"
        }
        ports {
          container_port = 8080
        }
      }
      container_concurrency = 80
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "0"
        "autoscaling.knative.dev/maxScale" = "10"
        "run.googleapis.com/client-name"   = "gitlab-duo-agent-platform"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Allow public unauthenticated traffic for hackathon judges
resource "google_cloud_run_service_ia_member" "public_access" {
  location = google_cloud_run_service.omnipay_gateway.location
  project  = google_cloud_run_service.omnipay_gateway.project
  service  = google_cloud_run_service.omnipay_gateway.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "service_url" {
  description = "Live URL of deployed service on Google Cloud Run"
  value       = google_cloud_run_service.omnipay_gateway.status[0].url
}
