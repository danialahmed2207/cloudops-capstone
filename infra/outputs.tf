output "staging_public_ip" {
  description = "Oeffentliche IP der Staging-EC2 (kommt als Secret EC2_IP_STAGING in GitHub)"
  value       = aws_instance.staging.public_ip
}

output "staging_url" {
  description = "URL der Staging-Umgebung"
  value       = "http://${aws_instance.staging.public_ip}"
}
