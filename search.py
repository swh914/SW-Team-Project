import firebase_admin
from firebase_admin import credentials, db

# Firebase 서비스 계정 키 파일 경로
cred = credentials.Certificate("C:/Users/0914s/Desktop/SWproject/serviceAccountKey.json")

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


def filter_items_by_keyword(keyword):
    """
    검색어에 따라 물품을 필터링하는 함수
    :param keyword: 사용자가 입력한 검색어
    :return: 필터링된 물품 목록
    """
    data = items_ref.get()
    filtered_items = []

    if data:
        for key, item in data.items():
            # 물품 이름이나 설명에 검색어가 포함된 경우 필터링
            if keyword.lower() in item.get('name', '').lower() or keyword.lower() in item.get('description', '').lower():
                filtered_items.append(item)

    return filtered_items


def display_category_menu():
    """카테고리 선택 메뉴 출력"""
    print("\n1. 직접 검색어 입력")
    print("2. 카테고리로 검색")
    print("3. 창닫음")


def search_items():
    """카테고리 또는 검색어로 물품 필터링"""
    while True:
        display_category_menu()

        try:
            choice = int(input("\n원하는 검색 방법을 선택하세요: "))

            if choice == 1:
                # 검색어로 검색
                keyword = input("\n검색할 키워드를 입력하세요: ").strip()
                if keyword:
                    filtered_items = filter_items_by_keyword(keyword)

                    if filtered_items:
                        print(f"\n'{keyword}' 검색어로 검색된 물품:")
                        for item in filtered_items:
                            print(f"{item['name']} - {item['category']} - {item['price']}원 - {item['status']}")
                    else:
                        print(f"\n'{keyword}' 검색어에 해당하는 물품이 없습니다.")
                else:
                    print("검색어를 입력해주세요.")

            elif choice == 2:
                # 카테고리로 검색
                print("\n카테고리를 선택하세요:")
                for idx, category in enumerate(categories):
                    print(f"{idx + 1}. {category}")
                print(f"{len(categories) + 1}. 뒤로가기")

                category_choice = int(input("\n선택한 카테고리 번호를 입력하세요: ")) - 1

                if category_choice == len(categories):  # "뒤로가기" 선택
                    continue
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

            elif choice == 3:
                # 프로그램 종료
                print("프로그램을 종료합니다.")
                break

            else:
                print("유효하지 않은 선택입니다. 다시 시도해주세요.")

        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력해주세요.")


if __name__ == "__main__":
    search_items()
