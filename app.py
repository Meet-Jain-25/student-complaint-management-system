from flask import Flask, render_template

from config import Config
from extensions import db, login_manager


def create_app():
    """Application factory."""

    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    @app.route("/")
    def home():
        return render_template("index.html")

    # Import models so SQLAlchemy knows about them
    from models.user import User

    # Register authentication routes
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from routes.student import student_bp
    app.register_blueprint(student_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)