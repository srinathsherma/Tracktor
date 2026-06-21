# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = "categories"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)

    tickets = db.relationship("Ticket", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"


class Technician(db.Model):
    __tablename__ = "technicians"

    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone       = db.Column(db.String(20), nullable=True)
    job_title   = db.Column(db.String(100), nullable=True)
    department  = db.Column(db.String(100), nullable=True)
    date_joined = db.Column(db.DateTime, nullable=True)
    bio         = db.Column(db.Text, nullable=True)

    tickets = db.relationship("Ticket", back_populates="technician")

    def __repr__(self):
        return f"<Technician {self.name}>"


class Ticket(db.Model):
    __tablename__ = "tickets"

    id            = db.Column(db.Integer, primary_key=True)
    title         = db.Column(db.String(200), nullable=False)
    description   = db.Column(db.Text, nullable=False)
    status        = db.Column(db.String(20), nullable=False, default="open")
    priority      = db.Column(db.String(20), nullable=False, default="medium") 
    technician_id = db.Column(db.Integer, db.ForeignKey("technicians.id"), nullable=True)
    category_id   = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    notes         = db.Column(db.Text, nullable=True)

    date_requested = db.Column(db.DateTime, nullable=False,
                               default=lambda: datetime.now(timezone.utc))
    date_completed = db.Column(db.DateTime, nullable=True)
    created_at     = db.Column(db.DateTime, nullable=False,
                               default=lambda: datetime.now(timezone.utc))
    updated_at     = db.Column(db.DateTime, nullable=False,
                               default=lambda: datetime.now(timezone.utc),
                               onupdate=lambda: datetime.now(timezone.utc))

    technician = db.relationship("Technician", back_populates="tickets")
    category   = db.relationship("Category", back_populates="tickets")

    def __repr__(self):
        return f"<Ticket #{self.id} [{self.status}] {self.title!r}>"