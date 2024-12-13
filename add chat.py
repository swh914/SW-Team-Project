import tkinter as tk
from tkinter import messagebox
import os
import firebase_admin
from firebase_admin import credentials, db
from tkinter import messagebox

# Firebase 초기화
cred = credentials.Certificate(r"C:\Users\qkrtk\Desktop\SW_Dev\SW-Team-Project\serviceAccountKey.json")  # 서비스 계정 키 파일 경로
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sw-project-7ef51-default-rtdb.firebaseio.com'  # Firebase Realtime Database URL
})

# 데이터 파일 이름
DATA_FILE = "user_data.txt"
PRODUCTS_FILE = "products.txt"
USER_INFO_FILE = "user_info.txt"  # 사용자 정보 저장 파일



# 전역 변수로 회원 정보 저장
current_user_name = ""
current_user_phone = ""
current_user_address = ""  # 거주지
current_user_interests = ""  # 관심 물품

# 회원정보 저장 함수
def save_user(username, password, name, phone):
    global current_user_name, current_user_phone
    '''
    with open(DATA_FILE, "a") as file:
        file.write(f"{username},{password},{name},{phone}\n")
    current_user_name = name  # 회원가입 시 이름 저장
    current_user_phone = phone  # 회원가입 시 전화번호 저장
    '''
    ref = db.reference('users')  # 'items' 경로 참조
    ref.push({
        'name': name,
        'password': password,
        'phone': phone,
        'username': username  # 카테고리 추가
    })

# 회원가입 함수
def register():
    reg_username = entry_reg_id.get()
    reg_password = entry_reg_password.get()
    reg_name = entry_reg_name.get()
    reg_phone = entry_reg_phone.get()

    # 정보 입력 여부 확인
    if not reg_username or not reg_password or not reg_name or not reg_phone:
        messagebox.showerror("회원가입 오류", "모든 정보를 입력해주세요.")
        return

    # 전화번호 앞에 010을 자동으로 붙임
    reg_phone = "010" + reg_phone

    # 사용자 정보 저장
    save_user(reg_username, reg_password, reg_name, reg_phone)
    messagebox.showinfo("회원가입 성공", "회원가입이 완료되었습니다!")
    reg_window.destroy()

def write_data(name, price, status, category):
    ref = db.reference('items')  # 'items' 경로 참조
    ref.push({
        'name': name,
        'price': price,
        'status': status,
        'category': category  # 카테고리 추가
    })

    print(f"{name}이(가) 데이터베이스에 성공적으로 추가되었습니다.")

# 로그인 함수
def login():
    username = entry_id.get()
    password = entry_password.get()

    ref = db.reference('users')

    if not username or not password:
        messagebox.showerror("로그인 오류", "아이디와 비밀번호를 입력하세요.")
        return

    '''
    if not os.path.exists(DATA_FILE):
        messagebox.showerror("로그인 오류", "회원정보가 없습니다. 회원가입을 진행해주세요.")
        return

    # 저장된 사용자 정보 확인
    with open(DATA_FILE, "r") as file:
        for line in file:
            username, password, name, phone = line.strip().split(",")
            if user_id == username and user_password == password:
                messagebox.showinfo("로그인 성공", f"환영합니다, {user_id}님!")
                root.withdraw()  # 로그인 후 기존 창을 숨김
                global current_user_name, current_user_phone
                current_user_name = name  # 로그인 후 이름 정보 업데이트
                current_user_phone = phone  # 로그인 후 전화번호 정보 업데이트
                
                # 로그인 후 사용자 정보를 불러오기
                load_user_info()
                show_main_screen()  # 메인 화면으로 넘어가기
                return
    '''

    data = ref.get()
    for key, user in data.items():  # data가 딕셔너리라면
        if user['username'] == username and user['password'] == password:
            global current_user_name, current_user_phone
            current_user_name = user['name']
            current_user_phone = user['phone']

            messagebox.showinfo("로그인 성공", f"환영합니다, {current_user_name}님!")
            show_main_screen()  # 메인 화면 호출
            return

    messagebox.showerror("로그인 실패", "아이디 또는 비밀번호가 잘못되었습니다.")

