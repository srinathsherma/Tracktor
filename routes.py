# routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Ticket, Technician, Category
from datetime import datetime, timezone
from email_helper import (
    send_ticket_assigned_email,
    send_ticket_closed_email,
    send_critical_ticket_email
)

tickets_bp = Blueprint('tickets', __name__)

# ── Home page — list all tickets with filtering ───────────────────
@tickets_bp.route('/')
def index():
    search        = request.args.get('search', '').strip()
    status        = request.args.get('status', '')
    priority      = request.args.get('priority', '')
    category_id   = request.args.get('category_id', '')
    technician_id = request.args.get('technician_id', '')

    query = Ticket.query

    if search:
        query = query.filter(
            db.or_(
                Ticket.title.ilike(f'%{search}%'),
                Ticket.description.ilike(f'%{search}%')
            )
        )
    if status:
        query = query.filter(Ticket.status == status)
    if priority:
        query = query.filter(Ticket.priority == priority)
    if category_id:
        query = query.filter(Ticket.category_id == category_id)
    if technician_id:
        query = query.filter(Ticket.technician_id == technician_id)

    tickets     = query.order_by(Ticket.date_requested.desc()).all()
    technicians = Technician.query.order_by(Technician.name).all()
    categories  = Category.query.order_by(Category.name).all()

    return render_template('index.html',
                           tickets=tickets,
                           technicians=technicians,
                           categories=categories,
                           search=search,
                           status=status,
                           priority=priority,
                           category_id=category_id,
                           technician_id=technician_id)

# ── New ticket — show form and handle submission ───────────────────
@tickets_bp.route('/tickets/new', methods=['GET', 'POST'])
def new_ticket():
    technicians = Technician.query.order_by(Technician.name).all()
    categories  = Category.query.order_by(Category.name).all()

    if request.method == 'POST':
        technician_id = request.form.get('technician_id') or None
        priority      = request.form.get('priority', 'medium')

        ticket = Ticket(
            title         = request.form['title'],
            description   = request.form['description'],
            status        = 'open',
            priority      = priority,
            technician_id = technician_id,
            category_id   = request.form.get('category_id') or None,
            notes         = request.form.get('notes') or None,
        )
        db.session.add(ticket)
        db.session.commit()

        # ── Send email if technician assigned ─────────────────────
        if technician_id:
            technician = Technician.query.get(technician_id)
            if technician:
                send_ticket_assigned_email(technician, ticket)

        # ── Send email to all technicians if critical ─────────────
        if priority == 'critical':
            all_technicians = Technician.query.all()
            send_critical_ticket_email(all_technicians, ticket)

        return redirect(url_for('tickets.index'))

    return render_template('new_ticket.html',
                           technicians=technicians,
                           categories=categories)

# ── View ticket ───────────────────────────────────────────────────
@tickets_bp.route('/tickets/<int:ticket_id>')
def view_ticket(ticket_id):
    ticket = db.get_or_404(Ticket, ticket_id)
    return render_template('view_ticket.html', ticket=ticket)

# ── Edit ticket ───────────────────────────────────────────────────
@tickets_bp.route('/tickets/<int:ticket_id>/edit', methods=['GET', 'POST'])
def edit_ticket(ticket_id):
    ticket      = db.get_or_404(Ticket, ticket_id)
    technicians = Technician.query.order_by(Technician.name).all()
    categories  = Category.query.order_by(Category.name).all()

    if request.method == 'POST':
        old_technician_id = ticket.technician_id
        new_technician_id = request.form.get('technician_id') or None

        ticket.title         = request.form['title']
        ticket.description   = request.form['description']
        ticket.status        = request.form['status']
        ticket.priority      = request.form.get('priority', 'medium')
        ticket.technician_id = new_technician_id
        ticket.category_id   = request.form.get('category_id') or None
        ticket.notes         = request.form.get('notes') or None
        ticket.updated_at    = datetime.now(timezone.utc)

        db.session.commit()

        # ── Send email if technician changed ──────────────────────
        if new_technician_id and new_technician_id != str(old_technician_id):
            technician = Technician.query.get(new_technician_id)
            if technician:
                send_ticket_assigned_email(technician, ticket)

        return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))

    return render_template('edit_ticket.html',
                           ticket=ticket,
                           technicians=technicians,
                           categories=categories)

# ── Close ticket ──────────────────────────────────────────────────
@tickets_bp.route('/tickets/<int:ticket_id>/close', methods=['POST'])
def close_ticket(ticket_id):
    ticket                = db.get_or_404(Ticket, ticket_id)
    ticket.status         = 'closed'
    ticket.date_completed = datetime.now(timezone.utc)
    ticket.updated_at     = datetime.now(timezone.utc)

    db.session.commit()

    # ── Send email to assigned technician ─────────────────────────
    if ticket.technician:
        send_ticket_closed_email(ticket.technician, ticket)

    return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))