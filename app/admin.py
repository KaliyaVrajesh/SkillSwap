from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import User, Skill, SwapRequest, db
from functools import wraps
from sqlalchemy import func, desc
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    # Calculate stats
    stats = {
        'total_users': User.query.count(),
        'active_swaps': SwapRequest.query.filter_by(status='accepted').count(),
        'total_skills': Skill.query.count(),
        'public_users': User.query.filter_by(is_public=True).count(),
    }
    
    # Get registration trends (dummy data for now)
    stats['registration_dates'] = []
    stats['registration_counts'] = []
    stats['top_skills'] = {'labels': [], 'values': []}
    
    recent_actions = []  # You can expand this later
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_actions=recent_actions)

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/skills')
@login_required
@admin_required
def manage_skills():
    skills = Skill.query.all()
    return render_template('admin/skills.html', skills=skills)

@admin_bp.route('/swaps')
@login_required
@admin_required
def manage_swaps():
    swaps = SwapRequest.query.all()
    return render_template('admin/swaps.html', swaps=swaps)
