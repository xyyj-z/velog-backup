---
title: Presigned URL
date: 2026-03-27
tags: []
---

---

# VPC - 1

- 기본  VPC 생성

---

# RDS

- 생성
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/9f67a443-7201-473f-a9e4-041d348636d6/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/61a6933f-3988-49f4-9ac0-db72b7d18812/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/b0085741-55ed-4288-a8dd-0bedd4144e4b/image.png)

    

- Secrets-Manager
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/881b8479-2507-4a5e-b599-3990ec224d9b/image.png)

    

- 접속/ table 생성
    
    ```sql
    USE demo;
    ```
    
    ```sql
    CREATE TABLE orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        item VARCHAR(255),
        quantity INT,
        status VARCHAR(50) DEFAULT 'pending'
        );
    ```
    

---

# S3

- 업로드용 s3-bucket 생성

---

# EC2

- 그냥 생성

- CMD
    
    ```bash
    sudo yum install mariadb105 -y
    ```
    
    ```bash
    mkdir python
    sudo yum install python3.12-pip -y
    python3.12 -m pip install pymysql -t python
    zip -r pymysql-layer.zip python
    ```
    
    ```bash
    aws s3 cp pymysql-layer.zip s3://{s3 bucket 이름}/
    ```
    

---

# Lambda

- Layer
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/5b50b7f7-9a6f-4aa1-a3a6-cc31e05aee3b/image.png)

    

- Function
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/21b3e0f6-4527-4fa7-9f48-2d59bda3dfd5/image.png)

    
    - Layer
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/5d4e6459-5de5-436f-8e8b-cac059b6b9ab/image.png)

        
    
    - 권한
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/520f57c5-6e24-412a-b21a-b4a35f31c2be/image.png)

        
    
    - VPC
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/e55f6eb4-d8c7-4f65-9dca-bc4f572f983b/image.png)

        
        - RDS 랑 같은 subnet으로
    
    - 환경 변수
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/e9ae5ba3-010b-4002-b083-05a001142046/image.png)

        
    
    - Code
        
       ```python
        import json
        import pymysql
        import boto3
        import os
        from datetime import datetime
        
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
                    # RDS에서 전체 조회
                    cursor.execute("SELECT * FROM orders")
                    result = cursor.fetchall()
            finally:
                conn.close()
        
            # 결과를 S3에 JSON으로 저장
            s3 = boto3.client('s3')
            bucket = os.environ['BUCKET_NAME']
            key = f"results/{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
            print(1)
            s3.put_object(
                Bucket=bucket,
                Key=key,
                Body=json.dumps(result, ensure_ascii=False, default=str),
                ContentType='application/json'
            )
        
            # Presigned URL 생성 (5분 유효)
            url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': key},
                ExpiresIn=300
            )
        
            return {
                'statusCode': 200,
                'body': json.dumps({'download_url': url})
            }
       ```
        
   
    ---
    
    # VPC - 2
    
    - Endpoint
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/023d2751-39ad-4500-81bc-3105396c92ff/image.png)

        
        - lambda랑 같은 subnet
    
    - Security-Group
        
        ![](https://velog.velcdn.com/images/sorkdlrlsek/post/97c9f604-d981-4048-8c0e-80b29f0af31f/image.png)

        

---

# Lambda

- Test-Template에 아무것도 안 넣고 test ㄱ
- 그럼 성공함

- s3 가봐
    
    ![](https://velog.velcdn.com/images/sorkdlrlsek/post/27d60258-50fc-4697-b559-3bc1d3740a63/image.png)
    - result나옴
