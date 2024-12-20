import tkinter as tk
from tkinter import messagebox
import os
import firebase_admin
from firebase_admin import credentials, db
from tkinter import messagebox
from tkinter import scrolledtext
import threading
import subprocess
import win32gui, win32con

#  pywin32 에러 날 시 10line, 810,811 line 주석처리 하세요~~

cred = credentials.Certificate("C:/Users/USER/Desktop/project/serviceAccountKey.json")  # 서비스 계정 키 파일 경로
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sw-project-7ef51-default-rtdb.firebaseio.com'  # Firebase Realtime Database URL
})

categories = [
    "디지털/가전", "가구/인테리어", "유아동/유아도서", "생활/가공식품",
    "여성의류/잡화", "뷰티/미용", "남성의류/잡화", "스포츠/레저",
    "게임/취미", "도서/티켓/음반", "반려동물용품", "기타"
]


checklists = {
    "별로예요": [
        "시간약속을 안 지켜요", "채팅 메시지를 읽고도 답이 없어요.",
        "원하지 않는 가격을 계속 요구해요.", "예약만 하고 거래 시간을 명확하게 알려주지 않아요",
        "거래 시간과 장소를 정한 후 거래 직전 취소했어요.",
        "거래 시간과 장소를 정한 후 연락이 안돼요.",
        "약속 장소에 나타나지 않았어요.", "상품 상태가 설명과 달라요.",
        "반말을 사용해요.", "불친절해요."
    ],
    "좋아요": [
        "물품설명이 자세해요.", "물품상태가 설명한 것과 같아요.",
        "좋은 물품을 저렴하게 판매해요.", "나눔을 해주셨어요.",
        "안심결제를 잘 받아줘요.", "시간 약속을 잘 지켜요.",
        "친절하고 매너가 좋아요.", "응답이 빨라요."
    ],
    "최고예요": [
        "물품설명이 자세해요.", "물품상태가 설명한 것과 같아요.",
        "좋은 물품을 저렴하게 판매해요.", "나눔을 해주셨어요.",
        "안심결제를 잘 받아줘요.", "시간 약속을 잘 지켜요.",
        "친절하고 매너가 좋아요.", "응답이 빨라요."
    ]
}

selected_checkbuttons = []

current_user_id = ""
current_user_name = ""
current_user_phone = ""
current_user_address = ""  # 거주지
current_user_interests = ""  # 관심 물품

# 회원정보 저장 함수
def save_user(username, password, name, phone):
    global current_user_name, current_user_phone

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

def write_data(name, price, description, category):
    if current_user_name:  # current_user_name이 설정되어 있는지 확인
        ref = db.reference('items')  # 'items' 경로 참조
        ref.push({  # current_user_name을 저장
            'name': name,
            'price': price,
            'description': description,
            'username': current_user_name,
            'category': category  # 카테고리 추가
        })
        print(f"상품 '{name}'이(가) 등록되었습니다.")
    else:
        print("현재 로그인된 사용자가 없습니다. 상품 등록을 실패했습니다.")

# 로그인 함수
def login():
    username = entry_id.get()
    password = entry_password.get()

    ref = db.reference('users')

    if not username or not password:
        messagebox.showerror("로그인 오류", "아이디와 비밀번호를 입력하세요.")
        return



    data = ref.get()
    for key, user in data.items():  # data가 딕셔너리라면
        if user['username'] == username and user['password'] == password:
            global current_user_name, current_user_phone
            current_user_name = user['name']
            current_user_phone = user['phone']

            messagebox.showinfo("로그인 성공", f"환영합니다, {current_user_name}님!")
            root.withdraw()
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
        ("채팅", show_chat_list),
        ("구매내역", show_purchase_history),  # "탭 4"를 "구매내역"으로 변경
        ("내 정보", show_user_info)  # 내 정보 버튼
        
    ]

    for text, command in tab_buttons:
        button = tk.Button(bottom_tabs_frame, text=text, command=command, width=10, height=2)
        button.pack(side="left", padx=5)


# 채팅목록 화면 함수
def show_chat_list():
    subprocess.run(['python', 'C:/Users/USER/Desktop/project/chat_app.py', current_user_name])

