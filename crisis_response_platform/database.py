import sqlite3

def init_db():
    conn = sqlite3.connect('crisis.db')
    c = conn.cursor()
    
    # Users (Admin, Dispatcher, Responder)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # Incidents
    c.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            location TEXT,
            priority INTEGER,
            status TEXT,
            assigned_unit TEXT,
            media_path TEXT
        )
    ''')
    
    # Vehicles
    c.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            location TEXT,
            status TEXT
        )
    ''')
    
    # Notifications
    c.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
