resource "google_kms_key_ring" "keyring" {
  name     = var.keyring_name
  location = var.location
}

resource "google_kms_crypto_key" "key" {
  name            = var.key_name
  key_ring        = google_kms_key_ring.keyring.id
  purpose         = "ENCRYPT_DECRYPT"
  rotation_period = var.rotation_period
}

resource "google_kms_crypto_key_iam_policy" "policy" {
  crypto_key_id = google_kms_crypto_key.key.id
  policy_data   = var.policy_json
}
