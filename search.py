import firebase_admin
from firebase_admin import credentials, db

# Firebase 서비스 계정 키 파일 경로
cred = credentials.Certificate("C:/Users/cic/Desktop/SWproject/serviceAccountKey.json")

# Firebase 초기화
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sw-project-7ef51-default-rtdb.firebaseio.com'  # Firebase URL
})

# 카테고리 리스트
categories = [
    "디지털/가전", "가구/인테리어", "유아동/유아도서", "생활/가공식품",
    "여성의류/잡화", "뷰티/미용", "남성의류/잡화", "스포츠/레저",
    "게임/취미", "도서/티켓/음반", "반려동물용품", "기타", "삽니다"
]

# Firebase 경로 참조
items_ref = db.reference('items')


def filter_items_by_category(category):
    """
    카테고리에 따라 물품을 필터링하는 함수
    :param category: 선택한 카테고리
    :return: 필터링된 물품 목록
    """
    data = items_ref.get()
    filtered_items = []

    if data:
        for key, item in data.items():
            if item.get('category') == category:
                filtered_items.append(item)

    return filtered_items


def display_category_menu():
    """카테고리 선택 메뉴 출력"""
    print("\n카테고리를 선택하세요:")
    for idx, category in enumerate(categories):
        print(f"{idx+1}. {category}")
    print(f"{len(categories) + 1}. 창닫음")


def search_items_by_category():
    """카테고리를 선택하여 필터링된 물품 출력"""
    while True:
        display_category_menu()

        try:
            category_choice = int(input("\n선택한 카테고리 번호를 입력하세요: ")) - 1

            if category_choice == len(categories):  # "창닫음" 선택
                print("프로그램을 종료합니다.")
                break
            elif 0 <= category_choice < len(categories):
                selected_category = categories[category_choice]
                filtered_items = filter_items_by_category(selected_category)

                if filtered_items:
                    print(f"\n{selected_category} 카테고리에서 검색된 물품:")
                    for item in filtered_items:
                        print(f"{item['name']} - {item['category']} - {item['price']}원 - {item['status']}")
                else:
                    print(f"\n{selected_category} 카테고리에는 검색된 물품이 없습니다.")

            else:
                print("유효하지 않은 카테고리 번호입니다. 다시 선택해주세요.")

        except ValueError:
            print("잘못된 입력입니다. 다시 선택해주세요.")


if __name__ == "__main__":
    search_items_by_category()
