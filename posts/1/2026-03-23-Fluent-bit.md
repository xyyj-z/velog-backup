---
title: Fluent-bit
date: 2026-03-23
tags: []
---

## ASG + Fluent Bit + CloudWatch Log 수집
---
- 우선 알잘딱으로 ASG를 생성 해준다.
---
### Launch Templates
```bash
#!/bin/bash

sudo yum install mariadb105 -y

sudo pip3 install flask pymysql boto3
curl https://raw.githubusercontent.com/fluent/fluent-bit/master/install.sh | sh
sudo systemctl enable --now fluent-bit

aws s3 cp s3://demo-worldpay/app.py .

cat > /etc/fluent-bit/fluent-bit.conf << 'EOF'
[SERVICE]
    Flush         1
    Log_Level     info
    Daemon        off
    HTTP_Server   On
    HTTP_Listen   0.0.0.0
    HTTP_Port     2020

[INPUT]
    Name              tail
    Tag               app.*		# OUTPUT의 Match와 동일하게 맞춰야 함
    Path    		  /var/log/**/*.log		# 특정 경로 주어지면 변경
    Mem_Buf_Limit     5MB
    Skip_Long_Lines   On
    Refresh_Interval  10

[OUTPUT]
    Name            cloudwatch_logs
    Match           app.*		# INPUT의 Tag와 동일하게 맞춰야 함
    region          ap-northeast-2
    log_group_name  /worldpay/app-server
    auto_create_group   true
    log_stream_prefix   app-server-
EOF

sudo python3 app.py
```
- app.py

  [app.py example](https://github.com/sorkdlrlsek/1-/blob/main/app.py)


- fluent-bit 설치 및 실행
> curl https://raw.githubusercontent.com/fluent/fluent-bit/master/install.sh | sh
sudo systemctl enable --now fluent-bit

> 여기서 "/var/log/**/*.log" 는 .log 파일 전부 수집임
경로 주어지면 그때 바꾸면 됨
ex) /var/log/worldpay/app.log

- python application 실행
> sudo python3 app.py

### Test
- cmd 창을 하나 더 킨다.
> curl http://localhost:8080/health

![](https://velog.velcdn.com/images/sorkdlrlsek/post/18f9d4a1-246c-4952-9f57-9cd4ed74b159/image.png)


![](https://velog.velcdn.com/images/sorkdlrlsek/post/bcea055e-1947-4011-a142-f514e3d512fb/image.png)
