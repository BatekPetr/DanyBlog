import os

from flask import render_template, Flask

from model import bcrypt, db, login_manager, migrate, mail
from config import config

# Import blueprints
from src.accounts.views import accounts_bp
from src.core.views import core_bp
from src.posts.views import posts_bp

from src.accounts.models import User


def create_app(cfg):

    app = Flask(__name__)

    # Konfigurace databáze a cesta pro nahrávání souborů
    app.config['SECRET_KEY'] = cfg.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = cfg.SQLALCHEMY_DATABASE_URI
    app.config['UPLOAD_FOLDER'] = cfg.UPLOAD_FOLDER
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = cfg.DEBUG

    # Konfigurece emailu
    app.config['MAIL_SERVER'] = cfg.MAIL_SERVER
    app.config['MAIL_PORT'] = cfg.MAIL_PORT
    app.config['MAIL_USE_SSL'] = cfg.MAIL_USE_SSL
    app.config['MAIL_USE_TLS'] = cfg.MAIL_USE_TLS
    app.config['MAIL_USERNAME'] = cfg.ADMIN_EMAIL
    app.config['MAIL_PASSWORD'] = cfg.ADMIN_EMAIL_APP_PASS


    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    mail.init_app(app)
    migrate.init_app(app, db)

    # Registering blueprints
    app.register_blueprint(accounts_bp)
    app.register_blueprint(core_bp)
    app.register_blueprint(posts_bp)

    login_manager.login_view = "accounts.login"
    login_manager.login_message_category = "danger"

    # # Po zmene DB modelu je nutne vymazat a znovu-vytvorit tabulky
    # with core.app_context():
    #     db.drop_all()  # Vymaze existujici tabulky

    # Vytvoření databázových tabulek při prvním spuštění
    with app.app_context():
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('404.html'), 404


# Select configuration here
cfg = config["development"]
app = create_app(cfg)


if __name__ == "__main__":
    app.run(debug=cfg.DEBUG)