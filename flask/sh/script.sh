#!/bin/bash
##ls -al > file.txt
cd ../hands-on
terraform apply -auto-approve > ../flask/terraform.txt
#echo $hello > file.txt