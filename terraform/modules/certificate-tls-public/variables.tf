variable "cert_cn" {
  description = "The primary name the cert is for"
  type        = string
}

variable "r53_zone_id" {
  description = "The Route53 Zone ID for the domain/zone that should be used for DNS records"
  type        = string
}

variable "cert_san_list" {
  description = "A List of strings to include in the SAN list of the HTTPS Certificate created for this LB"
  type        = list(string)
  default     = []
}
