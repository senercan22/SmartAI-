"""
config.py — Merkezi Yapılandırma Yönetimi
==========================================
Tüm ortam değişkenleri ve sabit ayarlar BURADAN okunur.
Hiçbir kod dosyası doğrudan os.environ okumaz; hepsi bu sınıfı kullanır.
"""

import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()


class Config:
    """Temel yapılandırma sınıfı — tüm ortamlar bu sınıftan türer."""

    # ── Güvenlik ────────────────────────────────────────────────────────────
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")

    # ── Veritabanı ──────────────────────────────────────────────────────────
    SQLITE_DB_PATH = os.environ.get("SQLITE_DB_PATH", "smartlead.db")

    # ── Yapay Zekâ API ──────────────────────────────────────────────────────
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

    # Hangi AI sağlayıcı kullanılacak
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")

    # ── İşletme Kimliği (System Prompt'un temeli) ───────────────────────────
    BUSINESS_NAME = os.environ.get("BUSINESS_NAME", "ADSC")
    BUSINESS_CONTEXT = os.environ.get(
        "BUSINESS_CONTEXT",
        (
            "ADSC; yüzeysel reklam kalıplarını reddeden, markalara geçici gürültüler yerine derinlemesine hikayeler ve kalıcı bağlar kazandıran sinematik, minimalist ve stratejik bir yaratıcı ajanstır. Sıradanlığa karşı net bir duruş sergileyen ajansımız, dijital dünyanın karmaşasında markaların özünü ortaya çıkarır. Sektörün bu konuda yaşadığı ezberci ve sığ yaklaşımlardaki büyük eksikliği görerek, geleneksel kalıpları yıkan gerilla reklamcılığı taktiklerini en keskin şekilde kullanarak ön plana çıkmayı hedefler."
        ),
    )

    # ── CORS İzin Verilen Kaynaklar ──────────────────────────────────────────
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")


class DevelopmentConfig(Config):
    """Geliştirme ortamı — debug açık, verbose loglar."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production ortamı — debug kapalı, güvenlik maksimum."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Test ortamı — in-memory veritabanı kullanılır."""
    DEBUG = True
    TESTING = True
    SQLITE_DB_PATH = ":memory:"


# Ortam adına göre yapılandırma seçici
config_selector = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}