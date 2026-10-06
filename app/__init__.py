from flask import Flask
from flask_cors import CORS
from config import config_selector

def create_app(config_name="development"):
    app = Flask(__name__)
    
    # Ayarları config.py üzerinden yükle
    app.config.from_object(config_selector[config_name])

    # KRİTİK ÇÖZÜM: Tüm rotalar için CORS'u (Wix erişimini) serbest bırakıyoruz
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Rotaları (Blueprints) içeri aktar ve uygulamaya kaydet
    from app.routes import api_bp, main_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(main_bp)

    return app