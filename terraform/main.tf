terraform {
  required_version = ">= 1.0"
}

provider "local" {}

resource "local_file" "pipeline_info" {
  filename = "${path.module}/pipeline_info.txt"

  content = <<EOT
Oslo Mobility Lakehouse
Infrastructure managed with Terraform
EOT
}
