---
title: RDS + Lambda + API Gateway
date: 2026-03-26
tags: []
---

---
# VPC

- 기본 VPC
---
# RDS

- 생성
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/896b933e-8410-4d63-a384-b6e681e29d79/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/1451cfd0-8d22-4c04-8492-17be2f44e4c9/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/ffc0e542-a4fd-4296-8ec1-7202041f6e00/image.png)

    

- Secret Manager
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/1835f229-7fa7-4d39-870e-8217182a0ca1/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/abd427f5-5f74-4278-aef1-17638b09a4e9/image.png)

    

- RDS 접속
    - DataBase
        
       > CREATE DATABASE demo;
         USE demo;
        
        
    - Table
        
        ```bash
        CREATE TABLE demo-table (
        	id VARCHAR(255),
        	name VARCHAR(255)
        	);
        ```   

---

# S3

- S3 만들기
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/dedabc23-d69b-43cf-8ed7-2c8e3d65c931/image.png)

    
- EC2-CMD
  ```bash
  mkdir python
  sudo yum install python3.12-pip -y
  python3.12 -m pip install pymysql -t python
  zip -r pymysql-layer.zip python
  ```

  ```bash
  aws s3 cp pymysql-layer.zip s3://{S3 이름}/
  ```

    - S3 올리기

---

# VPC-Endpoint

![](https://velog.velcdn.com/images/sorkdlrlsek/post/91be78f9-1e6c-4f96-951b-33b55825f248/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/2cc9ab23-1c62-4d49-bde4-5abee05ad219/image.png)


- RDS 있는 subnet

![](https://velog.velcdn.com/images/sorkdlrlsek/post/d4260e11-aa49-4706-95c4-6b77d9f488c7/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/e2dccfcf-f8e6-405d-8e80-47fa0b2a1aec/image.png)


- Source : 해당 VPC CIDR


- Lambda는 nat gateway 혹은 endpoint를 통해서만 나갈 수 있음
  - 그래서 꼭 nat gateway가 있는 subnet 아니면 endpoint를 만들어 줘야 함
---

# Lambda

- Layer
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/ebe7121e-4259-4915-b52c-f28e105cd5ad/image.png)

    

- Function
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/70144336-ae0b-4cc2-b05c-f1832465f454/image.png)
    - Layer랑 runtime version 맞추기
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/f8c3c25a-761b-4705-acce-e26816fdd2d2/image.png)

    
    - [AWSLambdaVPCAccessExecutionRole](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/policies/details/arn%3Aaws%3Aiam%3A%3Aaws%3Apolicy%2Fservice-role%2FAWSLambdaVPCAccessExecutionRole) 추가
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/b0f64a5f-c2d8-4cd0-85f2-4e6c8de5dac8/image.png)
    - RDS가 있는 Subnet
    - Lambda는 OutBound만 있으면 됨 (InBound)는 없어도 잘 돌아감
   ![](https://velog.velcdn.com/images/sorkdlrlsek/post/2956026b-5ff9-4a6c-8db2-f5366b7d0c23/image.png)
    - Value : Secret Manger 이름
  ![](https://velog.velcdn.com/images/sorkdlrlsek/post/07604084-a217-4444-b373-455ae4a5e3cf/image.png)

    
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
        
        def get_conn():
            secret = get_secret()
            return pymysql.connect(
                host=secret['host'],
                user=secret['username'],
                password=secret['password'],
                db=secret['dbname'],
                port=int(secret['port']),
                cursorclass=pymysql.cursors.DictCursor
            )
        
        def response(success, data=None, message=None, status=200):
            body = {"success": success}
            if data is not None:
                body["data"] = data
            if message:
                body["message"] = message
            return {
                "statusCode": status,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(body, ensure_ascii=False, default=str)
            }
        
        def lambda_handler(event, context):
            print(event)
            method = event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method")
            params = event.get("queryStringParameters") or {}
            body = {}
            if event.get("body"):
                body = json.loads(event["body"])
        
            conn = get_conn()
            try:
                with conn.cursor() as cursor:
        
                    if method == "POST":
                        columns = ", ".join(body.keys())
                        placeholders = ", ".join(["%s"] * len(body))
                        values = tuple(body.values())
                        cursor.execute(
                            f"INSERT INTO <table_name> ({columns}) VALUES ({placeholders})",
                            values
                        )
                        conn.commit()
                        return response(True, {"id": cursor.lastrowid}, status=201)
        
                    elif method == "GET" and "id" not in params:
                        cursor.execute(f"SELECT * FROM <table_name>")
                        return response(True, cursor.fetchall())
        
                    elif method == "GET" and "id" in params:
                        cursor.execute(f"SELECT * FROM <table_name> WHERE id = %s", (params["id"],))
                        row = cursor.fetchone()
                        if not row:
                            return response(False, message="Not found", status=404)
                        return response(True, row)
        
                    elif method == "PUT":
                        update_fields = {k: v for k, v in body.items() if k != "id"}
                        set_clause = ", ".join([f"{k} = %s" for k in update_fields.keys()])
                        values = tuple(update_fields.values()) + (body["id"],)
                        cursor.execute(
                            f"UPDATE <table_name> SET {set_clause} WHERE id = %s",
                            values
                        )
                        conn.commit()
                        if cursor.rowcount == 0:
                            return response(False, message="Not found", status=404)
                        return response(True, {"updated": cursor.rowcount})
        
                    elif method == "DELETE":
                        cursor.execute(f"DELETE FROM <table_name> WHERE id = %s", (params["id"],))
                        conn.commit()
                        if cursor.rowcount == 0:
                            return response(False, message="Not found", status=404)
                        return response(True, {"deleted": cursor.rowcount})
        
            finally:
                conn.close()
        ```
        
        - Test
        ```json
        {
          "httpMethod": "GET",
          "queryStringParameters": null,
          "body": null
        }
        ```
            
  
  - 함수 URL
  ![](https://velog.velcdn.com/images/sorkdlrlsek/post/42305a03-feb9-462f-b195-898845676de2/image.png)



 - 값 넣기
```bash
curl -X POST https://<function-url>/   -H "Content-Type: application/json"   -d '{"id": "1", "name": "홍길동"}'
```
        

- 확인하기
```bash
MySQL [demo]> SELECT * FROM demo;
+------+-----------+
| id   | name      |
+------+-----------+
| 1    | 홍길동    |
+------+-----------+
1 row in set (0.001 sec)
```



---

# API Gateway

- 리소스
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/09a0f197-ce7b-4fcb-8398-b28a96d14a89/image.png)

    
    - 메서드
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/e6bd98f6-a444-419b-b9be-6a1f31c64e8a/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/1318eb86-55d4-4e7b-9db6-0472bad57bf7/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/8c0765fd-f5a2-4667-9ce1-f2e4dc332e6a/image.png)

   
     - 다 이렇게
         - GET
         - POST
         - PUT
         - DELETE
     - 4개 만들기
        
- API 배포
    
    ![업로드중..](blob:https://velog.io/70f9adcf-59c0-42f9-a7bc-b815ec310443)![업로드중..](blob:https://velog.io/10f62a1e-d225-443b-a67c-429da457d5ba)

    
```bash
https://jaam8c9zi4.execute-api.ap-northeast-2.amazonaws.com/prod/demo
```
- 뒤에 demo를 붙인다.
