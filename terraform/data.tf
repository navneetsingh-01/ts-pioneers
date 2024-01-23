data "aws_iam_policy_document" "noah_lambda_role_policy_document" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_route53_zone" "selected" {
  name         = "us-west-2.${var.env}.btna.sfdc.sh"
  private_zone = false
}

data "vault_generic_secret" "secrets" {
  path = "app_secrets/noah_secrets"
}
