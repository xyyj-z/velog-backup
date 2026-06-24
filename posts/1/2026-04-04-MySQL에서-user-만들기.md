---
title: MySQL에서 user 만들기
date: 2026-04-04
tags: []
---

---
# USER 만들기
```bash
CREATE USER '{user 이름}'@'%' IDENTIFIED BY '{user 비밀번호}';
```
---
# USER 특정 권한 주기
```bash
GRANT SELECT, INSERT, UPDATE, DELETE ON worldpay.* TO '{user 이름}'@'%';
```
- SELECT, INSERT, UPDATE, DELETE 권한 준 거

> GRANT [권한] ON [데이터베이스].[테이블] TO '{user_name}'@'%';

```bash
FLUSH PRIVILEGES;
```
- 권한 즉시 적용
---
---
# MySQL 권한 예시
## 1. 데이터 조작 (DML)

| 권한 | 설명 |
|------|------|
| `SELECT` | 데이터 조회 |
| `INSERT` | 데이터 삽입 |
| `UPDATE` | 데이터 수정 |
| `DELETE` | 데이터 삭제 |

---

## 2. 데이터 정의 (DDL)

| 권한 | 설명 |
|------|------|
| `CREATE` | DB / 테이블 / 뷰 생성 |
| `DROP` | DB / 테이블 / 뷰 삭제 |
| `ALTER` | 테이블 구조 변경 |
| `INDEX` | 인덱스 생성 / 삭제 |
| `CREATE VIEW` | 뷰 생성 |
| `SHOW VIEW` | 뷰 정의 조회 |
| `CREATE TEMPORARY TABLES` | 임시 테이블 생성 |
| `TRUNCATE` | 테이블 전체 삭제 (ALTER에 포함) |

---

## 3. 프로시저 / 함수

| 권한 | 설명 |
|------|------|
| `CREATE ROUTINE` | 프로시저 / 함수 생성 |
| `ALTER ROUTINE` | 프로시저 / 함수 수정 / 삭제 |
| `EXECUTE` | 프로시저 / 함수 실행 |

---

## 4. 트리거 / 이벤트

| 권한 | 설명 |
|------|------|
| `TRIGGER` | 트리거 생성 / 삭제 / 실행 |
| `EVENT` | 이벤트 스케줄러 관리 |

---

## 5. 관리자 권한

| 권한 | 설명 |
|------|------|
| `GRANT OPTION` | 자신이 가진 권한을 다른 유저에게 부여 가능 |
| `CREATE USER` | 유저 생성 / 삭제 / 수정 |
| `RELOAD` | `FLUSH` 명령 실행 |
| `SHUTDOWN` | MySQL 서버 종료 |
| `PROCESS` | 실행 중인 쿼리 목록 조회 |
| `SUPER` | 최고 관리자 권한 (설정 변경 등) |
| `REFERENCES` | 외래키 제약 생성 |
| `LOCK TABLES` | 테이블 잠금 |
| `SHOW DATABASES` | 전체 DB 목록 조회 |
| `FILE` | 서버 파일 읽기 / 쓰기 |

---

## 6. 복제 (Replication)

| 권한 | 설명 |
|------|------|
| `REPLICATION SLAVE` | 복제 슬레이브 연결 허용 |
| `REPLICATION CLIENT` | 복제 상태 조회 |
| `BINLOG ADMIN` | 바이너리 로그 관리 |

---

## 한 번에 모든 권한 부여 / 회수
```sql
-- 모든 권한 부여
GRANT ALL PRIVILEGES ON 데이터베이스명.* TO '유저명'@'%';

-- 모든 권한 회수
REVOKE ALL PRIVILEGES ON 데이터베이스명.* FROM '유저명'@'%';
```

---

## 실무에서 자주 쓰는 권한 조합
```sql
-- 일반 서비스 계정 (데이터 CRUD만)
GRANT SELECT, INSERT, UPDATE, DELETE ON mydb.* TO 'app_user'@'%';

-- 개발자 계정 (구조 변경 포함)
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX ON mydb.* TO 'dev_user'@'%';

-- 읽기 전용 계정 (분석 / 모니터링용)
GRANT SELECT ON mydb.* TO 'readonly_user'@'%';
```
