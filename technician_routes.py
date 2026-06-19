# technician_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Technician

technicians_bp = Blueprint('technicians', __name__)

# ── List all technicians ───────────────────────────────────────────
@technicians_bp.route('/technicians')
def list_technicians():
    technicians = Technician.query.order_by(Technician.name).all()
    return render_template('technicians.html', technicians=technicians)

# ── Add new technician ─────────────────────────────────────────────
@technicians_bp.route('/technicians/new', methods=['GET', 'POST'])
def new_technician():
    error = None

    if request.method == 'POST':
        name  = request.form['name'].strip()
        email = request.form['email'].strip().lower()

        # Check for duplicate email
        existing = Technician.query.filter_by(email=email).first()
        if existing:
            error = f'A technician with the email {email} already exists.'
        else:
            technician = Technician(name=name, email=email)
            db.session.add(technician)
            db.session.commit()
            return redirect(url_for('technicians.list_technicians'))

    return render_template('new_technician.html', error=error)

# ── Delete technician ──────────────────────────────────────────────
@technicians_bp.route('/technicians/<int:technician_id>/delete', methods=['POST'])
def delete_technician(technician_id):
    technician = db.get_or_404(Technician, technician_id)
    db.session.delete(technician)
    db.session.commit()
    return redirect(url_for('technicians.list_technicians'))