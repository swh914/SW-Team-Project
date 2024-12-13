import tkinter as tk
from tkinter import messagebox
import os

# 데이터 파일 이름
USER_DATA_FILE = "user_data.txt"
PRODUCTS_FILE = "products.txt"
USER_INFO_FILE = "user_info.txt"  # 사용자 추가 정보 저장

# 전역 변수
current_user_name = ""
current_user_phone = ""
current_user_address = ""  # 거주지
current_user_interests = ""  # 관심 물품

# 기본 상품 데이터 추가 (테스트용)
def ensure_test_data():
    if not os.path.exists(PRODUCTS_FILE) or os.stat(PRODUCTS_FILE).st_size == 0:
        with open(PRODUCTS_FILE, "w") as file:
            file.write("테스트 상품1,10000,테스트 설명1\n")
            file.write("테스트 상품2,20000,테스트 설명2\n")

# 회원가입 함수
def register():
    reg_username = entry_reg_id.get()
    reg_password = entry_reg_password.get()
    reg_name = entry_reg_name.get()
    reg_phone = entry_reg_phone.get()

    if not reg_username or not reg_password or not reg_name or not reg_phone:
        messagebox.showerror("회원가입 오류", "모든 정보를 입력해주세요.")
        return

    reg_phone = "010" + reg_phone
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{reg_username},{reg_password},{reg_name},{reg_phone}\n")
    messagebox.showinfo("회원가입 성공", "회원가입이 완료되었습니다!")
    reg_window.destroy()

# 로그인 함수
def login():
    user_id = entry_id.get()
    user_password = entry_password.get()

    if not os.path.exists(USER_DATA_FILE):
        messagebox.showerror("로그인 오류", "회원정보가 없습니다. 회원가입을 진행해주세요.")
        return

    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            username, password, name, phone = line.strip().split(",")
            if user_id == username and user_password == password:
                global current_user_name, current_user_phone
                current_user_name = name
                current_user_phone = phone
                messagebox.showinfo("로그인 성공", f"환영합니다, {name}님!")
                root.withdraw()
                load_user_info()  # 사용자 정보 불러오기
                show_main_screen()
                return

    messagebox.showerror("로그인 실패", "아이디 또는 비밀번호가 잘못되었습니다.")

