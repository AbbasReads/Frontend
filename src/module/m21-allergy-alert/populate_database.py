#!/usr/bin/env python3
"""
Standalone script to populate MongoDB Atlas with M21 Allergy Alert System data
Run this script to fill your database with comprehensive test data
"""

import sys
import os
from datetime import datetime, date
from bson import ObjectId

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def populate_database():
    """Populate MongoDB Atlas with comprehensive test data"""
    
    print("🚀 M21 Database Population Script")
    print("=" * 50)
    
    # Get MongoDB connection string
    connection_string = input("Enter your MongoDB Atlas connection string: ").strip()
    
    if not connection_string:
        print("❌ Connection string is required!")
        return False
    
    # Validate connection string
    if not connection_string.startswith("mongodb+srv://"):
        print("❌ Please use a MongoDB Atlas connection string (mongodb+srv://)")
        return False
    
    # Add database name if not present
    if "/m21_allergy_alert" not in connection_string:
        if "?" in connection_string:
            connection_string = connection_string.replace("?", "/m21_allergy_alert?")
        else:
            connection_string += "/m21_allergy_alert"
    
    print(f"🔗 Connecting to MongoDB Atlas...")
    
    try:
        from pymongo import MongoClient
        
        # Connect to MongoDB
        client = MongoClient(
            connection_string,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=20000,
            socketTimeoutMS=30000,
            retryWrites=True
        )
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas successfully!")
        
        # Get database
        db = client["m21_allergy_alert"]
        
        # Drop existing collections
        print("🗑️ Clearing existing data...")
        collections = ["patients", "allergies", "medications", "patient_allergies", 
                      "cross_reactivity_rules", "drug_class_allergies", "alternatives", 
                      "prescriptions", "alert_log"]
        
        for collection in collections:
            try:
                db[collection].drop()
                print(f"   ✓ Dropped {collection}")
            except Exception as e:
                print(f"   ⚠️ Could not drop {collection}: {e}")
        
        print("🌱 Populating database with test data...")
        
        # 1. Insert Patients
        patients_data = [
            {
                "_id": "patient_1",
                "name": "Arjun Sharma",
                "dob": "1990-05-10",
                "sex": "M",
                "created_at": datetime.now()
            },
            {
                "_id": "patient_2", 
                "name": "Priya Singh",
                "dob": "1985-11-22",
                "sex": "F",
                "created_at": datetime.now()
            },
            {
                "_id": "patient_3",
                "name": "Rahul Verma", 
                "dob": "2001-03-15",
                "sex": "M",
                "created_at": datetime.now()
            },
            {
                "_id": "patient_4",
                "name": "Anita Gupta",
                "dob": "1978-08-30",
                "sex": "F", 
                "created_at": datetime.now()
            },
            {
                "_id": "patient_5",
                "name": "Vikram Patel",
                "dob": "1995-12-05",
                "sex": "M",
                "created_at": datetime.now()
            }
        ]
        
        db.patients.insert_many(patients_data)
        print(f"   ✓ Inserted {len(patients_data)} patients")
        
        # 2. Insert Allergies
        allergies_data = [
            {"_id": "allergy_1", "allergy_name": "Penicillin", "allergy_type": "Drug", "created_at": datetime.now()},
            {"_id": "allergy_2", "allergy_name": "Amoxicillin", "allergy_type": "Drug", "created_at": datetime.now()},
            {"_id": "allergy_3", "allergy_name": "Aspirin", "allergy_type": "Drug", "created_at": datetime.now()},
            {"_id": "allergy_4", "allergy_name": "Sulfonamides", "allergy_type": "Drug", "created_at": datetime.now()},
            {"_id": "allergy_5", "allergy_name": "Cephalosporins", "allergy_type": "Drug", "created_at": datetime.now()},
            {"_id": "allergy_6", "allergy_name": "NSAIDs", "allergy_type": "Drug", "created_at": datetime.now()},
            {"_id": "allergy_7", "allergy_name": "Peanuts", "allergy_type": "Food", "created_at": datetime.now()},
            {"_id": "allergy_8", "allergy_name": "Shellfish", "allergy_type": "Food", "created_at": datetime.now()},
            {"_id": "allergy_9", "allergy_name": "Latex", "allergy_type": "Latex", "created_at": datetime.now()},
            {"_id": "allergy_10", "allergy_name": "Dust Mites", "allergy_type": "Environmental", "created_at": datetime.now()},
            {"_id": "allergy_11", "allergy_name": "Ibuprofen", "allergy_type": "Drug", "created_at": datetime.now()},
            {"_id": "allergy_12", "allergy_name": "Codeine", "allergy_type": "Drug", "created_at": datetime.now()}
        ]
        
        db.allergies.insert_many(allergies_data)
        print(f"   ✓ Inserted {len(allergies_data)} allergies")
        
        # 3. Insert Medications
        medications_data = [
            {"_id": "med_1", "med_name": "Amoxicillin", "drug_class": "Penicillin", "active_ingredients": "Amoxicillin trihydrate", "created_at": datetime.now()},
            {"_id": "med_2", "med_name": "Penicillin V", "drug_class": "Penicillin", "active_ingredients": "Penicillin V potassium", "created_at": datetime.now()},
            {"_id": "med_3", "med_name": "Cephalexin", "drug_class": "Cephalosporin", "active_ingredients": "Cephalexin monohydrate", "created_at": datetime.now()},
            {"_id": "med_4", "med_name": "Cefuroxime", "drug_class": "Cephalosporin", "active_ingredients": "Cefuroxime axetil", "created_at": datetime.now()},
            {"_id": "med_5", "med_name": "Ibuprofen", "drug_class": "NSAID", "active_ingredients": "Ibuprofen", "created_at": datetime.now()},
            {"_id": "med_6", "med_name": "Aspirin", "drug_class": "NSAID", "active_ingredients": "Acetylsalicylic acid", "created_at": datetime.now()},
            {"_id": "med_7", "med_name": "Naproxen", "drug_class": "NSAID", "active_ingredients": "Naproxen sodium", "created_at": datetime.now()},
            {"_id": "med_8", "med_name": "Azithromycin", "drug_class": "Macrolide", "active_ingredients": "Azithromycin dihydrate", "created_at": datetime.now()},
            {"_id": "med_9", "med_name": "Clarithromycin", "drug_class": "Macrolide", "active_ingredients": "Clarithromycin", "created_at": datetime.now()},
            {"_id": "med_10", "med_name": "Trimethoprim-Sulfamethoxazole", "drug_class": "Sulfonamide", "active_ingredients": "Sulfamethoxazole, Trimethoprim", "created_at": datetime.now()},
            {"_id": "med_11", "med_name": "Sulfadiazine", "drug_class": "Sulfonamide", "active_ingredients": "Sulfadiazine", "created_at": datetime.now()},
            {"_id": "med_12", "med_name": "Acetaminophen", "drug_class": "Analgesic", "active_ingredients": "Paracetamol", "created_at": datetime.now()},
            {"_id": "med_13", "med_name": "Morphine", "drug_class": "Opioid", "active_ingredients": "Morphine sulfate", "created_at": datetime.now()},
            {"_id": "med_14", "med_name": "Codeine", "drug_class": "Opioid", "active_ingredients": "Codeine phosphate", "created_at": datetime.now()},
            {"_id": "med_15", "med_name": "Ciprofloxacin", "drug_class": "Fluoroquinolone", "active_ingredients": "Ciprofloxacin hydrochloride", "created_at": datetime.now()},
            {"_id": "med_16", "med_name": "Levofloxacin", "drug_class": "Fluoroquinolone", "active_ingredients": "Levofloxacin hemihydrate", "created_at": datetime.now()}
        ]
        
        db.medications.insert_many(medications_data)
        print(f"   ✓ Inserted {len(medications_data)} medications")
        
        # 4. Insert Patient Allergies
        patient_allergies_data = [
            # Arjun Sharma (patient_1) - allergic to Penicillin and Peanuts
            {"_id": str(ObjectId()), "patient_id": "patient_1", "allergy_id": "allergy_1", "date_recorded": "2023-01-10", "notes": "Severe rash and swelling observed during previous treatment", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "patient_id": "patient_1", "allergy_id": "allergy_7", "date_recorded": "2022-05-15", "notes": "Anaphylactic reaction to peanut exposure", "created_at": datetime.now()},
            
            # Priya Singh (patient_2) - allergic to NSAIDs and Shellfish
            {"_id": str(ObjectId()), "patient_id": "patient_2", "allergy_id": "allergy_6", "date_recorded": "2022-06-05", "notes": "GI distress and stomach ulcers from NSAID use", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "patient_id": "patient_2", "allergy_id": "allergy_8", "date_recorded": "2021-03-20", "notes": "Hives and difficulty breathing after shellfish consumption", "created_at": datetime.now()},
            
            # Rahul Verma (patient_3) - allergic to Sulfonamides and Ibuprofen
            {"_id": str(ObjectId()), "patient_id": "patient_3", "allergy_id": "allergy_4", "date_recorded": "2024-02-20", "notes": "Anaphylaxis history with sulfonamide antibiotics", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "patient_id": "patient_3", "allergy_id": "allergy_11", "date_recorded": "2023-08-10", "notes": "Severe allergic reaction to ibuprofen", "created_at": datetime.now()},
            
            # Anita Gupta (patient_4) - allergic to Cephalosporins and Latex
            {"_id": str(ObjectId()), "patient_id": "patient_4", "allergy_id": "allergy_5", "date_recorded": "2020-11-12", "notes": "Cross-reactivity concern due to penicillin allergy family history", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "patient_id": "patient_4", "allergy_id": "allergy_9", "date_recorded": "2019-07-08", "notes": "Contact dermatitis from latex gloves", "created_at": datetime.now()},
            
            # Vikram Patel (patient_5) - allergic to Codeine and Dust Mites
            {"_id": str(ObjectId()), "patient_id": "patient_5", "allergy_id": "allergy_12", "date_recorded": "2023-04-18", "notes": "Respiratory depression and nausea with codeine", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "patient_id": "patient_5", "allergy_id": "allergy_10", "date_recorded": "2022-01-25", "notes": "Chronic asthma triggered by dust mites", "created_at": datetime.now()}
        ]
        
        db.patient_allergies.insert_many(patient_allergies_data)
        print(f"   ✓ Inserted {len(patient_allergies_data)} patient allergies")
        
        # 5. Insert Cross-Reactivity Rules
        cross_reactivity_data = [
            # Penicillin allergy cross-reacts with Cephalosporins
            {"_id": str(ObjectId()), "allergen_id": "allergy_1", "reactive_med_id": "med_3", "risk_level": "High", "risk_score": 0.80, "created_at": datetime.now()},
            {"_id": str(ObjectId()), "allergen_id": "allergy_1", "reactive_med_id": "med_4", "risk_level": "High", "risk_score": 0.75, "created_at": datetime.now()},
            
            # NSAID cross-reactivity
            {"_id": str(ObjectId()), "allergen_id": "allergy_6", "reactive_med_id": "med_5", "risk_level": "Critical", "risk_score": 0.95, "created_at": datetime.now()},
            {"_id": str(ObjectId()), "allergen_id": "allergy_6", "reactive_med_id": "med_6", "risk_level": "Critical", "risk_score": 0.90, "created_at": datetime.now()},
            {"_id": str(ObjectId()), "allergen_id": "allergy_6", "reactive_med_id": "med_7", "risk_level": "High", "risk_score": 0.85, "created_at": datetime.now()},
            
            # Specific drug cross-reactivities
            {"_id": str(ObjectId()), "allergen_id": "allergy_3", "reactive_med_id": "med_5", "risk_level": "Medium", "risk_score": 0.60, "created_at": datetime.now()},
            {"_id": str(ObjectId()), "allergen_id": "allergy_11", "reactive_med_id": "med_6", "risk_level": "High", "risk_score": 0.70, "created_at": datetime.now()},
            {"_id": str(ObjectId()), "allergen_id": "allergy_11", "reactive_med_id": "med_7", "risk_level": "Medium", "risk_score": 0.55, "created_at": datetime.now()},
            
            # Sulfonamide cross-reactivity
            {"_id": str(ObjectId()), "allergen_id": "allergy_4", "reactive_med_id": "med_10", "risk_level": "Critical", "risk_score": 0.95, "created_at": datetime.now()},
            {"_id": str(ObjectId()), "allergen_id": "allergy_4", "reactive_med_id": "med_11", "risk_level": "High", "risk_score": 0.80, "created_at": datetime.now()},
            
            # Opioid cross-reactivity
            {"_id": str(ObjectId()), "allergen_id": "allergy_12", "reactive_med_id": "med_13", "risk_level": "Medium", "risk_score": 0.65, "created_at": datetime.now()},
            
            # Lower risk cross-reactivities (below threshold)
            {"_id": str(ObjectId()), "allergen_id": "allergy_1", "reactive_med_id": "med_8", "risk_level": "Low", "risk_score": 0.30, "created_at": datetime.now()},
            {"_id": str(ObjectId()), "allergen_id": "allergy_5", "reactive_med_id": "med_8", "risk_level": "Low", "risk_score": 0.25, "created_at": datetime.now()}
        ]
        
        db.cross_reactivity_rules.insert_many(cross_reactivity_data)
        print(f"   ✓ Inserted {len(cross_reactivity_data)} cross-reactivity rules")
        
        # 6. Insert Drug Class Allergies
        drug_class_allergies_data = [
            {"_id": str(ObjectId()), "drug_class": "Penicillin", "allergy_id": "allergy_1", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "drug_class": "Penicillin", "allergy_id": "allergy_2", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "drug_class": "Cephalosporin", "allergy_id": "allergy_5", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "drug_class": "NSAID", "allergy_id": "allergy_6", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "drug_class": "NSAID", "allergy_id": "allergy_3", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "drug_class": "NSAID", "allergy_id": "allergy_11", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "drug_class": "Sulfonamide", "allergy_id": "allergy_4", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "drug_class": "Opioid", "allergy_id": "allergy_12", "created_at": datetime.now()}
        ]
        
        db.drug_class_allergies.insert_many(drug_class_allergies_data)
        print(f"   ✓ Inserted {len(drug_class_allergies_data)} drug class allergies")
        
        # 7. Insert Alternatives
        alternatives_data = [
            # Penicillin alternatives
            {"_id": str(ObjectId()), "original_med_id": "med_1", "alternative_med_id": "med_8", "reason": "Macrolide antibiotic - safe for penicillin-allergic patients", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "original_med_id": "med_1", "alternative_med_id": "med_9", "reason": "Alternative macrolide with similar spectrum", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "original_med_id": "med_2", "alternative_med_id": "med_8", "reason": "Azithromycin as penicillin alternative", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "original_med_id": "med_2", "alternative_med_id": "med_15", "reason": "Fluoroquinolone alternative for penicillin allergy", "created_at": datetime.now()},
            
            # NSAID alternatives
            {"_id": str(ObjectId()), "original_med_id": "med_5", "alternative_med_id": "med_12", "reason": "Acetaminophen for pain relief without NSAID risks", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "original_med_id": "med_6", "alternative_med_id": "med_12", "reason": "Non-NSAID analgesic alternative", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "original_med_id": "med_7", "alternative_med_id": "med_12", "reason": "Safer pain management option", "created_at": datetime.now()},
            
            # Cephalosporin alternatives
            {"_id": str(ObjectId()), "original_med_id": "med_3", "alternative_med_id": "med_8", "reason": "Macrolide alternative for cephalosporin allergy", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "original_med_id": "med_3", "alternative_med_id": "med_15", "reason": "Fluoroquinolone as cephalosporin substitute", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "original_med_id": "med_4", "alternative_med_id": "med_9", "reason": "Clarithromycin for cephalosporin-allergic patients", "created_at": datetime.now()},
            
            # Sulfonamide alternatives
            {"_id": str(ObjectId()), "original_med_id": "med_10", "alternative_med_id": "med_8", "reason": "Azithromycin instead of sulfonamide antibiotic", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "original_med_id": "med_10", "alternative_med_id": "med_15", "reason": "Ciprofloxacin as sulfonamide alternative", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "original_med_id": "med_11", "alternative_med_id": "med_9", "reason": "Macrolide alternative to sulfonamide", "created_at": datetime.now()},
            
            # Opioid alternatives
            {"_id": str(ObjectId()), "original_med_id": "med_14", "alternative_med_id": "med_12", "reason": "Non-opioid analgesic for codeine-allergic patients", "created_at": datetime.now()},
            {"_id": str(ObjectId()), "original_med_id": "med_13", "alternative_med_id": "med_12", "reason": "Acetaminophen for pain management", "created_at": datetime.now()}
        ]
        
        db.alternatives.insert_many(alternatives_data)
        print(f"   ✓ Inserted {len(alternatives_data)} alternatives")
        
        # 8. Insert Sample Prescriptions
        prescriptions_data = [
            # Safe prescriptions
            {"_id": "prescription_1", "patient_id": "patient_1", "med_id": "med_8", "dose": "500mg", "frequency": "Once daily", "start_date": "2026-03-15", "status": "Pending", "created_at": datetime.now()},
            {"_id": "prescription_2", "patient_id": "patient_2", "med_id": "med_12", "dose": "500mg", "frequency": "Every 6 hours", "start_date": "2026-03-16", "status": "Pending", "created_at": datetime.now()},
            {"_id": "prescription_3", "patient_id": "patient_5", "med_id": "med_15", "dose": "250mg", "frequency": "Twice daily", "start_date": "2026-03-17", "status": "Pending", "created_at": datetime.now()},
            
            # Problematic prescriptions (will trigger alerts)
            {"_id": "prescription_4", "patient_id": "patient_1", "med_id": "med_1", "dose": "500mg", "frequency": "Three times daily", "start_date": "2026-03-18", "status": "Pending", "created_at": datetime.now()},
            {"_id": "prescription_5", "patient_id": "patient_2", "med_id": "med_5", "dose": "400mg", "frequency": "Every 8 hours", "start_date": "2026-03-19", "status": "Pending", "created_at": datetime.now()},
            {"_id": "prescription_6", "patient_id": "patient_3", "med_id": "med_10", "dose": "800mg", "frequency": "Twice daily", "start_date": "2026-03-20", "status": "Pending", "created_at": datetime.now()},
            {"_id": "prescription_7", "patient_id": "patient_1", "med_id": "med_3", "dose": "250mg", "frequency": "Four times daily", "start_date": "2026-03-21", "status": "Pending", "created_at": datetime.now()},
            {"_id": "prescription_8", "patient_id": "patient_4", "med_id": "med_4", "dose": "500mg", "frequency": "Twice daily", "start_date": "2026-03-22", "status": "Pending", "created_at": datetime.now()}
        ]
        
        db.prescriptions.insert_many(prescriptions_data)
        print(f"   ✓ Inserted {len(prescriptions_data)} prescriptions")
        
        # 9. Create indexes for better performance
        print("📊 Creating database indexes...")
        
        # Patients collection indexes
        db.patients.create_index("name")
        
        # Patient allergies indexes
        db.patient_allergies.create_index("patient_id")
        db.patient_allergies.create_index("allergy_id")
        db.patient_allergies.create_index([("patient_id", 1), ("allergy_id", 1)], unique=True)
        
        # Medications indexes
        db.medications.create_index("med_name", unique=True)
        db.medications.create_index("drug_class")
        
        # Cross-reactivity rules indexes
        db.cross_reactivity_rules.create_index("allergen_id")
        db.cross_reactivity_rules.create_index("reactive_med_id")
        db.cross_reactivity_rules.create_index("risk_score")
        
        # Drug class allergies indexes
        db.drug_class_allergies.create_index("drug_class")
        db.drug_class_allergies.create_index("allergy_id")
        
        # Prescriptions indexes
        db.prescriptions.create_index("patient_id")
        db.prescriptions.create_index("med_id")
        db.prescriptions.create_index("status")
        
        # Alert log indexes
        db.alert_log.create_index("patient_id")
        db.alert_log.create_index("alert_type")
        db.alert_log.create_index("logged_at")
        
        print("   ✓ Created database indexes")
        
        # Close connection
        client.close()
        
        print("\n🎉 DATABASE POPULATION COMPLETED!")
        print("=" * 50)
        print("✅ Successfully populated MongoDB Atlas with:")
        print(f"   • {len(patients_data)} Patients with diverse profiles")
        print(f"   • {len(allergies_data)} Allergies (drugs, food, environmental)")
        print(f"   • {len(medications_data)} Medications across 6 drug classes")
        print(f"   • {len(patient_allergies_data)} Patient-allergy relationships")
        print(f"   • {len(cross_reactivity_data)} Cross-reactivity rules")
        print(f"   • {len(drug_class_allergies_data)} Drug class mappings")
        print(f"   • {len(alternatives_data)} Safe medication alternatives")
        print(f"   • {len(prescriptions_data)} Sample prescriptions")
        print("   • Complete database indexes for performance")
        print("\n🚀 Your M21 Allergy Alert System is ready to use!")
        print("   Visit your Streamlit app to test the functionality.")
        
        return True
        
    except ImportError:
        print("❌ pymongo not installed. Install it with: pip install pymongo")
        return False
    except Exception as e:
        print(f"❌ Error populating database: {e}")
        return False


