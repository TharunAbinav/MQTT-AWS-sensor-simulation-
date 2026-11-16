output "aws_iot_endpoint" {
  description = "AWS IoT Core Data-ATS Endpoint"
  value       = data.aws_iot_endpoint.iot_endpoint.endpoint_address
}

output "thing_arn" {
  description = "ARN of the provisioned IoT Thing"
  value       = aws_iot_thing.demo_device.arn
}
