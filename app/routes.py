from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, current_user, login_required
try:
    from werkzeug.urls import url_parse
except ImportError:
    from urllib.parse import urlparse as url_parse
from app import db
from app.models import User, Skill, SwapRequest
from app.forms import LoginForm, RegistrationForm, SkillForm, SwapRequestForm, ProfileSettingsForm
from werkzeug.utils import secure_filename
from flask import current_app
import os
from flask import session, jsonify

# PIL import with error handling
try:
    from PIL import Image
except ImportError:
    Image = None
    print("Warning: PIL not installed. Profile photo resizing disabled.")

# Blueprint definitions - FIXED ORDER
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
profile_bp = Blueprint('profile', __name__, url_prefix='/profile')  
swaps_bp = Blueprint('swaps', __name__, url_prefix='/swaps')

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[21].lower() in current_app.config.get('ALLOWED_EXTENSIONS', {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'})

# ... keep all your existing route functions exactly as they are ...




# ======================
# Blueprint Initialization
# ======================

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config.get('ALLOWED_EXTENSIONS', {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'})

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
profile_bp = Blueprint('profile', __name__, url_prefix='/profile')
swaps_bp = Blueprint('swaps', __name__, url_prefix='/swaps')
main_bp = Blueprint('main', __name__)

# ======================
# Authentication Routes
# ======================

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))  # Fixed: use index instead of dashboard
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')  # Fixed: use index instead of dashboard
        return redirect(next_page)
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))  # Fixed: use index instead of dashboard
        
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'danger')
            return redirect(url_for('auth.register'))
            
        existing_username = User.query.filter_by(username=form.username.data.strip()).first()
        if existing_username:
            flash('Username already taken. Please choose a different username.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower()
        )
        user.set_password(form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            
            # Automatically log in the new user
            login_user(user)
            
            flash(f'Welcome to SkillSwap, {user.username}! Your account has been created successfully.', 'success')
            return redirect(url_for('main.index'))  # Fixed: use index instead of dashboard
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))  # Fixed: use index instead of home

@auth_bp.route('/oauth/<provider>')
def oauth_login(provider):
    """OAuth login route - placeholder for future implementation"""
    flash(f'{provider.title()} login coming soon!', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))  # Fixed: use index instead of dashboard
    
    # Basic form handling - you'll need to create ResetPasswordRequestForm
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        if email:
            user = User.query.filter_by(email=email).first()
            if user:
                # TODO: Implement email sending logic
                flash('Check your email for password reset instructions.', 'info')
            else:
                flash('Email address not found.', 'danger')
        else:
            flash('Please enter an email address.', 'danger')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password_request.html')

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))  # Fixed: use index instead of dashboard
    
    # TODO: Implement token verification and password reset
    flash('Password reset functionality coming soon!', 'info')
    return redirect(url_for('auth.login'))

# ======================
# Profile Routes
# ======================

@profile_bp.route('')
@login_required
def view():
    try:
        # Get user's skills for display
        offered_skills = Skill.query.filter_by(offered_by_id=current_user.id).all()
        wanted_skills = Skill.query.filter_by(wanted_by_id=current_user.id).all()
        
        # Get recent swap requests for the user
        recent_requests = SwapRequest.query.filter(
            (SwapRequest.sender_id == current_user.id) | 
            (SwapRequest.receiver_id == current_user.id)
        ).order_by(SwapRequest.created_at.desc()).limit(5).all()
        
        return render_template('profile/view.html',
                             user=current_user,
                             offered_skills=offered_skills,
                             wanted_skills=wanted_skills,
                             recent_requests=recent_requests)
    except Exception as e:
        flash('Error loading profile. Please try again.', 'danger')
        current_app.logger.error(f"Profile view error: {str(e)}")
        return redirect(url_for('main.index'))


# Remove the first edit function (around line 132-180) and keep only this one:

