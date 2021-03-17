from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')


db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = 'some_random_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from my_app.auth.views import auth
app.register_blueprint(auth)

db.create_all()
