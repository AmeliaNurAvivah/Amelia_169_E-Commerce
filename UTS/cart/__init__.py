# flask_app/__init__.py

from flask import Flask

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = "replace-with-secret"

    # register routes
    
    from interface.flask.routes import web
    

    app.register_blueprint(web)

    return app
