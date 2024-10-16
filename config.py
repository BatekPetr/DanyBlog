import os
from src.instance import config as instance_config

# Základní nastavení
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads/'

    # Mail Settings
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_DEBUG = False

    MAIL_DEFAULT_SENDER = instance_config.ADMIN_EMAIL
    ADMIN_EMAIL = instance_config.ADMIN_EMAIL
    ADMIN_EMAIL_APP_PASS = instance_config.ADMIN_EMAIL_APP_PASS

    SECRET_KEY = instance_config.SECRET_KEY
    SECURITY_PASSWORD_SALT = instance_config.SECURITY_PASSWORD_SALT

# Vývojové prostředí
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or instance_config.SQLALCHEMY_DATABASE_URI

# Testovací prostředí
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False  # Pokud testujete formuláře

# Produkční prostředí
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI') or instance_config.SQLALCHEMY_DATABASE_URI

# Volba konfigurace podle prostředí
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}