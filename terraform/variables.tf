variable "env" {
  type = string
}

variable "role_arn" {
  description = "Assumed role arn"
  type        = string
}

variable "region" {
  type = string
}

variable "vault_token" {
  type = string
}

locals {
  layer_zip_path            = "layer.zip"
  layer_name                = "noah_lambda_requirements_layer"
  requirements_path         = "../${path.module}/lambda_functions/layers/python.zip"
  api_gateway_custom_domain = "noah-webhook-receiver.us-west-2.${var.env}.btna.sfdc.sh"
}

