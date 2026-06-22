"""Точка входу: Flask-роути для кіоска."""
from flask import Flask, render_template, request

from db import get_by_barcode, init_db

app = Flask(__name__)


@app.route("/")
def index():
    """Головна сторінка.

    Сканер працює як клавіатура: «друкує» штрихкод у поле і тисне Enter.
    Форма відправляється методом GET, тож штрихкод прилітає в ?barcode=...

    - немає barcode у запиті  -> показуємо порожнє поле вводу (index.html)
    - є barcode               -> шукаємо товар і показуємо результат (product.html)
    """
    barcode = request.args.get("barcode", "").strip()
    if not barcode:
        return render_template("index.html")

    product = get_by_barcode(barcode)
    return render_template("product.html", product=product, barcode=barcode)


if __name__ == "__main__":
    init_db()  # переконатися, що таблиця існує перед стартом
    # host=0.0.0.0 -> доступно з інших пристроїв у мережі (телефон, кіоск), не лише localhost.
    # use_reloader=False -> щоб пізніше планувальник синхри не запускався двічі.
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
