variable "aws_region" {
  description = "AWS-Region für alle Ressourcen"
  type        = string
  default     = "eu-central-1"
}

variable "project" {
  description = "Projektname – Präfix für Namen und Tags"
  type        = string
  default     = "cloudops-capstone"
}

variable "instance_type" {
  description = "EC2-Instanztyp (Free Tier: t3.micro)"
  type        = string
  default     = "t3.micro"
}

variable "ssh_public_key_path" {
  description = "Pfad zum öffentlichen SSH-Key für die EC2-Instanzen"
  type        = string
  default     = "~/.ssh/cloudops-capstone.pub"
}

variable "allowed_ssh_cidr" {
  description = "CIDR, das per SSH zugreifen darf (0.0.0.0/0 = überall; für GitHub Actions nötig oder eigene IP eintragen)"
  type        = string
  default     = "0.0.0.0/0"
}
