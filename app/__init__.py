from flask import Flask
from app.db import db_session, init_db
from app.config import Config
from app.routes import get_routes
from flask_login import LoginManager
from app.models import User
from app.db import db_session
from app.seed_seat import create_seat, seed_movies
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # 抓取secretKEY,API
    init_db()
    # database
    seed_movies()
    create_seat()
    get_routes(app)
    # route

    login_manager.init_app(app)
    # login..

    @login_manager.user_loader
    def load_user(user_id):
        return db_session.query(User).get(user_id)
# 這個會被自動觸發
# 簡單來說，load_user 就是 Flask-Login 跟你的資料庫之間的「橋樑」，告訴它「拿到 session 裡的 user_id，要怎麼把它變成一個 User 物件」。

    @app.teardown_appcontext
    def close_session(exception=None):
        db_session.remove()
    return app
