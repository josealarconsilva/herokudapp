from flask import Flask, request, render_template_string
from database import init_db
from fetch_data import fetch_and_store_data
import sqlite3

app = Flask(__name__)

# Initialize the database
init_db()

@app.route("/")
def main():
    return '''
    <form action="/fetch_and_store" method="POST">
        <input type="submit" value="Fetch and Store Data">
    </form>
    <br>
    <a href="/view_data">View Stored Data</a>
    '''

@app.route("/fetch_and_store", methods=["POST"])
def fetch_and_store():
    fetch_and_store_data()
    return '''
    Data fetched and stored in the database!
    <br>
    <a href="/view_data">View Stored Data</a>
    '''

@app.route("/view_data")
def view_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, body FROM posts')
    posts = cursor.fetchall()
    conn.close()

    # Simple HTML template to display data
    html = '''
    <h1>Stored Posts</h1>
    <ul>
        {% for post in posts %}
            <li><strong>{{ post[1] }}</strong>: {{ post[2] }}</li>
        {% endfor %}
    </ul>
    <br>
    <a href="/">Go Back</a>
    '''
    return render_template_string(html, posts=posts)

if __name__ == "__main__":
    app.run(debug=True)
