inputs = {
  project = "secure-project-tutorial"
}

remote_state {
  backend = "gcs"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    project  = "secure-project-tutorial"
    location = "europe-west1"
    bucket = "secure-project-tutorial-terraform-state-llm-sandbox"
    prefix   = "${path_relative_to_include()}"
  }
}