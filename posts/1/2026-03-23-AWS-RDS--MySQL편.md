---
title: AWS RDS (MySQL편)
date: 2026-03-23
tags: []
---

---
명령어 정리편
Tips: sql은 실행하기 전 마지막에 ';' 을 붙인다.

---
## DATABASE
- DATABASE 생성
> CREATE DATABASE {원하는 database 이름};

- DATABASE 삭제
> DROP DATABASE {원하는 database 이름};

- 그 해당 DATABASE 를 사용하고 싶다면?
> USE {해당 DATABASE 이름};

![](https://velog.velcdn.com/images/sorkdlrlsek/post/6c29c8f3-a17f-4dbc-b760-cee432b585de/image.png)

---
## TABLE
- TABLE 생성
> CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10, 2),
    hire_date DATE
);


![](https://velog.velcdn.com/images/sorkdlrlsek/post/bc4fc28a-0f92-4121-9607-590950a6c465/image.png)

- TABLE 자세하게 확인하기
>DESC {TABLE명};

![](https://velog.velcdn.com/images/sorkdlrlsek/post/ed2d9344-5856-4e76-a3f3-5f3aceb66448/image.png)


- Data 조회
> SELECT * FROM {TABLE명};

![](https://velog.velcdn.com/images/sorkdlrlsek/post/4b179812-27f0-410d-a3a2-608ff724e127/image.png)


- Data 갱신
> UPDATE {TABLE명};

![](https://velog.velcdn.com/images/sorkdlrlsek/post/1379d0b5-017b-446e-b07d-2cfcea5797bf/image.png)

- Data 삭제
> DELETE FROM {TABLE명};

![업로드중..](blob:https://velog.io/c9d1a8e5-ef4a-4f30-a325-b6674a4a3e94)

