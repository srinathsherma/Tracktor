# category_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Category

categories_bp = Blueprint('categories', __name__)

# ── List all categories ────────────────────────────────────────────
@categories_bp.route('/categories')
def list_categories():
    categories = Category.query.order_by(Category.name).all()
    return render_template('categories.html', categories=categories)

# ── Add new category ───────────────────────────────────────────────
@categories_bp.route('/categories/new', methods=['GET', 'POST'])
def new_category():
    error = None

    if request.method == 'POST':
        name        = request.form['name'].strip()
        description = request.form.get('description', '').strip() or None

        # Check for duplicate name
        existing = Category.query.filter_by(name=name).first()
        if existing:
            error = f'A category named "{name}" already exists.'
        else:
            category = Category(name=name, description=description)
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('categories.list_categories'))

    return render_template('new_category.html', error=error)

# ── Delete category ────────────────────────────────────────────────
@categories_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    category = db.get_or_404(Category, category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('categories.list_categories'))