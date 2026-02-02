from flask import Flask, render_template, request
import sqlite3
import os

DB_PATH = 'clicks.db'
def init_db():
    if not os.path.exists(DB_PATH):
        db = sqlite3.connect(DB_PATH)

        # Only ONE row, NO id
        db.execute('''
            CREATE TABLE IF NOT EXISTS global_clicks (
                count INTEGER NOT NULL
            )
        ''')

        # Get ALL rows (0 or 1 expected)
        rows = db.execute('SELECT * FROM global_clicks')
        rows = rows.fetchall()
        
        # Count in Python - super clear!
        if len(rows) == 0:
            db.execute('INSERT INTO global_clicks (count) VALUES (0)')
            db.commit()
        
        db.close()
        print('Database ready.')

init_db()

app = Flask(__name__)

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
    app.run()
