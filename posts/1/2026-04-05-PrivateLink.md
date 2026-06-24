---
title: PrivateLink
date: 2026-04-05
tags: []
---

---
# VPC
- 다른 VPC 2개를 만들어 준다.
---
- app VPC 에는
  - Bastion, Application EC2, ALB, ASG, Endpoint 등이 있다.
- db VPC 에는 
  - RDS, NLB 등이 있다.
---
---
### 기본 틀
- ASG를 통해서 Application을 배포하고, PrivateLink, NLB를 통해서 RDS에 접근할 수 있다.
- RDS를 KMS으로 암호화 함, 그걸 Application EC2에서 복호화 함
---
# RDS
- port: 3309
- dbname: worldpay
- kms key를 만들어서 적용


- RDS 만들고, SecretsManager 만들기

- Security-Group
![](https://velog.velcdn.com/images/sorkdlrlsek/post/08d44472-6a3d-4945-baa3-b664b78d3292/image.png)
---
# Application
### Launch Template
```bash
#!/bin/bash

sudo yum install mariadb105 -y

aws s3 cp s3://denmo/app /home/ec2-user

chmod +x /home/ec2-user/app

/home/ec2-user/app -p 8080 &
```
- **"/home/ec2-user/app -p 8080 &"** 여기에서 **"&"** 이거는 BackGround에서 실행한다는 의미
- /home/ec2-user/ 를 붙이는 이유는 application ec2 접속했을 때, 바로 ls로 보이게 하기 위해서
- -p 8080 은 8080 port로 PortForwarding 한 거임


- kms 복호화를 위해 인라인 정책 추가
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": [
                "kms:Encrypt",
                "kms:Decrypt"
            ],
            "Resource": [
                "arn:aws:kms:ap-northeast-2:515682373899:key/803ab75d-30bc-4a97-a120-b45e8ce15ad9"
            ]
        }
    ]
}
```


- Security-Group
![](https://velog.velcdn.com/images/sorkdlrlsek/post/59ffc616-7dbd-48f4-a74c-a971cf4dddd6/image.png)
---
- alb는 그냥 적당히 80으로 열고, app VPC에 만든다.
- alb의 target-group은 아까 port forwarding 8080으로 했으니까 8080으로 연다. 
---
# NLB
- internal
- db VPC에 만든다.
- Listener는 TCP 3309로 뚫는다.


- Security-Group
![](https://velog.velcdn.com/images/sorkdlrlsek/post/ac0b535e-1f09-49e7-ac53-b7ee5bc4b8ca/image.png)



### nlb Target-Group
- Target Type: IP
- TCP 3309
- Target IP: RDS ENDPOINT의 주소
  ```bash
  dig {RDS Endpoint}   #이렇게 치면 RDS 주소가 나오는데 그걸 Target IP Address에 넣으면 된다.
  ```
---
# PrivateLink
### Endpoint Service
- 위에서 생성한 NLB, IPv4를 선택하고 생성

### Endpoint
- Type: NLB 및 GWLB를 사용하는 엔드포인트 서비스
- Endpoint Service의 서비스 이름을 가져와서 사용
- Security-Group
![](https://velog.velcdn.com/images/sorkdlrlsek/post/6eff73b3-e53b-4f48-9a38-91a613825487/image.png)


> 이렇게 되면 Application EC2가 RDS에 접근해서 Secret Value를 가져올 수 있음
