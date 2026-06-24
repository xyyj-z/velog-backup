---
title: S3 Event + Lamba + RDS
date: 2026-03-27
tags: []
---

---
Lambda를 통한 자동 INSERT

---
# VPC

- 기본 VPC

- Endpoint
    - Secrets-Manager
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/628a2e0c-0d94-4126-b4d6-7a14c2768adb/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/37577ca6-bd47-4743-8411-47f990a33995/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/fd60bd8c-e830-4f6d-8c18-be9d4bab0a60/image.png)

        
        - endpoint-sg
            
            ![](https://velog.velcdn.com/images/sorkdlrlsek/post/6ef1854a-1365-4ad0-b76f-2df269082db0/image.png)

            
    - S3
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/e9c925c8-b12b-4163-b0ff-e054b358f9b3/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/8e5b235b-8f45-41b5-836b-a7e42669152f/image.png)

        
        - gateway 선택
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/fb996238-4033-4ae2-85fe-e1e1d0cc4f34/image.png)

        
        - Lambda 서브넷 라우팅 테이블 선택

---

# RDS - 1

- 생성
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/dd21f450-68a8-4343-a513-b7973eddaae0/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/bc07310c-b323-4d83-86d6-5d90bf73d3cc/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/75cd71d0-3316-4a93-9f75-dddd0e8760c8/image.png)

    

- Secret Manger
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/8ea68671-b99b-4245-a736-cc5aca052813/image.png)

    

- Security-Group
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/1ba98cc9-d199-4bdb-ab15-500967ed1a49/image.png)

    

- 접속
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/6e4304d4-1021-4e44-869e-90fd5e8416bc/image.png)
    ```bash
    USE demo;
    ```
    
    ```bash
    CREATE TABLE demo (
    	id INT AUTO_INCREMENT PRIMARY KEY,
    	name VARCHAR(255)
    	);
    ```
    

---

# S3

- 생성
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/47d9e763-db15-4096-b3f1-725774388c3a/image.png)

    

- Upload
    
    ```bash
    id,name
    1,홍길동
    2,김철수
    ```
    
    - test를 위해 `data.csv` 로 업로드

---

# EC2

- 그냥 생성
    - admin
- CMD
    
    ```bash
    mkdir python
    sudo yum install python3.12-pip -y
    python3.12 -m pip install pymysql -t python
    zip -r pymysql-layer.zip python
    aws s3 cp pymysql-layer.zip s3://{s3 bucket name}/
    ```
    

---

# Lmabda

- Layer
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/802e915c-d3ca-4bb1-a42a-91cd99a92c7f/image.png)
    
- Function
    - 생성
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/e6a29579-9e14-4643-b5e8-07fc7ebc98a6/image.png)

        
    - Layer 연결
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/d943f84c-2847-471c-8f66-6f4aa83cdb29/image.png)

        
    - 권한
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/7602eef7-21cf-4ad9-8321-4332c7d04f25/image.png)

        
    - VPC
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/6aa4d47c-7a67-4128-a3be-6a485d76e39e/image.png)

        
    - 환경 변수
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/f1d41f9c-7321-4441-bf3a-e60c03e1e27d/image.png)

        
        - Value : Secret Manger 이름
    - Test
        - 새 event 생성
            - 템플릿
                
                ![](https://velog.velcdn.com/images/sorkdlrlsek/post/ae3a1d5d-d717-4da1-b91b-44fdb8d36f2f/image.png)

                
                ```json
                {
                  "Records": [
                    {
                      "eventVersion": "2.0",
                      "eventSource": "aws:s3",
                      "awsRegion": "us-east-1",
                      "eventTime": "1970-01-01T00:00:00.000Z",
                      "eventName": "ObjectCreated:Put",
                      "userIdentity": {
                        "principalId": "EXAMPLE"
                      },
                      "requestParameters": {
                        "sourceIPAddress": "127.0.0.1"
                      },
                      "responseElements": {
                        "x-amz-request-id": "EXAMPLE123456789",
                        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
                      },
                      "s3": {
                        "s3SchemaVersion": "1.0",
                        "configurationId": "testConfigRule",
                        "bucket": {
                >         "name": "demo-s3-mysql",
                          "ownerIdentity": {
                            "principalId": "EXAMPLE"
                          },
                          "arn": "arn:aws:s3:::example-bucket"
                        },
                        "object": {
                >         "key": "data.csv",
                          "size": 1024,
                          "eTag": "0123456789abcdef0123456789abcdef",
                          "sequencer": "0A1B2C3D4E5F678901"
                        }
                      }
                    }
                  ]
                }
                ```
                
                - 여기서 name이랑 key만 바꾸기
     - code
    ```python
    import json
    import pymysql
    import boto3
    import os
    import csv

    def get_secret():
        client = boto3.client('secretsmanager')
        secret = client.get_secret_value(SecretId=os.environ['SECRET_NAME'])
        return json.loads(secret['SecretString'])

    def lambda_handler(event, context):
        secret = get_secret()
        conn = pymysql.connect(
            host=secret['host'],
            user=secret['username'],
            password=secret['password'],
            db=secret['dbname'],
            port=int(secret['port']),
            cursorclass=pymysql.cursors.DictCursor
        )
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket, Key=key)
        lines = obj['Body'].read().decode('utf-8').splitlines()
        reader = csv.DictReader(lines)
        try:
            with conn.cursor() as cursor:
                for row in reader:
                    columns = ", ".join(row.keys())
                    placeholders = ", ".join(["%s"] * len(row))
                    values = tuple(row.values())
                    cursor.execute(f"INSERT INTO demo ({columns}) VALUES ({placeholders})", values)
            conn.commit()
            return {"statusCode": 200, "body": "INSERT 완료"}
        finally:
            conn.close()
    ```

- Test ㄱ
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/cbca72ec-6f7e-4b22-8bf9-ed5ebe569d85/image.png)

    
    - 확인
        
        
        ```json
        MySQL [demo]> SELECT * FROM demo;
        +----+-----------+
        | id | name      |
        +----+-----------+
        |  1 | 홍길동    |
        |  2 | 김철수    |
        +----+-----------+
        2 rows in set (0.001 sec)
        ```