# 회원가입 창 열기
def open_register_window():
    global reg_window, entry_reg_id, entry_reg_password, entry_reg_name, entry_reg_phone

    # 회원가입 창 생성
    reg_window = tk.Toplevel(root)
    reg_window.title("회원가입")
    reg_window.geometry("400x400")  # 창 크기 키움

    # 회원가입 입력 필드
    tk.Label(reg_window, text="아이디:").pack(pady=5)
    entry_reg_id = tk.Entry(reg_window)
    entry_reg_id.pack(pady=5)

    tk.Label(reg_window, text="비밀번호:").pack(pady=5)
    entry_reg_password = tk.Entry(reg_window, show="*")
    entry_reg_password.pack(pady=5)

    tk.Label(reg_window, text="이름:").pack(pady=5)
    entry_reg_name = tk.Entry(reg_window)
    entry_reg_name.pack(pady=5)

    tk.Label(reg_window, text="전화번호:").pack(pady=5)
    entry_reg_phone = tk.Entry(reg_window)
    entry_reg_phone.pack(pady=5)

    # 회원가입 버튼
    tk.Button(reg_window, text="회원가입", command=register, width=20).pack(pady=10)

# 메인 화면 함수
def show_main_screen():
    global main_window
    main_window = tk.Toplevel(root)
    main_window.title("등록 상품")
    main_window.geometry("500x700")
    main_window.configure(bg="#A8D08D")

    # 메인 화면 내용
    tk.Label(main_window, text="등록 상품", font=("Arial", 20)).pack(pady=20)

    # 탭 UI (하단 5개 탭 버튼)
    create_bottom_tabs(main_window)

# 하단 탭 UI 생성 함수
def create_bottom_tabs(parent):
    # 하단 탭을 위한 프레임 생성
    bottom_tabs_frame = tk.Frame(parent)
    bottom_tabs_frame.pack(side="bottom", fill="x", pady=10)

    # 각 탭에 대한 버튼들
    tab_buttons = [
        ("상품 목록", show_product_list),
        ("상품 등록", open_add_product_window),
        ("검색", search_items),  # 검색 버튼 추가
        ("채팅", chat_app),
        ("구매내역", show_purchase_history),  # "탭 4"를 "구매내역"으로 변경
        ("내 정보", show_user_info)  # 내 정보 버튼
        
    ]

    for text, command in tab_buttons:
        button = tk.Button(bottom_tabs_frame, text=text, command=command, width=10, height=2)
        button.pack(side="left", padx=5)




        
# 채팅목록 화면 함수
def show_chat_list():
    chat_window = tk.Toplevel(root)
    chat_window.title("채팅 목록")
    chat_window.geometry("500x500")  # 창 크기 조정

    # 예시로 채팅 목록을 보여주는 라벨
    try:
        with open("chat_list.txt", "r") as file:
            chats = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        chats = []

    if not chats:
        tk.Label(chat_window, text="채팅 목록이 없습니다.", font=("Arial", 14)).pack(pady=20)
    else:
        for chat in chats:
            tk.Label(chat_window, text=f"채팅방: {chat}").pack(pady=5)


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

    
# 구매내역 화면 함수
def show_purchase_history():
    purchase_window = tk.Toplevel(root)
    purchase_window.title("구매내역")
    purchase_window.geometry("500x500")  # 창 크기 조정

    # 구매내역을 나타내는 라벨
    try:
        with open("purchase_history.txt", "r") as file:
            purchases = [line.strip().split(",") for line in file.readlines()]
    except FileNotFoundError:
        purchases = []

    if not purchases:
        tk.Label(purchase_window, text="구매내역이 없습니다.", font=("Arial", 14)).pack(pady=20)
    else:
        for purchase in purchases:
            tk.Label(purchase_window, text=f"상품명: {purchase[0]}, 가격: {purchase[1]}, 날짜: {purchase[2]}").pack(pady=5)

# 구매내역 저장 함수 (구매한 상품을 기록할 때 사용)
def save_purchase_history(product_name, product_price):
    from datetime import datetime

    purchase_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 현재 날짜 및 시간
    with open("purchase_history.txt", "a") as file:
        file.write(f"{product_name},{product_price},{purchase_date}\n")