@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = ProfileSettingsForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        current_user.availability = form.availability.data

        # Handle profile photo upload
        if form.profile_photo.data:
            filename = secure_filename(form.profile_photo.data.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            form.profile_photo.data.save(file_path)
            current_user.profile_photo = filename

            image = Image.open(file_path)
            image = image.convert("RGB")  # Ensures compatibility
            image = image.resize((400, 400))  # Resize to 100x100
            image.save(file_path, format='JPEG')  # Save resized image

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.view'))

    # Pre-fill the form with existing values
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.bio.data = current_user.bio
    form.location.data = current_user.location
    form.availability.data = current_user.availability

    return render_template('profile/edit.html', form=form)

@profile_bp.route('/skill/<int:skill_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    
    # Check if user owns this skill
    if skill.offered_by_id != current_user.id and skill.wanted_by_id != current_user.id:
        abort(403)
    
    form = SkillForm(obj=skill)
    
    # Pre-populate skill_type based on current skill
    if skill.offered_by_id == current_user.id:
        form.skill_type.data = 'offered'
    else:
        form.skill_type.data = 'wanted'
    
    if form.validate_on_submit():
        try:
            skill.name = form.name.data.strip()
            skill.availability = form.availability.data.strip() if form.availability.data else None
            
            # Handle skill type change
            if form.skill_type.data == 'offered':
                skill.offered_by_id = current_user.id
                skill.wanted_by_id = None
            else:
                skill.wanted_by_id = current_user.id
                skill.offered_by_id = None
            
            db.session.commit()
            flash(f'Skill "{skill.name}" has been updated!', 'success')
            return redirect(url_for('profile.view'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the skill. Please try again.', 'danger')
            current_app.logger.error(f"Skill update error: {str(e)}")
            return redirect(url_for('profile.edit_skill', skill_id=skill_id))
    
    return render_template('profile/edit_skill.html', form=form, skill=skill)

@profile_bp.route('/skill/add', methods=['GET', 'POST'])
@login_required
def add_skill():
    form = SkillForm()
    if form.validate_on_submit():
        try:
            skill = Skill(
                name=form.name.data.strip(),
                offered_by_id=current_user.id if form.skill_type.data == 'offered' else None,
                wanted_by_id=current_user.id if form.skill_type.data == 'wanted' else None,
                # availability=form.availability.data.strip() if form.availability.data else None
            )
            db.session.add(skill)
            db.session.commit()
            flash(f'Skill "{skill.name}" added successfully!', 'success')
            return redirect(url_for('profile.view'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the skill.', 'danger')
            current_app.logger.error(f"Add skill error: {str(e)}")

    return render_template('profile/add_skill.html', form=form, user=current_user)

@profile_bp.route('/skill/<int:skill_id>/delete', methods=['POST'])
@login_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    
    # Check if user owns this skill
    if skill.offered_by_id != current_user.id and skill.wanted_by_id != current_user.id:
        abort(403)
    
    try:
        skill_name = skill.name
        db.session.delete(skill)
        db.session.commit()
        flash(f'Skill "{skill_name}" has been deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the skill. Please try again.', 'danger')
        current_app.logger.error(f"Delete skill error: {str(e)}")
    
    return redirect(url_for('profile.view'))

# ======================
# Swap Routes
# ======================

@swaps_bp.route('/browse')
@login_required
def browse():
    try:
        search_query = request.args.get('q', '').strip()
        skill_filter = request.args.get('skill', '').strip()
        
        # Base query - exclude current user and only show public profiles
        query = User.query.filter(
            User.is_public == True,
            User.id != current_user.id
        )
        
        if search_query:
            query = query.filter(User.username.ilike(f'%{search_query}%'))
        
        if skill_filter:
            # Fixed: Proper skill filtering with joins
            query = query.join(Skill, 
                (Skill.offered_by_id == User.id) | (Skill.wanted_by_id == User.id)
            ).filter(Skill.name.ilike(f'%{skill_filter}%')).distinct()
        
        users = query.all()
        return render_template('swaps/browse.html', 
                             users=users, 
                             search_query=search_query,
                             skill_filter=skill_filter)
    except Exception as e:
        flash('Error loading browse page. Please try again.', 'danger')
        current_app.logger.error(f"Browse error: {str(e)}")
        return redirect(url_for('main.index'))

@swaps_bp.route('/request/<int:user_id>', methods=['GET', 'POST'])
@login_required
def send_request(user_id):
    receiver = User.query.get_or_404(user_id)
    
    # Check if user is trying to send request to themselves
    if receiver.id == current_user.id:
        flash('You cannot send a swap request to yourself.', 'warning')
        return redirect(url_for('swaps.browse'))
    
    # Check if request already exists
    existing_request = SwapRequest.query.filter_by(
        sender_id=current_user.id,
        receiver_id=receiver.id,
        status='pending'
    ).first()
    
    if existing_request:
        flash('You already have a pending request with this user.', 'warning')
        return redirect(url_for('swaps.browse'))
    
    form = SwapRequestForm()
    if form.validate_on_submit():
        try:
            swap = SwapRequest(
                sender_id=current_user.id,
                receiver_id=receiver.id,
                message=form.message.data.strip() if form.message.data else None
            )
            db.session.add(swap)
            db.session.commit()
            flash(f'Swap request sent to {receiver.username} successfully!', 'success')
            return redirect(url_for('swaps.browse'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while sending the request. Please try again.', 'danger')
            current_app.logger.error(f"Send request error: {str(e)}")
            return redirect(url_for('swaps.send_request', user_id=user_id))
    
    return render_template('swaps/send_request.html', form=form, receiver=receiver)

@swaps_bp.route('/requests')
@login_required
def manage_requests():
    try:
        received = SwapRequest.query.filter_by(receiver_id=current_user.id).order_by(SwapRequest.created_at.desc()).all()
        sent = SwapRequest.query.filter_by(sender_id=current_user.id).order_by(SwapRequest.created_at.desc()).all()
        return render_template('swaps/requests.html', received=received, sent=sent)
    except Exception as e:
        flash('Error loading swap requests. Please try again.', 'danger')
        current_app.logger.error(f"Manage requests error: {str(e)}")
        return redirect(url_for('main.index'))

@swaps_bp.route('/request/<int:request_id>/accept', methods=['POST'])
@login_required
def accept_request(request_id):
    swap = SwapRequest.query.get_or_404(request_id)
    
    # Check if user is the receiver and request is pending
    if swap.receiver_id != current_user.id:
        abort(403)
    
    if swap.status != 'pending':
        flash('This request has already been processed.', 'warning')
        return redirect(url_for('swaps.manage_requests'))
    
    try:
        swap.status = 'accepted'
        db.session.commit()
        flash(f'Swap request from {swap.sender.username} accepted!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while accepting the request. Please try again.', 'danger')
        current_app.logger.error(f"Accept request error: {str(e)}")
    
    return redirect(url_for('swaps.manage_requests'))

@swaps_bp.route('/request/<int:request_id>/reject', methods=['POST'])
@login_required
def reject_request(request_id):
    swap = SwapRequest.query.get_or_404(request_id)
    
    # Check if user is the receiver and request is pending
    if swap.receiver_id != current_user.id:
        abort(403)
    
    if swap.status != 'pending':
        flash('This request has already been processed.', 'warning')
        return redirect(url_for('swaps.manage_requests'))
    
    try:
        swap.status = 'rejected'
        db.session.commit()
        flash(f'Swap request from {swap.sender.username} rejected.', 'info')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while rejecting the request. Please try again.', 'danger')
        current_app.logger.error(f"Reject request error: {str(e)}")
    
    return redirect(url_for('swaps.manage_requests'))

@swaps_bp.route('/request/<int:request_id>/complete', methods=['POST'])
@login_required
def complete_request(request_id):
    swap = SwapRequest.query.get_or_404(request_id)
    
    # Check if user is involved in this swap and it's accepted
    if swap.sender_id != current_user.id and swap.receiver_id != current_user.id:
        abort(403)
    
    if swap.status != 'accepted':
        flash('This request cannot be completed in its current state.', 'warning')
        return redirect(url_for('swaps.manage_requests'))
    
    try:
        swap.status = 'completed'
        db.session.commit()
        flash('Swap marked as completed!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while completing the swap. Please try again.', 'danger')
        current_app.logger.error(f"Complete request error: {str(e)}")
    
    return redirect(url_for('swaps.manage_requests'))

@swaps_bp.route('/request/<int:request_id>/cancel', methods=['POST'])
@login_required
def cancel_request(request_id):
    """Allow users to cancel their own pending requests"""
    swap = SwapRequest.query.get_or_404(request_id)
    
    # Check if user is the sender and request is pending
    if swap.sender_id != current_user.id:
        abort(403)
    
    if swap.status != 'pending':
        flash('This request cannot be cancelled in its current state.', 'warning')
        return redirect(url_for('swaps.manage_requests'))
    
    try:
        db.session.delete(swap)
        db.session.commit()
        flash('Swap request cancelled successfully.', 'info')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while cancelling the request. Please try again.', 'danger')
        current_app.logger.error(f"Cancel request error: {str(e)}")
    
    return redirect(url_for('swaps.manage_requests'))

# ======================
# Main Routes
# ======================
from flask import session, jsonify

@main_bp.route('/toggle-dark-mode', methods=['POST'])
def toggle_dark_mode():
    """Toggle dark mode setting in session"""
    current_mode = session.get('dark_mode', False)
    session['dark_mode'] = not current_mode
    return jsonify({
        'success': True, 
        'dark_mode': session['dark_mode']
    })



@main_bp.route('/')
def index():
    """Root route - serves as both landing page and dashboard"""
    if current_user.is_authenticated:
        # Get user's skills for the dashboard
        try:
            offered_skills = Skill.query.filter_by(offered_by_id=current_user.id).all()
            wanted_skills = Skill.query.filter_by(wanted_by_id=current_user.id).all()
            
            # Get recent swap requests
            recent_requests = SwapRequest.query.filter(
                (SwapRequest.sender_id == current_user.id) | 
                (SwapRequest.receiver_id == current_user.id)
            ).order_by(SwapRequest.created_at.desc()).limit(5).all()
            
            return render_template('main/dashboard.html', 
                                 offered_skills=offered_skills, 
                                 wanted_skills=wanted_skills,
                                 recent_requests=recent_requests)
        except Exception as e:
            # If dashboard fails, show a simple authenticated page
            current_app.logger.error(f"Dashboard error: {str(e)}")
            return render_template('main/dashboard.html', 
                                 offered_skills=[], 
                                 wanted_skills=[],
                                 recent_requests=[])
    else:
        # Show landing page for non-authenticated users
        return render_template('main/landing.html')

@main_bp.route('/home')
def home():
    """Home page - redirect to index to avoid loops"""
    return redirect(url_for('main.index'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard - redirect to index to avoid loops"""
    return redirect(url_for('main.index'))

# ======================
# Error Handlers
# ======================

@main_bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@main_bp.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

# ======================
# Additional Utility Routes
# ======================

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')

@main_bp.route('/contact')
def contact():
    """Contact page"""
    return render_template('main/contact.html')

@main_bp.route('/search')
@login_required
def search():
    """Global search functionality"""
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('main.index'))
    
    try:
        # Search users
        users = User.query.filter(
            User.is_public == True,
            User.id != current_user.id,
            User.username.ilike(f'%{query}%')
        ).limit(10).all()
        
        # Search skills
        skills = Skill.query.filter(
            Skill.name.ilike(f'%{query}%')
        ).limit(10).all()
        
        return render_template('main/search_results.html', 
                             query=query, 
                             users=users, 
                             skills=skills)
    except Exception as e:
        flash('Error performing search. Please try again.', 'danger')
        current_app.logger.error(f"Search error: {str(e)}")
        return redirect(url_for('main.index'))

@profile_bp.route('/upload_photo', methods=['POST'])
@login_required
def upload_photo():
    """Handle profile photo upload"""
    if 'file' not in request.files:
        flash('No file selected.', 'danger')
        return redirect(url_for('profile.edit'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected.', 'danger')
        return redirect(url_for('profile.edit'))
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            # Add timestamp to avoid conflicts
            import time
            timestamp = str(int(time.time()))
            filename = f"{current_user.id}_{timestamp}_{filename}"
            
            # Ensure upload directory exists
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
            
            # Update user's profile photo
            current_user.profile_photo = filename
            db.session.commit()
            
            flash('Profile photo updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error uploading photo. Please try again.', 'danger')
            current_app.logger.error(f"Photo upload error: {str(e)}")
    else:
        flash('Invalid file type. Please upload an image file.', 'danger')
    
    return redirect(url_for('profile.edit'))

@main_bp.route('/user/<int:user_id>')
@login_required
def view_user_profile(user_id):
    """View another user's public profile"""
    user = User.query.get_or_404(user_id)
    
    # Check if profile is public or if it's the current user
    if not user.is_public and user.id != current_user.id:
        flash('This profile is private.', 'warning')
        return redirect(url_for('swaps.browse'))
    
    try:
        offered_skills = Skill.query.filter_by(offered_by_id=user.id).all()
        wanted_skills = Skill.query.filter_by(wanted_by_id=user.id).all()
        
        return render_template('main/user_profile.html',
                             user=user,
                             offered_skills=offered_skills,
                             wanted_skills=wanted_skills)
    except Exception as e:
        flash('Error loading user profile. Please try again.', 'danger')
        current_app.logger.error(f"View user profile error: {str(e)}")
        return redirect(url_for('swaps.browse'))
    
# Replace your existing profile_bp.route('/edit') with this updated version:

from PIL import Image  # Add this import at the top of your file

def resize_image(image_path, max_size=(300, 300)):
    """Resize image to maximum dimensions while maintaining aspect ratio"""
    with Image.open(image_path) as img:
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(image_path, optimize=True, quality=85)
