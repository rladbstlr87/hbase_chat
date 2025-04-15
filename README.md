0. 의존성 관리 `pip freeze > requirements.txt`
```shell
pip install fastapi uvicorn happybase
```

1. fastapi 서버 실행
```shell
uvicorn main:app --reload
# 혹은
uvicorn main:app --reload --port 하고싶은포트
```

2. thrift(Hbase) 서버 실행
```shell
$HBASE_HOME/bin/hbase-daemon.sh start thrift
```

> fastapi 서버와 thrift 서버가 동시 실행상태
> fastapi 서버로 받은 걸 hbase 서버로 넘겨주는 역할

3. 테이블 생성(hbase shell)
```
create 'chatrooms', 'info'
create 'messages', 'info'
```
- hbase에서 할 일 끝

4. pydantic으로 모델 상속하여 모델링