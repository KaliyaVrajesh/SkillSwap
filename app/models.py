# from datetime import datetime
# from app import db, login_manager
# from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash

# class User(UserMixin, db.Model):
#     """User model with authentication and profile details."""
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True, nullable=False)
#     email = db.Column(db.String(120), index=True, unique=True, nullable=False)
#     password_hash = db.Column(db.String(128))
#     is_public = db.Column(db.Boolean, default=True)
#     location = db.Column(db.String(100), nullable=True)  # Added location field
#     profile_photo = db.Column(db.String(200), nullable=True)  # Changed from profile_pic
#     bio = db.Column(db.Text, nullable=True)  # Added bio field
#     availability = db.Column(db.String(50), nullable=True)  # Added availability field
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     # Relationships
#     skills_offered = db.relationship('Skill', backref='offered_by', foreign_keys='Skill.offered_by_id', lazy='dynamic')
#     skills_wanted = db.relationship('Skill', backref='wanted_by', foreign_keys='Skill.wanted_by_id', lazy='dynamic')
#     sent_swap_requests = db.relationship('SwapRequest', foreign_keys='SwapRequest.sender_id', backref='sender', lazy='dynamic')
#     received_swap_requests = db.relationship('SwapRequest', foreign_keys='SwapRequest.receiver_id', backref='receiver', lazy='dynamic')

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
    
#     # Add helper property for template compatibility
#     @property
#     def name(self):
#         return self.username

#     def __repr__(self):
#         return f'<User {self.username}>'

# class Skill(db.Model):
#     """Skills offered/wanted by users."""
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     offered_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     wanted_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     availability = db.Column(db.String(100))  # e.g., "Weekends, Evenings"

#     def __repr__(self):
#         return f'<Skill {self.name}>'

# class SwapRequest(db.Model):
#     """Swap requests between users."""
#     id = db.Column(db.Integer, primary_key=True)
#     sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     message = db.Column(db.Text)
#     status = db.Column(db.String(20), default='pending')  # 'accepted', 'rejected', 'completed'
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     feedback = db.Column(db.Text)

#     def __repr__(self):
#         return f'<SwapRequest {self.id}: {self.sender.username} -> {self.receiver.username}>'

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# # In models.py under User class:

# @property
# def offered_skills(self):
#     from app.models import Skill
#     return Skill.query.filter_by(offered_by_id=self.id).all()

# @property
# def wanted_skills(self):
#     from app.models import Skill
#     return Skill.query.filter_by(wanted_by_id=self.id).all()

# class User(UserMixin, db.Model):
#     """User model with authentication and profile details."""
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True, nullable=False)
#     email = db.Column(db.String(120), index=True, unique=True, nullable=False)
#     password_hash = db.Column(db.String(128))
#     is_public = db.Column(db.Boolean, default=True)
#     is_admin = db.Column(db.Boolean, default=False)  # Add this line
#     location = db.Column(db.String(100), nullable=True)
#     profile_photo = db.Column(db.String(200), nullable=True)
#     bio = db.Column(db.Text, nullable=True)
#     availability = db.Column(db.String(50), nullable=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     # Your existing relationships and methods...

from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """User model with authentication and profile details."""
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_public = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)  # Added for admin access
    location = db.Column(db.String(100), nullable=True)
    profile_photo = db.Column(db.String(200), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    availability = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    skills_offered = db.relationship('Skill', backref='offered_by', foreign_keys='Skill.offered_by_id', lazy='dynamic')
    skills_wanted = db.relationship('Skill', backref='wanted_by', foreign_keys='Skill.wanted_by_id', lazy='dynamic')
    sent_swap_requests = db.relationship('SwapRequest', foreign_keys='SwapRequest.sender_id', backref='sender', lazy='dynamic')
    received_swap_requests = db.relationship('SwapRequest', foreign_keys='SwapRequest.receiver_id', backref='receiver', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Helper properties for template compatibility
    @property
    def name(self):
        return self.username
    
    @property
    def offered_skills(self):
        return Skill.query.filter_by(offered_by_id=self.id).all()

    @property
    def wanted_skills(self):
        return Skill.query.filter_by(wanted_by_id=self.id).all()

    def __repr__(self):
        return f'<User {self.username}>'


class Skill(db.Model):
    """Skills offered/wanted by users."""
    __tablename__ = 'skill'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    offered_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    wanted_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    availability = db.Column(db.String(100))  # e.g., "Weekends, Evenings"

    def __repr__(self):
        return f'<Skill {self.name}>'


class SwapRequest(db.Model):
    """Swap requests between users."""
    __tablename__ = 'swap_request'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # 'accepted', 'rejected', 'completed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    feedback = db.Column(db.Text)

    def __repr__(self):
        return f'<SwapRequest {self.id}: {self.sender.username} -> {self.receiver.username}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
