import json
import os
from flask import Flask, render_template, request, redirect, url_for
from pymysql import connect, OperationalError
from pythonProject1.database.select import select_dict
from pythonProject1.database.sql_provider import SQLProvider


app = Flask(__name__)

with open("db_connect.json") as file:
    db_connect = json.load(file)
    app.config['db_config'] = db_connect
    print(app.config)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@app.route('/')
def hello():
    return render_template('main.html')

'''@app.route('/static')
def static_index():
    try:
        # первый объект необходимый для подключения
        conn = connect(host='127.0.0.1', user='root', password='public', database='supermarket')
        # второй объект необходимый для подключения
        cursor = conn.cursor()
    except OperationalError as err:
        print(err.args)
        return 'ошибка подключения'
    _sql = f"""select cat_name from categories"""
    cursor.execute(_sql)
    categories = cursor.fetchall()
    return render_template('main.html', categories=categories)'''

# Главная страница выбора поиска
@app.route('/search_options')
def search_options():
    return render_template('/search/search.html')  # Страница с выбором типа поиска

@app.route('/search_price')
def search_price():
    return render_template('/search/search_price_form.html')  # Возвращаем форму для поиска


@app.route('/dynamic', methods=['GET'])
def dynamic():
    # Проверяем, какой тип запроса был сделан
    prod_category = request.args.get('prod_category')
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)

    if prod_category:
        # Поиск по категории
        _sql = provider.get("product.sql", prod_category=f"'{prod_category}'")
        result = select_dict(app.config['db_config'], _sql)
        search_type = 'category'
        prod_title = f"Результат для категории {prod_category}"

    elif min_price is not None and max_price is not None:
        # Поиск по диапазону цен
        _sql = provider.get("price.sql", min_price=min_price, max_price=max_price)
        result = select_dict(app.config['db_config'], _sql)
        search_type = 'price'
        prod_title = f"Товары в диапазоне от {min_price} до {max_price} руб."

    else:
        return render_template('/error/request_not_found.html')

    if result:
        return render_template("dynamic.html", prod_title=prod_title, products=result, search_type=search_type)
    else:
        return render_template('/error/request_not_found.html')



@app.route('/search_category', methods=['GET', 'POST'])
def search_category():
    if request.method == 'POST':
        prod_category = request.form.get('prod_category')  # Получаем категорию из формы
        return redirect(url_for('dynamic', prod_category=prod_category))  # Перенаправляем на страницу с результатами
    return render_template('/search/search_form.html')  # Возвращаем форму для поиска


app.run(host="127.0.0.1", port=5001)
