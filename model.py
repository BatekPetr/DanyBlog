from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
login_manager = LoginManager()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()