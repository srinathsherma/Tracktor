# app.py
from flask import Flask
from models import db
from routes import tickets_bp
from technician_routes import technicians_bp
from category_routes import categories_bp
from flask_mail import Mail
from dotenv import load_dotenv
import os

# ── Load environment variables from .env file ─────────────────────
load_dotenv()

app = Flask(__name__)

# ── Database config ───────────────────────────────────────────────
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + os.path.join(BASE_DIR, 'issuetracker.db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-before-production')

# ── Email config ──────────────────────────────────────────────────
app.config['MAIL_SERVER']   = 'smtp.gmail.com'
app.config['MAIL_PORT']     = 587
app.config['MAIL_USE_TLS']  = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = (
    'Tracktor', os.environ.get('MAIL_USERNAME')
)

# ── Initialise extensions ─────────────────────────────────────────
db.init_app(app)
mail = Mail(app)

# ── Register blueprints ───────────────────────────────────────────
app.register_blueprint(tickets_bp)
app.register_blueprint(technicians_bp)
app.register_blueprint(categories_bp)

# ── Create tables on first run ────────────────────────────────────
with app.app_context():
    db.create_all()

# ── Run ───────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5001)