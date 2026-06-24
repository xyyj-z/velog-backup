---
title: Lambda API Gateway
date: 2026-04-04
tags: []
---

---
# POST
```python
import json
import boto3
import pymysql
import os



def resp(statusCode, body):
    return {
        'statusCode': statusCode,
        'body': json.dumps(body, ensure_ascii=False, default=str)
    }

def get_secret():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(
        SecretId='{Secrets Manager 이름}',
    )
    return json.loads(response['SecretString'])


def get_conn():
    secret = get_secret()
    try:
        conn = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            passwd = secret['password'],
            db=os.environ['DB_NAME'],
            port=3306,
            charset ='utf8'
            )
        print('db 연결 성공')
        return conn
    except Exception as e:
        print(f'db 연결 실패 {e}')


def insert_data(body):
    conn = get_conn()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "INSERT into orders (order_id, item_name, user_name, quantity, total_price, ordered_at) values (%s,%s,%s,%s,%s,%s)"
    curs.execute(sql, (body['order_id'], body['item_name'], body['user_name'], body['quantity'], body['total_price'], body['ordered_at']))
    conn.commit()
    order_id = body['order_id']
    return resp(201, {"message": "Order created successfully", "order_id": order_id})


def lambda_handler(event, context):
    print(event)
    method = event['httpMethod']
    body = json.loads(event['body'])
    if method == 'POST':
        return insert_data(body)
```
- **Function URL** 이랑은 **method**만 다름
---
# GET
```python
 import json
import boto3
import pymysql
import os


def resp(statusCode, body):
    return {
        'statusCode': statusCode,
        'body': json.dumps(body, ensure_ascii=False, default=str)
    }

def get_secret():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(
        SecretId='{Secrets Manager 이름}',
    )
    return json.loads(response['SecretString'])


def get_conn():
    secret = get_secret()
    try:
        conn = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            passwd=secret['password'],
            db=os.environ['DB_NAME'],
            port=3306,
            charset='utf8'
        )
        print('db 연결 성공')
        return conn
    except Exception as e:
        print(f'db 연결 실패 {e}')


def select_data():
    conn = get_conn()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM orders"
    curs.execute(sql)
    result = curs.fetchall()
    return resp(200, result)


def lambda_handler(event, context):
    print(event)
    method = event['httpMethod']

    if method == 'GET':
        return select_data()
```
- **Function URL** 이랑은 **method**만 다름
---
# PUT
```python
import json
import boto3
import pymysql
import os


def resp(statusCode, body):
    return {
        'statusCode': statusCode,
        'body': json.dumps(body, ensure_ascii=False, default=str)
    }

def get_secret():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(
        SecretId='{Secrets Manager 이름}',
    )
    return json.loads(response['SecretString'])


def get_conn():
    secret = get_secret()
    try:
        conn = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            passwd=secret['password'],
            db=os.environ['DB_NAME'],
            port=3306,
            charset='utf8'
        )
        print('db 연결 성공')
        return conn
    except Exception as e:
        print(f'db 연결 실패 {e}')


def update_data(body):
    conn = get_conn()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "UPDATE orders SET {바꿀 컬럼}=%s WHERE {찾을 기준 컬럼}=%s"
    curs.execute(sql, (body['item_name'], body['user_name'], body['quantity'], body['total_price'], body['ordered_at'], body['order_id']))
    conn.commit()
    return resp(200, {"message": "Order updated successfully", "order_id": body['order_id']})


def lambda_handler(event, context):
    print(event)
    method = event['httpMethod']

    if method == 'PUT':
        body = json.loads(event['body'])
        return update_data(body)
```
- **Function URL** 이랑은 **method**만 다름
---
# DELETE
```python
import json
import boto3
import pymysql
import os


def resp(statusCode, body):
    return {
        'statusCode': statusCode,
        'body': json.dumps(body, ensure_ascii=False, default=str)
    }

def get_secret():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(
        SecretId='{Secrets Manager 이름}',
    )
    return json.loads(response['SecretString'])


def get_conn():
    secret = get_secret()
    try:
        conn = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            passwd=secret['password'],
            db=os.environ['DB_NAME'],
            port=3306,
            charset='utf8'
        )
        print('db 연결 성공')
        return conn
    except Exception as e:
        print(f'db 연결 실패 {e}')


def delete_data(body):
    conn = get_conn()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    placeholders = ', '.join(['%s'] * len(body['ids']))
    sql = f"DELETE FROM {테이블명} WHERE {삭제 기준 컬럼} IN ({placeholders})"
    curs.execute(sql, body['ids'])
    conn.commit()
    return resp(200, {"message": "deleted successfully"})


def lambda_handler(event, context):
    print(event)
    method = event['httpMethod']

    if method == 'DELETE':
        body = json.loads(event['body'])
        return delete_data(body)v
```
- **Function URL** 이랑은 **method**만 다름
---
# POST + GET + PUT + DELETE
```python
import json
import boto3
import pymysql
import os



def resp(statusCode, body):
    return {
        'statusCode': statusCode,
        'body': json.dumps(body, ensure_ascii=False, default=str)
    }

def get_secret():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(
        SecretId='{Secrets Manager 이름}',
    )
    return json.loads(response['SecretString'])


def get_conn():
    secret = get_secret()
    try:
        conn = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            passwd = secret['password'],
            db=os.environ['DB_NAME'],
            port=3306,
            charset ='utf8'
            )
        print('db 연결 성공')
        return conn
    except Exception as e:
        print(f'db 연결 실패 {e}')


def insert_data(body):
    conn = get_conn()
    curs eel이거는 뭐야
    = "INSERT into orders (order_id, item_name, user_name, quantity, total_price, ordered_at) values (%s,%s,%s,%s,%s,%s)"
    curs.execute(sql, (body['order_id'], body['item_name'], body['user_name'], body['quantity'], body['total_price'], body['ordered_at']))
    conn.commit()
    order_id = body['order_id']
    return resp(201, {"message": "Order created successfully", "order_id": order_id})


def select_data():
    conn = get_conn()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM orders"
    curs.execute(sql)
    result = curs.fetchall()
    return resp(200, result)


def update_data(body):
    conn = get_conn()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "UPDATE orders SET {바꿀 컬럼}=%s WHERE {찾을 기준 컬럼}=%s"
    curs.execute(sql, (body['item_name'], body['user_name'], body['quantity'], body['total_price'], body['ordered_at'], body['order_id']))
    conn.commit()
    return resp(200, {"message": "Order updated successfully", "order_id": body['order_id']})


def delete_data(body):
    conn = get_conn()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    placeholders = ', '.join(['%s'] * len(body['ids']))
    sql = f"DELETE FROM {테이블명} WHERE {삭제 기준 컬럼} IN ({placeholders})"
    curs.execute(sql, body['ids'])
    conn.commit()
    return resp(200, {"message": "deleted successfully"})


def lambda_handler(event, context):
    print(event)
    method = event['httpMethod']


    if method == 'POST':
        body = json.loads(event['body'])
        return insert_data(body)
    
    elif method == 'GET':
        return select_data()

    elif method == 'PUT':
        body = json.loads(event['body'])
        return update_data(body)

    elif method == 'DELETE':
        body = json.loads(event['body'])
        return delete_data(body)
```
---
### 결국 Function URL 과 다른 점
- POST, GET, PUT, DELETE 할 때, event 에서 다른 것
  - Method
  > - Function URL : method = **event['requestContext']['http']['method']**
  > - API Gateway : method = **event['httpMethod']
  - Path
  > - Function URL : event['requestContext']['http']['path']
  > - API Gateway : event['path']


- 이것들 말고도 검나 많은데 이 2개가 **CRUD** 에서 가장 많이 쓰임
