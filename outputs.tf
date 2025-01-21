output "instance_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.flask_app.public_ip
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket created"
  value       = aws_s3_bucket.flask_bucket.bucket
}

