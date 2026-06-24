---
title: Cloudwatch-Agent
date: 2026-04-06
tags: []
---

---
- Cloudwatch-agent install
```bash
sudo yum install amazon-cloudwatch-agent -y
```
---
- Cloudwatch-agent 설정
```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
```
| 질문 | 선택 |
|------|------|
| OS | Linux |
| 실행 환경 | EC2 |
| 실행 유저 | root |
| StatsD | no |
| CollectD | no |
| 호스트 메트릭 (CPU 등) | no |
| 기존 설정 파일 import | no |
| 로그 파일 수집 | yes |
| Log file path | /var/log/cloud-init.log |
| Log group name | messages (기본값) |
| Log group class | STANDARD |
| Log stream name | {instance_id} (기본값) |
| Log retention | -1 (무기한) |
| 추가 로그 파일 | no |
| X-ray traces | no |
| SSM parameter store 저장 | no |
---
- Cloudwatch-agent 실행
```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
-a fetch-config \
-m ec2 \
-s \
-c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json
```
---
- 만약 실행 헀는데도 cloudwatch에 log-group이 안 생긴다면
```bash
sudo cloud-init clean --logs
sudo cloud-init init
```
  - 새 log가 쌓이는 명령어
