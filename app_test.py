"""POC-версія для домашнього тесту: товари з goods.json, без бази та 1С."""
import json
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)


@app.after_request
def no_cache(response):
    """IE6 агресивно кешує GET. Вимикаємо кеш, щоб повторний скан того ж ШК
    не показував стару сторінку з кешу браузера кіоска."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


BASE_DIR = Path(__file__).resolve().parent
GOODS_PATH = BASE_DIR / "goods.json"


def load_goods():
    """{штрихкод: {дані}}. Читаємо на кожен запит, щоб редагувати goods.json без рестарту."""
    with open(GOODS_PATH, encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def index():
    barcode = request.args.get("barcode", "").strip()
    if not barcode:
        return render_template("index.html")

    product = load_goods().get(barcode)  # None, якщо штрихкоду нема у файлі
    return render_template("product.html", product=product, barcode=barcode)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
