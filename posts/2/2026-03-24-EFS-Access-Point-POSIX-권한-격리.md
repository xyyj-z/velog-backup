---
title: EFS Access Point POSIX 권한 격리
date: 2026-03-24
tags: []
---

## Access Point로 User 나누기
- 이 시나리오의 핵심
  - Access Point 설정

---
### VPC 생성
- 기본 VPC
![](https://velog.velcdn.com/images/sorkdlrlsek/post/baa10165-2fb9-4718-aa04-b987d669a42a/image.png)

---
### EC2 생성
![](https://velog.velcdn.com/images/sorkdlrlsek/post/7c274f44-5b0c-4aa0-9812-bac8c94cbcbd/image.png)

---
### EFS
#### File System
- 사용자 지정으로 만들기
![](https://velog.velcdn.com/images/sorkdlrlsek/post/0e54e6e4-1152-4f0c-acf0-7ccd40697da9/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/06f9969f-0278-462b-be12-ef691cbaeecc/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/960fda2b-57e1-4bb4-9123-18c6fbe8b6e6/image.png)
- EC2랑 같은 region 하나만 선택해도 됨
![](https://velog.velcdn.com/images/sorkdlrlsek/post/56f25e38-d341-4c16-9c17-b742842d155d/image.png)
> "elasticfilesystem:ClientMount" 정책에 이것만 추가

```json
{
    "Version": "2012-10-17",
    "Id": "efs-policy-wizard-359339ce-e086-417e-b02f-e646f76aa573",
    "Statement": [
        {
            "Sid": "efs-statement-f717ae3a-f57b-409c-80e4-470bf3ae5206",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": [
                "elasticfilesystem:ClientWrite",
                "elasticfilesystem:ClientMount"
            ],
            "Condition": {
                "Bool": {
                    "elasticfilesystem:AccessedViaMountTarget": "true"
                }
            }
        },
        {
            "Sid": "efs-statement-b39bc697-c850-4885-9881-6efc417e5ed0",
            "Effect": "Deny",
            "Principal": {
                "AWS": "*"
            },
            "Action": "*",
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "false"
                }
            }
        }
    ]
}
```
#### Access Point
- id test로 최소 2개가 필요

![](https://velog.velcdn.com/images/sorkdlrlsek/post/6738cce9-4aeb-43e1-a304-0d5015369e32/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/054b756f-c5f2-41bc-8059-0fb83e2bb8ef/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/6a26a77d-9024-4615-8f50-3e8b72bcfa1b/image.png)
> POSIX 사용자에 UID/GID를 넣으면 그 Access Point로 마운트할 때 누가 접속하든 강제로 그 UID/GID로 바꿔버림 -> 그래서 하면 안돼 쌰갈!

![](https://velog.velcdn.com/images/sorkdlrlsek/post/e7b2807e-8229-491c-ba36-5fce685014af/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/054b756f-c5f2-41bc-8059-0fb83e2bb8ef/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/ec32e92c-6fd8-4fa7-b8f4-749c6e0c729c/image.png)

---
### EC2
- IAM
![](https://velog.velcdn.com/images/sorkdlrlsek/post/a7c1421a-cf53-4bc2-b3f7-42bed04e8d6f/image.png)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Statement1",
      "Effect": "Allow",
      "Action": [
        "elasticfilesystem:ClientWrite",
        "elasticfilesystem:ClientMount",
        "elasticfilesystem:ClientRootAccess"
      ],
      "Resource": "arn:aws:elasticfilesystem:ap-northeast-2:515682373899:file-system/fs-0e4c82df979e06fec"
    }
  ]
}
```

- EC2에 정책 연결

- CMD
> sudo yum install amazon-efs-utils -y
> sudo mkdir -p /mnt/1
> sudo mkdir -p /mnt/2
> sudo adduser -u 1001 {원하는 사용자명}
> sudo adduser -u 1002 {원하는 사용자명}
> sudo mount -t efs -o tls,accesspoint=fsap-05dfaffc7f2f10df5 fs-0043ef6052c5254aa:/ /mnt/1
> sudo mount -t efs -o tls,accesspoint=fsap-071ffce6cd949869e fs-0043ef6052c5254aa:/ /mnt/2

  - 각각 다른 Access Point로 /mnt/1, /mnt/2 하나씩

- 잘 됐는지 확인 
---
> sudo -u {1001:사용자명} ls /mnt/1

  - 아까 1001인 AP로 /mnt/1에 mount 했으므로 이 명령어를 쳤을 때, 성공해서 아무 것도 나오면 안 됨
---
> sudo -u {1001:사용자명} ls /mnt/2
  
  - 아까 1002인 AP로 /mnt/2에 mount 했으므로 이 명령어를 쳤을 때, 
  > "ls: cannot open directory '/mnt/2': Permission denied" 라고 나옴
---
> sudo -u {1002:사용자명} ls /mnt/1

  - 아까 1001인 AP로 /mnt/1로 mount 했으므로 이 명령어를 쳤을 때, 
  > "ls: cannot open directory '/mnt/1': Permission denied" 라고 나옴
---
> sudo -u {1002:사용자명} ls /mnt/2

  - 아까 1002인 AP로 /mnt/2에 mount 했으므로 이 명령어를 쳤을 때, 성공해서 아무 것도 나오면 안 됨
---

![](https://velog.velcdn.com/images/sorkdlrlsek/post/c0af3c63-eb34-4fe1-a005-322cb97fff8d/image.png)
