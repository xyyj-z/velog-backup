---
title: Lambda Function URL
date: 2026-04-03
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
    method = event['requestContext']['http']['method']
    body = json.loads(event['body'])
    if method == 'POST':
        return insert_data(body)
```
- 요구사항에 따라서 
 > - SecretsManager 이름
 > - secret 값 가져오는 거 (환경 변수 **OR** SecretsManager)
 > - sql **삽입 Data**
 > - 반환 값

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
    method = event['requestContext']['http']['method']

    if method == 'GET':
        return select_data()
```
- sql 만 바꿔서 쓰면 됨
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
    method = event['requestContext']['http']['method']

    if method == 'PUT':
        body = json.loads(event['body'])
        return update_data(body)
```
- sql 에서 무슨 컬럼을 기준으로 어떤 컬럼들을 바꿀건지만 잘 쓰면 됨
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
    method = event['requestContext']['http']['method']

    if method == 'DELETE':
        body = json.loads(event['body'])
        return delete_data(body)

```
- 테이블명, 삭제 기준 컬럼만 바꿔서

- DELETE Example
  - 예시 테이블

  order_id | item_name | user_name
  ---------|-----------|----------
  1        | 피자       | 홍길동
  2        | 치킨       | 김철수
  3        | 피자       | 박영희
  4        | 햄버거     | 홍길동
  5        | 치킨       | 홍길동
  > 케이스 1 - order_id 기준 (고유값)

  DELETE FROM orders WHERE order_id IN (1)

  결과:
  
  order_id | item_name | user_name
  ---------|-----------|----------
  2        | 치킨       | 김철수
  3        | 피자       | 박영희
  4        | 햄버거     | 홍길동
  5        | 치킨       | 홍길동
  order_id는 고유값이라 정확히 1개만 삭제된다.

  > 케이스 2 - order_id 여러 개

  DELETE FROM orders WHERE order_id IN (1, 2, 3)

  결과:
  
  order_id | item_name | user_name
  ---------|-----------|----------
  4        | 햄버거     | 홍길동
  5        | 치킨       | 홍길동
  IN 안에 있는 1, 2, 3 전부 삭제된다.

  > 케이스 3 - item_name 기준 (중복값 주의)

  DELETE FROM orders WHERE item_name IN ('피자')

  결과:
  
  order_id | item_name | user_name
  ---------|-----------|----------
  2        | 치킨       | 김철수
  4        | 햄버거     | 홍길동
  5        | 치킨       | 홍길동
  item_name이 '피자'인 row가 order_id 1, 3 둘 다 삭제된다.
  고유값이 아닌 컬럼을 기준으로 하면 여러 row가 한 번에 삭제될 수 있다.
  
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
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "INSERT into orders (order_id, item_name, user_name, quantity, total_price, ordered_at) values (%s,%s,%s,%s,%s,%s)"
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
    method = event['requestContext']['http']['method']


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
