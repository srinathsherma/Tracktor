# routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Ticket, Technician, Category
from datetime import datetime, timezone

# A Blueprint is a way to organise routes in a separate file
# We register it with the main app in app.py
tickets_bp = Blueprint('tickets', __name__)

# ── Home page — list all tickets ──────────────────────────────────
@tickets_bp.route('/')
def index():
    # Grab filter values from the URL
    search       = request.args.get('search', '').strip()
    status       = request.args.get('status', '')
    priority     = request.args.get('priority', '')
    category_id  = request.args.get('category_id', '')
    technician_id = request.args.get('technician_id', '')

    # Start with all tickets
    query = Ticket.query

    # Apply filters one by one if they are set
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

    # Run the final query
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

# ── Dashboard ─────────────────────────────────────────────────────
@tickets_bp.route('/dashboard')
def dashboard():
    from sqlalchemy import func
    from datetime import date

    # ── Summary counts ────────────────────────────────────────────
    total_open = Ticket.query.filter(
        Ticket.status == 'open'
    ).count()

    total_in_progress = Ticket.query.filter(
        Ticket.status == 'in_progress'
    ).count()

    total_closed = Ticket.query.filter(
        Ticket.status == 'closed'
    ).count()

    total_critical = Ticket.query.filter(
        Ticket.priority == 'critical',
        Ticket.status != 'closed'
    ).count()

    closed_today = Ticket.query.filter(
        func.date(Ticket.date_completed) == date.today()
    ).count()

    unassigned = Ticket.query.filter(
        Ticket.technician_id == None,
        Ticket.status != 'closed'
    ).count()

    # ── Tickets by priority ───────────────────────────────────────
    by_priority = db.session.query(
        Ticket.priority,
        func.count(Ticket.id).label('count')
    ).filter(
        Ticket.status != 'closed'
    ).group_by(Ticket.priority).all()

    # ── Tickets by category ───────────────────────────────────────
    by_category = db.session.query(
        Category.name,
        func.count(Ticket.id).label('count')
    ).join(Ticket, Ticket.category_id == Category.id
    ).filter(
        Ticket.status != 'closed'
    ).group_by(Category.name).all()

    # ── Tickets by technician ─────────────────────────────────────
    by_technician = db.session.query(
        Technician.name,
        func.count(Ticket.id).label('count')
    ).join(Ticket, Ticket.technician_id == Technician.id
    ).filter(
        Ticket.status != 'closed'
    ).group_by(Technician.name).all()

    # ── Recent critical tickets ───────────────────────────────────
    critical_tickets = Ticket.query.filter(
        Ticket.priority == 'critical',
        Ticket.status != 'closed'
    ).order_by(Ticket.date_requested.desc()).limit(5).all()

    return render_template('dashboard.html',
                           total_open=total_open,
                           total_in_progress=total_in_progress,
                           total_closed=total_closed,
                           total_critical=total_critical,
                           closed_today=closed_today,
                           unassigned=unassigned,
                           by_priority=by_priority,
                           by_category=by_category,
                           by_technician=by_technician,
                           critical_tickets=critical_tickets)

# ── New ticket — show form and handle submission ───────────────────
@tickets_bp.route('/tickets/new', methods=['GET', 'POST'])
def new_ticket():
    technicians = Technician.query.order_by(Technician.name).all()
    categories  = Category.query.order_by(Category.name).all()

    if request.method == 'POST':
        ticket = Ticket(
            title         = request.form['title'],
            description   = request.form['description'],
            status        = 'open',
            priority      = request.form.get('priority', 'medium'), 
            technician_id = request.form.get('technician_id') or None,
            category_id   = request.form.get('category_id') or None,
            notes         = request.form.get('notes') or None,
        )
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for('tickets.index'))

    return render_template('new_ticket.html', technicians=technicians, categories=categories)

# ── View ticket — show full detail of a single ticket ─────────────
@tickets_bp.route('/tickets/<int:ticket_id>')
def view_ticket(ticket_id):
    ticket = db.get_or_404(Ticket, ticket_id)
    return render_template('view_ticket.html', ticket=ticket)

# ── Edit ticket — update details of an existing ticket ────────────
@tickets_bp.route('/tickets/<int:ticket_id>/edit', methods=['GET', 'POST'])
def edit_ticket(ticket_id):
    ticket      = db.get_or_404(Ticket, ticket_id)
    technicians = Technician.query.order_by(Technician.name).all()
    categories  = Category.query.order_by(Category.name).all() 

    if request.method == 'POST':
        ticket.title         = request.form['title']
        ticket.description   = request.form['description']
        ticket.status        = request.form['status']
        ticket.priority      = request.form.get('priority', 'medium') 
        ticket.technician_id = request.form.get('technician_id') or None
        ticket.category_id   = request.form.get('category_id') or None
        ticket.notes         = request.form.get('notes') or None
        ticket.updated_at    = datetime.now(timezone.utc)

        db.session.commit()
        return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))

    return render_template('edit_ticket.html', ticket=ticket, technicians=technicians, categories=categories)

# ── Close ticket ──────────────────────────────────────────────────
@tickets_bp.route('/tickets/<int:ticket_id>/close', methods=['POST'])
def close_ticket(ticket_id):
    ticket                = db.get_or_404(Ticket, ticket_id)
    ticket.status         = 'closed'
    ticket.date_completed = datetime.now(timezone.utc)
    ticket.updated_at     = datetime.now(timezone.utc)

    db.session.commit()
    return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))