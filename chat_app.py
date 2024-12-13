import firebase_admin
from firebase_admin import credentials, db
import tkinter as tk
from tkinter import scrolledtext
import threading
import sys

# Firebase 인증 정보 설정
cred = credentials.Certificate("C:/Users/USER/Desktop/project/serviceAccountKey.json")  # 서비스 계정 키 파일 경로
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sw-project-7ef51-default-rtdb.firebaseio.com'  # Firebase Realtime Database URL
})

sender_id = sys.argv[1]

# 🔹 메시지 저장 기능
def send_message(chat_id, sender_id, text):
    ref = db.reference(f'chats/{chat_id}/messages')
    ref.push({
        'sender_id': sender_id,
        'text': text
    })
    print(f"{sender_id}: {text}")

# 🔹 실시간 메시지 리스닝 기능 (UI 업데이트)
def listen_messages(chat_id, text_widget):
    ref = db.reference(f'chats/{chat_id}/messages')

    def stream_handler(message):
        if message.data:
            msg_data = message.data
            if msg_data.get('sender_id') == sender_id:
                print("same")
            else:    
                sender_id1 = msg_data.get('sender_id')
                text = msg_data.get('text')

                # Tkinter UI 업데이트는 메인 스레드에서 해야 하므로, `after`를 사용
                text_widget.after(0, lambda: update_chat(text_widget, sender_id1, text))

    ref.listen(stream_handler)

# 🔹 UI에서 채팅 메시지 업데이트
def update_chat(text_widget, sender_id, text):
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, f"{sender_id}: {text}\n")  # 메시지 표시
    text_widget.yview(tk.END)  # 자동으로 스크롤
    text_widget.config(state=tk.DISABLED)

# 🔹 카카오톡 스타일의 Tkinter GUI를 만드는 함수
def create_chat_gui():
    # Tkinter 윈도우 생성
    chat_root = tk.Tk()
    chat_root.title("Chat")

    # 스크롤 가능한 텍스트 위젯(메시지 표시 영역)
    text_widget = scrolledtext.ScrolledText(chat_root, width=50, height=20, wrap=tk.WORD)
    text_widget.pack(padx=10, pady=10)
    text_widget.config(state=tk.DISABLED)  # 사용자 입력 불가(읽기 전용)

    # 메시지 입력 필드
    message_input = tk.Entry(chat_root, width=50)
    message_input.pack(padx=10, pady=5)

    # 이전 메시지 표시 함수
    def display_history():
        ref = db.reference(f'chats/{chat_id}/messages')
        data = ref.get()

        if data:
            for key, item in data.items():
                update_chat(text_widget, item['sender_id'], item['text'])  # 이전 메시지 표시

    display_history()

    # 채팅 전송 버튼을 위한 함수
    def send_message_button():
        text = message_input.get()
        if text.strip():  # 빈 메시지는 보내지 않음
            send_message(chat_id, sender_id, text)
            update_chat(text_widget, sender_id, text)  # 자신이 보낸 메시지 표시
            message_input.delete(0, tk.END)  # 입력 필드 초기화

    # 전송 버튼
    send_button = tk.Button(chat_root, text="Send", command=send_message_button)
    send_button.pack(padx=10, pady=10)

    return chat_root, text_widget, message_input

# 🔹 채팅 앱 실행 함수
def chat_app():
    global sender_id, chat_id
    chat_id = 'room1'

    # Tkinter GUI 생성
    chat_root, text_widget, message_input = create_chat_gui()

    # 실시간 메시지 리스닝을 별도 스레드로 실행
    listener_thread = threading.Thread(target=listen_messages, args=(chat_id, text_widget))
    listener_thread.daemon = True  # 프로그램 종료 시 리스너도 종료됩니다.
    listener_thread.start()

    # Tkinter 이벤트 루프 시작
    chat_root.mainloop()

if __name__ == "__main__":
    chat_app()
