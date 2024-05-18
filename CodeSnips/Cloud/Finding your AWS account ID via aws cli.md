Sometimes you need to use your account ID in scripts so the following allows you to find it automatically.

```bash
aws sts get-caller-identity --query "Account" --output text
```

You can use it in a script like this:

```bash
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
```

See it in use in [[Pushing a docker image to AWS Elastic Container Registry (ECR)]].
