import os
import sqlite3

# Создаем папку "database", если её нет
os.makedirs('database', exist_ok=True)

# Подключаемся к базе данных в папке "database"
with sqlite3.connect('database/database.db') as db:
    cursor = db.cursor()

    # Таблица продуктов
    query = """
       CREATE TABLE IF NOT EXISTS products (
           product_id INTEGER PRIMARY KEY,
           name TEXT,
           category TEXT NOT NULL,
           price REAL NOT NULL
       )"""

    # Таблица покупателей
    query2 = """
       CREATE TABLE IF NOT EXISTS customers (
           customer_id INTEGER PRIMARY KEY,
           first_name TEXT NOT NULL,
           last_name TEXT NOT NULL,
           email TEXT NOT NULL UNIQUE
       )"""

    # Таблица заказов с правильной ссылкой на product_id
    query3 = """
       CREATE TABLE IF NOT EXISTS orders (
           order_id INTEGER PRIMARY KEY,
           customer_id INTEGER NOT NULL,
           product_id INTEGER NOT NULL,
           quantity INTEGER NOT NULL,
           order_date DATE NOT NULL,
           FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
           FOREIGN KEY (product_id) REFERENCES products(product_id)
       )"""

    # Выполняем запросы
    cursor.execute(query)
    cursor.execute(query2)
    cursor.execute(query3)

    # Сохраняем изменения
    db.commit()
