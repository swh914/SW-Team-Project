import asyncio
import websockets

async def send_message():
    """사용자로부터 메시지를 입력받아 서버로 보내는 함수"""
    uri = "ws://127.0.0.1:8765"
    async with websockets.connect(uri) as websocket:
        # 클라이언트 이름 입력 받기
        nickname = input("Enter your nickname: ")
        await websocket.send(f"{nickname} has joined the chat!")

        while True:
            message = input("Message: ")
            if message.lower() == 'exit':  # 'exit' 입력 시 종료
                break
            await websocket.send(f"{nickname}: {message}")

async def receive_message():
    """서버로부터 받은 메시지를 출력하는 함수"""
    uri = "ws://127.0.0.1:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(message)

# 클라이언트 시작
async def main():
    # 송신과 수신을 동시에 처리
    await asyncio.gather(send_message(), receive_message())

if __name__ == "__main__":
    asyncio.run(main())
