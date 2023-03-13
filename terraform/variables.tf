locals {
  data_lake_bucket = "gharchive_data_lake"
}

variable "project" {
  description = "Your GCP Project ID"
  default = "dataeng-375609"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "us-central1"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "gharchive_dataset"
}

variable "cloud_storage" {
  description = "cloud Dataset that raw data (from GCS) will be written to"
  type = string
  default = "gharchive_dataset_gcs"
}

variable "compute_instance" {
  type = string
  default = "gharhive-instance"
}

variable "machine_type" {
  type = string
  default = "e2-medium"
}

