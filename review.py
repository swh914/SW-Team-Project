# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 22:38:48 2024

@author: 82103
"""
import re

# Simulated data for a user’s purchase history
purchase_history = [
    {"product_id": 1, "product_name": "Vintage Table", "review_status": "후기 작성하기", "review": None},
    {"product_id": 2, "product_name": "Used Bicycle", "review_status": "후기 작성하기", "review": None},
]

# Checklists for each 거래 선호도
checklists = {
    "별로예요": [
        "시간약속을 안 지켜요",
        "채팅 메시지를 읽고도 답이 없어요.",
        "원하지 않는 가격을 계속 요구해요.",
        "예약만 하고 거래 시간을 명확하게 알려주지 않아요",
        "거래 시간과 장소를 정한 후 거래 직전 취소했어요.",
        "거래 시간과 장소를 정한 후 연락이 안돼요.",
        "약속 장소에 나타나지 않았어요.",
        "상품 상태가 설명과 달라요.",
        "반말을 사용해요.",
        "불친절해요."
    ],
    "좋아요": [
        "물품설명이 자세해요.",
        "물품상태가 설명한 것과 같아요.",
        "좋은 물품을 저렴하게 판매해요.",
        "나눔을 해주셨어요.",
        "안심결제를 잘 받아줘요.",
        "시간 약속을 잘 지켜요.",
        "친절하고 매너가 좋아요.",
        "응답이 빨라요."
    ],
    "최고예요": [
        "물품설명이 자세해요.",
        "물품상태가 설명한 것과 같아요.",
        "좋은 물품을 저렴하게 판매해요.",
        "나눔을 해주셨어요.",
        "안심결제를 잘 받아줘요.",
        "시간 약속을 잘 지켜요.",
        "친절하고 매너가 좋아요.",
        "응답이 빨라요."
    ]
}

# Function to display purchase history
def display_purchase_history():
    print("\n구매 내역:")
    for item in purchase_history:
        print(f"- {item['product_name']} ({item['review_status']})")

# Function to find a product by ID or name
def find_product(identifier):
    for product in purchase_history:
        if str(product["product_id"]) == identifier or product["product_name"].lower() == identifier.lower():
            return product
    return None

# Function to write a review
def write_review(product):
    # Check if a review already exists
    if product["review"] is not None:
        print(f"\n'{product['product_name']}'에 대한 보낸 후기 보기:")
        print("-" * 50)
        
        # Print the review text (if it exists)
        print(f"{product['review']['text']}")
        
        # Print checklist items with each item on a new line (only if review exists)
        for checklist in product["review"]["checklists"]:
            print(f"- {checklist}")
        
        print("-" * 50)
        return

    print(f"\n'{product['product_name']}'에 대한 리뷰 작성:")

    # Select 거래 선호도
    print("거래 선호도를 선택하세요:")
    for i, option in enumerate(checklists.keys(), 1):
        print(f"{i}. {option}")
    preference_choice = int(input("선택: ")) - 1
    preference = list(checklists.keys())[preference_choice]

    # Display corresponding checklists
    print(f"\n{preference} - 해당되는 항목을 선택하세요 (쉼표로 구분하여 입력):")
    for i, checklist in enumerate(checklists[preference], 1):
        print(f"{i}. {checklist}")
    
    checklist_choices = input("선택 (예: 1,3): ").strip()
    
    # Remove any trailing commas, dots or spaces, and split choices correctly
    checklist_choices = checklist_choices.rstrip(",.").strip()
    
    # Extract only the numbers (ignoring any non-numeric characters)
    checklist_choices = re.findall(r'\d+', checklist_choices)

    # Filter out any invalid characters and convert the valid choices into checklist items
    selected_checklists = []
    for i in checklist_choices:
        i = int(i)  # convert string to integer
        if i <= len(checklists[preference]) and i > 0:
            selected_checklists.append(checklists[preference][i - 1])
    
    # Ask if the user wants to write a textual review
    print("\n리뷰 내용을 입력하시겠습니까?")
    write_review_choice = input("리뷰를 작성하시려면 'y', 건너뛰려면 'n'을 입력하세요: ").strip().lower()

    if write_review_choice == "y":
        if preference == "별로예요":
            text_prompt = "아쉬웠던 점을 당근 팀에 알려주세요:"
        else:
            text_prompt = "따뜻한 거래 경험을 알려주세요!"
        text_review = input(f"{text_prompt} ")
    else:
        text_review = "작성하지 않음"

    # Save the review and update status
    product["review"] = {
        "preference": preference,
        "checklists": selected_checklists,
        "text": text_review
    }
    product["review_status"] = "보낸 후기 보기"
    print("\n리뷰가 성공적으로 작성되었습니다!")

# Main menu
def main():
    while True:
        display_purchase_history()
        choice = input("\n원하는 작업을 선택하세요 (상품 이름/ID 입력, 종료: q): ")
        if choice.lower() == "q":
            print("프로그램을 종료합니다.")
            break

        product = find_product(choice)
        if product:
            write_review(product)
        else:
            print("해당 상품을 찾을 수 없습니다.")

if __name__ == "__main__":
    main()

