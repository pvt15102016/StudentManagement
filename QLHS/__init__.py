from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
import cloudinary
from flask_login import LoginManager

app = Flask(__name__, template_folder="template")

app.secret_key = '^TDYGF^&FD&S7dft7dg7&TFđ)TIE)FUIUWGF^&S'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost/qlhs?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

cloudinary.config(
        cloud_name='ou-edu-vn',
        api_key='859828731383835',
        api_secret='MK9KhM3Csp7nXu3z0czVYQ_-c6Q'
)

login = LoginManager(app=app)

babel = Babel(app=app)

@babel.localeselector
def get_locale():
        return 'vi'