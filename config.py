import os


class Config:
    """Application configuration."""

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # SQLite database
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "complaints.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key for sessions and authentication
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "student-complaint-system-development-key"
    )