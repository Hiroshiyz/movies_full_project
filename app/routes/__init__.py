
# 一種modules components
from .auth_routes import auth_bp
from .movie_routes import movie_bp
# from .order_routes import order_bp


def get_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(movie_bp)
    # app.register_blueprint(order_bp)