# 메인 화면 함수
def show_main_screen():
    global main_window, canvas, product_list_frame

    ensure_test_data()  # 기본 상품 데이터 추가
    main_window = tk.Toplevel(root)
    main_window.title("메인 화면")
    main_window.geometry("500x700")
    main_window.configure(bg="#4CAF50")  # 밝은 초록색 배경

    tk.Label(main_window, text="메인 화면", font=("Arial", 20, "bold"), bg="#4CAF50", fg="white").pack(pady=10)

    product_frame = tk.Frame(main_window, bg="#4CAF50")
    product_frame.pack(fill="both", expand=True, pady=(10, 0))

    canvas = tk.Canvas(product_frame, bg="#4CAF50")
    scrollbar = tk.Scrollbar(product_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#4CAF50")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    product_list_frame = scrollable_frame
    update_product_list()

    create_bottom_tabs(main_window)

# 상품 목록 업데이트 함수
def update_product_list():
    for widget in product_list_frame.winfo_children():
        widget.destroy()

    if not os.path.exists(PRODUCTS_FILE) or os.stat(PRODUCTS_FILE).st_size == 0:
        tk.Label(product_list_frame, text="등록된 상품이 없습니다.", font=("Arial", 14), fg="gray", bg="#4CAF50").pack(pady=20)
        return

    with open(PRODUCTS_FILE, "r") as file:
        products = [line.strip().split(",") for line in file.readlines()]

    for product in products:
        product_name, product_price, product_description = product
        frame = tk.Frame(product_list_frame, pady=5, bg="#4CAF50")
        frame.pack(fill="x", padx=10)

        tk.Label(frame, text=f"상품명: {product_name}", font=("Arial", 12), bg="#4CAF50", fg="white").pack(anchor="w")
        tk.Label(frame, text=f"가격: {product_price}원", font=("Arial", 12), bg="#4CAF50", fg="white").pack(anchor="w")
        tk.Label(frame, text=f"설명: {product_description}", font=("Arial", 10), fg="gray", bg="#4CAF50").pack(anchor="w")

# 상품 등록 창
def open_product_registration():
    global product_reg_window, entry_product_name, entry_product_price, entry_product_description

    product_reg_window = tk.Toplevel(root)
    product_reg_window.title("상품 등록")
    product_reg_window.geometry("400x300")
    product_reg_window.configure(bg="#4CAF50")

    tk.Label(product_reg_window, text="상품명:", bg="#4CAF50", fg="white").pack(pady=5)
    entry_product_name = tk.Entry(product_reg_window)
    entry_product_name.pack(pady=5)

    tk.Label(product_reg_window, text="가격:", bg="#4CAF50", fg="white").pack(pady=5)
    entry_product_price = tk.Entry(product_reg_window)
    entry_product_price.pack(pady=5)

    tk.Label(product_reg_window, text="상품 설명:", bg="#4CAF50", fg="white").pack(pady=5)
    entry_product_description = tk.Entry(product_reg_window)
    entry_product_description.pack(pady=5)

    tk.Button(product_reg_window, text="등록", command=register_product, bg="white", fg="#4CAF50").pack(pady=10)

# 상품 등록 함수
def register_product():
    product_name = entry_product_name.get()
    product_price = entry_product_price.get()
    product_description = entry_product_description.get()

    if not product_name or not product_price or not product_description:
        messagebox.showerror("상품 등록 오류", "모든 정보를 입력해주세요.")
        return

    with open(PRODUCTS_FILE, "a") as file:
        file.write(f"{product_name},{product_price},{product_description}\n")

    messagebox.showinfo("상품 등록 성공", "상품이 등록되었습니다!")
    product_reg_window.destroy()
    update_product_list()

# 내 정보 화면
def show_user_info():
    global user_info_window, entry_address, entry_interests

    user_info_window = tk.Toplevel(root)
    user_info_window.title("내 정보")
    user_info_window.geometry("400x400")
    user_info_window.configure(bg="#4CAF50")  # 밝은 초록색 배경

    tk.Label(user_info_window, text=f"이름: {current_user_name}", font=("Arial", 14), bg="#4CAF50", fg="white").pack(pady=10)
    tk.Label(user_info_window, text=f"전화번호: {current_user_phone}", font=("Arial", 14), bg="#4CAF50", fg="white").pack(pady=10)

    tk.Label(user_info_window, text="거주지역:", bg="#4CAF50", fg="white").pack(pady=5)
    entry_address = tk.Entry(user_info_window)
    entry_address.insert(0, current_user_address)
    entry_address.pack(pady=5)

    tk.Label(user_info_window, text="관심 물품:", bg="#4CAF50", fg="white").pack(pady=5)
    entry_interests = tk.Entry(user_info_window)
    entry_interests.insert(0, current_user_interests)
    entry_interests.pack(pady=5)

    tk.Button(user_info_window, text="저장", command=save_user_info, bg="white", fg="#4CAF50").pack(pady=10)

# 내 정보 저장 함수
def save_user_info():
    global current_user_address, current_user_interests

    current_user_address = entry_address.get()
    current_user_interests = entry_interests.get()

    with open(USER_INFO_FILE, "a") as file:
        file.write(f"{current_user_name},{current_user_address},{current_user_interests}\n")

    messagebox.showinfo("저장 성공", "내 정보가 저장되었습니다.")

# 사용자 정보 불러오기 함수
def load_user_info():
    global current_user_address, current_user_interests

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

# 하단 탭 생성 함수
def create_bottom_tabs(parent):
    bottom_tabs_frame = tk.Frame(parent, bg="#4CAF50")
    bottom_tabs_frame.pack(side="bottom", fill="x", pady=10)

    tab_buttons = [
        ("상품등록", open_product_registration),
        ("채팅", lambda: print("채팅 클릭")),
        ("구매내역", lambda: print("구매내역 클릭")),
        ("내 정보", show_user_info)
    ]

    for text, command in tab_buttons:
        tk.Button(bottom_tabs_frame, text=text, command=command, width=15, height=2, bg="white", fg="#4CAF50").pack(side="left", expand=True)

# 메인 윈도우
root = tk.Tk()
root.title("울산마켓 로그인")
root.geometry("500x600")
root.configure(bg="#4CAF50")  # 밝은 초록색 배경

tk.Label(root, text="울산마켓", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white").pack(pady=20)
tk.Label(root, text="아이디:", bg="#4CAF50", fg="white").pack()
entry_id = tk.Entry(root)
entry_id.pack()

tk.Label(root, text="비밀번호:", bg="#4CAF50", fg="white").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="로그인", command=login, bg="white", fg="#4CAF50").pack(pady=10)
tk.Button(root, text="회원가입", command=lambda: print("회원가입 클릭"), bg="white", fg="#4CAF50").pack()

root.mainloop()