# 상품 목록을 위한 화면 (상품 판매 창)
def show_product_list():
    product_window = tk.Toplevel(root)
    product_window.title("상품 목록")
    product_window.geometry("500x500")  # 창 크기 조정

    ref = db.reference('items')  # 'items' 경로 참조
    data = ref.get()
    print("\n데이터베이스에 저장된 아이템 목록:")
    if data:
        for key, item in data.items():
            tk.Label(product_window, text=f"상품: {item['name']}").pack(pady=5)
            tk.Label(product_window, text=f"가격: {item['price']}").pack(pady=5)
            tk.Label(product_window, text=f"카테고리: {item['category']}").pack(pady=5)
            tk.Button(product_window, text="삭제", command=lambda p= item: delete_product(p, product_window)).pack(pady=5)
             # 판매완료 버튼 추가
            if item['status'] != '판매완료':  # 판매완료 상태가 아닌 경우에만 버튼 활성화
                tk.Button(product_window, text="판매완료", command=lambda p=item, key=key: mark_as_sold(p, key, product_window)).pack(pady=5)
            else:
                tk.Label(product_window, text="판매완료", fg="green").pack(pady=5)
    else:
        print("데이터베이스에 저장된 아이템이 없습니다.")

        
    # 상품 목록을 위한 화면 (상품 판매 창)
def show_product_list():
    product_window = tk.Toplevel(root)
    product_window.title("상품 목록")
    product_window.geometry("500x500")  # 창 크기 조정

    ref = db.reference('items')  # 'items' 경로 참조
    data = ref.get()
    if data:
        for key, item in data.items():
            # 상품 정보 표시
            tk.Label(product_window, text=f"상품명: {item['name']}").pack(pady=5)
            tk.Label(product_window, text=f"가격: {item['price']}").pack(pady=5)
            tk.Label(product_window, text=f"카테고리: {item['category']}").pack(pady=5)

            # 삭제 버튼
            tk.Button(product_window, text="삭제", command=lambda p=item: delete_product(p, product_window)).pack(pady=5)
            
            # 판매완료 버튼 (상품이 판매 완료되었을 경우 판매 상태 업데이트)
            tk.Button(product_window, text="판매완료", command=lambda p=item, key=key: mark_as_sold(p, key, product_window)).pack(pady=5)
    else:
        messagebox.showinfo("상품 목록", "등록된 상품이 없습니다.")   
    # 상품 추가 버튼
    tk.Button(product_window, text="상품 추가", command=open_add_product_window).pack(pady=10)



#==================================================
def read_data():
    ref = db.reference('items')  # 'items' 경로 참조
    data = ref.get()
    print("\n데이터베이스에 저장된 아이템 목록:")
    if data:
        for key, item in data.items():
            print(f"{item['name']} - {item['price']}원 - {item['status']} - {item['category']}")
            tk.Label(product_window, text=f"상품: {items['name']}").pack(pady=5)
            tk.Label(product_window, text=f"가격: {items['price']}").pack(pady=5)
            tk.Label(product_window, text=f"카테고리: {items['catgory']}").pack(pady=5)
            tk.Button(product_window, text="삭제", command=lambda p=product: delete_product(p, product_window)).pack(pady=5)
            tk.Button(product_window, text="판매완료", command=lambda p=item, key=key: mark_as_sold(p, key, product_window)).pack(pady=5)
    else:
        print("데이터베이스에 저장된 아이템이 없습니다.")

#==================================================




# 상품 추가 창 열기
def open_add_product_window():
    global add_product_window, entry_product_name, entry_product_price, entry_product_category

    # 상품 추가 창 생성
    add_product_window = tk.Toplevel(root)
    add_product_window.title("상품 추가")
    add_product_window.geometry("400x300")

    # 상품 추가 입력 필드
    tk.Label(add_product_window, text="상품명:").pack(pady=5)
    entry_product_name = tk.Entry(add_product_window)
    entry_product_name.pack(pady=5)

    tk.Label(add_product_window, text="가격:").pack(pady=5)
    entry_product_price = tk.Entry(add_product_window)
    entry_product_price.pack(pady=5)

    tk.Label(add_product_window, text="상품 설명:").pack(pady=5)
    entry_product_category = tk.Entry(add_product_window)
    entry_product_category.pack(pady=5)

    # 상품 추가 버튼
    tk.Button(add_product_window, text="추가", command=add_product).pack(pady=10)

#=====================================
def write_data(name, price, category):
    ref = db.reference('items')  # 'items' 경로 참조
    ref.push({
        'name': name,
        'price': price,
        'category': category  # 카테고리 추가
    })

    print(f"{name}이(가) 데이터베이스에 성공적으로 추가되었습니다.")
#=====================================

