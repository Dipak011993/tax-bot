
from flask import Flask, render_template, request
import json
import sqlite3

app = Flask(__name__)

# Load FAQ from JSON
with open('faq.json') as f:
    faq = json.load(f)

# Initialize database
def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    if request.method == "POST":
        question = request.form["question"].lower()
        found = False
        for keyword, response in faq.items():
            if keyword in question:
                answer = response
                found = True
                break
        if not found:
            answer = "Sorry, I don't know the answer yet."

        # Save to DB
        conn = sqlite3.connect('chat.db')
        c = conn.cursor()
        c.execute('INSERT INTO chat_history (question, answer) VALUES (?, ?)', (question, answer))
        conn.commit()
        conn.close()

    # Get all chat history
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('SELECT question, answer FROM chat_history ORDER BY id DESC')
    chat_history = c.fetchall()
    conn.close()

    return render_template("index.html", answer=answer, faq=faq, chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
