---
title: Redshift DDL 형식
date: 2026-04-06
tags: []
---

---
# CSV
```sql
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://버킷명/폴더/'
TABLE PROPERTIES ('skip.header.line.count'='1')
```
---
# TSV
```sql
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION 's3://버킷명/폴더/'
TABLE PROPERTIES ('skip.header.line.count'='1')
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
```sql
STORED AS PARQUET
LOCATION 's3://버킷명/폴더/'
```
---
# ORC
```sql
STORED AS ORC
LOCATION 's3://버킷명/폴더/'
```
---
# Avro
```sql
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.avro.AvroSerDe'
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat'
LOCATION 's3://버킷명/폴더/'
```
