# modules/cloud_nat/main.tf

# Create Cloud Router
resource "google_compute_router" "nat_router" {
  name    = "nat-router"
  network = var.vpc_name
  region  = var.region
  project = var.project_id
}

# Create Cloud NAT configuration
resource "google_compute_router_nat" "nat_config" {
  name                               = "nat-config"
  router                             = google_compute_router.nat_router.name
  region                             = var.region
  project                            = var.project_id
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

output "nat_router_name" {
  value = google_compute_router.nat_router.name
}

output "nat_config_name" {
  value = google_compute_router_nat.nat_config.name
}
