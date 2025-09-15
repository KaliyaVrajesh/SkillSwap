import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # Fix: Use absolute path for SQLite database
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.dirname(BASEDIR)  # Go up from app/ to project root
    INSTANCE_PATH = os.path.join(PROJECT_ROOT, 'instance')
    
    # Ensure instance directory exists
    os.makedirs(INSTANCE_PATH, exist_ok=True)
    
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("SQLALCHEMY_DATABASE_URI") or
        os.getenv("LOCAL_DATABASE_URI") or
        f"sqlite:///{os.path.join(INSTANCE_PATH, 'skillswap.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Login
    SESSION_PROTECTION = 'strong'
    
    # Email (optional)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    
    # File uploads
    UPLOAD_FOLDER = os.path.join(BASEDIR, "static", "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
