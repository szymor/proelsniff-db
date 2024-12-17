from flask import Flask, render_template
from datetime import datetime
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('sniffer_data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM sniffer_data').fetchall()
    conn.close()
    # Convert sniffer_id to hexadecimal and format timestamp
    formatted_data = [
        {
            'sniffer_id': hex(row['sniffer_id']),
            'flat': row['flat'],
            'timestamp': datetime.fromisoformat(row['timestamp']).strftime('%B %d, %Y %H:%M:%S')
        }
        for row in data
    ]
    return render_template('index.html', data=formatted_data)

if __name__ == '__main__':
    app.run(debug=True)
