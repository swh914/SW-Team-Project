import tkinter as tk 
from tkinter import messagebox, ttk
import firebase_admin
from firebase_admin import credentials, db
import threading

# Firebase 서비스 계정 키 파일 경로
cred = credentials.Certificate("C:/Users/0914s/Desktop/SWproject/serviceAccountKey.json")

# Firebase 초기화
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sw-project-7ef51-default-rtdb.firebaseio.com'
})

# 데이터베이스 참조
users_ref = db.reference("users")
products_ref = db.reference("products")
categories = [
    "디지털/가전", "가구/인테리어", "유아동/유아도서", "생활/가공식품",
    "여성의류/잡화", "뷰티/미용", "남성의류/잡화", "스포츠/레저",
    "게임/취미", "도서/티켓/음반", "반려동물용품", "기타", "삽니다"
]

# 로그인 함수
def login():
    global current_user_id, current_user_name
    user_id = entry_id.get().strip()
    user_password = entry_password.get().strip()

    if not user_id or not user_password:
        messagebox.showerror("로그인 오류", "아이디와 비밀번호을 입력해주세요.")
        return

    try:
        user_data = users_ref.child(user_id).get()

        if user_data and user_data["password"] == user_password:
            current_user_id = user_id
            current_user_name = user_data["name"]
            messagebox.showinfo("로그인 성공", f"{current_user_name}님, 환영합니다!")
            root.withdraw()
            show_main_screen()
        else:
            messagebox.showerror("로그인 실패", "아이디 또는 비밀번호이 잘못되었습니다.")
    except Exception as e:
        messagebox.showerror("Firebase 오류", f"로그인 중 오류 발생: {str(e)}")

# 메인 화면 함수
def show_main_screen():
    main_window = tk.Toplevel(root)
    main_window.title("메인 화면")
    main_window.geometry("500x500")

    tk.Label(main_window, text=f"{current_user_name}님, 환영합니다!", font=("Arial", 20)).pack(pady=20)

    create_bottom_tabs(main_window)

def create_bottom_tabs(parent):
    bottom_tabs_frame = tk.Frame(parent)
    bottom_tabs_frame.pack(side="bottom", fill="x", pady=10)

    # 버튼 리스트에 채팅 버튼 추가
    tabs = [
        ("상품 목록", show_product_list),
        ("상품 등록", open_add_product_window),
        ("검색", search_items),
        ("채팅", chat_placeholder)  # 채팅 버튼 추가 (기능 없음)
    ]

    for text, command in tabs:
        tk.Button(bottom_tabs_frame, text=text, command=command).pack(side="left", padx=5)

# 채팅 버튼의 임시 함수 (아직 기능 없음)
def chat_placeholder():
    messagebox.showinfo("채팅", "채팅 기능은 아직 준비 중입니다.")

# 상품 등록창 함수
def open_add_product_window():
    add_product_window = tk.Toplevel(root)
    add_product_window.title("상품 추가")

    tk.Label(add_product_window, text="상품명:").pack(pady=5)
    entry_product_name = tk.Entry(add_product_window)
    entry_product_name.pack()

    tk.Label(add_product_window, text="가격:").pack(pady=5)
    entry_product_price = tk.Entry(add_product_window)
    entry_product_price.pack()

    tk.Label(add_product_window, text="설명:").pack(pady=5)
    entry_product_description = tk.Entry(add_product_window)
    entry_product_description.pack()

    tk.Label(add_product_window, text="카테고리 선택:").pack(pady=5)
    selected_category = tk.StringVar(value=categories[0])
    tk.OptionMenu(add_product_window, selected_category, *categories).pack()

    def add_product():
        name = entry_product_name.get()
        price = entry_product_price.get()
        description = entry_product_description.get()
        category = selected_category.get()

        if not name or not price or not description:
            messagebox.showerror("오류", "모든 정보를 입력해주세요.")
            return

        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("오류", "가격 입력이 잘못되었습니다.")
            return

        products_ref.push({"name": name, "price": price, "description": description, "category": category})
        messagebox.showinfo("등록 성공", f"{name} 상품이 등록되었습니다.")
        add_product_window.destroy()

    tk.Button(add_product_window, text="등록", command=add_product).pack()

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

# 검색창 함수
def search_items():
    search_window = tk.Toplevel(root)
    search_window.title("검색")
    search_window.geometry("400x300")

    tk.Label(search_window, text="검색 옵션 선택", font=("Arial", 20)).pack(pady=10)

    tk.Button(search_window, text="직접 검색", command=direct_search).pack(pady=10)
    tk.Button(search_window, text="카테고리 검색", command=category_search).pack(pady=10)


# 상품 목록 화면 함수
def show_product_list():
    product_window = tk.Toplevel(root)
    product_window.title("상품 목록")
    product_window.geometry("400x400")

    tk.Label(product_window, text="상품 목록", font=("Arial", 20)).pack(pady=10)

    products_data = products_ref.get()

    if products_data:
        for key, product in products_data.items():
            product_frame = tk.Frame(product_window, padx=10, pady=5)
            product_frame.pack(fill="x", padx=5, pady=5)

            tk.Label(product_frame, text=f"{product['name']} - {product['price']}원").pack(side="left")
            tk.Label(product_frame, text=f"카테고리: {product['category']}").pack(side="right")

# 루트 tkinter 창 설정
root = tk.Tk()
root.title("로그인 화면")
root.geometry("300x300")

tk.Label(root, text="아이디:").pack(pady=5)
entry_id = tk.Entry(root)
entry_id.pack()

tk.Label(root, text="비밀번호:").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="로그인", command=login).pack(pady=20)

current_user_id = None
current_user_name = None

root.mainloop()
