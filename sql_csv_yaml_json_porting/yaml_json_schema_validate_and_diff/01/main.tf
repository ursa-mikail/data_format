provider "google" {
  project = "your-project-id"
  region  = "us-central1"
}

module "dev_keyset" {
  source         = "./modules/keyset"
  keyring_name   = "dev-ring"
  key_name       = "dev-key"
  location       = "us-central1"
  rotation_period = "2592000s"
  policy_json    = file("${path.module}/policies/rendered/dev-policy.json")
}