# 판매완료 버튼을 눌렀을 때 상품의 상태를 "판매완료"로 업데이트하는 함수
def mark_as_sold(product, key, product_window):
    ref = db.reference(f'items/{key}')  # 해당 상품 경로 참조
    ref.update({
        'status': '판매완료'  # 상태를 '판매완료'로 업데이트
    })

    messagebox.showinfo("판매완료", f"{product['name']} 상품이 판매완료 상태로 변경되었습니다.")
    product_window.destroy()
    show_product_list()  # 판매 완료 후 상품 목록 다시 표시

# 상품 추가 함수
def add_product():
    product_name = entry_product_name.get()
    product_price = entry_product_price.get()
    product_category = entry_product_category.get()

    if not product_name or not product_price or not product_category:
        messagebox.showerror("상품 추가 오류", "모든 정보를 입력해주세요.")
        return

    write_data(product_name, product_price, product_category)

    messagebox.showinfo("상품 추가 성공", "상품이 추가되었습니다.")
    add_product_window.destroy()

# 상품 삭제 함수
def delete_product(product, product_window):

    ref = db.reference('items')  # 'items' 경로 참조
    data = ref.get()
    print("\n데이터베이스에 저장된 아이템 목록:")
    if data:
        for key, item in data.items():
            if item == product:
                user_ref = ref.child(key)  # 해당 사용자의 경로 참조
                user_ref.delete()




    product_window.destroy()
    show_product_list()  # 삭제 후 상품 목록 다시 표시

# 내 정보 화면
def show_user_info():
    global user_info_window, entry_address, entry_interests

    user_info_window = tk.Toplevel(root)
    user_info_window.title("내 정보")
    user_info_window.geometry("400x400")

    # 이름과 전화번호를 보여주는 레이블
    tk.Label(user_info_window, text=f"이름: {current_user_name}", font=("Arial", 14)).pack(pady=10)
    tk.Label(user_info_window, text=f"전화번호: {current_user_phone}", font=("Arial", 14)).pack(pady=10)

    # 거주지역와 관심 물품을 수정할 수 있는 입력 필드
    tk.Label(user_info_window, text="거주지역:").pack(pady=5)
    entry_address = tk.Entry(user_info_window)
    entry_address.insert(0, current_user_address)  # 현재 거주지역 값을 넣어줌
    entry_address.pack(pady=5)

    tk.Label(user_info_window, text="관심 물품:").pack(pady=5)
    entry_interests = tk.Entry(user_info_window)
    entry_interests.insert(0, current_user_interests)  # 현재 관심 물품 값을 넣어줌
    entry_interests.pack(pady=5)

    # 저장 버튼
    tk.Button(user_info_window, text="저장", command=save_user_info).pack(pady=10)

# 내 정보 저장 함수
def save_user_info():
    global current_user_address, current_user_interests

    # 거주지와 관심 물품 입력값 가져오기
    current_user_address = entry_address.get()
    current_user_interests = entry_interests.get()

    # 사용자 정보 파일에 거주지역과 관심 물품 저장
    with open(USER_INFO_FILE, "a") as file:
        file.write(f"{current_user_name},{current_user_address},{current_user_interests}\n")

    messagebox.showinfo("저장 성공", "내 정보가 저장되었습니다.")

# 사용자 정보 불러오기 함수
def load_user_info():
    global current_user_address, current_user_interests

    # user_info.txt 파일에서 해당 사용자 정보를 찾기
    if os.path.exists(USER_INFO_FILE):
        with open(USER_INFO_FILE, "r") as file:
            lines = file.readlines()
            for line in lines:
                name, address, interests = line.strip().split(",")
                if name == current_user_name:
                    current_user_address = address
                    current_user_interests = interests
                    return
    current_user_address = ""
    current_user_interests = ""

    # 직접 검색 함수
def direct_search():
    search_query_window = tk.Toplevel(root)
    search_query_window.title("직접 검색")
    search_query_window.geometry("400x200")

    tk.Label(search_query_window, text="검색 키워드 입력").pack(pady=10)
    search_entry = tk.Entry(search_query_window, width=50)
    search_entry.pack(pady=10)

    def search():
        keyword = search_entry.get().strip().lower()

        if not keyword:
            messagebox.showerror("검색 오류", "검색 키워드를 입력해주세요.")
            return

        products_data = products_ref.get()

        result_window = tk.Toplevel(root)
        result_window.title(f"검색 결과: {keyword}")

        if products_data:
            for key, product in products_data.items():
                if keyword in product.get("name", "").lower():
                    product_frame = tk.Frame(result_window, borderwidth=1, relief="solid", padx=10, pady=10)
                    product_frame.pack(fill="x", padx=5, pady=5)

                    tk.Label(product_frame, text=f"상품명: {product['name']}", font=("Arial", 14)).pack(anchor="w")
                    tk.Label(product_frame, text=f"가격: {product['price']}원", font=("Arial", 12)).pack(anchor="w")
                    tk.Label(product_frame, text=f"카테고리: {product['category']}", font=("Arial", 12)).pack(anchor="w")
                    tk.Label(product_frame, text=f"설명: {product.get('description', '')}", font=("Arial", 12), wraplength=500).pack(anchor="w")
        else:
            tk.Label(result_window, text="등록된 상품이 없습니다.", font=("Arial", 16), fg="red").pack()

    tk.Button(search_query_window, text="검색", command=search).pack()