# 구매내역 화면 함수
def show_purchase_history():

    ref = db.reference('purchase_history')  # 'items' 경로 참조
    data = ref.get()

    count = 0

    if data:
        for key, item in data.items():
            # 물품 이름이나 설명에 검색어가 포함된 경우 필터링
            if item.get('username') == current_user_name:
                count += 1

    if count >= 1:

        product_window = tk.Toplevel(root)
        product_window.title("상품 목록")
        product_window.geometry("600x500")  # 창 크기 조정

        # 스크롤바 추가
        canvas = tk.Canvas(product_window)
        scrollbar = tk.Scrollbar(product_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        for key, item in data.items():
            # 물품 이름이나 설명에 검색어가 포함된 경우 필터링
            if item.get('username') == current_user_name:

                product_frame = tk.Frame(frame)
                product_frame.pack(pady=10, padx=10, fill="x", anchor="w")

                # 상품 정보 레이블
                tk.Label(product_frame, text=f"상품: {item['name']}", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
                tk.Label(product_frame, text=f"가격: {item['price']}원", font=("Arial", 10)).pack(anchor="w", padx=10)
                tk.Label(product_frame, text=f"카테고리: {item['category']}", font=("Arial", 10)).pack(anchor="w", padx=10)

                review_button = tk.Button(product_frame, text="후기", command=lambda p=item: review_product(p, product_window))
                review_button.pack(pady=5, padx=10, side="left")



    else:    
        messagebox.showinfo("알림", "데이터베이스에 저장된 상품이 없습니다.")

def on_category_click(category, window, checklist_items_frame):
    global selected_checkbuttons
    for item in checklist_items_frame.winfo_children():
        item.destroy()

    tk.Label(checklist_items_frame, text=f"{category} 항목:", font=("Helvetica", 14, "bold")).pack()

    for item in checklists.get(category, []):
        var = tk.BooleanVar()
        chk = tk.Checkbutton(checklist_items_frame, text=item, variable=var)
        chk.var = var
        chk.pack(anchor="w")

        selected_checkbuttons.append((chk, var))


def display_items(category):
    # 선택된 항목 프레임 내 위젋 삭제
    for item in checklist_items_frame.winfo_children():
        item.destroy()

    tk.Label(checklist_items_frame, text=f"{category} 항목:", font=("Helvetica", 14, "bold")).pack()

    # 카테고리에 해당하는 각 항목을 체크박스로 생성
    for item in checklists.get(category, []):
        var = tk.BooleanVar()
        chk = tk.Checkbutton(checklist_items_frame, text=item, variable=var)
        chk.var = var  # 각 체크박스의 변수 참조 저장
        chk.pack(anchor="w")

        # 선택한 값을 저장
        selected_checkbuttons.append((chk, var))

def confirm_selection(product, review_window):
    global selected_checkbuttons
    selected_items = [chk.cget("text") for chk, var in selected_checkbuttons if var.get()]
    ref = db.reference('purchase_history')
    data = ref.get()

    if selected_items:
        if data:
            # 제품 데이터 확인 및 리뷰 저장
            for key, item in data.items():
                if item == product:
                    for idx, review in enumerate(selected_items):
                        ref.child(key).update({
                            f'review_{idx+1}': review
                        })

        else:
            messagebox.showinfo("리뷰 저장", "해당 제품이 데이터베이스에 존재하지 않습니다.")

    else:
        messagebox.showinfo("리뷰 선택 확인", "선택된 항목이 없습니다.")
    print(selected_items)
    selected_checkbuttons = []
    review_window.destroy()


#후기
def review_product(product, product_window):
    review_window = tk.Toplevel(product_window)  # Toplevel으로 창 생성
    review_window.title("review")
    review_window.geometry("400x500")

    category_buttons_frame = tk.Frame(review_window)
    category_buttons_frame.pack(fill=tk.X, pady=10)

    tk.Button(category_buttons_frame, text="별로예요", command=lambda: on_category_click("별로예요", review_window, checklist_items_frame)).pack(side=tk.LEFT, padx=10)
    tk.Button(category_buttons_frame, text="좋아요", command=lambda: on_category_click("좋아요", review_window, checklist_items_frame)).pack(side=tk.LEFT, padx=10)
    tk.Button(category_buttons_frame, text="최고예요", command=lambda: on_category_click("최고예요", review_window, checklist_items_frame)).pack(side=tk.LEFT, padx=10)

    # 리뷰 창 내 항목 프레임 설정
    checklist_items_frame = tk.Frame(review_window)
    checklist_items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Button(review_window, text="확인", command=lambda:confirm_selection(product, review_window)).pack(pady=10)

    # 선택된 체크박스 저장 리스트




    '''
    ref = db.reference('items')  # 'items' 경로 참조
    data = ref.get()
    print("\n데이터베이스에 저장된 아이템 목록:")

    reference_1 = db.reference('purchase_history')


    if data:
        for key, item in data.items():
            if item == product:
                if item['username'] == current_user_name:
                    messagebox.showinfo("경고", "자신이 등록한 상품입니다.")
                    break
                reference_1.push({
                    'seller':item['username'],
                    'username': current_user_name,
                    'name': item['name'],
                    'price': item['price'],
                    'description': item['description'],
                    'category': item['category']
                    })
                user_ref = ref.child(key)  # 해당 사용자의 경로 참조
                user_ref.delete()

                product_window.destroy()
                show_product_list()  # 삭제 후 상품 목록 다시 표시
    '''

 
# 구매내역 저장 함수 (구매한 상품을 기록할 때 사용)
def save_purchase_history(product_name, product_price):
    from datetime import datetime

    purchase_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 현재 날짜 및 시간
    with open("purchase_history.txt", "a") as file:
        file.write(f"{product_name},{product_price},{purchase_date}\n")

# 상품 목록을 위한 화면 (상품 판매 창)
def show_product_list():
    # 새로운 창 생성
    product_window = tk.Toplevel(root)
    product_window.title("상품 목록")
    product_window.geometry("600x500")  # 창 크기 조정

    # 스크롤바 추가
    canvas = tk.Canvas(product_window)
    scrollbar = tk.Scrollbar(product_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Firebase에서 데이터 가져오기
    ref = db.reference('items')  # 'items' 경로 참조
    data = ref.get()

    print("\n데이터베이스에 저장된 아이템 목록:")

    if data:
        for key, item in data.items():
            # 각 상품을 프레임에 표시
            product_frame = tk.Frame(frame)
            product_frame.pack(pady=10, padx=10, fill="x", anchor="w")

            # 상품 정보 레이블
            tk.Label(product_frame, text=f"상품: {item['name']}", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
            tk.Label(product_frame, text=f"가격: {item['price']}원", font=("Arial", 10)).pack(anchor="w", padx=10)
            tk.Label(product_frame, text=f"카테고리: {item['category']}", font=("Arial", 10)).pack(anchor="w", padx=10)

            # 삭제 버튼
            delete_button = tk.Button(product_frame, text="구매", command=lambda p=item: purchase_product(p, product_window))
            delete_button.pack(pady=5, padx=10, side="left")

            if item['username']:
                if item['username'] == current_user_name:
                    delete_button = tk.Button(product_frame, text="삭제", command=lambda p=item: delete_product(p, product_window))
                    delete_button.pack(pady=5, padx=10, side="left")



    else:
        print("데이터베이스에 저장된 아이템이 없습니다.")
        messagebox.showinfo("알림", "데이터베이스에 저장된 상품이 없습니다.")

    # 상품 추가 버튼
    tk.Button(product_window, text="상품 추가", command=lambda: open_add_product_window(product_window), bg="lightblue", relief="raised").pack(pady=10, padx=10)



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
            tk.Button(product_window, text="삭제", command=lambda p=product: purchase_product(p, product_window)).pack(pady=5)
    else:
        print("데이터베이스에 저장된 아이템이 없습니다.")

#==================================================




# 상품 추가 창 열기
def open_add_product_window(product_window):
    global add_product_window, entry_product_name, entry_product_price, entry_product_description, entry_product_category

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


    category_button = tk.Menubutton(add_product_window, text="카테고리", relief="raised")

    # 카테고리 메뉴 생성
    category_menu = tk.Menu(category_button, tearoff=0)

    # 카테고리 메뉴에 항목 추가
    for category in categories:
        category_menu.add_command(label=category, command=lambda cat=category: on_category_select(cat, category_button))

    # Menubutton에 메뉴 설정
    category_button["menu"] = category_menu

    # 메뉴 버튼을 윈도우에 배치
    category_button.pack(pady=10)


    # 상품 추가 버튼
    tk.Button(add_product_window, text="추가", command=lambda : add_product(product_window)).pack(pady=10)

#카테고리 선택 함수
def on_category_select(category, category_button):
    global entry_product_category
    # 메뉴에서 카테고리를 선택했을 때 호출되는 함수
    entry_product_category = category
    category_button.config(text=category)



# 상품 추가 함수
def add_product(product_window):
    product_name = entry_product_name.get()
    product_price = entry_product_price.get()
    product_description = entry_product_description.get()
    product_category = entry_product_category

    if not product_name or not product_price or not product_description:
        messagebox.showerror("상품 추가 오류", "모든 정보를 입력해주세요.")
        return

    write_data(product_name, product_price, product_description, product_category)

    messagebox.showinfo("상품 추가 성공", "상품이 추가되었습니다.")
    add_product_window.destroy()
    product_window.destroy()
    show_product_list()


def delete_product(product, product_window):
    ref = db.reference('items')  # 'items' 경로 참조
    data = ref.get()

    if data:
        for key, item in data.items():
            if item == product:
                user_ref = ref.child(key)  # 해당 사용자의 경로 참조
                user_ref.delete()
                
    product_window.destroy()
    show_product_list()  # 삭제 후 상품 목록 다시 표시

# 상품 삭제 함수
def purchase_product(product, product_window):


    ref = db.reference('items')  # 'items' 경로 참조
    data = ref.get()
    print("\n데이터베이스에 저장된 아이템 목록:")

    reference_1 = db.reference('purchase_history')


    if data:
        for key, item in data.items():
            if item == product:
                if item['username'] == current_user_name:
                    messagebox.showinfo("경고", "자신이 등록한 상품입니다.")
                    break
                reference_1.push({
                    'seller':item['username'],
                    'username': current_user_name,
                    'name': item['name'],
                    'price': item['price'],
                    'description': item['description'],
                    'category': item['category']
                    })
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

        # Firebase에서 데이터 가져오기
        ref = db.reference('items')  # 'items' 경로 참조
        data = ref.get()
        keyword = search_entry.get().strip().lower()

        count = 0

        if data:
            for key, item in data.items():
                # 물품 이름이나 설명에 검색어가 포함된 경우 필터링
                if keyword.lower() in item.get('name', '').lower() or keyword.lower() in item.get('description', '').lower():
                    count += 1

        if count >= 1:

            product_window = tk.Toplevel(root)
            product_window.title("상품 목록")
            product_window.geometry("600x500")  # 창 크기 조정

            # 스크롤바 추가
            canvas = tk.Canvas(product_window)
            scrollbar = tk.Scrollbar(product_window, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)

            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)

            frame = tk.Frame(canvas)
            canvas.create_window((0, 0), window=frame, anchor="nw")

            frame.bind(
                "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            for key, item in data.items():
                # 물품 이름이나 설명에 검색어가 포함된 경우 필터링
                if keyword.lower() in item.get('name', '').lower() or keyword.lower() in item.get('description', '').lower():

                    product_frame = tk.Frame(frame)
                    product_frame.pack(pady=10, padx=10, fill="x", anchor="w")

                    # 상품 정보 레이블
                    tk.Label(product_frame, text=f"상품: {item['name']}", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
                    tk.Label(product_frame, text=f"가격: {item['price']}원", font=("Arial", 10)).pack(anchor="w", padx=10)
                    tk.Label(product_frame, text=f"카테고리: {item['category']}", font=("Arial", 10)).pack(anchor="w", padx=10)

                    # 삭제 버튼
                    delete_button = tk.Button(product_frame, text="구매", command=lambda p=item: purchase_product(p, product_window))
                    delete_button.pack(pady=5, padx=10, side="left")

 
        else:    
            messagebox.showinfo("알림", "데이터베이스에 저장된 상품이 없습니다.")




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
       
        # Firebase에서 데이터 가져오기
        ref = db.reference('items')  # 'items' 경로 참조
        data = ref.get()
        category = selected_category.get()
        count = 0

        if data:
            for key, item in data.items():
                if item.get('category') == category:
                    
                    count += 1
        if count >= 1:

            product_window = tk.Toplevel(root)
            product_window.title("상품 목록")
            product_window.geometry("600x500")  # 창 크기 조정

            # 스크롤바 추가
            canvas = tk.Canvas(product_window)
            scrollbar = tk.Scrollbar(product_window, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)

            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)

            frame = tk.Frame(canvas)
            canvas.create_window((0, 0), window=frame, anchor="nw")

            frame.bind(
                "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            for key, item in data.items():
                if item.get('category') == category:

                    product_frame = tk.Frame(frame)
                    product_frame.pack(pady=10, padx=10, fill="x", anchor="w")

                    # 상품 정보 레이블
                    tk.Label(product_frame, text=f"상품: {item['name']}", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
                    tk.Label(product_frame, text=f"가격: {item['price']}원", font=("Arial", 10)).pack(anchor="w", padx=10)
                    tk.Label(product_frame, text=f"카테고리: {item['category']}", font=("Arial", 10)).pack(anchor="w", padx=10)

                    # 삭제 버튼
                    delete_button = tk.Button(product_frame, text="구매", command=lambda p=item: purchase_product(p, product_window))
                    delete_button.pack(pady=5, padx=10, side="left")

        else:
            messagebox.showinfo("알림", "데이터베이스에 저장된 상품이 없습니다.")

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


hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide , win32con.SW_HIDE)
# GUI 실행
root.mainloop()