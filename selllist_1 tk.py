import tkinter as tk
from tkinter import messagebox
import os

# 데이터 파일 이름
USER_DATA_FILE = "user_data.txt"
PRODUCTS_FILE = "products.txt"

# 전역 변수
current_user_name = ""

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
                global current_user_name
                current_user_name = name
                messagebox.showinfo("로그인 성공", f"환영합니다, {name}님!")
                root.withdraw()
                show_main_screen()
                return

    messagebox.showerror("로그인 실패", "아이디 또는 비밀번호가 잘못되었습니다.")
# 상품 목록 업데이트 함수
def update_product_list():
    """
    상품 목록을 갱신하고, products.txt에서 데이터를 읽어와 표시합니다.
    """
    for widget in product_list_frame.winfo_children():
        widget.destroy()

    # 파일이 없거나 비어 있을 경우 처리
    if not os.path.exists(PRODUCTS_FILE) or os.stat(PRODUCTS_FILE).st_size == 0:
        tk.Label(product_list_frame, text="등록된 상품이 없습니다.", font=("Arial", 14), fg="gray").pack(pady=20)
        return

    # 파일에서 상품 읽어오기
    with open(PRODUCTS_FILE, "r") as file:
        products = [line.strip().split(",") for line in file.readlines()]

    for product in products:
        product_name, product_price, product_description = product
        frame = tk.Frame(product_list_frame, pady=5)
        frame.pack(fill="x", padx=10)

        # 상품 정보 표시
        tk.Label(frame, text=f"상품명: {product_name}", font=("Arial", 12)).pack(anchor="w")
        tk.Label(frame, text=f"가격: {product_price}원", font=("Arial", 12)).pack(anchor="w")
        tk.Label(frame, text=f"설명: {product_description}", font=("Arial", 10), fg="gray").pack(anchor="w")

        # 수정/삭제 버튼
        button_frame = tk.Frame(frame)
        button_frame.pack(anchor="w", pady=5)
        tk.Button(button_frame, text="수정", command=lambda p=product: open_edit_product_window(p)).pack(side="left", padx=5)
        tk.Button(button_frame, text="삭제", command=lambda p=product: delete_product(p)).pack(side="left", padx=5)

# 상품 등록 함수
def add_product():
    """
    상품을 등록하고, 목록을 갱신합니다.
    """
    product_name = entry_product_name.get()
    product_price = entry_product_price.get()
    product_description = entry_product_description.get()

    if not product_name or not product_price or not product_description:
        messagebox.showerror("상품 등록 오류", "모든 정보를 입력해주세요.")
        return

    # 파일에 상품 저장
    with open(PRODUCTS_FILE, "a") as file:
        file.write(f"{product_name},{product_price},{product_description}\n")

    messagebox.showinfo("상품 등록 성공", "상품이 등록되었습니다.")
    add_product_window.destroy()
    update_product_list()

# 기본 상품 데이터 추가 (테스트용)
def ensure_test_data():
    """
    products.txt가 없거나 비어 있으면 테스트용 데이터를 추가합니다.
    """
    if not os.path.exists(PRODUCTS_FILE) or os.stat(PRODUCTS_FILE).st_size == 0:
        with open(PRODUCTS_FILE, "w") as file:
            file.write("테스트 상품1,10000,테스트 설명1\n")
            file.write("테스트 상품2,20000,테스트 설명2\n")

