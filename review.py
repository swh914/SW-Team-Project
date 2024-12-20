<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 22:38:48 2024

@author: 82103
"""
import sqlite3
import os

# SQLite DB 초기화
def initialize_db():
    conn = sqlite3.connect("carrot_trade.db")
    cur = conn.cursor()
    # 구매 내역 테이블 생성
    cur.execute("""
        CREATE TABLE IF NOT EXISTS purchase_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            review_status TEXT DEFAULT '후기 작성하기',
            preference TEXT,
            checklist TEXT,
            review TEXT
        )
    """)
    conn.commit()
    conn.close()

# 구매 내역 출력
def display_purchase_history():
    conn = sqlite3.connect("carrot_trade.db")
    cur = conn.cursor()
    cur.execute("SELECT id, product_name, review_status FROM purchase_history")
    rows = cur.fetchall()
    conn.close()

    print("\n구매 내역:")
    for row in rows:
        print(f"{row[0]}. {row[1]} ({row[2]})")

# 구매 내역에서 상품 찾기
def find_product(product_id):
    conn = sqlite3.connect("carrot_trade.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM purchase_history WHERE id = ?", (product_id,))
    product = cur.fetchone()
    conn.close()
    return product

# 후기 작성
def write_review(product):
    # 리뷰 이미 작성 여부 확인
    if product[3] is not None:
        print(f"\n'{product[1]}'에 대한 보낸 후기 보기:")
        print("-" * 50)
        if product[5]:
            print(product[5])  # 리뷰 텍스트 출력
        if product[4]:
            checklists = product[4].split(", ")
            for item in checklists:
                print(f"- {item}")
        print("-" * 50)
        return

    print(f"\n'{product[1]}'에 대한 리뷰 작성:")

    # 거래 선호도 선택
    preferences = ["별로예요", "좋아요", "최고예요"]
    for i, pref in enumerate(preferences, 1):
        print(f"{i}. {pref}")

    while True:
        try:
            pref_choice = int(input("거래 선호도를 선택하세요: ")) - 1
            if 0 <= pref_choice < len(preferences):
                preference = preferences[pref_choice]
                break
            else:
                print("\n유효하지 않은 선택입니다. 다시 선택해주세요.")
        except ValueError:
            print("숫자만 입력해주세요.")

    # 체크리스트 선택
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

    print(f"\n{preference} - 해당되는 항목을 선택하세요 (쉼표로 구분하여 입력):")
    for i, checklist in enumerate(checklists[preference], 1):
        print(f"{i}. {checklist}")
    checklist_choices = input("선택 (예: 1,3): ").strip()

    # 입력값 처리 (잘못된 입력은 무시하고 유효한 것만 선택)
    selected_checklists = []
    for i in checklist_choices.replace(".", ",").split(","):
        try:
            choice = int(i.strip()) - 1
            if 0 <= choice < len(checklists[preference]):
                selected_checklists.append(checklists[preference][choice])
        except ValueError:
            pass  # 잘못된 입력은 무시

    # 리뷰 내용 입력
    review_text = input("리뷰 내용을 입력해주세요 (건너뛰려면 엔터): ").strip()

    # 데이터 저장
    conn = sqlite3.connect("carrot_trade.db")
    cur = conn.cursor()
    cur.execute("""
        UPDATE purchase_history
        SET review_status = '보낸 후기 보기',
            preference = ?,
            checklist = ?,
            review = ?
        WHERE id = ?
    """, (preference, ", ".join(selected_checklists), review_text, product[0]))
    conn.commit()
    conn.close()

    print("\n리뷰가 성공적으로 작성되었습니다!")

# 데이터 삽입 (예제용)
def seed_data():
    conn = sqlite3.connect("carrot_trade.db")
    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO purchase_history (product_name)
        VALUES (?)
    """, [("Vintage Table",), ("Used Bicycle",)])
    conn.commit()
    conn.close()

