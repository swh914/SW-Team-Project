import asyncio
import websockets

connected_clients = set()  # 연결된 클라이언트를 관리할 집합

async def chat_handler(websocket, path):
    """클라이언트 연결과 메시지 송수신 처리"""
    # 클라이언트 연결 추가
    connected_clients.add(websocket)
    try:
        # 클라이언트로부터 메시지를 지속적으로 받음
        async for message in websocket:
            print(f"Received message: {message}")

            # 모든 클라이언트에게 메시지 브로드캐스트
            for client in connected_clients:
                if client != websocket:  # 메시지를 보낸 클라이언트는 제외
                    try:
                        await client.send(message)
                    except:
                        connected_clients.remove(client)
    finally:
        # 연결 종료 시 클라이언트 리스트에서 제거
        connected_clients.remove(websocket)

async def main():
    """서버를 실행"""
    server = await websockets.serve(chat_handler, '127.0.0.1', 8765)
    print("Server started on ws://127.0.0.1:8765")
    await server.wait_closed()

# 서버 시작
if __name__ == "__main__":
    asyncio.run(main())
