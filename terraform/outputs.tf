output "ecr_repository_url" {
  value = data.aws_ecr_repository.app_repo.repository_url
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  value = aws_ecs_service.app_service.name
}

output "ec2_public_ip" {
  value = aws_instance.ecs_host.public_ip
}

output "alb_dns_name" {
  value = "http://${aws_lb.main.dns_name}"
}
