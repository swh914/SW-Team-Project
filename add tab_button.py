import tkinter as tk
from tkinter import messagebox
import os

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
    with open(DATA_FILE, "a") as file:
        file.write(f"{username},{password},{name},{phone}\n")
    current_user_name = name  # 회원가입 시 이름 저장
    current_user_phone = phone  # 회원가입 시 전화번호 저장

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

# 로그인 함수
def login():
    user_id = entry_id.get()
    user_password = entry_password.get()

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
        ("상품등록", open_add_product_window),
        ("검색", lambda: show_message("검색  클릭")),
        ("채팅", show_chat_list),
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

    # 상품 목록을 나타내는 라벨
    try:
        with open(PRODUCTS_FILE, "r") as file:
            products = [line.strip().split(",") for line in file.readlines()]
    except FileNotFoundError:
        products = []

    for product in products:
        tk.Label(product_window, text=f"상품: {product[0]}").pack(pady=5)
        tk.Label(product_window, text=f"가격: {product[1]}").pack(pady=5)
        tk.Label(product_window, text=f"설명: {product[2]}").pack(pady=5)
        tk.Button(product_window, text="삭제", command=lambda p=product: delete_product(p, product_window)).pack(pady=5)

    # 상품 추가 버튼
    tk.Button(product_window, text="상품 추가", command=open_add_product_window).pack(pady=10)

# 상품 추가 창 열기
def open_add_product_window():
    global add_product_window, entry_product_name, entry_product_price, entry_product_description

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
    entry_product_description = tk.Entry(add_product_window)
    entry_product_description.pack(pady=5)

    # 상품 추가 버튼
    tk.Button(add_product_window, text="추가", command=add_product).pack(pady=10)

# 상품 추가 함수
def add_product():
    product_name = entry_product_name.get()
    product_price = entry_product_price.get()
    product_description = entry_product_description.get()

    if not product_name or not product_price or not product_description:
        messagebox.showerror("상품 추가 오류", "모든 정보를 입력해주세요.")
        return

    with open(PRODUCTS_FILE, "a") as file:
        file.write(f"{product_name},{product_price},{product_description}\n")

    messagebox.showinfo("상품 추가 성공", "상품이 추가되었습니다.")
    add_product_window.destroy()

# 상품 삭제 함수
def delete_product(product, product_window):
    with open(PRODUCTS_FILE, "r") as file:
        products = file.readlines()

    with open(PRODUCTS_FILE, "w") as file:
        for line in products:
            if line.strip() != ",".join(product):
                file.write(line)

    messagebox.showinfo("상품 삭제", f"{product[0]} 상품이 삭제되었습니다.")
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
