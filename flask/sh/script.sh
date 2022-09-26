#!/bin/bash
##ls -al > file.txt
cd ../terraform
aws configure set aws_access_key_id $KUBEFORM_ACCESS_KEY_ID
aws configure set aws_secret_access_key $KUBEFORM_SECRET_ACCESS_KEY 
terraform apply -auto-approve \
-var node_group_num=$NodeGroupNum \
-var instance_type=$InstanceType
#echo $hello > file.txt