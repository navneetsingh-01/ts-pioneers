terraform {
  required_version = ">= 1.1.8"
}

resource "aws_acm_certificate" "this" {
  domain_name               = var.cert_cn
  validation_method         = "DNS"
  subject_alternative_names = var.cert_san_list
  tags = {
    Name        = var.cert_cn
    Description = var.cert_cn
  }

  lifecycle {
    create_before_destroy = true
  }
}

data "aws_route53_zone" "this" {
  zone_id = var.r53_zone_id
}

resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.this.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }
  zone_id = data.aws_route53_zone.this.zone_id
  name    = each.value.name
  type    = each.value.type
  ttl     = "60"
  records = [each.value.record]
}