# 카테고리 검색 함수
def category_search():
    category_window = tk.Toplevel(root)
    category_window.title("카테고리 선택")
    category_window.geometry("400x300")

    tk.Label(category_window, text="원하는 카테고리 선택", font=("Arial", 18)).pack(pady=10)

    selected_category = tk.StringVar(value=categories[0])
    tk.OptionMenu(category_window, selected_category, *categories).pack()

    def search():
        category = selected_category.get()
        products_data = products_ref.get()

        result_window = tk.Toplevel(root)
        result_window.title(f"{category} 카테고리 검색")

        if products_data:
            found = False
            for key, product in products_data.items():
                if product.get("category") == category:
                    product_frame = tk.Frame(result_window, borderwidth=1, relief="solid", padx=10, pady=10)
                    product_frame.pack(fill="x", padx=5, pady=5)

                    tk.Label(product_frame, text=f"상품명: {product['name']}", font=("Arial", 14)).pack(anchor="w")
                    tk.Label(product_frame, text=f"가격: {product['price']}원", font=("Arial", 12)).pack(anchor="w")
                    tk.Label(product_frame, text=f"설명: {product.get('description', '')}", font=("Arial", 12), wraplength=500).pack(anchor="w")

                    found = True

            if not found:
                tk.Label(result_window, text="해당 카테고리의 상품이 없습니다.", font=("Arial", 16), fg="red").pack()

        else:
            tk.Label(result_window, text="등록된 상품이 없습니다.", font=("Arial", 16), fg="red").pack()

    tk.Button(category_window, text="검색", command=search).pack(pady=20)

# 검색창 화면
def search_items():
    search_window = tk.Toplevel(root)
    search_window.title("검색")
    search_window.geometry("400x300")

    tk.Label(search_window, text="검색 옵션 선택", font=("Arial", 20)).pack(pady=10)

    tk.Button(search_window, text="직접 검색", command=direct_search).pack(pady=10)
    tk.Button(search_window, text="카테고리 검색", command=category_search).pack(pady=10)



# 알림 메시지 함수 (탭 클릭 시 알림)
def show_message(message):
    messagebox.showinfo("탭 클릭", message)

# 메인 윈도우 생성
root = tk.Tk()
root.title("울산마켓 로그인")
root.geometry("500x600")  # 창 크기 확대
root.configure(bg="#A8D08D")  # 짙은 초록색 파스텔 컬러

# "울산마켓" 제목 레이블 추가
tk.Label(root, text="울산마켓", font=("Arial", 24, "bold"), bg="#A8D08D", fg="white").pack(pady=20)

# 로그인 입력 필드
tk.Label(root, text="아이디:", font=("Arial", 14), bg="#A8D08D", fg="white").pack(pady=5)
entry_id = tk.Entry(root, font=("Arial", 14))
entry_id.pack(pady=5)

tk.Label(root, text="비밀번호:", font=("Arial", 14), bg="#A8D08D", fg="white").pack(pady=5)
entry_password = tk.Entry(root, font=("Arial", 14), show="*")
entry_password.pack(pady=5)

# 로그인 버튼
tk.Button(root, text="로그인", command=login, font=("Arial", 14), bg="white", fg="#A8D08D", width=20).pack(pady=20)

# 회원가입 버튼
tk.Button(root, text="회원가입", command=open_register_window, font=("Arial", 14), bg="white", fg="#A8D08D", width=20).pack(pady=10)

# 하단 문구
footer_label = tk.Label(root, text="울산마켓과 함께 하는 즐거운 거래!", font=("Arial", 12, "italic"), bg="#A8D08D", fg="white")
footer_label.pack(pady=30)

# GUI 실행
root.mainloop()
