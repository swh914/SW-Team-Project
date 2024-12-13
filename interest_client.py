import asyncio
import websockets

async def send_interest(websocket):
    """사용자가 관심 있는 해시태그를 설정"""
    interests = input("Enter your interests (comma separated): ")
    await websocket.send(interests)  # 관심 해시태그를 서버로 전송

async def receive_notification(websocket):
    """서버로부터 알림을 수신"""
    while True:
        message = await websocket.recv()
        print(f"Notification: {message}")

async def main():
    uri = "ws://127.0.0.1:8765"
    async with websockets.connect(uri) as websocket:
        await send_interest(websocket)  # 관심 해시태그 설정
        await receive_notification(websocket)  # 알림 수신

if __name__ == "__main__":
    asyncio.run(main())
