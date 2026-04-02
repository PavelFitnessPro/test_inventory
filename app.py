import os
import pg8000
import time

print("Запуск системы учета...")
time.sleep(5)  # Ждем пару секунд, чтобы база успела загрузиться

host = os.environ.get("DB_HOST", "db")
user = os.environ.get("DB_USER", "admin")
password = os.environ.get("DB_PASS", "secretpassword")
database = os.environ.get("DB_NAME", "inventory_db")

try:
    print(f"Подключение к базе {database} на сервере {host}...")
    conn = pg8000.connect(host=host, user=user, password=password, database=database)
    cursor = conn.cursor()
    
    # Создаем таблицу, если ее нет
    cursor.execute("CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name VARCHAR(50), qty INT);")
    
    # Добавляем товар
    cursor.execute("INSERT INTO items (name, qty) VALUES ('Ноутбук', 10);")
    conn.commit()
    
    print("УСПЕХ: Товар успешно записан в настоящую базу PostgreSQL!")
    conn.close()
except Exception as e:
    print(f"ОШИБКА БАЗЫ ДАННЫХ: {e}")
