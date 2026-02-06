from flask import Flask, render_template, redirect, url_for

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mysecretkey'
    
    
    @app.route("/")
    def index():
        return render_template ("pages/guests/index.html")
    
    from .routes import guest_bp, user_bp
    
    app.register_blueprint(guest_bp)
    app.register_blueprint(user_bp)
    
    return app