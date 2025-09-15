import traceback
import sys

try:
    print("=== STARTING TEST ===")
    
    # Test 1: Basic imports
    print("Testing imports...")
    import os
    print("✅ os imported")
    
    # Test 2: dotenv import  
    try:
        from dotenv import load_dotenv
        print("✅ dotenv imported")
    except ImportError as e:
        print(f"❌ dotenv import failed: {e}")
        print("Install with: pip install python-dotenv")
        sys.exit(1)
    
    # Test 3: Load .env file
    print("Loading .env file...")
    load_dotenv()
    print("✅ .env loaded")
    
    # Test 4: Check environment variables
    print("\n=== ENVIRONMENT VARIABLES ===")
    sqlalchemy_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
    local_uri = os.getenv('LOCAL_DATABASE_URI')
    
    print(f"SQLALCHEMY_DATABASE_URI: {sqlalchemy_uri}")
    print(f"LOCAL_DATABASE_URI: {local_uri}")
    
    # Test 5: Config import
    print("\n=== TESTING CONFIG IMPORT ===")
    try:
        from app.config import Config
        print("✅ Config imported successfully")
        
        config = Config()
        print(f"Final Database URI: {config.SQLALCHEMY_DATABASE_URI}")
        
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        traceback.print_exc()
    
    print("\n=== TEST COMPLETE ===")
    
except Exception as e:
    print(f"❌ CRITICAL ERROR: {e}")
    traceback.print_exc()
