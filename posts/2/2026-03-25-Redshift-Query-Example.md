---
title: Redshift Query Example
date: 2026-03-25
tags: []
---

---
  [orders.csv](https://github.com/sorkdlrlsek/1-/blob/main/orders.csv)
  
  [customers.csv](https://github.com/sorkdlrlsek/1-/blob/main/customers.csv)
  
---
## 1. 2024년 이후 주문 중 COMPLETE 상태인 것만 조회하시오
```sql
SELECT order_date, status
FROM orders
WHERE order_date >= '2024-01-01'
AND status = 'COMPLETE';
```
---

## 2. 지역별 총 매출 합계를 높은 순으로 출력하시오
```sql
SELECT region, SUM(amount) AS total
FROM orders
GROUP BY region
ORDER BY total DESC;
```
---

## 3. 고객 이름과 주문 금액을 함께 출력하시오
```sql
SELECT c.name, o.amount
FROM customers c
JOIN orders o ON o.customer_id = c.id;
```
---

## 4. orders 테이블에서 CANCEL 상태인 주문을 제외하고, 금액이 100000 이상인 것만 조회하시오.
```sql
SELECT status, amount
FROM orders
WHERE NOT status IN ('CANCEL')
    AND amount >= 100000;
```
---

## 5. orders 테이블에서 제품별 주문 횟수와 평균 금액을 구하고, 평균 금액이 높은 순으로 출력하시오.
```sql
SELECT product, COUNT(*) , AVG(amount) AS aver
FROM orders
GROUP BY product
ORDER BY aver DESC;
```
---
## 6. orders 테이블에서 지역별 총 매출을 구하되 총 매출이 500000 이상인 지역만 출력하시오.
```sql
SELECT region, SUM(amount) AS amount_total
FROM orders
GROUP BY region
HAVING amount_total >= 500000
ORDER BY amount_total DESC;
```
  - WHERE 은 집계 결과에 못 씀
---
## 7. 고객 등급(grade)이 VIP 또는 GOLD인 고객의 주문 내역을 출력하시오. (고객 이름, 주문 ID, 금액 포함)
```sql
SELECT c.name, o.order_id, o.amount
FROM customers c 
JOIN orders o ON o.customer_id = c.id
WHERE c.grade IN ('VIP', 'GOLD')
ORDER BY o.amount DESC;
```
---
## 8. orders 테이블에서 가장 비싼 주문의 정보를 출력하시오. (MAX 사용 금지, 서브쿼리 사용)

```sql
SELECT *
FROM orders
WHERE amount = (SELECT amount 
                FROM orders 
                ORDER BY amount DESC 
                LIMIT 1);
```
---
## 9. 제품별로 금액 순위를 매기고, 각 제품에서 1등인 주문만 출력하시오.
```sql
SELECT product, MAX(amount) AS max_amount
FROM orders
GROUP BY product
ORDER BY max_amount DESC;
```
