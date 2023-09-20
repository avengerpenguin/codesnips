Makes use of [[Finding your AWS account ID via aws cli]].

```bash
# Configure to need
IMAGE_NAME=myimage
IMAGE_TAG=v1.0.0
AWS_REGION=us-west-1

# Get account ID to construct ECR tag
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)

# Full image name and tag
DOCKER_IMAGE="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$IMAGE_NAME$:$IMAGE_TAG"

# Assumes current dir has a Dockerfile
docker build --tag $DOCKER_IMAGE .
docker push $IMAGE
```
