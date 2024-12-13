from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt

# Flask 애플리케이션 생성
app = Flask(__name__)

# 데이터베이스 URI 설정 (SQLite 사용)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # 데이터베이스 파일이 프로젝트 폴더에 저장됩니다.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 변경 사항 추적을 비활성화
db = SQLAlchemy(app)

# 사용자 모델 정의 (사용자 정보 저장)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 기본키
    username = db.Column(db.String(120), unique=True, nullable=False)  # 고유한 사용자 이름
    password = db.Column(db.String(200), nullable=False)  # 암호화된 비밀번호

# 회원가입 API
@app.route('/register', methods=['POST'])
def register():
    # JSON 데이터에서 사용자 이름과 비밀번호 받기
    username = request.json.get('username')
    password = request.json.get('password')

    # 비밀번호 암호화
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # 사용자 정보 데이터베이스에 저장
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully!"}), 201

# 로그인 API
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # 사용자 조회
    user = User.query.filter_by(username=username).first()

    # 사용자 존재 여부 및 비밀번호 비교
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 400

if __name__ == '__main__':
    # 애플리케이션 컨텍스트 내에서 데이터베이스 테이블 생성
    with app.app_context():
        db.create_all()  # 데이터베이스 테이블 생성
    
    # 서버 실행
    app.run(debug=True)
