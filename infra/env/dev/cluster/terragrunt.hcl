include {
  path = find_in_parent_folders()
}

terraform {
  source = "git::git@github.com:terraform-google-modules/terraform-google-kubernetes-engine.git//modules/private-cluster?ref=v32.0.4"
}


inputs = {
  project_id = "secure-project-tutorial"
  name       = "llm-cluster"

  regional = false
  region   = "europe-west1"
  zones    = ["europe-west1-c"]

  network           = "my-vpc-network"
  subnetwork        = "my-subnet"
  
  # Network configuration
  enable_private_endpoint    = false
  enable_private_nodes      = true
  master_ipv4_cidr_block   = "172.16.0.0/28"  # Private IP range for master
  ip_range_pods            = "gke-pods"        # Reference to secondary range
  ip_range_services        = "gke-services"    # Reference to secondary range

  # Rest of the configuration remains the same as before
  release_channel           = "REGULAR"
  deletion_protection       = false
  http_load_balancing      = true
  network_policy           = true
  horizontal_pod_autoscaling = true
  filestore_csi_driver     = false
  dns_cache                = true

  create_service_account = false
  service_account        = "vm-primary@secure-project-tutorial.iam.gserviceaccount.com"

  remove_default_node_pool = true

  node_pools = [
    {
      name               = "frontend-pool"
      machine_type       = "n2-standard-2"
      min_count         = 1
      max_count         = 1
      disk_size_gb      = 20
      disk_type         = "pd-ssd"
      image_type        = "COS_CONTAINERD"
      auto_repair       = true
      auto_upgrade      = true
      initial_node_count = 1
      local_ssd_count   = 0
    },
    {
      name               = "backend-pool"
      machine_type       = "n2-standard-2"
      min_count         = 1
      max_count         = 1
      disk_size_gb      = 20
      disk_type         = "pd-ssd"
      image_type        = "COS_CONTAINERD"
      auto_repair       = true
      auto_upgrade      = true
      initial_node_count = 1
      local_ssd_count   = 0
    },
    {
      name               = "llm-pool"
      machine_type       = "n2-standard-2"
      min_count         = 2
      max_count         = 2
      disk_size_gb      = 20
      disk_type         = "pd-ssd"
      image_type        = "COS_CONTAINERD"
      auto_repair       = true
      auto_upgrade      = true
      initial_node_count = 1

    }
  ]

  node_pools_oauth_scopes = {
    all = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/servicecontrol",
      "https://www.googleapis.com/auth/service.management.readonly",
      "https://www.googleapis.com/auth/trace.append",
    ]
  }

  node_pools_labels = {
    all = {
      environment = "production"
    }
    frontend-pool = {
      workload = "frontend"
    }
    backend-pool = {
      workload = "backend"
    }
    llm-pool = {
      workload = "llm"
    }
  }

  node_pools_taints = {
    llm-pool = [
      {
        key    = "llm"
        value  = "true"
        effect = "NO_SCHEDULE"
      }
    ]
  }
}