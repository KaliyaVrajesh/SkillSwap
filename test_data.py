import sys
from os.path import abspath, dirname

sys.path.insert(0, dirname(abspath(__file__)))

from app import create_app, db
from app.models import User, Skill, SwapRequest

app = create_app()

with app.app_context():
    # Create test user
    test_user = User(
        username='testuser',
        email='test@example.com',
        is_admin=False,
        location='Test City'
    )
    test_user.set_password('password123')
    
    db.session.add(test_user)
    db.session.commit()
    
    # Create test skill
    test_skill = Skill(
        name='Python Programming',
        offered_by_id=test_user.id
    )
    
    db.session.add(test_skill)
    db.session.commit()
    
    print("✅ Test data created!")
    print("Now check your admin panel - it should show data!")
