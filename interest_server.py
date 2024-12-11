import asyncio
import websockets

# 사용자 관심 해시태그
user_interests = {
    "user1": ["피규어", "책"],
    "user2": ["전자제품", "모바일"],
}

# 연결된 사용자 목록
connected_clients = {}

# 물건 등록 예시
items = [
    {"title": "한정판 피규어", "description": "정품 피규어, 상태 매우 좋음", "hashtags": ["피규어", "한정판"]},
    {"title": "새로운 모바일", "description": "최신형 모바일, 상태 양호", "hashtags": ["모바일", "전자제품"]},
    # 더 많은 물건을 추가할 수 있음
]

async def notify_user(websocket, message):
    """웹소켓을 통해 알림을 보내는 함수"""
    await websocket.send(message)

async def item_check_and_notify():
    """새로운 물건이 등록될 때마다 알림을 보내는 함수"""
    for item in items:
        for user, interests in user_interests.items():
            # 물건 해시태그가 사용자의 관심 해시태그와 일치하는지 확인
            if any(hashtag in item["hashtags"] for hashtag in interests):
                if user in connected_clients:
                    # 해당 사용자가 연결된 상태라면 알림 전송
                    message = f"새로운 물건이 등록되었습니다: {item['title']} - {item['description']}"
                    await notify_user(connected_clients[user], message)

async def chat_handler(websocket, path):
    """클라이언트 연결 및 채팅 처리"""
    # 사용자가 서버에 연결될 때 닉네임을 받아 저장
    user_name = await websocket.recv()
    connected_clients[user_name] = websocket
    
    try:
        # 클라이언트로부터 메시지를 받음
        async for message in websocket:
            print(f"{user_name}: {message}")
    finally:
        # 연결 종료 시 사용자를 목록에서 제거
        del connected_clients[user_name]

async def main():
    """서버 실행 및 물건 등록 시 알림 전송"""
    # 서버 시작
    server = await websockets.serve(chat_handler, '127.0.0.1', 8765)
    print("Server started on ws://127.0.0.1:8765")
    
    # 물건 등록 시 알림을 주기적으로 확인
    while True:
        await item_check_and_notify()
        await asyncio.sleep(5)  # 5초마다 물건 등록 상태 확인

# 서버 실행
if __name__ == "__main__":
    asyncio.run(main())
