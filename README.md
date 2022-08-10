# [kube-form](https://kube-form.web.app/)

<p align="center">
    <a href="https://kube-form.web.app/">
        <img src="https://user-images.githubusercontent.com/31841502/183807820-a7edab99-8468-4178-a454-316f3de84d3a.png">
    </a>
    <h3 align="center">
        <a href="">Visit the live app</a>
    </h3>
    
</p>

## 🗂 Contents

-   [Features](#-features)
-   [About](#-about)
-   [Install](#-install)
-   [Author](#-author)
-   [Task](#-task)
-   [Release](#-release)
-   [License](#-license)

## 🎉 Features

-   **API Server** - API Server by Flask

    -   Flask를 이용해 API 서버 구조를 만들고, 쉘 스크립트를 수행하는데에 사용하였습니다.

-   **Terraform** - AWS EKS 상의 쿠버네티스 클러스터 환경을 프로비저닝한 Terraform 구성

    -  클라우드 환경의 쿠버네티스 클러스터를 제작하기 위해 AWS 인프라를 생성해야 합니다.
    -  워커노드들에 해당되는 EC2들과 이 EC2 인스턴스들을 private 서브넷에 배치하고, 이들이 외부와 통신하기위한 NAT gateway, NLB 등 많은 AWS 인프라를 생성해야 합니다. 
    -  이 모든 리소스들을 Terraform을 사용해 인프라들을 프로비저닝 해두는 작업을 완료했습니다. 

-   **YAML File** - kubectl 명령을 위해 필요한 구성관리 파일들
    -  생성된 클라우드 리소스들을 배경으로 쿠버네티스 클러스터를 생성하기 위해 구성관리 파일들을 자동으로 생성합니다.
    -  구성관리 파일들을 kubectl 명령으로 클러스터를 생성한 다음, 정보들을 가져와 클라이언트로 전송합니다.


## 😀 Author

-   [서청운](https://github.com/newdeal123)

## 🌋 Contributing

-   I will not be accepting PR's on this repository. Feel free to fork and maintain your own version.

## 📄 License

-   This project is open source and available under the [MIT License](LICENSE).
