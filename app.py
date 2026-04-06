import os
import pg8000
import time
from flask import Flask

app = Flask(__name__)

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
        print(f"Ошибка БД: {e}")

# Этот декоратор говорит: когда кто-то заходит на главную страницу (/), выполни эту функцию
@app.route('/')
def show_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items;")
    rows = cursor.fetchall()
    conn.close()
    
    html = "<h1>🚀 Мой Супер Склад 2.0</h1><ul>"
    if not rows:
        html += "<li>Склад пуст</li>"
    else:
        for row in rows:
            html += f"<li>ID: {row[0]} | Товар: {row[1]} | Остаток: {row[2]} шт.</li>"
    html += "</ul>"
    return html

if __name__ == "__main__":
    time.sleep(3) # Ждем загрузку БД
    init_db()
    # Запускаем веб-сервер Flask на порту 5000
    app.run(host='0.0.0.0', port=5000)
