# kube-form-BE
Backend infra structure by using terraform

## After Terraform apply
aws eks update-kubeconfig --name <output.cluster_name> --region ap-northeast-2

## nginx docker image
kubectl run --port 80 --image nginx nginx

## port forwarding 3000 to 80
kubectl port-forward nginx 3000:80

