from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('project.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['POST'])
def add():
    content = request.form.get('content')
    if content:
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/api/add_idea', methods=['POST'])
def api_add_idea():
    # Target this endpoint with your iPhone Shortcut via your ngrok/Cloudflare tunnel
    data = request.get_json()
    content = data.get('content')
    facebook = data.get('facebook', 0)
    instagram = data.get('instagram', 0)
    tiktok = data.get('tiktok', 0)
    youtube = data.get('youtube', 0)
    linkedin = data.get('linkedin', 0)

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO posts (content, facebook, instagram, tiktok, youtube, linkedin, channel)
        VALUES (?, ?, ?, ?, ?, ?, 'iPhone API')
    ''', (content, facebook, instagram, tiktok, youtube, linkedin))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 201

@app.route('/update_platform', methods=['POST'])
def update_platform():
    data = request.get_json()
    post_id = data['id']
    platform = data['platform']
    value = 1 if data['value'] else 0

    valid_platforms = ['facebook', 'instagram', 'tiktok', 'youtube', 'linkedin']
    if platform in valid_platforms:
        conn = get_db_connection()
        conn.execute(f'UPDATE posts SET {platform} = ? WHERE id = ?', (value, post_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.get_json()
    post_id = data['id']
    status = data['status']

    valid_statuses = ['Idea', 'Planned', 'Posted']
    if status in valid_statuses:
        conn = get_db_connection()
        conn.execute('UPDATE posts SET status = ? WHERE id = ?', (status, post_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
