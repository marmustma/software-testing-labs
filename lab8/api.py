"""Учебное REST API для нагрузочного тестирования (ЛР8): каталог товаров."""
from flask import Flask, abort, jsonify, request

app = Flask(__name__)

PRODUCTS = [
    {"id": i, "name": f"Товар №{i}", "price": round(99.9 + i * 10.5, 2), "in_stock": i % 3 != 0}
    for i in range(1, 101)
]


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/api/products")
def products():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    start = (page - 1) * size
    return jsonify(page=page, size=size, total=len(PRODUCTS), items=PRODUCTS[start:start + size])


@app.get("/api/products/<int:pid>")
def product(pid):
    if not 1 <= pid <= len(PRODUCTS):
        abort(404)
    return jsonify(PRODUCTS[pid - 1])


if __name__ == "__main__":
    from waitress import serve
    print("API запущено: http://127.0.0.1:8000")
    serve(app, host="127.0.0.1", port=8000, threads=16)
