#!/usr/bin/env python3
"""
Setup script for M21 Allergy Alert System
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_mongodb():
    """Check if MongoDB is running"""
    try:
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        print("✅ MongoDB is running and accessible")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("Please ensure MongoDB is installed and running:")
        print("  - Install: https://docs.mongodb.com/manual/installation/")
        print("  - Start: mongod")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    # Check if we're in a virtual environment
    if sys.prefix == sys.base_prefix:
        print("⚠️  Warning: Not in a virtual environment")
        print("Consider creating one: python -m venv venv && source venv/bin/activate")
    
    # Install requirements
    if run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing dependencies"):
        return True
    else:
        print("Try upgrading pip: python -m pip install --upgrade pip")
        return False

def setup_database():
    """Setup MongoDB database"""
    print("🗄️ Setting up MongoDB database...")
    
    # Change to database directory and run setup
    original_dir = os.getcwd()
    try:
        os.chdir("database")
        if run_command(f"{sys.executable} setup_db.py", "Setting up database"):
            return True
        else:
            return False
    finally:
        os.chdir(original_dir)

def main():
    """Main setup function"""
    print("🏥 M21 Allergy Alert System Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check MongoDB
    if not check_mongodb():
        print("\n🔧 MongoDB Setup Instructions:")
        print("1. Install MongoDB: https://docs.mongodb.com/manual/installation/")
        print("2. Start MongoDB service:")
        print("   - macOS: brew services start mongodb-community")
        print("   - Linux: sudo systemctl start mongod")
        print("   - Windows: Start MongoDB service from Services")
        print("3. Run this setup script again")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("❌ Failed to setup database")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n🚀 Next steps:")
    print("1. Start the backend API:")
    print("   cd backend && python -m uvicorn main:app --reload")
    print("\n2. Start the Streamlit frontend:")
    print("   cd frontend && streamlit run app.py")
    print("\n3. Open your browser to:")
    print("   - Frontend: http://localhost:8501")
    print("   - API Docs: http://localhost:8000/docs")
    
    print("\n📚 Additional Information:")
    print("- API Base URL: http://localhost:8000")
    print("- MongoDB Database: m21_allergy_alert")
    print("- Documentation: docs/REPORT.md")

if __name__ == "__main__":
    main()