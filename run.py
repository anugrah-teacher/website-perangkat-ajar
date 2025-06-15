from routes import app

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes import main
    app.register_blueprint(main)

    app.config['UPLOAD_FOLDER'] = 'uploads'  # lokasi penyimpanan file

    return app


