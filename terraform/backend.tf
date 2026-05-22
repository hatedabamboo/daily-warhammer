terraform {
  backend "s3" {
    bucket       = "daily-warhammer-state"
    key          = "terraform.tfstate"
    region       = "eu-west-1"
    encrypt      = true
    use_lockfile = true
  }
}
