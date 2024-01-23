###########################################################
# API GATEWAY
###########################################################

# Create the API Gateway
resource "aws_api_gateway_rest_api" "noah_webhook_api" {
  name        = "noah_webhook_api"
  description = "API Gateway for NOAH"
  lifecycle {
    create_before_destroy = true
  }
}

# Create the API Gateway resource
resource "aws_api_gateway_resource" "noah_webhook_resource" {
  rest_api_id = aws_api_gateway_rest_api.noah_webhook_api.id
  parent_id   = aws_api_gateway_rest_api.noah_webhook_api.root_resource_id
  path_part   = "noah-webhook"
}

# Create the API Gateway method
resource "aws_api_gateway_method" "noah_webhook_method" {
  rest_api_id   = aws_api_gateway_rest_api.noah_webhook_api.id
  resource_id   = aws_api_gateway_resource.noah_webhook_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

# Create the API Gateway integration
resource "aws_api_gateway_integration" "noah_webhook_integration" {
  rest_api_id             = aws_api_gateway_rest_api.noah_webhook_api.id
  resource_id             = aws_api_gateway_resource.noah_webhook_resource.id
  http_method             = aws_api_gateway_method.noah_webhook_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.noah_lambda.invoke_arn
}

# Create the API Gateway deployment
resource "aws_api_gateway_deployment" "noah_webhook_deployment" {
  rest_api_id = aws_api_gateway_rest_api.noah_webhook_api.id
  stage_name  = "prod"
  depends_on  = [aws_api_gateway_integration.noah_webhook_integration]
  lifecycle {
    create_before_destroy = true
  }
}

###########################################################
# S3 BUCKET
###########################################################

# Create an S3 bucket to store lambda source code (zip archives)
resource "aws_s3_bucket" "noah_lambda_bucket" {
  bucket        = "hack-lambda-noah-${var.env}"
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "noah_lambda_bucket_versioning" {
  bucket = aws_s3_bucket.noah_lambda_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "noah_lambda_bucket_lifecycle_configurations" {
  bucket = aws_s3_bucket.noah_lambda_bucket.id
  rule {
    id     = "rule-1"
    status = "Enabled"
    abort_incomplete_multipart_upload {
      days_after_initiation = 2
    }
  }
}

# Disable all public access to the S3 bucket
resource "aws_s3_bucket_public_access_block" "noah_lambda_bucket" {
  bucket = aws_s3_bucket.noah_lambda_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Create ZIP archive with a lambda function
data "archive_file" "noah_zip" {
  type = "zip"

  source_dir  = "../${path.module}/lambda_functions/noah"
  output_path = "../${path.module}/lambda_functions/noah.zip"
}

# Upload ZIP archive with lambda to S3 bucket
resource "aws_s3_object" "noah_lambda_bucket_s3_object" {
  bucket = aws_s3_bucket.noah_lambda_bucket.id

  key    = "noah.zip"
  source = data.archive_file.noah_zip.output_path

  etag = filemd5(data.archive_file.noah_zip.output_path)
}

###########################################################
# LAMBDA FUNCTION
###########################################################

# Create the Lambda function
resource "aws_lambda_function" "noah_lambda" {
  function_name = "noah-lambda"

  s3_bucket = aws_s3_bucket.noah_lambda_bucket.id
  s3_key    = aws_s3_object.noah_lambda_bucket_s3_object.key

  runtime = "python3.10"
  timeout = 600
  handler = "function.lambda_handler"
  environment {
    variables = {
      SIGNING_SECRET    = data.vault_generic_secret.secrets.data["SIGNING_SECRET"],
      SLACK_BOT_TOKEN   = data.vault_generic_secret.secrets.data["SLACK_BOT_TOKEN"],
      SF_ACCESS_TOKEN   = data.vault_generic_secret.secrets.data["SF_ACCESS_TOKEN"],
      SF_INSTANCE_URL   = data.vault_generic_secret.secrets.data["SF_INSTANCE_URL"],
      INCIDENTS_CHANNEL = data.vault_generic_secret.secrets.data["INCIDENTS_CHANNEL"]
    }
  }
  role             = aws_iam_role.noah_lambda_role.arn
  source_code_hash = data.archive_file.noah_zip.output_base64sha256
  depends_on       = [aws_s3_bucket.noah_lambda_bucket]

  layers = [aws_lambda_layer_version.noah_dependencies_layer.arn]

  tracing_config {
    mode = "Active"
  }
  memory_size = 512

  # reserved_concurrent_executions = 20

    # vpc_config {
    #   subnet_ids         = data.aws_subnets.noah_subnets.ids
    #   security_group_ids = data.aws_security_groups.noah_sg.ids
    # }
}

# Create the IAM role for the Lambda function
resource "aws_iam_role" "noah_lambda_role" {
  name               = "noah-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.noah_lambda_role_policy_document.json
}

# Attach the necessary policy to the IAM role
resource "aws_iam_role_policy_attachment" "noah_lambda_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.noah_lambda_role.name
}

# Attach the AWS managed policy for Lambda VPC access
resource "aws_iam_role_policy_attachment" "vacos_slack_webhook_vpc_lambda_policy_attachment" {
  role       = aws_iam_role.noah_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

# Attach the necessary policy to the IAM role for S3
resource "aws_iam_role_policy_attachment" "noah_S3_lambda_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
  role       = aws_iam_role.noah_lambda_role.name
}

# Grant access to Api Gateway to invoke a lambda function
resource "aws_lambda_permission" "noah_api_gateway_invoke_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.noah_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.noah_webhook_api.execution_arn}/*/POST/noah-webhook"
}

###########################################################
# LAMBDA LAYERS
###########################################################

resource "aws_lambda_layer_version" "noah_dependencies_layer" {
  filename            = local.requirements_path
  layer_name          = local.layer_name
  source_code_hash    = filebase64sha256(local.requirements_path)
  compatible_runtimes = ["python3.10", "python3.9"]
}

###########################################################
# API GATEWAY CUSTOM DOMAIN NAME
###########################################################

module "api_gateway_certificate" {
  source = "./modules/certificate-tls-public"

  # Module Input Variables
  r53_zone_id = data.aws_route53_zone.selected.id
  cert_cn     = local.api_gateway_custom_domain
}

resource "aws_apigatewayv2_domain_name" "noah_webhook_receiver" {
  domain_name = local.api_gateway_custom_domain

  domain_name_configuration {
    certificate_arn = module.api_gateway_certificate.certificate_arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }
}

resource "aws_route53_record" "noah_webhook_receiver" {
  name    = local.api_gateway_custom_domain
  type    = "A"
  zone_id = data.aws_route53_zone.selected.id

  alias {
    name                   = aws_apigatewayv2_domain_name.noah_webhook_receiver.domain_name_configuration[0].target_domain_name
    zone_id                = aws_apigatewayv2_domain_name.noah_webhook_receiver.domain_name_configuration[0].hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_apigatewayv2_api_mapping" "noah_webhook_receiver" {
  api_id      = aws_api_gateway_rest_api.noah_webhook_api.id
  domain_name = local.api_gateway_custom_domain
  stage       = aws_api_gateway_deployment.noah_webhook_deployment.stage_name
}

###########################################################
# VPC 
###########################################################

# Get the VPC
data "aws_vpc" "noah_vpc" {
  filter {
    name   = "tag:deployPlatform"
    values = ["true"]
  }
}

# Get the subnet IDs
data "aws_subnets" "noah_subnets" {
  filter {
    name   = "tag:default_natgw"
    values = ["true"]
  }
}

# Get the security group ID for the Lambda function
data "aws_security_groups" "noah_sg" {
  filter {
    name   = "tag:lambda_default_sg"
    values = ["true"]
  }
}