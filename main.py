from fastapi import FastAPI
import happybase
from pydantic import BaseModel
import uuid
from datetime import datetime

class Chatroom(BaseModel):
    room_name: str

class Message(BaseModel):
    room_id: str
    content: str

connection = happybase.Connection('localhost', port=9090) # thrift 서버와 연결하는 값 지정
connection.open() # 실제 연결동작

app = FastAPI()

# '/'(루트)요청으로 들어왔을 때 아래의 함수 내용을 실행해 주세요 라는 구문
@app.get('/') # => urls.py
def index(): # => views.py
    return {'hello': 'world'}

# 총 4가지 라우팅 만들거임
# 채팅방, 

@app.post('/chatroom') # POST 요청으로 챗룸이 들어오면 실행할거다
def create_chatroom(chatroom: Chatroom):
    table = connection.table('chatrooms')
    chatroom_id = str(uuid.uuid4())
    table.put(chatroom_id, {'info:room_name': chatroom.room_name}    )
    return {
        'chatroom_id': chatroom_id,
        'room_name': chatroom.room_name
    }

@app.get('/chatrooms') # 지금 생성된 채팅방 목록 출력
def get_chatrooms():
    table = connection.table('chatrooms')
    rows = table.scan() # hbase : scan '테이블이름'

    result = []
    
    for k, v in rows:
        result.append(
            {
                'chatroom_id': k,
                'room_name': v[b'info:room_name'],
            }
        )
    return result

@app.post('/messages') # 메시지 보내고
def create_message(message: Message):
    table = connection.table('messages')

    room_id = message.room_id
    timestamp = int(datetime.now().timestamp() * 1000)
    message_id = f'{room_id}-{timestamp}'

    table.put(message_id, {'info:content': message.content, 'info:room_id': room_id})

    return {
        'message_id': message_id,
        'room_id': room_id,
        'content': message.content,
    }

@app.get('/chatrooms/{room_id}/messages') # 채팅방의 메시지들 출력
def get_messages(room_id: str):
    table = connection.table('messages')
    prefix = room_id.encode('utf-8') # 룸아이디로 시작하는 것 모두 찾기

    rows = table.scan(row_prefix=prefix, reverse=True) # 앞에 시작하는 글자가 채팅방의 이름인 경우만

    result = []
    for k, v in rows:
        result.append({
            'message_id': k,
            'room_id': v[b'info:room_id'],
            'content': v[b'info:content'],
        })
    return result