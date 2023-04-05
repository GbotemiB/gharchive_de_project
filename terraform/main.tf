terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}


provider "google" {
  credentials = file("/home/gbotemi/Downloads/dataeng-375609-fac7ec0c9b2b.json")

  project = var.project
  region = var.region
 
}
 
//resources to create ubuntu 22.04 with 30gb of space
resource "google_compute_instance" "default" {
  name         = var.compute_instance
  machine_type = var.machine_type
  zone         = "${var.region}-c"


  boot_disk {
    initialize_params {
      image = "ubuntu-2204-jammy-v20230302"
      size=30
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
  }
}

//resources to create a cloud storage bucket
resource "google_storage_bucket" "data-lake-bucket" {
  
  name          = var.cloud_storage
  location      = var.region
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
}

//resources to create a bigquery dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  # location   = var.region
}