# create_db.py

import sqlite3

# Connect to (or create) the crisis.db database
conn = sqlite3.connect('crisis.db')
c = conn.cursor()

# Create Users table
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')

# Create Incidents table
c.execute('''
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        location TEXT,
        priority INTEGER,
        media TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Insert default users
c.execute('INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)', ('admin', 'adminpass', 'admin'))
c.execute('INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)', ('police', 'policepass', 'police'))
c.execute('INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)', ('fire', 'firepass', 'fire_brigade'))
c.execute('INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)', ('ambulance', 'ambulancepass', 'ambulance_team'))

# Commit and close
conn.commit()
conn.close()

print("✅ Database 'crisis.db' created successfully with default users!")