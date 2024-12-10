import firebase_admin
from firebase_admin import credentials, db

# Firebase 서비스 계정 키 파일 경로
cred = credentials.Certificate("C:/Users/cic/Desktop/SWproject/serviceAccountKey.json")

# Firebase 초기화
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sw-project-7ef51-default-rtdb.firebaseio.com'  # Firebase URL
})

print("Firebase 초기화 완료")

# 데이터 쓰기 함수
def write_data(name, price, status):
    ref = db.reference('items')  # 'items' 경로 참조
    ref.push({
        'name': name,
        'price': price,
        'status': status
    })

    print(f"{name}이(가) 데이터베이스에 성공적으로 추가되었습니다.")

# 데이터 읽기 함수
def read_data():
    ref = db.reference('items')  # 'items' 경로 참조
    data = ref.get()
    print("\n데이터베이스에 저장된 아이템 목록:")
    if data:
        for key, item in data.items():
            print(f"{item['name']} - {item['price']}원 - {item['status']}")
    else:
        print("데이터베이스에 저장된 아이템이 없습니다.")

# 터미널 입력을 통해 아이템 등록하는 함수
def register_item():
    while True:
        print("\n아이템 등록")
        name = input("아이템 이름 입력 (종료하려면 'exit' 입력): ")
        if name.lower() == 'exit':
            break

        try:
            price = int(input("아이템 가격 입력: "))
            status = input("아이템 상태 입력 (판매중/판매완료): ")

            write_data(name, price, status)
        except ValueError:
            print("잘못된 입력입니다. 가격을 정확하게 입력해주세요.")

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