variable "aws_region" {
  default = "us-east-1"
}

variable "ecs_ami_id" {
  description = "ECS Optimized AMI ID"
  # Latest ECS-optimized Amazon Linux 2023 AMI for us-east-1
  default     = "ami-0bcad7d4493b66a48" 
}

variable "instance_type" {
  default = "t3.micro"
}

variable "key_name" {
  description = "Name of the existing EC2 key pair"
  type        = string
}
