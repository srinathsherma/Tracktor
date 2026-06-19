# app.py
from flask import Flask
from models import db
from routes import tickets_bp 
from technician_routes import technicians_bp
from category_routes import categories_bp  

import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + os.path.join(BASE_DIR, 'issuetracker.db'))
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'change-this-before-going-to-production'

db.init_app(app)

app.register_blueprint(tickets_bp)
app.register_blueprint(technicians_bp)
app.register_blueprint(categories_bp)        

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5001)