variable "aws_region" {
  type    = string
  default = "eu-west-1"
}

variable "default_tags" {
  default = {
    environment = "prod"
    tfmanaged   = "true"
  }
  description = "List of default tags applies to each resource"
  type        = map(string)
}

variable "environment" {
  type    = string
  default = "production"
}

variable "schedule_expression" {
  type        = string
  description = "EventBridge Scheduler cron or rate expression"
  default     = "cron(0 9 * * ? *)"
}

variable "schedule_timezone" {
  type    = string
  default = "UTC"
}

variable "bluesky_handle" {
  type      = string
  sensitive = true
}

variable "bluesky_password" {
  type      = string
  sensitive = true
}

variable "github_org" {
  type        = string
  description = "GitHub organisation or username (used in OIDC trust policy)"
}

variable "github_repo" {
  type    = string
  default = "daily-warhammer"
}

variable "create_github_oidc_provider" {
  type        = bool
  default     = true
  description = "Set true if the GitHub Actions OIDC provider does not yet exist in this AWS account"
}
