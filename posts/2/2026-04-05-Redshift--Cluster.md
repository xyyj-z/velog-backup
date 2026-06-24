---
title: Redshift (Cluster)
date: 2026-04-05
tags: []
---

---
# Cluster
---
---
### 생성
![](https://velog.velcdn.com/images/sorkdlrlsek/post/fd325dc3-a63f-4020-9d75-115b4d0ae0bf/image.png)
- iam role 따로 생성해서 연결
![](https://velog.velcdn.com/images/sorkdlrlsek/post/0015e8bd-29aa-4677-8f1b-46b54b442c69/image.png)
- 사용자랑 password 설정
- Network 설정은 알잘딱
- DB도 알아서 하면 됨
---
### Cluster Connect
- query 편집기
- 위에서 설정한 db 이름, username, password 로 연결한다.
---
그리고 여기서부터 COPY와 SCHEMA로 나눠짐

### COPY
1. table 생성
```sql
CREATE TABLE employee (
    id INT,
    name VARCHAR(100),
    department VARCHAR(100),
    salary INT
);
```
2. COPY
```sql
COPY {방금 만든 table명}
FROM '{data가 있는 s3 경로}'
IAM_ROLE '{위에서 만든 role arn}'
FORMAT AS {data file의 foramt}
IGNOREHEADER 1  # 첫 번째 line 무시하라는 의미
REGION '{region}';
```
3. S3에 Query 결과 올리기
```sql
UNLOAD ('SELECT * FROM spectrum.employee')	# 이 UNLOAD 안에서 실행하는 query의 결과를 저장하겠다.
TO 's3://skills-redshift-data-2413/output/'	# 결과 올릴 s3 folder 경로
IAM_ROLE 'arn:aws:iam::515682373899:role/skills-redshift-role'
FORMAT AS CSV
HEADER;
```

---

### SCHEMA
1. 외부 Schema 생성
```sql
CREATE EXTERNAL SCHEMA spectrum	# SCHEMA 뒤에 생성하고 싶은 SCHEMA 이름을 적는다.
FROM DATA CATALOG	# Glue Data Catalog 를 쓰겠다.
DATABASE 'skills-redshift-db'	# Glue 에 이런 이름의 DataBase를 생성하겠다.
IAM_ROLE 'arn:aws:iam::515682373899:role/skills-redshift-role'	# Redshift에 붙어 있는 role arn
CREATE EXTERNAL DATABASE IF NOT EXISTS;	# 위에서 정의한 DataBase가 없으면 새로 만들고, 있으면 원래 있던 거 참조
```
2. 외부 Table 생성
```sql
CREATE EXTERNAL TABLE spectrum.employee (	# 위에서 생성한 {Schema 이름}.{생성하고 싶은 Table 이름}
    id          INT,
    name        VARCHAR(100),
    department  VARCHAR(100),
    salary      INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://skills-redshift-data-2413/employee/'	# LOCATION은 항상 폴더까지만
TABLE PROPERTIES ('skip.header.line.count'='1')	# 첫 번째 line skip
```
3. S3에 Query 결과 올리기
```sql
UNLOAD ('SELECT * FROM spectrum.employee')	# 이 UNLOAD 안에서 실행하는 query의 결과를 저장하겠다.
TO 's3://skills-redshift-data-2413/output/'	# 결과 올릴 s3 folder 경로
IAM_ROLE 'arn:aws:iam::515682373899:role/skills-redshift-role'
FORMAT AS CSV
HEADER;
```
