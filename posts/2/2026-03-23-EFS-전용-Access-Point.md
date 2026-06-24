---
title: EFS 전용 Access Point
date: 2026-03-23
tags: []
---

## Access Point를 통해 나누기
- 이 시나리오의 핵심
  - 전용 Access Point를 생성해, 각 EC2는 자신의 전용 Access Point를 통해서만 EFS에 Mount 할 수 있음
---
### VPC 생성
- 기본 VPC
![](https://velog.velcdn.com/images/sorkdlrlsek/post/baa10165-2fb9-4718-aa04-b987d669a42a/image.png)

---
### EC2 2개 생성
- 그냥 Public으로 만들고 pem.key 있이 만들어야 함
- 각각의 Security-Group을 만들어야 함
![](https://velog.velcdn.com/images/sorkdlrlsek/post/35bcc156-1531-4d38-adb7-373b9e0f8b22/image.png)

---
### EFS
#### File System
- 사용자 지정으로 만들기
![](https://velog.velcdn.com/images/sorkdlrlsek/post/2e34a131-b161-4baa-8744-9c2d5dad8943/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/ac04f411-5d57-4536-b972-75e6bc230a93/image.png)
- 해당 instance에 맞는 region에 해당 secrutiy-group 할당
![](https://velog.velcdn.com/images/sorkdlrlsek/post/8fd4f1a9-1cfc-498f-b1af-8946cea2cdb8/image.png)
- 이렇게 선택하면
```json
{
    "Version": "2012-10-17",
    "Id": "efs-policy-wizard-da59015f-cd1d-4ed7-9902-67ea8abdabcd",
    "Statement": [
        {
            "Sid": "efs-statement-01db8acd-685b-4778-987a-6132fe7ec444",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": [
                "elasticfilesystem:ClientWrite"
            ],
            "Condition": {
                "Bool": {
                    "elasticfilesystem:AccessedViaMountTarget": "true"
                }
            }
        },
        {
            "Sid": "efs-statement-24530708-6ca1-4724-b710-d8af417860ba",
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
- 여기에 더 추가해야 함
```json
"elasticfilesystem:ClientMount"
```
```json
        {
            "Sid": "DenyWithoutAccessPoint",
            "Effect": "Deny",
            "Principal": {
                "AWS": "*"
            },
            "Action": "elasticfilesystem:ClientMount",
            "Condition": {
                "Bool": {
                    "elasticfilesystem:AccessPointRequired": "false"
                }
            }
        }

```
- 이걸 추가해서 최종적으로
```json
{
    "Version": "2012-10-17",
    "Id": "efs-policy-wizard-da59015f-cd1d-4ed7-9902-67ea8abdabcd",
    "Statement": [
        {
            "Sid": "efs-statement-01db8acd-685b-4778-987a-6132fe7ec444",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": [
                "elasticfilesystem:ClientWrite",
>>>>>>>         "elasticfilesystem:ClientMount"
            ],
            "Condition": {
                "Bool": {
                    "elasticfilesystem:AccessedViaMountTarget": "true"
                }
            }
        },
        {
            "Sid": "efs-statement-24530708-6ca1-4724-b710-d8af417860ba",
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
>>>>    {
            "Sid": "DenyWithoutAccessPoint",
            "Effect": "Deny",
            "Principal": {
                "AWS": "*"
            },
            "Action": "elasticfilesystem:ClientMount",
            "Condition": {
                "Bool": {
                    "elasticfilesystem:AccessPointRequired": "false"
                }
            }
>>>>    }
    ]
}
```
#### Access Point
- dev
![](https://velog.velcdn.com/images/sorkdlrlsek/post/ea0da6b1-09cb-488d-b73e-37d41d3f78d3/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/74f18025-14c8-41a7-86ae-9a23218f0313/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/7f430f23-ee61-4fc8-aa34-0066254deb60/image.png)


- ops
![](https://velog.velcdn.com/images/sorkdlrlsek/post/63b2d155-c8cf-41d1-bd0f-e4728c75943b/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/035fa790-9422-4756-b48c-3fb53654292b/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/64446354-b04b-4ba1-a8fc-518a8800907e/image.png)

> 위에 쓰는 ID는 아무거나 상관 없음.
허나, Access Point 권한은 보통 755를 많이 씀

![](https://velog.velcdn.com/images/sorkdlrlsek/post/788cde29-6caa-449b-90c9-06887704985b/image.png)

---
### EC2-Policy
- demo-dev
![](https://velog.velcdn.com/images/sorkdlrlsek/post/eaeb32ea-d3fe-4072-979e-89acc64c2d40/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/f0082933-ca21-43d5-97ba-cff1fbf1f7d4/image.png)
> - Amazon Resource Name : EFS ARN
> - Conditions Value : demo-dev/Access Point ARN
```json
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
      "Resource": "arn:aws:elasticfilesystem:ap-northeast-2:515682373899:file-system/fs-049e95db2e960a79d",
      "Condition": {
        "StringEquals": {
          "elasticfilesystem:AccessPointArn": "arn:aws:elasticfilesystem:ap-northeast-2:515682373899:access-point/fsap-0ebeeaa4f14974df1"
        }
      }
    }
  ]
}
```


- demo-ops
![](https://velog.velcdn.com/images/sorkdlrlsek/post/eaeb32ea-d3fe-4072-979e-89acc64c2d40/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/7fd76f30-ed9d-4e6a-9da8-98c57834ee74/image.png)
> - Amazon Resource Name : EFS ARN
> - Conditions Value : demo-ops/Access Point ARN
```json
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
      "Resource": "arn:aws:elasticfilesystem:ap-northeast-2:515682373899:file-system/fs-049e95db2e960a79d",
      "Condition": {
        "StringEquals": {
          "elasticfilesystem:AccessPointArn": "arn:aws:elasticfilesystem:ap-northeast-2:515682373899:access-point/fsap-05bf9543c698ebb53"
        }
      }
    }
  ]
}
```

> 이걸 각 instance에 연결

---
### EC2
- Security-Group
![](https://velog.velcdn.com/images/sorkdlrlsek/post/bbcfa2ab-86d8-40b2-8a06-0fc3b56f87ab/image.png)
  - NFS 뚫기



- 각 instance에서 
  ```
  sudo yum install amazon-efs-utils -y
  ```
  ```
  mkdir -p /efs
  ```
![](https://velog.velcdn.com/images/sorkdlrlsek/post/61847695-bc48-4340-be03-1ca1476fa192/image.png)
해서 나온 걸 그대로 치면 안 됨

> sudo mount -t efs -o tls,accesspoint=fsap-0ebeeaa4f14974df1 fs-049e95db2e960a79d:/ /efs
- 여기서 맨 끝 부분을 mkdir로 만든 Mount Point에 맞추기
