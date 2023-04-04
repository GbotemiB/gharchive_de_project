terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}


provider "google" {
  credentials = file("/home/gbotemi/Downloads/test_user.json")

  project = var.project
  region = var.region
 
}
 
//resources to create ubuntu 20.04 with 25gb of space
resource "google_compute_instance" "default" {
  name         = var.compute_instance
  machine_type = var.machine_type
  zone         = "${var.region}-c"


  boot_disk {
    initialize_params {
      image = "ubuntu-2004-focal-v20230302"
      size=25
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
  force_destroy = true
}

//resources to create a bigquery dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  location   = var.region
}
