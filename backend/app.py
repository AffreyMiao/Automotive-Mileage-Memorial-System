from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = 'database.db'

# 初始化数据库
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            buy_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            mileage INTEGER NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    model = request.form['model']
    buy_date = request.form['buyDate']
    end_date = request.form['endDate']
    mileage = request.form['mileage']
    notes = request.form.get('notes', '')
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO records (model, buy_date, end_date, mileage, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (model, buy_date, end_date, mileage, notes, created_at))
    conn.commit()
    conn.close()
    return redirect(url_for('records'))

@app.route('/records')
def records():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM records ORDER BY created_at DESC')
    records = c.fetchall()
    conn.close()
    return render_template('records.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)

