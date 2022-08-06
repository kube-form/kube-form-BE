import boto3

nlb = ["game-nlba0d10ed945754412aa7f70165a58f478-4215d606d1aa79a6.elb.ap-northeast-2.amazonaws.com", "hello-nlba379b487d3c5f475681a3d270a41d162-fce3f192a530dd98.elb.ap-northeast-2.amazonaws.com", "mario-nlba773aa889f90047ddb1d0f613e4946c0-687cc77c45f57548.elb.ap-northeast-2.amazonaws.com"]
ret = []
for n in nlb : 
    ret.append({"name" : n[:n.find("-nlb")], "entry_point" : n[n.find("-nlb")+4:]})
print(ret)