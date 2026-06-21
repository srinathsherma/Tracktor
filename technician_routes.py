# technician_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Technician
from datetime import datetime, timezone
import hashlib

technicians_bp = Blueprint('technicians', __name__)

# ── Gravatar helper ────────────────────────────────────────────────
def gravatar_url(email, size=120):
    email_hash = hashlib.md5(email.lower().strip().encode()).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"

# ── List all technicians ───────────────────────────────────────────
@technicians_bp.route('/technicians')
def list_technicians():
    technicians = Technician.query.order_by(Technician.name).all()
    return render_template('technicians.html',
                           technicians=technicians,
                           gravatar_url=gravatar_url)

# ── View technician profile ────────────────────────────────────────
@technicians_bp.route('/technicians/<int:technician_id>')
def view_technician(technician_id):
    technician = db.get_or_404(Technician, technician_id)
    return render_template('view_technician.html',
                           technician=technician,
                           gravatar_url=gravatar_url)

# ── Add new technician ─────────────────────────────────────────────
@technicians_bp.route('/technicians/new', methods=['GET', 'POST'])
def new_technician():
    error = None

    if request.method == 'POST':
        name  = request.form['name'].strip()
        email = request.form['email'].strip().lower()

        existing = Technician.query.filter_by(email=email).first()
        if existing:
            error = f'A technician with the email {email} already exists.'
        else:
            technician = Technician(
                name        = name,
                email       = email,
                phone       = request.form.get('phone') or None,
                job_title   = request.form.get('job_title') or None,
                department  = request.form.get('department') or None,
                bio         = request.form.get('bio') or None,
                date_joined = datetime.now(timezone.utc)
            )
            db.session.add(technician)
            db.session.commit()
            return redirect(url_for('technicians.list_technicians'))

    return render_template('new_technician.html', error=error)

# ── Edit technician profile ────────────────────────────────────────
@technicians_bp.route('/technicians/<int:technician_id>/edit', methods=['GET', 'POST'])
def edit_technician(technician_id):
    technician = db.get_or_404(Technician, technician_id)
    error      = None

    if request.method == 'POST':
        email = request.form['email'].strip().lower()

        existing = Technician.query.filter_by(email=email).first()
        if existing and existing.id != technician.id:
            error = f'A technician with the email {email} already exists.'
        else:
            technician.name       = request.form['name'].strip()
            technician.email      = email
            technician.phone      = request.form.get('phone') or None
            technician.job_title  = request.form.get('job_title') or None
            technician.department = request.form.get('department') or None
            technician.bio        = request.form.get('bio') or None

            db.session.commit()
            return redirect(url_for('technicians.view_technician',
                                    technician_id=technician.id))

    return render_template('edit_technician.html',
                           technician=technician,
                           error=error, gravatar_url=gravatar_url)

# ── Delete technician ──────────────────────────────────────────────
@technicians_bp.route('/technicians/<int:technician_id>/delete', methods=['POST'])
def delete_technician(technician_id):
    technician = db.get_or_404(Technician, technician_id)
    db.session.delete(technician)
    db.session.commit()
    return redirect(url_for('technicians.list_technicians'))