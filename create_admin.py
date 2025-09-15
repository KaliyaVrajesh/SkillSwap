import sys
from os.path import abspath, dirname

sys.path.insert(0, dirname(abspath(__file__)))

from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Make Gamexvrajesh admin
    user = User.query.filter_by(username='Gamexvrajesh').first()
    
    if user:
        user.is_admin = True
        db.session.commit()
        print(f"✅ {user.username} is now admin!")
    else:
        print("❌ User not found!")
    
    # Also create admin user
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@skillswap.com',
            is_admin=True,
            is_public=False
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created!")
