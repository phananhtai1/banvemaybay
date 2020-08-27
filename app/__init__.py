from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "\x11\xad\xc4\xc0h\xdbk\x0b^\x9d\xc1\xa2\xb6^9\x87"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/demo5?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)

admin = Admin(app=app, name="Ban Ve May Bay", template_mode="bootstrap3")

login = LoginManager(app=app)
