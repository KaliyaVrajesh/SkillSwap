import os
from app import create_app, db


app = create_app()

if __name__ == '__main__':
    # Ensure instance directory exists
    os.makedirs('instance', exist_ok=True)
    
    # Create database tables within app context
    with app.app_context():
        try:
            # Force absolute path for SQLite
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            print(f"🔍 Using database: {db_uri}")
            
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"❌ Database creation failed: {e}")
            print("App will still start - database will be created on first request")
    
    print("🚀 Starting Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=True)
