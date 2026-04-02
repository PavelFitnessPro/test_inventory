import os
import pg8000
import time

host = os.environ.get("DB_HOST", "db")
user = os.environ.get("DB_USER", "admin")
password = os.environ.get("DB_PASS", "secretpassword")
database = os.environ.get("DB_NAME", "inventory_db")

def get_connection():
    return pg8000.connect(host=host, user=user, password=password, database=database)

def init_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name VARCHAR(50), qty INT);")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Ошибка инициализации базы: {e}")

def show_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items;")
    rows = cursor.fetchall()
    print("\n📦 --- СКЛАД ---")
    if not rows:
        print("Склад пуст.")
    else:
        for row in rows:
            print(f"ID: {row[0]} | Товар: {row[1]} | Остаток: {row[2]} шт.")
    print("-----------------\n")
    conn.close()

def add_item():
    name = input("Введите название товара: ")
    qty = input("Введите количество: ")
    conn = get_connection()
    cursor = conn.cursor()
    # Безопасная вставка данных
    cursor.execute("INSERT INTO items (name, qty) VALUES (%s, %s);", (name, int(qty)))
    conn.commit()
    print("✅ Товар успешно добавлен!")
    conn.close()

if __name__ == "__main__":
    print("⏳ Ожидание запуска базы данных...")
    time.sleep(3) # Ждем, чтобы PostgreSQL точно успел включиться
    init_db()
    
    while True:
        print("1. Посмотреть склад")
        print("2. Добавить товар")
        print("3. Выход")
        choice = input("Выберите действие (1-3): ")
        
        if choice == '1':
            show_items()
        elif choice == '2':
            add_item()
        elif choice == '3':
            print("Выход из системы. До свидания!")
            break
        else:
            print("❌ Ошибка: Неверный ввод.")
