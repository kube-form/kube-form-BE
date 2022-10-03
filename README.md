# [kube-form](https://kube-form.web.app/)

<p align="center">
    <a href="https://kube-form.web.app/">
        <img src="https://user-images.githubusercontent.com/31841502/183884426-e720a67d-0aad-4551-9c2f-c8b0cf8cac08.png", style="width:500px;">
    </a>
    <h3 align="center">
        <a href="">Visit the live app</a>
    </h3>
    
</p>

## 🏆 Info
kubeform 프로젝트에서 사용자가 정의한 k8s 다이어그램대로 AWS EKS 환경을 생성하고 사용자가 정의한 docker image들을 적용시키는 작업을 자동화했습니다.  
Flask API 서버에서 POST 요청을 받으면, 사용자의 IAM User를 기반으로 AWS EKS 클러스터를 Terraform을 이용해 생성합니다.    
생성한 이후 사용자가 정의한 docker image들을 워커노드에 apply하는 작업을 자동화 하기 위해 yaml manifest 파일들을 자동으로 편집하고 적용시키는 작업을 완료했습니다. 

## 🗂 Structure

-   **flask** - API Server by Flask

    -   Flask를 이용해 API 서버 구조를 만들고, 쉘 스크립트를 수행하는데에 사용하였습니다.

-   **terraform** - AWS EKS 상의 쿠버네티스 클러스터 환경을 프로비저닝한 Terraform 구성

    -  클라우드 환경의 쿠버네티스 클러스터를 제작하기 위해 AWS 인프라를 생성해야 합니다.
    -  워커노드들에 해당되는 EC2들과 이 EC2 인스턴스들을 private 서브넷에 배치하고, 이들이 외부와 통신하기위한 NAT gateway, NLB 등 많은 AWS 인프라를 생성해야 합니다. 
    -  이 모든 리소스들을 Terraform을 사용해 인프라들을 프로비저닝 해두는 작업을 완료했습니다. 

-   **sample, k8s** - kubectl 명령을 위해 필요한 yaml 매니패스트 파일들
    -  생성된 클라우드 리소스들을 배경으로 쿠버네티스 클러스터를 생성하기 위해 구성관리 파일들을 자동으로 생성합니다.
    -  구성관리 파일들을 kubectl 명령으로 클러스터를 생성한 다음, 정보들을 가져와 클라이언트로 전송합니다.
 

## 🎉 Features
![AWS ](https://user-images.githubusercontent.com/31841502/183807939-d5a5c84e-40f2-4806-ad57-75444c4030b2.png)

사용자에게 EKS 쿠버네티스 환경을 제작해주는 절차는 크게 2가지로 나뉩니다.
1. Terraform으로 사용자의 클라우드 환경에서 여러 개의 AWS 인프라를 생성
2. EKS에 kubectl으로 접속해 사용자가 정의한 클러스터 구조를 디플로이먼트화 하여 적용

### [Terraform으로 사용자의 클라우드 환경에서 여러 개의 AWS 인프라를 생성]
클라우드 상의 쿠버네티스 환경을 설치하기 위해서는 단순히 EKS 서비스만 생성해서는 안됩니다. EKS는 마스터 노드의 역할을 하는 두뇌일뿐, 워커노드들에 해당되는 EC2들과
이 EC2 인스턴스들을 private 서브넷에 배치하고, 이들이 외부와 통신하기위한 NAT gateway, NLB 등 많은 AWS 인프라를 생성해야 합니다. 이 모든 리소스들을 Terraform을 사용해 인프라들을 프로비저닝 해두는 작업을 완료했습니다. 사용자가 정의한 워커노드 개수,인스턴스 유형 등들을 변수로 받아 Terraform apply작업을 완료하면 10분~12분 사이에 모든 인프라 구성이 자동으로 생성됩니다.


### [EKS에 kubectl으로 접속해 사용자가 정의한 클러스터 구조를 디플로이먼트화 하여 적용]
 
AWS상의 인프라 생성이 완료되면 쿠버네티스 클러스터를 적용시킬 차례입니다. 클라이언트에서 받은 사용자가 정의한 클러스터 정보를 JSON 형태로 제공받아 이 요소들을 deployment.yaml, service.yaml, namespace.yaml 등의 구성관리 파일로 자동으로 작성하는 알고리즘을 Flask 서버로 자체 설계, 개발하였습니다. 구성관리 파일이 자동으로 생성되면, 이 파일들을 EKS에 적용시키는 단계로 넘어갑니다. kubectl을 통해 모든 서비스들을 적용시키고나면 각각의 서비스로 연결되는 인그레스 컨트롤러 진입점들을 알 수 있고, 이 정보들을 모아 사용자들이 정보를 확인할 수 있도록 클라이언트로 전달합니다.


## 😀 Author

-   [서청운](https://github.com/newdeal123)

## 🌋 Contributing

-   I will not be accepting PR's on this repository. Feel free to fork and maintain your own version.

## 📄 License

-   This project is open source and available under the [MIT License](LICENSE).
