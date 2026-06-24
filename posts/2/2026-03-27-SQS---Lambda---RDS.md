---
title: SQS + Lambda + RDS
date: 2026-03-27
tags: []
---

---

# VPC

- 기본 VPC 생성

- endpoint
    - sqs
    - secretsmanager

---

# S3

- pymysql 저장 할 s3 생성

---

# EC2

- EC2 아무렇게나 생성
    - admin

- CMD
    
    ```sql
    mkdir python
    sudo yum install python3.12-pip -y
    python3.12 -m pip install pymysql -t python
    zip -r pymysql-layer.zip python
    aws s3 cp pymysql-layer.zip s3://{s3 이름}/
    ```
    

---

# RDS

- 생성
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/eff8f208-ca38-427f-ac0e-ae8696241975/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/711e2468-8621-4130-b7bd-1e87e62f22c4/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/ce2cdc88-5f25-4a80-baa4-e16051d530a6/image.png)

    

- Secrets Manager
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/7b2cc233-1fe6-4033-ba0c-1cd4b774b174/image.png)

    

- 접속/ table 생성
    
    ```sql
    USE demo;
    ```
    
    ```sql
    CREATE TABLE demo (
        id INT AUTO_INCREMENT PRIMARY KEY,
        item VARCHAR(255),
        quantity INT,
        status VARCHAR(50) DEFAULT 'pending'
        );
    ```
    

---

# SQS

- 생성
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/815fa13a-5bc9-487b-894f-eedcb50cc0bf/image.png)

    

---

# Lambda

- Layer
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/10dcf4ca-43df-47f6-a478-7a450e837d31/image.png)

    
- Function
    - 생성
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/edcecdd5-ecb6-4fc6-aa30-7a0fe36da7ff/image.png)

        
    
    - Layer
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/19f6132b-797c-4b9f-b051-03754ab2da87/image.png)

        
    
    - 권한
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/904a68e1-01c3-430b-a5a7-a1bd0263464a/image.png)

        
    
    - VPC
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/bf9b9a93-519f-42c3-8bfb-ab1124b97a69/image.png)

        
        - RDS랑 같은 subnet
    
    - 환경 변수
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/22e71a0b-83c1-4997-8af7-026acf6b131b/image.png)

        
        - Key: Secrets Manager
    
    - Trigger
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/15736e83-3454-493a-bd16-8538438d3a44/image.png)

        
    
    - Code
        
        ```python
        import json
        import pymysql
        import boto3
        import os
        
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
        
            try:
                with conn.cursor() as cursor:
                    for record in event['Records']:
                        body = json.loads(record['body'])
                        action = body.get('action')
        
                        if action == 'insert':
                            cursor.execute(
                                "INSERT INTO demo (item, quantity) VALUES (%s, %s)",
                                (body['item'], body['quantity'])
                            )
        
                        elif action == 'update':
                            cursor.execute(
                                "UPDATE demo SET status = %s WHERE id = %s",
                                (body['status'], body['id'])
                            )
        
                conn.commit()
                return {"statusCode": 200, "body": "처리 완료"}
            finally:
                conn.close()
        ```
        
    
    - Test-json
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/46c198ab-2e5a-436c-abc3-0f40d97e8c72/image.png)

        
        ```json
        {
          "Records": [
            {
              "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
              "receiptHandle": "MessageReceiptHandle",
              "body": "Hello from SQS!",
              "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1523232000000",
                "SenderId": "123456789012",
                "ApproximateFirstReceiveTimestamp": "1523232000001"
              },
              "messageAttributes": {},
              "md5OfBody": "{{{md5_of_body}}}",
              "eventSource": "aws:sqs",
              "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
              "awsRegion": "us-east-1"
            }
          ]
        }
        ```
        
        - 위에서 밑으로 변경
        
        ```json
        {
          "Records": [
            {
              "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
              "receiptHandle": "MessageReceiptHandle",
              "body": "{\"action\": \"insert\", \"item\": \"노트북\", \"quantity\": 2}",
              "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1523232000000",
                "SenderId": "123456789012",
                "ApproximateFirstReceiveTimestamp": "1523232000001"
              },
              "messageAttributes": {},
              "md5OfBody": "{{{md5_of_body}}}",
              "eventSource": "aws:sqs",
              "eventSourceARN": "arn:aws:sqs:ap-northeast-2:123456789012:MyQueue",
              "awsRegion": "ap-northeast-2"
            }
          ]
        }
        ```
        
        - region, body만 바꿔주기
    
    - test하고, RDS 확인하기
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/a4c8a829-7dc8-497e-86ed-5a11ed5a39dc/image.png)

        

---

# SQS에서 test

![](https://velog.velcdn.com/images/sorkdlrlsek/post/08ae4397-92df-40dd-969e-ceecaf6ce1ea/image.png)

- RDS에서 확인
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/f6c10c6e-73ff-49c5-9033-30017c179257/image.png)

