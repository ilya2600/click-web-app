from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'clicks.db'

def get_count():
    db = sqlite3.connect(DB_PATH)
    row = db.execute('SELECT count FROM global_clicks').fetchone()
    db.close()
    return row[0]


def increment_count():
    db = sqlite3.connect(DB_PATH)
    db.execute('UPDATE global_clicks SET count = count + 1')
    db.commit()
    row = db.execute('SELECT count FROM global_clicks').fetchone()
    db.close()
    return row[0]


def init_db():
    if not os.path.exists(DB_PATH):
        db = sqlite3.connect(DB_PATH)

        # Only ONE row, NO id
        db.execute('''
            CREATE TABLE global_clicks (
                count INTEGER NOT NULL
            )
        ''')

        db.execute('INSERT INTO global_clicks (count) VALUES (0)')
        db.commit()
        db.close()

        print('Database created and initialized.')


# ----------------------
# Routes
# ----------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        increment_count()
    count = get_count()
    return render_template("clickpost.html", count=count)



# ----------------------
# Main
# ----------------------

if __name__ == '__main__':
    init_db()
    app.run()
