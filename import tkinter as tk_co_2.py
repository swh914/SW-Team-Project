import tkinter as tk
from tkinter import messagebox, Toplevel
import os

# 사용자 데이터 파일
USER_DATA_FILE = "user_data.txt"
PRODUCT_DATA_FILE = "product_data.txt"

# 사용자 데이터 저장 함수
def save_user(username, password):
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{password}\n")

# 사용자 데이터 불러오기 함수
def load_users():
    users = {}
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                username, password = line.strip().split(",")
                users[username] = password
    return users

# 상품 데이터 저장 함수
def save_product(title, description):
    with open(PRODUCT_DATA_FILE, "a") as file:
        file.write(f"{title},{description}\n")

# 상품 데이터 불러오기 함수
def load_products():
    products = []
    if os.path.exists(PRODUCT_DATA_FILE):
        with open(PRODUCT_DATA_FILE, "r") as file:
            for line in file:
                title, description = line.strip().split(",")
                products.append((title, description))
    return products

# 회원가입 함수
def register_user():
    reg_username = entry_reg_id.get()
    reg_password = entry_reg_password.get()

    if not reg_username or not reg_password:
        messagebox.showerror("회원가입 오류", "아이디와 비밀번호를 모두 입력해주세요.")
        return

    users = load_users()
    if reg_username in users:
        messagebox.showerror("회원가입 오류", "이미 존재하는 아이디입니다.")
        return

    save_user(reg_username, reg_password)
    messagebox.showinfo("회원가입 성공", "회원가입이 완료되었습니다!")
    reg_window.destroy()

# 로그인 함수
def login_user():
    username = entry_login_id.get()
    password = entry_login_password.get()

    users = load_users()
    if username in users and users[username] == password:
        messagebox.showinfo("로그인 성공", f"환영합니다, {username}님!")
        open_product_window()
    else:
        messagebox.showerror("로그인 실패", "아이디 또는 비밀번호가 잘못되었습니다.")

# 상품 등록 창 열기
def open_product_window():
    global product_window, entry_product_title, entry_product_description

    product_window = Toplevel(root)
    product_window.title("상품 관리")
    product_window.geometry("400x500")

    tk.Label(product_window, text="상품 등록", font=("Arial", 16, "bold")).pack(pady=10)

    # 상품 제목
    tk.Label(product_window, text="상품 제목:").pack(pady=5)
    entry_product_title = tk.Entry(product_window, width=30)
    entry_product_title.pack(pady=5)

    # 상품 설명
    tk.Label(product_window, text="상품 설명:").pack(pady=5)
    entry_product_description = tk.Entry(product_window, width=30)
    entry_product_description.pack(pady=5)

    # 상품 등록 버튼
    tk.Button(product_window, text="상품 등록", command=add_product).pack(pady=10)

    # 상품 목록 보기
    tk.Button(product_window, text="상품 목록 보기", command=show_products).pack(pady=10)

# 상품 등록 함수
def add_product():
    title = entry_product_title.get()
    description = entry_product_description.get()

    if not title or not description:
        messagebox.showerror("상품 등록 오류", "모든 필드를 입력해주세요.")
        return

    save_product(title, description)
    messagebox.showinfo("등록 완료", "상품이 등록되었습니다.")
    entry_product_title.delete(0, tk.END)
    entry_product_description.delete(0, tk.END)

# 상품 목록 보기 함수
def show_products():
    products = load_products()
    if not products:
        messagebox.showinfo("상품 목록", "등록된 상품이 없습니다.")
        return

    product_list_window = Toplevel(root)
    product_list_window.title("상품 목록")
    product_list_window.geometry("400x300")

    for title, description in products:
        tk.Label(product_list_window, text=f"제목: {title}\n설명: {description}", anchor="w", justify="left").pack(pady=5)

# 회원가입 창 열기
def open_register_window():
    global reg_window, entry_reg_id, entry_reg_password

    reg_window = Toplevel(root)
    reg_window.title("회원가입")
    reg_window.geometry("300x200")

    tk.Label(reg_window, text="회원가입", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Label(reg_window, text="아이디:").pack(pady=5)
    entry_reg_id = tk.Entry(reg_window)
    entry_reg_id.pack(pady=5)

    tk.Label(reg_window, text="비밀번호:").pack(pady=5)
    entry_reg_password = tk.Entry(reg_window, show="*")
    entry_reg_password.pack(pady=5)

    tk.Button(reg_window, text="회원가입", command=register_user).pack(pady=10)

# 메인 윈도우
root = tk.Tk()
root.title("로그인 화면")
root.geometry("500x600")

# 이미지 로드
try:
    carrot_img = tk.PhotoImage(file="carrot_logo_large.png")
    logo_label = tk.Label(root, image=carrot_img)
    logo_label.pack(pady=20)
except Exception as e:
    tk.Label(root, text="이미지를 불러올 수 없습니다.", font=("Arial", 20, "bold")).pack(pady=20)

# 로그인 창
tk.Label(root, text="아이디:").pack(pady=5)
entry_login_id = tk.Entry(root)
entry_login_id.pack(pady=5)

tk.Label(root, text="비밀번호:").pack(pady=5)
entry_login_password = tk.Entry(root, show="*")
entry_login_password.pack(pady=5)

tk.Button(root, text="로그인", command=login_user).pack(pady=10)
tk.Button(root, text="회원가입", command=open_register_window).pack(pady=10)

root.mainloop()
