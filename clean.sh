#!/bin/bash

az login
export ARM_SUBSCRIPTION_ID="$(az account show --output tsv --query "id")"

cd terraform || { echo "Failed to change directory to terraform"; exit 1; }

read -p "Are you sure you want to destroy all Terraform-managed resources and clean the state? (y/N): " confirm
if [[ $confirm = [yY] ]]; then
  echo "Destroying all Terraform-managed resources..."
  if ! terraform destroy --auto-approve; then
    echo "Failed to destroy resources."
    exit 1
  fi
fi

# Remove terraform state files and directories
files_to_remove=(".terraform" ".terraform.lock.hcl" "terraform.tfstate" "terraform.tfstate.backup")

read -p "Are you sure you want to remove all terraform state files (y/N): " confirm1
if [[ $confirm1 = [yY] ]]; then
  echo "Removing files and directories..."
  for file in "${files_to_remove[@]}"; do
    if [ -e "$file" ]; then
      echo "Removing $file"
      rm -rf "$file"
    else
      echo "$file does not exist, skipping."
    fi
  done
fi

cd .. || { echo "Failed to change directory to project root "; exit 1; }

# Remove all .databricks directories
read -p "Are you sure you want to remove all .databricks directories (y/N): " confirm2
if [[ $confirm2 = [yY] ]]; then

  echo "Searching for .databricks directories"
  mapfile -t databricks_dirs < <(find . -type d -name ".databricks")
  if [ ${#databricks_dirs[@]} -eq 0 ]; then
    echo "No .databricks directories found."
  else
    for dir in "${databricks_dirs[@]}"; do
      echo "Removing $dir"
      rm -rf "$dir"
    done
    echo "All .databricks directories removed."
  fi
fi