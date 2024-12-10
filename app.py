import firebase_admin
from firebase_admin import credentials, db

# Firebase 서비스 계정 키 파일 경로
cred = credentials.Certificate("C:/Users/0914s/Desktop/SWproject/serviceAccountKey.json")

# Firebase 초기화
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sw-project-7ef51-default-rtdb.firebaseio.com'  # Firebase URL
})

print("Firebase 초기화 완료")

# 데이터 쓰기 함수
def write_data(name, price, status, category):
    ref = db.reference('items')  # 'items' 경로 참조
    ref.push({
        'name': name,
        'price': price,
        'status': status,
        'category': category  # 카테고리 추가
    })

    print(f"{name}이(가) 데이터베이스에 성공적으로 추가되었습니다.")

# 데이터 읽기 함수
def read_data():
    ref = db.reference('items')  # 'items' 경로 참조
    data = ref.get()
    print("\n데이터베이스에 저장된 아이템 목록:")
    if data:
        for key, item in data.items():
            print(f"{item['name']} - {item['price']}원 - {item['status']} - {item['category']}")
    else:
        print("데이터베이스에 저장된 아이템이 없습니다.")

# 카테고리 목록
categories = [
    "디지털/가전", "가구/인테리어", "유아동/유아도서", "생활/가공식품",
    "여성의류/잡화", "뷰티/미용", "남성의류/잡화", "스포츠/레저",
    "게임/취미", "도서/티켓/음반", "반려동물용품", "기타", "삽니다"
]

# 상태 목록
statuses = ["판매중", "판매완료"]

# 터미널 입력을 통해 아이템 등록하는 함수
def register_item():
    while True:
        print("\n아이템 등록")
        name = input("아이템 이름 입력 (종료하려면 'exit' 입력): ")
        if name.lower() == 'exit':
            break

        try:
            # 가격 입력 검증
            price = input("아이템 가격 입력 (숫자만 입력): ")
            if not price.isdigit():
                raise ValueError("가격은 숫자만 입력해야 합니다.")
            price = int(price)

            # 상태 선택
            print("\n상태 선택:")
            for idx, status in enumerate(statuses, start=1):
                print(f"{idx}. {status}")
            status_choice = int(input("상태 번호를 입력하세요: "))
            if 1 <= status_choice <= len(statuses):
                status = statuses[status_choice - 1]
            else:
                raise ValueError("잘못된 상태 선택입니다.")

            # 카테고리 선택
            print("\n카테고리 선택:")
            for idx, category in enumerate(categories, start=1):
                print(f"{idx}. {category}")
            category_choice = int(input("카테고리 번호를 입력하세요: "))
            if 1 <= category_choice <= len(categories):
                category = categories[category_choice - 1]
            else:
                raise ValueError("잘못된 카테고리 선택입니다.")

            write_data(name, price, status, category)
        except ValueError as ve:
            print(f"입력 오류: {ve}. 다시 시도해주세요.")
        except Exception as e:
            print(f"예상치 못한 오류 발생: {e}. 다시 시도해주세요.")

# 메뉴 선택 함수
def main():
    while True:
        print("\n메뉴:")
        print("1. 아이템 등록")
        print("2. 데이터베이스 내 아이템 조회")
        print("3. 프로그램 종료")

        choice = input("\n원하는 메뉴 번호를 입력하세요: ")

        if choice == "1":
            register_item()
        elif choice == "2":
            read_data()
        elif choice == "3":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 1, 2, 3 중 하나를 선택해주세요.")

# 프로그램 실행 시작
main()
