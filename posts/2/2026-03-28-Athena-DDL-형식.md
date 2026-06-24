---
title: Athena DDL 형식
date: 2026-03-28
tags: []
---

---
# CSV
```sql
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://버킷명/폴더/'
TBLPROPERTIES ('skip.header.line.count'='1')
```
---
# TSV
```sql
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION 's3://버킷명/폴더/'
TBLPROPERTIES ('skip.header.line.count'='1')
```
---
# JSON
```sql
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
STORED AS TEXTFILE
LOCATION 's3://버킷명/폴더/'
```
---
# Parquet
* 바이너리 형식
```sql
STORED AS PARQUET
LOCATION 's3://버킷명/폴더/'
```
---
# ORC
* 바이너리 형식
```sql
STORED AS ORC
LOCATION 's3://버킷명/폴더/'
```
---
# Avro
* 바이너리 형식
```sql
STORED AS AVRO
LOCATION 's3://버킷명/폴더/'
```
---
#### 구분자 형식
* DELIMITED
  > 단순 구분자 파일 (CSV, TSV 등)

* SERDE
  > JSON, 복잡한 CSV, 로그 파일 등
