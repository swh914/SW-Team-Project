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
            try:
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
            except ValueError:
                print(f"잘못된 데이터: {line.strip()}")
                continue

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
    main_window.title("메인 화면")
    main_window.geometry("500x700")

    # 메인 화면 내용
    tk.Label(main_window, text="메인 화면", font=("Arial", 20)).pack(pady=20)

    # 탭 UI (하단 5개 탭 버튼)
    create_bottom_tabs(main_window)

# 하단 탭 UI 생성 함수
def create_bottom_tabs(parent):
    bottom_tabs_frame = tk.Frame(parent)
    bottom_tabs_frame.pack(side="bottom", fill="x", pady=10)

    tab_buttons = [
        ("상품등록", open_add_product_window),
        ("탭 2", lambda: show_message("탭 2 클릭")),
        ("탭 3", lambda: show_message("탭 3 클릭")),
        ("탭 4", lambda: show_message("탭 4 클릭")),
        ("내 정보", show_user_info)
    ]

    for text, command in tab_buttons:
        button = tk.Button(bottom_tabs_frame, text=text, command=command, width=10, height=2)
        button.pack(side="left", padx=5)

# 상품 등록 창 열기
def open_add_product_window():
    global add_product_window, entry_product_name, entry_product_price, entry_product_description, category_var

    categories = [
        "전자기기", "의류 및 패션", "가구 및 생활",
        "유아용품", "스포츠 및 레저", "책 및 문구", "기타"
    ]

    add_product_window = tk.Toplevel(root)
    add_product_window.title("상품 추가")
    add_product_window.geometry("400x400")

    tk.Label(add_product_window, text="상품명:").pack(pady=5)
    entry_product_name = tk.Entry(add_product_window)
    entry_product_name.pack(pady=5)

    tk.Label(add_product_window, text="가격:").pack(pady=5)
    entry_product_price = tk.Entry(add_product_window)
    entry_product_price.pack(pady=5)

    tk.Label(add_product_window, text="상품 설명:").pack(pady=5)
    entry_product_description = tk.Entry(add_product_window)
    entry_product_description.pack(pady=5)

    tk.Label(add_product_window, text="카테고리:").pack(pady=5)
    category_var = tk.StringVar(value="카테고리 선택")
    category_menu = tk.OptionMenu(add_product_window, category_var, *categories)
    category_menu.pack(pady=5)

    tk.Button(add_product_window, text="추가", command=add_product).pack(pady=10)

# 상품 추가 함수
def add_product():
    product_name = entry_product_name.get()
    product_price = entry_product_price.get()
    product_description = entry_product_description.get()
    product_category = category_var.get()

    if not product_name or not product_price or not product_description or product_category == "카테고리 선택":
        messagebox.showerror("상품 추가 오류", "모든 정보를 입력해주세요.")
        return

    with open(PRODUCTS_FILE, "a") as file:
        file.write(f"{product_name},{product_price},{product_description},{product_category}\n")

    messagebox.showinfo("상품 추가 성공", "상품이 추가되었습니다.")
    add_product_window.destroy()

# 메인 윈도우 생성
root = tk.Tk()
root.title("울산마켓 로그인")
root.geometry("500x600")
root.configure(bg="#A8D08D")

tk.Label(root, text="울산마켓", font=("Arial", 24, "bold"), bg="#A8D08D", fg="white").pack(pady=20)
tk.Label(root, text="아이디:", font=("Arial", 14), bg="#A8D08D", fg="white").pack(pady=5)
entry_id = tk.Entry(root, font=("Arial", 14))
entry_id.pack(pady=5)

tk.Label(root, text="비밀번호:", font=("Arial", 14), bg="#A8D08D", fg="white").pack(pady=5)
entry_password = tk.Entry(root, font=("Arial", 14), show="*")
entry_password.pack(pady=5)

tk.Button(root, text="로그인", command=login, font=("Arial", 14), bg="white", fg="#A8D08D", width=20).pack(pady=20)
tk.Button(root, text="회원가입", command=open_register_window, font=("Arial", 14), bg="white", fg="#A8D08D", width=20).pack(pady=10)

footer_label = tk.Label(root, text="울산마켓과 함께 하는 즐거운 거래!", font=("Arial", 12, "italic"), bg="#A8D08D", fg="white")
footer_label.pack(pady=30)

root.mainloop()
