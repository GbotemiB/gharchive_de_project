## Terraform Overview

This contains instruction on how to create a Google cloud storage, Google storage buckets and Google compute engine using [Terraform](https://www.terraform.io)


### Introduction

1. What is [Terraform](https://www.terraform.io)?
   * open-source tool by [HashiCorp](https://www.hashicorp.com), used for provisioning infrastructure resources
   * supports DevOps best practices for change management
   * Managing configuration files in source control to maintain an ideal provisioning state 
     for testing and production environments
2. What is IaC?
   * Infrastructure-as-Code
   * build, change, and manage your infrastructure in a safe, consistent, and repeatable way 
     by defining resource configurations that you can version, reuse, and share.
3. Some advantages
   * Infrastructure lifecycle management
   * Version control commits
   * Very useful for stack-based deployments, and with cloud providers such as AWS, GCP, Azure, K8S…
   * State-based approach to track resource changes throughout deployments


## Getting Started

### Installing Terraform
visit [Terraform Download page](https://developer.hashicorp.com/terraform/downloads) to download either for windows, linux or Mac OS. Also follow the instructions to setting Terraform.
To verify your installation, run `terraform -help`

### Creating GCP infrastructure with Terraform

#### Requirements

* A google cloud platform account. If you don't have one, you can create a free account thats comes with a $300 credit [here](https://console.cloud.google.com/freetrial/)

#### Setting up GCP
* A GCP project. [create one here](https://console.cloud.google.com/projectcreate). Keep note of your Project ID. it should look like this `PROJECT_NAME-453233`
* Enable Compute Engine for your project in the [GCP Console](https://console.developers.google.com/apis/library/compute.googleapis.com)
* [Create a Service Account key](https://console.cloud.google.com/apis/credentials/serviceaccountkey). This will used throughout the entire project. 
  * Select the project you created in the previous step
  * Navigate to the [IAM section](https://console.cloud.google.com/iam-admin/serviceaccounts)
* ![test](/terraform/image/create service account.png)