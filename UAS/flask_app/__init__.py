# flask_app/__init__.py

from flask import Flask

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = "replace-with-secret"

    # register routes
    from flask_app.routes.routes import main_bp
    from flask_app.routes.auth_routes import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app