# 프로그램 메인 루프
def main():
    if not os.path.exists("carrot_trade.db"):
        initialize_db()
        seed_data()

    while True:
        display_purchase_history()
        choice = input("\n작업을 선택하세요 (상품 ID 입력, 종료: q): ").strip()
        if choice.lower() == "q":
            print("프로그램을 종료합니다.")
            break

        if choice.isdigit():
            product = find_product(int(choice))
            if product:
                write_review(product)
            else:
                print("해당 상품을 찾을 수 없습니다.")
        else:
            print("유효한 상품 ID를 입력해주세요.")

if __name__ == "__main__":
    main()
=======
import os
import firebase_admin
from firebase_admin import credentials, db

# Firebase 초기화
def initialize_firebase():
    if not firebase_admin._apps:
 cred = credentials.Certificate("C:/Users/USER/Desktop/SWproject/serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://sw-project-7ef51-default-rtdb.firebaseio.com'

        })

# items 목록 출력
def display_items():
    ref = db.reference('items')
    items = ref.get() or {}

    print("\n물품 목록:")
    for index, (key, value) in enumerate(items.items(), start=1):
        print(f"{index}. {value['product_name']} ({value.get('review_status', '후기 작성하기')})")

    return list(items.items())

# items에서 물품 데이터 가져오기
def find_item(items, choice):
    if 0 <= choice < len(items):
        return items[choice]
    return None

# 후기 작성
def write_review(item_key, item_data):
    if item_data.get('preference'):
        print(f"\n'{item_data['product_name']}'에 대한 보낸 후기 보기:")
        print("-" * 50)
        if item_data.get('review'):
            print(item_data['review'])  # 리뷰 텍스트 출력
        if item_data.get('checklist'):
            checklists = item_data['checklist'].split(", ")
            for checklist in checklists:
                print(f"- {checklist}")
        print("-" * 50)
        return

    print(f"\n'{item_data['product_name']}'에 대한 리뷰 작성:")

    # 거래 선호도 선택
    preferences = ["별로예요", "좋아요", "최고예요"]
    for i, pref in enumerate(preferences, 1):
        print(f"{i}. {pref}")

    while True:
        try:
            pref_choice = int(input("거래 선호도를 선택하세요: ")) - 1
            if 0 <= pref_choice < len(preferences):
                preference = preferences[pref_choice]
                break
            else:
                print("\n유효하지 않은 선택입니다. 다시 선택해주세요.")
        except ValueError:
            print("숫자만 입력해주세요.")

    # 체크리스트 선택
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

    print(f"\n{preference} - 해당되는 항목을 선택하세요 (쉼표로 구분하여 입력):")
    for i, checklist in enumerate(checklists[preference], 1):
        print(f"{i}. {checklist}")
    checklist_choices = input("선택 (예: 1,3): ").strip()

    selected_checklists = []
    for i in checklist_choices.replace(".", ",").split(","):
        try:
            choice = int(i.strip()) - 1
            if 0 <= choice < len(checklists[preference]):
                selected_checklists.append(checklists[preference][choice])
        except ValueError:
            pass  # 잘못된 입력은 무시

    review_text = input("리뷰 내용을 입력해주세요 (건너뛰려면 엔터): ").strip()

    # 데이터 저장
    ref = db.reference(f'items/{item_key}')
    ref.update({
        'review_status': '보낸 후기 보기',
        'preference': preference,
        'checklist': ", ".join(selected_checklists),
        'review': review_text
    })

    print("\n리뷰가 성공적으로 작성되었습니다!")

# 프로그램 메인 루프
def main():
    initialize_firebase()

    while True:
        items = display_items()
        choice = input("\n작업을 선택하세요 (상품 번호 입력, 종료: q): ").strip()

        if choice.lower() == "q":
            print("프로그램을 종료합니다.")
            break

        if choice.isdigit():
            choice = int(choice) - 1
            selected_item = find_item(items, choice)
            if selected_item:
                item_key, item_data = selected_item
                write_review(item_key, item_data)
            else:
                print("유효하지 않은 번호입니다. 다시 시도해주세요.")
        else:
            print("유효한 번호를 입력해주세요.")

if __name__ == "__main__":
    main()
>>>>>>> feature/network&search1
