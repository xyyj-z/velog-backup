---
title: Lambda + EFS (TLS)
date: 2026-03-24
tags: []
---

---
- 핵심
  - IAM Role 태그 기반 접근 차단 + Lambda 연동

---
### VPC 생성
- 기본 VPC
![](https://velog.velcdn.com/images/sorkdlrlsek/post/baa10165-2fb9-4718-aa04-b987d669a42a/image.png)

---
### EC2 3개 생성
- Security-Group NFS도 뚫기
![](https://velog.velcdn.com/images/sorkdlrlsek/post/af5ac937-e7e6-4e1b-b2e8-ab42bfaf015c/image.png)


![](https://velog.velcdn.com/images/sorkdlrlsek/post/1831b05c-9d92-46de-b424-617d4fe42ad4/image.png)
  - bad-web은 tag로 걸러내는 용

---
### EFS
#### File System
- 사용자 지정으로 만들기
![](https://velog.velcdn.com/images/sorkdlrlsek/post/ec8d7805-ccbc-45bf-9030-855e927e6ab5/image.png)
- 각 region에 맞는 보안 그룹 선택
![](https://velog.velcdn.com/images/sorkdlrlsek/post/41506f3d-81d1-4214-a894-8b38e971c295/image.png)
```json
{
    "Version": "2012-10-17",
    "Id": "efs-policy-wizard-a7dde1e0-0eaa-4487-891d-5e4e203bfec6",
    "Statement": [
        {
            "Sid": "efs-statement-f8468a4c-36bf-4628-8642-fcfa5c7adde1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": [
                "elasticfilesystem:ClientWrite",
                "elasticfilesystem:ClientMount",
                "elasticfilesystem:ClientRootAccess"
            ],
            "Condition": {
                "Bool": {
                    "elasticfilesystem:AccessedViaMountTarget": "true"
                }
            }
        },
        {
            "Sid": "efs-statement-4632443a-1258-435b-98eb-bcd2f668623c",
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
        },
        {
            "Sid": "DenyBlockedTag",
            "Effect": "Deny",
            "Principal": {"AWS": "*"},
            "Action": "elasticfilesystem:ClientMount",
            "Condition": {
                "StringEquals": {
                    "aws:PrincipalTag/Role": "bad"
                }
            }
        }
    ]
}
```
> "elasticfilesystem:ClientMount"
                "elasticfilesystem:ClientRootAccess"

```json
{
            "Sid": "DenyBlockedTag",
            "Effect": "Deny",
            "Principal": {"AWS": "*"},
            "Action": "elasticfilesystem:ClientMount",
            "Condition": {
                "StringEquals": {
                    "aws:PrincipalTag/Role": "bad"
                }
            }
        }
```
- 2개 추가

#### Access Point
![](https://velog.velcdn.com/images/sorkdlrlsek/post/b84dbd11-dbb5-425c-a86d-294718420cc9/image.png)


---
#### EC2
- CMD
```
sudo yum install amazon-efs-utils -y
sudo mkdir -p /mnt/efs
sudo mount -t efs -o tls fs-XXXXXXXXXXXXXX:/ /mnt/efs
```
- web-ec2-1 에서 이거 하면
```
echo "tlqkf" | sudo tee /mnt/efs/readme.txt
```
- web-ec2-2 에서도 확인 가능
```
ls /mnt/efs/
```
### ![](https://velog.velcdn.com/images/sorkdlrlsek/post/00348ebd-a955-46a9-817f-9c96205e0f63/image.png)

- IAM Role
![](https://velog.velcdn.com/images/sorkdlrlsek/post/af30cdcf-cce6-42c3-b712-b500d9d8747a/image.png)
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Statement1",
      "Effect": "Allow",
      "Action": [
        "elasticfilesystem:ClientMount",
        "elasticfilesystem:ClientWrite",
        "elasticfilesystem:ClientRootAccess"
      ],
      "Resource": "arn:aws:elasticfilesystem:ap-northeast-2:515682373899:file-system/fs-01d095c8b43e94e12"
    }
  ]
}
```
![](https://velog.velcdn.com/images/sorkdlrlsek/post/5f3e496c-a829-4a76-b775-b1d8e38afa5c/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/4a743988-5d20-4a9f-a36d-d9652d27a70b/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/96fa4600-c645-4ba5-b99d-32a9282e5429/image.png)
- Role Tag로 구별하기 위해서 태그 붙여주기
## ![](https://velog.velcdn.com/images/sorkdlrlsek/post/7292a5d8-4872-4deb-a7f7-dfed4866fdde/image.png)

---
### Lambda
![](https://velog.velcdn.com/images/sorkdlrlsek/post/47b71c68-ca3c-4a1c-8052-ef456bad0000/image.png)

#### 구성

- 권한
![](https://velog.velcdn.com/images/sorkdlrlsek/post/42fc0650-2063-4b7a-84b0-1949e0c8f8f9/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/866c3e6f-488f-4cbb-963e-ea6ce6847c21/image.png)
  > AmazonVPCFullAccess,
>  AmazonElasticFileSystemFullAccess,
 > AWSLambdaVPCAccessExecutionRole

- VPC
![](https://velog.velcdn.com/images/sorkdlrlsek/post/44caec23-450a-4441-a233-e661f6e1bcee/image.png)

- File System
![](https://velog.velcdn.com/images/sorkdlrlsek/post/5c572cd8-cbe0-4b69-b54b-5fd9720d37c6/image.png)
  - CMD에서 
  > sudo mkdir -p /mnt/lambda
  sudo mount -t efs -o tls fs-01d095c8b43e94e12:/ /mnt/lambda

#### 코드
```python
import os

def lambda_handler(event, context):
    stream = os.popen('cat /mnt/lambda/readme.txt')
    output = stream.read()
    return output
```
