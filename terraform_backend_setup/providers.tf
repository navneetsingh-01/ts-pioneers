###########################################################
# Dynamo DB
###########################################################

resource "aws_dynamodb_table" "hack-tfstate-lock-table-noah" {
  name         = "hack-tfstate-lock-table-noah"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
  point_in_time_recovery {
    enabled = true
  }
}

###########################################################
# S3 BUCKET
###########################################################

resource "aws_s3_bucket" "hack-tfstate-noah" {
  bucket = "hack-tfstate-noah"
}

resource "aws_s3_bucket_versioning" "hack-tfstate-versioning-noah" {
  bucket = aws_s3_bucket.hack-tfstate-noah.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "hack-tfstate-noah-lifecycle-configurations" {
  bucket = aws_s3_bucket.hack-tfstate-noah.id
  rule {
    id     = "rule-1"
    status = "Enabled"
    abort_incomplete_multipart_upload {
      days_after_initiation = 2
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "hack-tfstate-server-side-encryption-noah" {
  bucket = aws_s3_bucket.hack-tfstate-noah.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Resource to avoid error "AccessControlListNotSupported: The bucket does not allow ACLs"
resource "aws_s3_bucket_ownership_controls" "hack-tfstate-ownership-control-noah" {
  bucket = aws_s3_bucket.hack-tfstate-noah.id
  rule {
    object_ownership = "ObjectWriter"
  }
}

resource "aws_s3_bucket_acl" "hack-tfstate-acl-noah" {
  bucket     = aws_s3_bucket.hack-tfstate-noah.id
  acl        = "private"
  depends_on = [aws_s3_bucket_ownership_controls.hack-tfstate-ownership-control-noah]
}

resource "aws_s3_bucket_public_access_block" "hack-tfstate-public-access-noah" {
  bucket                  = aws_s3_bucket.hack-tfstate-noah.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
