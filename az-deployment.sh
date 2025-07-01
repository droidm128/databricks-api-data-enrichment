az login
export ARM_SUBSCRIPTION_ID="$(az account show --output tsv --query "id")"
cd terraform
terraform init
terraform apply
