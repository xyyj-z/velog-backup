---
title: Lambda + EFS
date: 2026-04-04
tags: []
---

---
# VPC
- public 2개
- private 2개
![](https://velog.velcdn.com/images/sorkdlrlsek/post/19d96ea7-6965-45f6-9910-647241313903/image.png)
---
# EFS
- Security-Group
![](https://velog.velcdn.com/images/sorkdlrlsek/post/16644cb7-6f9c-472f-8cc7-2835834ffc5f/image.png)
  - lambda, ec2 로 뚫어주기

- File system
![](https://velog.velcdn.com/images/sorkdlrlsek/post/3e5692eb-15c8-4538-9234-699a1ace7f8b/image.png)

- Access Point
알아서 그냥 root path, uid 설정하고 생성
---
# EC2
- 그냥 public에 ec2 생성
- Security-Group
![](https://velog.velcdn.com/images/sorkdlrlsek/post/248e26ab-b494-4266-a87f-ba92c5bead5c/image.png)

```bash
sudo yum install amazon-efs-utils -y
sudo yum install httpd -y
sudo mkdir -p /var/www/html
```
![](https://velog.velcdn.com/images/sorkdlrlsek/post/89c54f7f-275e-418d-a4c7-10966e2e1f26/image.png)
- efs access point에서 연결 명령어 가져오기

- 자동 Mount
```bash
sudo vi /etc/fstab
<EFS 파일 시스템 DNS>:/ <마운트 경로> nfs4 nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport,_netdev 0 0
```

---
# Lambda
- 권한
![](https://velog.velcdn.com/images/sorkdlrlsek/post/3eb7fae4-429b-439f-8916-f2a8eaaee3e1/image.png)

- vpc
![](https://velog.velcdn.com/images/sorkdlrlsek/post/de589e8b-592d-4545-9d62-4ea5e3ed11be/image.png)
  - mount 되어 있는 


- File System
![](https://velog.velcdn.com/images/sorkdlrlsek/post/f103cdea-7c9f-4c8f-ae98-7bb8ddb17a8e/image.png)
  - 여기서 **path**는 아무렇게나 해도 상관 없음
  - 만약 mount 된 az가 a 밖에 없는데 위에 vpc 설정에서 az를 a,b 선택 한다면 여기서 error가 뜨게 됨

- Code
```python
import os

EFS_MOUNT_PATH = '/mnt/lambda' 

def lambda_handler(event, context):
    file_name = "index.html"
    file_path = os.path.join(EFS_MOUNT_PATH, file_name)
    content = event.get('gmdsi',)
    
    try:
        if not os.path.exists(EFS_MOUNT_PATH):
            return {"error": f"Mount path {EFS_MOUNT_PATH} not found"}

        with open(file_path, 'w') as f:
            f.write(content)
        
        files = os.listdir(EFS_MOUNT_PATH)
        
        return {
            'statusCode': 200,
            'body': f"Successfully wrote to {file_path}. Current files: {files}"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
```
- EFS_MOUNT_PATH 는 위에서 설정한 경로
  - event template
  ```json
  {
     "gmdsi": "test"
   }
  ```

![](https://velog.velcdn.com/images/sorkdlrlsek/post/25dc5756-7935-47ea-a6da-111718a2bf4e/image.png)
