---
title: S3 특정 Bucket/Folder 접근 허용
date: 2026-03-28
tags: []
---

---

- A, B bucket이 있다는 가정

---

## **EC2 Role Policy (EC2 → A 버킷만 접근)**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::A-bucket/*"
      ]
    }
  ]
}
```

---

## **S3 Bucket Policy (특정 EC2 Role만 접근 허용)**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:role/ec2-role"
      },
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::A-bucket/*"
      ]
    }
  ]
}
```
