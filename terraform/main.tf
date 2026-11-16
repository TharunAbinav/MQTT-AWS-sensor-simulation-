terraform {
  required_version = ">= 1.3.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
    http = {
      source  = "hashicorp/http"
      version = "~> 3.4"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# 1. Fetch AWS IoT Data-ATS Endpoint automatically
data "aws_iot_endpoint" "iot_endpoint" {
  endpoint_type = "iot:Data-ATS"
}

# 2. Provision the AWS IoT Thing
resource "aws_iot_thing" "demo_device" {
  name = var.thing_name
}

# 3. Create X.509 Certificate & Keys automatically
resource "aws_iot_certificate" "device_cert" {
  active = true
}

# 4. Create the IoT Security Policy
resource "aws_iot_policy" "demo_policy" {
  name = var.policy_name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "iot:Connect",
          "iot:Publish",
          "iot:Subscribe",
          "iot:Receive"
        ]
        Resource = "*"
      }
    ]
  })
}

# 5. Attach Policy to Certificate
resource "aws_iot_policy_attachment" "policy_attach" {
  policy = aws_iot_policy.demo_policy.name
  target = aws_iot_certificate.device_cert.arn
}

# 6. Attach Certificate to IoT Thing
resource "aws_iot_thing_principal_attachment" "thing_attach" {
  principal = aws_iot_certificate.device_cert.arn
  thing     = aws_iot_thing.demo_device.name
}

# 7. Download Amazon Root CA 1 and save certs directly to ../certs/
data "http" "root_ca" {
  url = "https://www.amazontrust.com/repository/AmazonRootCA1.pem"
}

resource "local_file" "root_ca_file" {
  content  = data.http.root_ca.response_body
  filename = "${path.module}/../certs/AmazonRootCA1.pem"
}

resource "local_file" "cert_file" {
  content  = aws_iot_certificate.device_cert.certificate_pem
  filename = "${path.module}/../certs/certificate.pem.crt"
}

resource "local_sensitive_file" "private_key_file" {
  content  = aws_iot_certificate.device_cert.private_key
  filename = "${path.module}/../certs/private.pem.key"
}
