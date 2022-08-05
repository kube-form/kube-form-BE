import boto3
client = boto3.client('s3')
resource = boto3.resource('s3')

bucket = resource.Bucket('kube-form')
bucket.objects.filter(Prefix=f"newdeal3/").delete()