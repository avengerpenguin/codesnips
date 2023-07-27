---
tags: aws, mq, aws mq, rabbitmq, terraform, hcl
---

AWS Secrets Manager is used to store the RabbitMQ admin password.

```hcl
terraform {  
	required_version = ">= 1.2.0"  
  
	required_providers {  
		aws = {  
		source = "hashicorp/aws"  
		version = "~> 4.16"  
	}  
}  
  
provider "aws" {  
	region = var.aws-region
}  
    
data "aws_vpc" "vpc" {  
	id = var.vpc-id
}  
  
data "aws_subnets" "private" {
	filter {
		name = "vpc-id"
		values = [data.aws_vpc.vpc.id]
	}
	filter {
		# Assumes private=1 is the tag for private subnets
		# Adjust based on exact subnet setup
		name = "private"
		values = ["1"]  
	}
}  
  
data "aws_secretsmanager_secret" "rabbitmq_secret" {  
	name = "rabbitmq-password"
}
  
data "aws_secretsmanager_secret_version" "rabbitmq_secret_version" {  
	secret_id = data.aws_secretsmanager_secret.rabbitmq_secret.id  
}  
    
resource "aws_mq_broker" "rabbit" {  
	broker_name = var.mq-broker-name
  
	engine_type = "RabbitMQ"
	# Change to latest if out of date
	engine_version = "3.10.20"  
	host_instance_type = "mq.t3.micro"  
	publicly_accessible = false  
	security_groups = [
		...
	]
	# Fixed to one subnet as SINGLE_INSTANCE is used
	# Expand to use more or all subnets in a multi node setup
	subnet_ids = [data.aws_subnets.private.ids[0]]
	deployment_mode = "SINGLE_INSTANCE"  
  
	user {  
		username = "admin"
		password = jsondecode(data.aws_secretsmanager_secret_version.rabbitmq_secret_version.secret_string)["admin"]  
	}  
}  
  
# Host and IP are not direct properties of aws_mq_broker
# for RabbitMQ, so examples below show one way to extract
module "shell_ip" {
	source  = "Invicton-Labs/shell-resource/external"
	command_unix = "dig +short $(echo $URL | cut -d'/' -f3 | cut -d':' -f1) | grep -v '\\.$'"  
	environment = {
		URL = aws_mq_broker.mq.instances.0.console_url  
	}
	depends_on = [aws_mq_broker.mq]
}  
  
module "shell_host" {  
	source  = "Invicton-Labs/shell-resource/external"
	command_unix = "echo $URL | cut -d'/' -f3 | cut -d':' -f1"
	environment = {
		URL = aws_mq_broker.mq.instances.0.console_url
	}
	depends_on = [aws_mq_broker.mq]  
}
  
output "mq-host" {  
	value = module.shell_host.stdout  
}  
  
output "mq-ip" {  
	value = module.shell_ip.stdout  
}  
  
output "mq-console" {  
	value = aws_mq_broker.mq.instances.0.console_url  
}  
```