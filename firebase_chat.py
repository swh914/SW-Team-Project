import firebase_admin
from firebase_admin import credentials, db

# Firebase 인증 정보 설정
cred = credentials.Certificate("C:/Users/0914s/Desktop/SWproject/serviceAccountKey.json")  # 서비스 계정 키 파일 경로
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sw-project-7ef51-default-rtdb.firebaseio.com'  # Firebase Realtime Database URL
})

# 🔹 메시지 저장 기능
def send_message(chat_id, sender_id, text):
    ref = db.reference(f'chats/{chat_id}/messages')
    ref.push({
        'sender_id': sender_id,
        'text': text
    })
    print(f"{sender_id}: {text}")

# 🔹 실시간 메시지 리스닝 기능
def listen_messages(chat_id):
    ref = db.reference(f'chats/{chat_id}/messages')

    def stream_handler(message):
        if message.data:
            msg_data = message.data

            # 딕셔너리 키 존재 여부 확인
            sender_id = msg_data.get('sender_id', 'Unknown')
            text = msg_data.get('text', '')

            print(f"{sender_id}: {text}")

    ref.listen(stream_handler)

# 🔹 채팅 테스트 기능 (메시지 보내기 및 리스닝 테스트)
def chat_app():
    chat_id = 'room1'
    sender_id = input("Enter your username: ")

    # Start listening to messages in a separate thread
    import threading
    listener_thread = threading.Thread(target=listen_messages, args=(chat_id,))
    listener_thread.daemon = True  # 프로그램 종료 시 리스너도 종료됩니다.
    listener_thread.start()

    # 채팅 전송 루프
    while True:
        text = input("Enter your message (type 'quit' to exit): ")
        if text.lower() == "quit":
            print("Exiting chat...")
            break
        send_message(chat_id, sender_id, text)

if __name__ == "__main__":
    chat_app()