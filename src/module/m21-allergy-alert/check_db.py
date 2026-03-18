"""
Quick database check script
"""
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from shared.database import db_manager

print("Connecting to database...")
if db_manager.connect():
    print("✅ Database connected successfully!")
    
    # Check collections
    collections = db_manager.db.list_collection_names()
    print(f"\n📊 Collections found: {len(collections)}")
    for coll in collections:
        count = db_manager.get_collection(coll).count_documents({})
        print(f"  - {coll}: {count} documents")
    
    # Check patients
    print("\n👥 Patients:")
    patients = list(db_manager.get_collection("patients").find())
    for p in patients:
        print(f"  - {p['_id']}: {p['name']}")
    
    # Check patient allergies
    print("\n🚨 Patient Allergies:")
    patient_allergies = list(db_manager.get_collection("patient_allergies").find())
    for pa in patient_allergies:
        print(f"  - Patient: {pa['patient_id']}, Allergy: {pa['allergy_id']}")
    
    print("\n✅ Database check complete!")
else:
    print("❌ Database connection failed!")
