variable "aws_region" {
  description = "AWS Region for IoT Core"
  type        = string
  default     = "us-east-1"
}

variable "thing_name" {
  description = "Name of the AWS IoT Thing"
  type        = string
  default     = "MyDemoDevice"
}

variable "policy_name" {
  description = "Name of the AWS IoT Policy"
  type        = string
  default     = "DemoPolicy"
}
