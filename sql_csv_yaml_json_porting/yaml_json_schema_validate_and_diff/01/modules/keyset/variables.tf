variable "keyring_name" {}
variable "key_name" {}
variable "location" {}
variable "rotation_period" {
  default = "2592000s" # 30 days
}
variable "policy_json" {}