# 메인 화면 함수
def show_main_screen():
    global main_window, canvas, product_list_frame

    main_window = tk.Toplevel(root)
    main_window.title("메인 화면")
    main_window.geometry("500x700")

    # 상단 "메인 화면" 제목
    tk.Label(main_window, text="메인 화면", font=("Arial", 20, "bold")).pack(pady=10)

    # 상품 목록 영역 (스크롤 가능)
    product_frame = tk.Frame(main_window)
    product_frame.pack(fill="both", expand=True, pady=(10, 0))

    canvas = tk.Canvas(product_frame)
    scrollbar = tk.Scrollbar(product_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

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

    # 하단 탭
    create_bottom_tabs(main_window)

# 상품 목록 업데이트 함수
def update_product_list():
    for widget in product_list_frame.winfo_children():
        widget.destroy()

    if not os.path.exists(PRODUCTS_FILE) or os.stat(PRODUCTS_FILE).st_size == 0:
        tk.Label(product_list_frame, text="등록된 상품이 없습니다.", font=("Arial", 14), fg="gray").pack(pady=20)
    else:
        with open(PRODUCTS_FILE, "r") as file:
            products = [line.strip().split(",") for line in file.readlines()]

        for product in products:
            product_name, product_price, product_description = product
            frame = tk.Frame(product_list_frame, pady=5)
            frame.pack(fill="x", padx=10)

            tk.Label(frame, text=f"상품명: {product_name}", font=("Arial", 12)).pack(anchor="w")
            tk.Label(frame, text=f"가격: {product_price}원", font=("Arial", 12)).pack(anchor="w")
            tk.Label(frame, text=f"설명: {product_description}", font=("Arial", 10), fg="gray").pack(anchor="w")

            button_frame = tk.Frame(frame)
            button_frame.pack(anchor="w", pady=5)
            tk.Button(button_frame, text="수정", command=lambda p=product: open_edit_product_window(p)).pack(side="left", padx=5)
            tk.Button(button_frame, text="삭제", command=lambda p=product: delete_product(p)).pack(side="left", padx=5)

# 상품 수정 창 열기
def open_edit_product_window(product):
    global edit_product_window, entry_edit_name, entry_edit_price, entry_edit_description

    product_name, product_price, product_description = product

    edit_product_window = tk.Toplevel(root)
    edit_product_window.title("상품 수정")
    edit_product_window.geometry("400x300")

    tk.Label(edit_product_window, text="상품명:").pack(pady=5)
    entry_edit_name = tk.Entry(edit_product_window)
    entry_edit_name.insert(0, product_name)
    entry_edit_name.pack(pady=5)

    tk.Label(edit_product_window, text="가격:").pack(pady=5)
    entry_edit_price = tk.Entry(edit_product_window)
    entry_edit_price.insert(0, product_price)
    entry_edit_price.pack(pady=5)

    tk.Label(edit_product_window, text="설명:").pack(pady=5)
    entry_edit_description = tk.Entry(edit_product_window)
    entry_edit_description.insert(0, product_description)
    entry_edit_description.pack(pady=5)

    tk.Button(edit_product_window, text="수정", command=lambda: edit_product(product)).pack(pady=10)

# 상품 수정 함수
def edit_product(original_product):
    product_name, product_price, product_description = original_product

    new_name = entry_edit_name.get()
    new_price = entry_edit_price.get()
    new_description = entry_edit_description.get()

    if not new_name or not new_price or not new_description:
        messagebox.showerror("수정 오류", "모든 정보를 입력해주세요.")
        return

    with open(PRODUCTS_FILE, "r") as file:
        products = file.readlines()

    with open(PRODUCTS_FILE, "w") as file:
        for line in products:
            if line.strip() == ",".join(original_product):
                file.write(f"{new_name},{new_price},{new_description}\n")
            else:
                file.write(line)

    messagebox.showinfo("수정 성공", "상품 정보가 수정되었습니다.")
    edit_product_window.destroy()
    update_product_list()

# 상품 삭제 함수
def delete_product(product):
    with open(PRODUCTS_FILE, "r") as file:
        products = file.readlines()

    with open(PRODUCTS_FILE, "w") as file:
        for line in products:
            if line.strip() != ",".join(product):
                file.write(line)

    messagebox.showinfo("삭제 성공", f"상품 '{product[0]}'이(가) 삭제되었습니다.")
    update_product_list()

# 하단 탭 생성 함수
def create_bottom_tabs(parent):
    bottom_tabs_frame = tk.Frame(parent, bg="lightgray")
    bottom_tabs_frame.pack(side="bottom", fill="x", pady=10)

    tab_buttons = [
        ("상품등록", open_add_product_window),
        ("채팅", lambda: show_message("채팅 클릭")),
        ("구매내역", lambda: show_message("구매내역 클릭")),
        ("내 정보", lambda: show_message("내 정보 클릭"))
    ]

    for text, command in tab_buttons:
        tk.Button(bottom_tabs_frame, text=text, command=command, width=15, height=2).pack(side="left", expand=True)

# 상품 등록 창 열기
def open_add_product_window():
    global add_product_window, entry_product_name, entry_product_price, entry_product_description

    add_product_window = tk.Toplevel(root)
    add_product_window.title("상품 등록")
    add_product_window.geometry("400x300")

    tk.Label(add_product_window, text="상품명:").pack(pady=5)
    entry_product_name = tk.Entry(add_product_window)
    entry_product_name.pack(pady=5)

    tk.Label(add_product_window, text="가격:").pack(pady=5)
    entry_product_price = tk.Entry(add_product_window)
    entry_product_price.pack(pady=5)

    tk.Label(add_product_window, text="상품 설명:").pack(pady=5)
    entry_product_description = tk.Entry(add_product_window)
    entry_product_description.pack(pady=5)

    tk.Button(add_product_window, text="등록", command=add_product).pack(pady=10)

# 상품 등록 함수
def add_product():
    product_name = entry_product_name.get()
    product_price = entry_product_price.get()
    product_description = entry_product_description.get()

    if not product_name or not product_price or not product_description:
        messagebox.showerror("상품 등록 오류", "모든 정보를 입력해주세요.")
        return

    with open(PRODUCTS_FILE, "a") as file:
        file.write(f"{product_name},{product_price},{product_description}\n")

    messagebox.showinfo("상품 등록 성공", "상품이 등록되었습니다.")
    add_product_window.destroy()
    update_product_list()

# 알림 메시지 함수
def show_message(message):
    messagebox.showinfo("알림", message)

# 메인 윈도우
root = tk.Tk()
root.title("울산마켓 로그인")
root.geometry("500x600")

tk.Label(root, text="울산마켓", font=("Arial", 24, "bold")).pack(pady=20)
tk.Label(root, text="아이디:").pack()
entry_id = tk.Entry(root)
entry_id.pack()

tk.Label(root, text="비밀번호:").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="로그인", command=login).pack(pady=10)
tk.Button(root, text="회원가입", command=lambda: open_register_window()).pack()

root.mainloop()
