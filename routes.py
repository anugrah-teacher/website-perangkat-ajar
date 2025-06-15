from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'rahasia_super_aman_2025'  # Ganti kalau mau lebih aman

# Folder untuk menyimpan file upload
UPLOAD_FOLDER = os.path.join('files', 'sma')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Buat folder jika belum ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Halaman utama
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

# Halaman daftar produk perangkat ajar SMA
@app.route('/produk/sma')
def produk_sma():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    folder_path = app.config['UPLOAD_FOLDER']
    files = os.listdir(folder_path) if os.path.exists(folder_path) else []
    return render_template('produk.html', files=files)

# Proses upload file
@app.route('/upload', methods=['POST'])
def upload_file():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
    return redirect(url_for('produk_sma'))

# Download file
@app.route('/download/<path:filename>')
def download_file(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return 'Login gagal. Username atau password salah.'
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Jalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
