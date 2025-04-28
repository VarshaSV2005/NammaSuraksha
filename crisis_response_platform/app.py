from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_socketio import SocketIO, emit
import os
from werkzeug.utils import secure_filename
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'wav'}

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app)

# Utility to connect database
def get_db():
    conn = sqlite3.connect('crisis.db')
    conn.row_factory = sqlite3.Row
    return conn

# Check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (user, pwd))
        user_data = c.fetchone()
        conn.close()
        if user_data:
            session['user'] = user_data['username']
            session['role'] = user_data['role']
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    incidents = conn.execute('SELECT * FROM incidents ORDER BY priority ASC').fetchall()
    conn.close()
    return render_template('dashboard.html', incidents=incidents)

@app.route('/report', methods=['GET', 'POST'])
def report():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        loc = request.form['location']
        priority = request.form['priority']
        media = request.files['media']

        filename = None
        if media and allowed_file(media.filename):
            filename = secure_filename(media.filename)
            media.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = get_db()
        conn.execute('INSERT INTO incidents (title, description, location, priority, media, created_at) VALUES (?, ?, ?, ?, ?, ?)',
                     (title, desc, loc, priority, filename, datetime.now()))
        conn.commit()
        conn.close()

        socketio.emit('new_incident', {'message': f"New incident reported: {title}"}, broadcast=True)
        return redirect(url_for('dashboard'))
    return render_template('report.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# SocketIO Events
@socketio.on('message')
def handle_message(data):
    emit('message', data, broadcast=True)

@socketio.on('location_update')
def handle_location(data):
    emit('location_update', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
