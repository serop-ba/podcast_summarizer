# terragrunt/nat_gateway/terragrunt.hcl

# Define Terragrunt configuration for Cloud NAT
terraform {
  source = "../../..//modules/nat"
}

inputs = {
  project_id = "secure-project-tutorial"       # Replace with your actual GCP Project ID
  region     = "europe-west1"           # Replace with your desired region
  vpc_name   = "my-vpc-network"               # Replace with your VPC network name
}
