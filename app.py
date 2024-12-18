from flask import Flask, render_template, request
from datetime import datetime
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('accesslog.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    # Get filter criteria from query parameters
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    flat = request.args.get('flat')
    sniffer_id = request.args.get('sniffer_id')

    # Build the SQL query with optional filters
    query = 'SELECT * FROM sniffer_data WHERE 1=1'
    params = {}

    if start_time:
        query += ' AND timestamp >= :start_time'
        params['start_time'] = start_time
    if end_time:
        query += ' AND timestamp <= :end_time'
        params['end_time'] = end_time
    if flat:
        query += ' AND flat = :flat'
        params['flat'] = flat
    if sniffer_id:
        query += ' AND sniffer_id = :sniffer_id'
        if sniffer_id.startswith('0x'):
            # Interpret as hexadecimal if prefixed with '0x'
            params['sniffer_id'] = int(sniffer_id, 16)
        else:
            # Otherwise, interpret as decimal
            params['sniffer_id'] = int(sniffer_id)

    conn = get_db_connection()
    data = conn.execute(query, params).fetchall()
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
