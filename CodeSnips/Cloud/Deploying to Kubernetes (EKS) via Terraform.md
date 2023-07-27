---
tags: aws, eks, kubernetes, terraform, hcl, kubectl
---

Prerequisites:

- AWS cli configure with AWS keys
- `kubectl` command installed
- Kubernetes set up on AWS via EKS (change `host` and `cluster_ca_certificate` if Kubernetes set up another way)

```hcl
data "aws_eks_cluster" "eks" {  
	name = var.eks-cluster-name
}

provider "kubectl" {  
	load_config_file = false
	host = data.aws_eks_cluster.eks.endpoint
	cluster_ca_certificate = base64decode(data.aws_eks_cluster.eks.certificate_authority.0.data) 
	exec {  
		api_version = "client.authentication.k8s.io/v1beta1"
		args = ["eks", "get-token", "--cluster-name", data.aws_eks_cluster.cluster.id]
		command = "aws"
	}
}
  
data "kubectl_path_documents" "manifests" {  
	pattern = "path/to/yaml/*.yml"
}  
  
resource "kubectl_manifest" "manifest" {  
	count = length(data.kubectl_path_documents.manifests.documents)
	yaml_body = element(data.kubectl_path_documents.manifests.documents, count.index)
	wait_for_rollout = true
	depends_on = [kubernetes_manifest.config]
}  

/*
Example reference to AWS resource to pass to service
via config block below.
*/
data "aws_s3_bucket" "bucket" {  
	bucket = "my-bucket"  
}

/*  
Optional block to pass env vars to service.
Delete and the `depends_on` above if not needed.
Example belows show passing hostname of S3 bucket.
*/  
resource "kubernetes_manifest" "config" {  
	manifest = {  
		"apiVersion" = "v1"  
		"kind" = "ConfigMap"  
		"metadata" = {  
			"name" = "config"  
			"namespace" = "dsdservice"  
		}  
		"data" = {  
			"S3_BUCKET_HOST" = data.aws_s3_bucket.bucket.bucket_domain_name
		}
	}
}
```