
```hcl
terraform {
	required_providers {
		kafka = {
			source = "Mongey/kafka"
			version = "0.5.3"
		}
		http = {
			source = "hashicorp/http"
		}
	}
}
  
variable "vpc-id" {  
	type = string  
}

variable "msk-cluster-name" {  
	type = string 
}  
  
variable "archive-bucket-name" {  
	type = string 
}  

variable "archived-topics" {  
	type = list(string)  
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

# Allows access from all traffic in VPC private subnets
# Adjust if more fine-grained security is required
module "security_group" {  
	source = "terraform-aws-modules/security-group/aws"  
	version = "~> 5.0"  
  
	name = "${var.msk-cluster-name}-access"
	description = "Security group for MSK ${var.msk-cluster-name}"
	vpc_id = data.aws_vpc.vpc.id
  
	ingress_cidr_blocks = [data.aws_vpc.vpc.cidr_block]
	ingress_rules = [
		"kafka-broker-tcp",
		"kafka-broker-tls-tcp"
	]
}  

resource "aws_s3_bucket" "archive" {  
	bucket = var.archive-bucket-name
}  
  
resource "aws_s3_bucket_lifecycle_configuration" "expiration_policy" {  
	bucket = aws_s3_bucket.archive.id
	rule {
		status = "Enabled"
  
		expiration {
			# Adjust as desired
			days = 90
		}

		filter {
			prefix = "topics/"
		}
  
		id = "topics"
	}
}
 
data "http" "file" {
	# Note version needs updating when appropriate
	url = "https://d1i4a15mxbxib1.cloudfront.net/api/plugins/confluentinc/kafka-connect-s3/versions/10.5.1/confluentinc-kafka-connect-s3-10.5.1.zip"  
}
  
# Pretend contents are sensitive to avoid it printing binary data
resource "local_sensitive_file" "confluentinc-kafka-connect-s3" {  
	content_base64 = data.http.file.response_body_base64
	filename = "confluentinc-kafka-connect-s3.zip"
}
  
resource "aws_s3_object" "s3_sink_msk_connect_custom_plugin_code" {
	bucket = aws_s3_bucket.archive.id
	key = local_sensitive_file.confluentinc-kafka-connect-s3.filename
	source = local_sensitive_file.confluentinc-kafka-connect-s3.filename
	etag = local_sensitive_file.confluentinc-kafka-connect-s3.content_sha512
}  
  
module "msk_cluster" {  
	source = "terraform-aws-modules/msk-kafka-cluster/aws"  
  
	name = var.msk-cluster-name  
	kafka_version = "3.2.0"
	# Adjust as desired
	number_of_broker_nodes = 4  
  
	# Adjust as desired so long as it matches no. of nodes
	broker_node_client_subnets = [data.aws_subnets.subnets.ids.0, data.aws_subnets.subnets.ids.1]
	# Adjust as desired
	broker_node_instance_type = "kafka.m5.large"  
	# Adjust as desired
	broker_node_storage_info = {
		ebs_storage_info = { volume_size = 100 }
	}

	broker_node_security_groups = [  
		module.security_group.security_group_id  
	]

	configuration_name = "${var.msk-cluster-name}-config"
	# Adjust as desired
	configuration_server_properties = {  
		"auto.create.topics.enable" = true  
		"default.replication.factor" = 2
		"min.insync.replicas" = 1
		"num.io.threads" = 12
		"num.network.threads" = 10
		"num.partitions" = 24
		"num.replica.fetchers" = 2
		"replica.lag.time.max.ms" = 30000
		"unclean.leader.election.enable" = true
		"zookeeper.session.timeout.ms" = 18000
		"log.retention.hours" = 3
	}  

	connect_custom_plugins = {  
		s3_sink = {  
			name = "${var.msk-cluster-name}-s3-sink"  
			description = "Custom Plugin for S3 Sink"  
			content_type = "ZIP"
  
			s3_bucket_arn = aws_s3_bucket.archive.arn
			s3_file_key = aws_s3_object.s3_sink_msk_connect_custom_plugin_code.key

			timeouts = {
				create = "60m"
			}
		}
	}
}
  
resource "aws_mskconnect_connector" "s3_sink" {  
	name = "${var.msk-cluster-name}-archiver"  
  
	kafkaconnect_version = "2.7.1"  

	capacity {
		provisioned_capacity {
			worker_count = 1
		}
	}

	# Assumes JSON data and partitioned by the hour
	# See https://docs.confluent.io/kafka-connectors/s3-sink/current/configuration_options.html
	connector_configuration = {  
		"connector.class" = "io.confluent.connect.s3.S3SinkConnector"  
		"s3.region" = "us-west-2",  
		"format.class" = "io.confluent.connect.s3.format.bytearray.ByteArrayFormat",  
		"value.converter" = "org.apache.kafka.connect.converters.ByteArrayConverter",  
		"format.bytearray.extension" = ".json",  
		"path.format" = "'year'=YYYY/'month'=MM/'day'=dd/'hour'=HH"  
		"flush.size" = "1",  
		"schema.compatibility" = "NONE",  
		"topics" = var.archived-topics,
		"tasks.max" = "1",  
		"partitioner.class" = "io.confluent.connect.storage.partitioner.TimeBasedPartitioner",  
		"locale" = "en-GB",  
		"timezone" = "UTC",  
		"partition.duration.ms" = "3600000"  
		"storage.class" = "io.confluent.connect.s3.storage.S3Storage",  
		"s3.bucket.name" = aws_s3_bucket.archive.id,  
	}  
  
	kafka_cluster {
		apache_kafka_cluster {
			bootstrap_servers = module.msk_cluster.bootstrap_brokers_tls
  
			vpc {  
				security_groups = [module.security_group.security_group_id]  
				subnets = [data.aws_subnets.subnets.ids.0, data.aws_subnets.subnets.ids.1]  
			}
		}
	}

	kafka_cluster_client_authentication {
		authentication_type = "NONE"
	}
  
	kafka_cluster_encryption_in_transit {
		encryption_type = "TLS"
	}
  
	plugin {  
		custom_plugin {  
			arn = module.msk_cluster.connect_custom_plugins.s3_sink.arn  
			revision = module.msk_cluster.connect_custom_plugins.s3_sink.latest_revision  
		}
	}
  
	log_delivery {  
		worker_log_delivery {  
			cloudwatch_logs {  
				enabled = true  
				log_group = aws_cloudwatch_log_group.kafka-archiver-logs.name  
			}  
		}  
	}  
  
	service_execution_role_arn = aws_iam_role.connector_role.arn  
}  
  
resource "aws_cloudwatch_log_group" "kafka-archiver-logs" {  
	name = "${var.msk-cluster-name}-archiver"
}  
  
resource "aws_iam_role" "connector_role" {
	name = "${var.msk-cluster-name}-archiver-role"
	assume_role_policy = jsonencode({
		Version = "2012-10-17"  
		Statement = [  
			{  
				"Effect" : "Allow",  
				"Principal" : {  
					"Service" : "kafkaconnect.amazonaws.com"  
				},  
				"Action" : "sts:AssumeRole"  
			}  
		]  
	})  
}
  
resource "aws_iam_role_policy" "connector_role_policy" {  
	name = "${var.msk-cluster-name}-archiver-role-policy"  
	role = aws_iam_role.connector_role.id  
	policy = jsonencode({  
		Version = "2012-10-17"  
		Statement = [  
			{  
				"Effect" : "Allow",  
				"Action" : [  
					"s3:ListAllMyBuckets"  
				],  
				"Resource" : "arn:aws:s3:::*"  
			},  
			{  
				"Effect" : "Allow",  
				"Action" : [  
					"s3:ListBucket",  
					"s3:GetBucketLocation",  
					"s3:DeleteObject"  
				],  
				"Resource" : "arn:aws:s3:::*"  
			},  
			{  
				"Effect" : "Allow",  
				"Action" : [  
					"s3:PutObject",  
					"s3:GetObject",  
					"s3:AbortMultipartUpload",  
					"s3:ListMultipartUploadParts",  
					"s3:ListBucketMultipartUploads"  
				],  
				"Resource" : "*"  
			}  
		]  
	})  
}
```
