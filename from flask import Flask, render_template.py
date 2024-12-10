from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "secret_key"  # 플래시 메시지에 사용
DATA_FILE = "products.txt"

# 상품 데이터 파일 생성
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as file:
        pass  # 빈 파일 생성

# 상품 리스트 불러오기
def load_products():
    products = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            for line in file:
                product_id, name, price, description = line.strip().split("|")
                products.append({
                    "id": product_id,
                    "name": name,
                    "price": price,
                    "description": description
                })
    return products

# 상품 저장하기
def save_products(products):
    with open(DATA_FILE, "w") as file:
        for product in products:
            file.write(f"{product['id']}|{product['name']}|{product['price']}|{product['description']}\n")

# 홈 페이지 (상품 목록)
@app.route("/")
def index():
    products = load_products()
    return render_template("index.html", products=products)

# 상품 등록
@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]

        if not name or not price:
            flash("상품명과 가격은 필수 입력 항목입니다.", "danger")
            return redirect(url_for("add_product"))

        products = load_products()
        new_id = str(len(products) + 1)
        products.append({
            "id": new_id,
            "name": name,
            "price": price,
            "description": description
        })
        save_products(products)
        flash("상품이 성공적으로 등록되었습니다.", "success")
        return redirect(url_for("index"))

    return render_template("add.html")

# 상품 수정
@app.route("/edit/<product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    products = load_products()
    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        flash("상품을 찾을 수 없습니다.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        product["name"] = request.form["name"]
        product["price"] = request.form["price"]
        product["description"] = request.form["description"]
        save_products(products)
        flash("상품이 성공적으로 수정되었습니다.", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", product=product)

# 상품 삭제
@app.route("/delete/<product_id>", methods=["POST"])
def delete_product(product_id):
    products = load_products()
    products = [p for p in products if p["id"] != product_id]
    save_products(products)
    flash("상품이 성공적으로 삭제되었습니다.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
