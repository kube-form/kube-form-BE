cd .././hands-on
aws configure set aws_access_key_id $KUBEFORM_ACCESS_KEY_ID
aws configure set aws_secret_access_key $KUBEFORM_SECRET_ACCESS_KEY 
terraform output -json > .././flask/output.json