import sqlite3
import os

DB_PATH = "database/database.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    os.makedirs("database", exist_ok=True)
    with connect_db() as db:
        cursor = db.cursor()
        # Создаем таблицы
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                order_date DATE NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)
        db.commit()

def seed_data():
    with connect_db() as db:
        cursor = db.cursor()

        # Очистим старые данные
        cursor.execute("DELETE FROM orders")
        cursor.execute("DELETE FROM customers")
        cursor.execute("DELETE FROM products")

        # Продукты
        products = [
            (1, 'Lenovo44', 'Ноутбуки', 1500),
            (2, 'AsusA15', 'Ноутбуки', 2000),
            (3, 'iphone16pro', 'Телефоны', 900),
            (4, 'samsungs24', 'Телефоны', 540),
            (5, 'ipadair2', 'Планшеты', 600),
            (6, 'ipad 6 air', 'Планшеты', 230),
        ]
        cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products)

        # Клиенты
        customers = [
            (1, 'Андрей', 'Василий', 'andre12@gmail.com'),
            (2, 'Илья', 'Анатолий', 'ilyaanatoli23@gmail.com'),
            (3, 'Лев', 'Толстой', 'levtolstov34@gmail.com'),
            (4, 'Макс', 'Сергеевич', 'maksserhi23@gmail.com'),
            (5, 'Егор', 'Генадиевич', 'egorgenadiev56@gmail.com'),
        ]
        cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?)", customers)

        db.commit()

def insert_orders():
    orders = [
        (1, 1, 1, "2024-05-01"),
        (2, 2, 2, "2024-05-03"),
        (1, 3, 1, "2024-05-04"),
        (3, 1, 3, "2024-05-05"),
        (4, 4, 1, "2024-05-06"),
        (5, 6, 2, "2024-05-07"),
        (2, 5, 1, "2024-05-08")
    ]
    with connect_db() as db:
        cursor = db.cursor()
        cursor.executemany("""
            INSERT INTO orders (customer_id, product_id, quantity, order_date)
            VALUES (?, ?, ?, ?)
        """, orders)
        print("✅ Заказы добавлены.")

def total_sales():
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT SUM(p.price * o.quantity)
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
        """)
        result = cursor.fetchone()[0]
        print(f"💰 Общий объем продаж: {result:.2f} грн")

def orders_per_customer():
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT c.first_name, c.last_name, COUNT(o.order_id)
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id
        """)
        for row in cursor.fetchall():
            print(f"{row[0]} {row[1]}: {row[2]} заказ(ов)")

def average_order_value():
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT AVG(p.price * o.quantity)
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
        """)
        result = cursor.fetchone()[0]
        print(f"📦 Средний чек: {result:.2f} грн")

def most_popular_category():
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT p.category, COUNT(*) as cnt
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            GROUP BY p.category
            ORDER BY cnt DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            print(f"🔥 Самая популярная категория: {row[0]} ({row[1]} заказов)")

def product_count_by_category():
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT category, COUNT(*) FROM products GROUP BY category
        """)
        for row in cursor.fetchall():
            print(f"{row[0]}: {row[1]} товаров")

def update_prices():
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            UPDATE products
            SET price = price * 1.10
            WHERE LOWER(category) = 'телефоны'
        """)
        print("🔧 Цены на телефоны увеличены на 10%.")

def show_products():
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM products")
        for row in cursor.fetchall():
            print(row)


def menu():
    actions = {
        "1": ("Добавить заказы", insert_orders),
        "2": ("Общий объем продаж", total_sales),
        "3": ("Количество заказов на клиента", orders_per_customer),
        "4": ("Средний чек", average_order_value),
        "5": ("Популярная категория товаров", most_popular_category),
        "6": ("Товары по категориям", product_count_by_category),
        "7": ("Увеличить цены на телефоны на 10%", update_prices),
    }

    while True:
        print("\n===== МЕНЮ =====")
        for k, (desc, _) in actions.items():
            print(f"{k}. {desc}")
        print("0. Выйти")
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            break
        elif choice in actions:
            actions[choice][1]()
        else:
            print("❌ Неверный выбор")

def ask_commit():
    choice = input("Сохранить изменения? (y/n): ").strip().lower()
    if choice == 'y':
        print("✅ Изменения сохранены.")
    else:
        with connect_db() as db:
            db.rollback()
        print("🔄 Изменения отменены.")

if __name__ == "__main__":
    init_db()
    seed_data()
    menu()
    ask_commit()