if __name__ == "__main__":
    print("🏥 M21 Allergy Alert System - Database Population Script")
    print("This script will populate your MongoDB Atlas cluster with comprehensive test data.")
    print()
    
    # Check if pymongo is available
    try:
        import pymongo
        print(f"✅ pymongo version {pymongo.version} detected")
    except ImportError:
        print("❌ pymongo not found. Please install it first:")
        print("   pip install pymongo")
        sys.exit(1)
    
    print()
    print("📋 What this script will create:")
    print("   • 5 Test patients with varied allergy profiles")
    print("   • 12 Different allergies (drugs, food, environmental)")
    print("   • 16 Medications across 6 drug classes")
    print("   • Complex allergy relationships and cross-reactivity rules")
    print("   • Safe medication alternatives")
    print("   • Sample prescriptions for testing")
    print()
    
    confirm = input("Continue with database population? (y/N): ").strip().lower()
    if confirm in ['y', 'yes']:
        success = populate_database()
        if success:
            print("\n🎯 Next Steps:")
            print("1. Visit your Streamlit app")
            print("2. Check that sidebar shows 'Database Connected'")
            print("3. Go to Statistics page to verify data counts")
            print("4. Test the Prescription Validator with the test patients")
        sys.exit(0 if success else 1)
    else:
        print("❌ Database population cancelled.")
        sys.exit(0)