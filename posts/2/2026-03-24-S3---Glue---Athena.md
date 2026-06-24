---
title: S3 + Glue + Athena
date: 2026-03-24
tags: []
---

---
## s3
![](https://velog.velcdn.com/images/sorkdlrlsek/post/609759e8-7d99-4a33-89bd-1ed0c3412563/image.png)
  - 쿼리 결과를 담을 폴더 하나
  - 배포 파일을 올릴 폴더 하나
  
---
## Glue
### Databases
![](https://velog.velcdn.com/images/sorkdlrlsek/post/6a0025f6-51ff-4b01-97ba-82648582a145/image.png)

- 그냥 생성

### Crawlers
![](https://velog.velcdn.com/images/sorkdlrlsek/post/d3bd756e-48b7-4a55-88d6-bddedaa8b94f/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/97035fb0-0878-4c59-a3ba-823576987ffd/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/ce75fda9-fa10-44d5-b2c3-9038c1c06e6c/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/4b617bc9-423a-473d-b7ca-588da4243e71/image.png)
- AmazonS3FullAccess 추가![](https://velog.velcdn.com/images/sorkdlrlsek/post/18670b8f-2644-4f82-90a5-18fb36278734/image.png)
![](https://velog.velcdn.com/images/sorkdlrlsek/post/e91a5baf-4146-41a3-9584-3d1ec7de06d4/image.png)
- complete 되면 
  - Database Table 생김


---
## Athena
![](https://velog.velcdn.com/images/sorkdlrlsek/post/fee3eed5-58e1-4f31-8943-496a7faa8742/image.png)![](https://velog.velcdn.com/images/sorkdlrlsek/post/089dbe31-d5b2-4612-9cd9-d642ff8b0177/image.png)

> SELECT * FROM data LIMIT 10;

![](https://velog.velcdn.com/images/sorkdlrlsek/post/2e780c21-50d8-49fb-ae7f-e76aad36f090/image.png)
