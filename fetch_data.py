import requests
import sqlite3

def fetch_and_store_data():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    posts = response.json()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    for post in posts:
        cursor.execute('SELECT id FROM posts WHERE id = ?', (post['id'],))
        if cursor.fetchone() is None:
            cursor.execute('''
                INSERT INTO posts (id, title, body)
                VALUES (?, ?, ?)
            ''', (post['id'], post['title'], post['body']))

    conn.commit()
    conn.close()
