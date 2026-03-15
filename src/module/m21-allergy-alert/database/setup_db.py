"""
Database setup and seed data for M21 Allergy Alert System
Streamlit Cloud + MongoDB Atlas Exclusive
"""
import sys
import streamlit as st
from datetime import datetime, date
from bson import ObjectId

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.database import DatabaseManager
from shared.models import *


def setup_atlas_database():
    """Setup MongoDB Atlas database with collections and seed data"""
    
    # Cloud-only: Get connection string from Streamlit secrets
    connection_string = None
    
    if hasattr(st, 'secrets') and 'MONGODB_URL' in st.secrets:
        connection_string = st.secrets["MONGODB_URL"]
    
    if not connection_string:
        raise ValueError(
            "MongoDB Atlas connection string required! "
            "Please add MONGODB_URL to Streamlit Cloud secrets. "
            "This system only supports Streamlit Cloud + MongoDB Atlas deployment."
        )
    
    # Validate connection string format
    if not connection_string.startswith("mongodb+srv://"):
        raise ValueError(
            "Connection string must be a MongoDB Atlas connection string starting with mongodb+srv://"
        )
    
    print(f"🔗 Connecting to MongoDB Atlas...")
    
    # Initialize database manager
    db_manager = DatabaseManager(connection_string)
    
    if not db_manager.connect():
        print("❌ Failed to connect to MongoDB Atlas")
        return False
    
    print("🗑️ Dropping existing collections...")
    collections = ["patients", "allergies", "medications", "patient_allergies", 
                  "cross_reactivity_rules", "drug_class_allergies", "alternatives", 
                  "prescriptions", "alert_log"]
    
    for collection in collections:
        try:
            db_manager.get_collection(collection).drop()
        except Exception as e:
            print(f"Warning: Could not drop collection {collection}: {e}")
    
    print("📊 Creating collections and indexes...")
    db_manager.create_indexes()
    
    print("🌱 Seeding database with test data...")
    seed_data(db_manager)
    
    print("✅ MongoDB Atlas database setup completed successfully!")
    return True


def seed_data(db_manager: DatabaseManager):
    """Insert comprehensive test data"""
    
    # Insert Patients
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
    
    db_manager.get_collection("patients").insert_many(patients_data)
    print(f"   ✓ Inserted {len(patients_data)} patients")
    
    # Insert Allergies
    allergies_data = [
        {"_id": "allergy_1", "allergy_name": "Penicillin", "allergy_type": "Drug"},
        {"_id": "allergy_2", "allergy_name": "Amoxicillin", "allergy_type": "Drug"},
        {"_id": "allergy_3", "allergy_name": "Aspirin", "allergy_type": "Drug"},
        {"_id": "allergy_4", "allergy_name": "Sulfonamides", "allergy_type": "Drug"},
        {"_id": "allergy_5", "allergy_name": "Cephalosporins", "allergy_type": "Drug"},
        {"_id": "allergy_6", "allergy_name": "NSAIDs", "allergy_type": "Drug"},
        {"_id": "allergy_7", "allergy_name": "Peanuts", "allergy_type": "Food"},
        {"_id": "allergy_8", "allergy_name": "Shellfish", "allergy_type": "Food"},
        {"_id": "allergy_9", "allergy_name": "Latex", "allergy_type": "Latex"},
        {"_id": "allergy_10", "allergy_name": "Dust Mites", "allergy_type": "Environmental"},
        {"_id": "allergy_11", "allergy_name": "Ibuprofen", "allergy_type": "Drug"},
        {"_id": "allergy_12", "allergy_name": "Codeine", "allergy_type": "Drug"}
    ]
    
    for allergy in allergies_data:
        allergy["created_at"] = datetime.now()
    
    db_manager.get_collection("allergies").insert_many(allergies_data)
    print(f"   ✓ Inserted {len(allergies_data)} allergies")
    
    # Insert Medications
    medications_data = [
        {"_id": "med_1", "med_name": "Amoxicillin", "drug_class": "Penicillin", "active_ingredients": "Amoxicillin trihydrate"},
        {"_id": "med_2", "med_name": "Penicillin V", "drug_class": "Penicillin", "active_ingredients": "Penicillin V potassium"},
        {"_id": "med_3", "med_name": "Cephalexin", "drug_class": "Cephalosporin", "active_ingredients": "Cephalexin monohydrate"},
        {"_id": "med_4", "med_name": "Cefuroxime", "drug_class": "Cephalosporin", "active_ingredients": "Cefuroxime axetil"},
        {"_id": "med_5", "med_name": "Ibuprofen", "drug_class": "NSAID", "active_ingredients": "Ibuprofen"},
        {"_id": "med_6", "med_name": "Aspirin", "drug_class": "NSAID", "active_ingredients": "Acetylsalicylic acid"},
        {"_id": "med_7", "med_name": "Naproxen", "drug_class": "NSAID", "active_ingredients": "Naproxen sodium"},
        {"_id": "med_8", "med_name": "Azithromycin", "drug_class": "Macrolide", "active_ingredients": "Azithromycin dihydrate"},
        {"_id": "med_9", "med_name": "Clarithromycin", "drug_class": "Macrolide", "active_ingredients": "Clarithromycin"},
        {"_id": "med_10", "med_name": "Trimethoprim-Sulfamethoxazole", "drug_class": "Sulfonamide", "active_ingredients": "Sulfamethoxazole, Trimethoprim"},
        {"_id": "med_11", "med_name": "Sulfadiazine", "drug_class": "Sulfonamide", "active_ingredients": "Sulfadiazine"},
        {"_id": "med_12", "med_name": "Acetaminophen", "drug_class": "Analgesic", "active_ingredients": "Paracetamol"},
        {"_id": "med_13", "med_name": "Morphine", "drug_class": "Opioid", "active_ingredients": "Morphine sulfate"},
        {"_id": "med_14", "med_name": "Codeine", "drug_class": "Opioid", "active_ingredients": "Codeine phosphate"},
        {"_id": "med_15", "med_name": "Ciprofloxacin", "drug_class": "Fluoroquinolone", "active_ingredients": "Ciprofloxacin hydrochloride"},
        {"_id": "med_16", "med_name": "Levofloxacin", "drug_class": "Fluoroquinolone", "active_ingredients": "Levofloxacin hemihydrate"}
    ]
    
    for med in medications_data:
        med["created_at"] = datetime.now()
    
    db_manager.get_collection("medications").insert_many(medications_data)
    print(f"   ✓ Inserted {len(medications_data)} medications")
    
    # Insert Patient Allergies
    patient_allergies_data = [
        # Arjun Sharma (patient_1) - allergic to Penicillin and Peanuts
        {"patient_id": "patient_1", "allergy_id": "allergy_1", "date_recorded": "2023-01-10", "notes": "Severe rash and swelling observed during previous treatment"},
        {"patient_id": "patient_1", "allergy_id": "allergy_7", "date_recorded": "2022-05-15", "notes": "Anaphylactic reaction to peanut exposure"},
        
        # Priya Singh (patient_2) - allergic to NSAIDs and Shellfish
        {"patient_id": "patient_2", "allergy_id": "allergy_6", "date_recorded": "2022-06-05", "notes": "GI distress and stomach ulcers from NSAID use"},
        {"patient_id": "patient_2", "allergy_id": "allergy_8", "date_recorded": "2021-03-20", "notes": "Hives and difficulty breathing after shellfish consumption"},
        
        # Rahul Verma (patient_3) - allergic to Sulfonamides and Ibuprofen
        {"patient_id": "patient_3", "allergy_id": "allergy_4", "date_recorded": "2024-02-20", "notes": "Anaphylaxis history with sulfonamide antibiotics"},
        {"patient_id": "patient_3", "allergy_id": "allergy_11", "date_recorded": "2023-08-10", "notes": "Severe allergic reaction to ibuprofen"},
        
        # Anita Gupta (patient_4) - allergic to Cephalosporins and Latex
        {"patient_id": "patient_4", "allergy_id": "allergy_5", "date_recorded": "2020-11-12", "notes": "Cross-reactivity concern due to penicillin allergy family history"},
        {"patient_id": "patient_4", "allergy_id": "allergy_9", "date_recorded": "2019-07-08", "notes": "Contact dermatitis from latex gloves"},
        
        # Vikram Patel (patient_5) - allergic to Codeine and Dust Mites
        {"patient_id": "patient_5", "allergy_id": "allergy_12", "date_recorded": "2023-04-18", "notes": "Respiratory depression and nausea with codeine"},
        {"patient_id": "patient_5", "allergy_id": "allergy_10", "date_recorded": "2022-01-25", "notes": "Chronic asthma triggered by dust mites"}
    ]
    
    for pa in patient_allergies_data:
        pa["_id"] = str(ObjectId())
        pa["created_at"] = datetime.now()
    
    db_manager.get_collection("patient_allergies").insert_many(patient_allergies_data)
    print(f"   ✓ Inserted {len(patient_allergies_data)} patient allergies")
    
    # Insert Cross-Reactivity Rules
    cross_reactivity_data = [
        # Penicillin allergy cross-reacts with Cephalosporins
        {"allergen_id": "allergy_1", "reactive_med_id": "med_3", "risk_level": "High", "risk_score": 0.80},
        {"allergen_id": "allergy_1", "reactive_med_id": "med_4", "risk_level": "High", "risk_score": 0.75},
        
        # NSAID cross-reactivity
        {"allergen_id": "allergy_6", "reactive_med_id": "med_5", "risk_level": "Critical", "risk_score": 0.95},
        {"allergen_id": "allergy_6", "reactive_med_id": "med_6", "risk_level": "Critical", "risk_score": 0.90},
        {"allergen_id": "allergy_6", "reactive_med_id": "med_7", "risk_level": "High", "risk_score": 0.85},
        
        # Specific drug cross-reactivities
        {"allergen_id": "allergy_3", "reactive_med_id": "med_5", "risk_level": "Medium", "risk_score": 0.60},
        {"allergen_id": "allergy_11", "reactive_med_id": "med_6", "risk_level": "High", "risk_score": 0.70},
        {"allergen_id": "allergy_11", "reactive_med_id": "med_7", "risk_level": "Medium", "risk_score": 0.55},
        
        # Sulfonamide cross-reactivity
        {"allergen_id": "allergy_4", "reactive_med_id": "med_10", "risk_level": "Critical", "risk_score": 0.95},
        {"allergen_id": "allergy_4", "reactive_med_id": "med_11", "risk_level": "High", "risk_score": 0.80},
        
        # Opioid cross-reactivity
        {"allergen_id": "allergy_12", "reactive_med_id": "med_13", "risk_level": "Medium", "risk_score": 0.65},
        
        # Lower risk cross-reactivities (below threshold)
        {"allergen_id": "allergy_1", "reactive_med_id": "med_8", "risk_level": "Low", "risk_score": 0.30},
        {"allergen_id": "allergy_5", "reactive_med_id": "med_8", "risk_level": "Low", "risk_score": 0.25}
    ]
    
    for cr in cross_reactivity_data:
        cr["_id"] = str(ObjectId())
        cr["created_at"] = datetime.now()
    
    db_manager.get_collection("cross_reactivity_rules").insert_many(cross_reactivity_data)
    print(f"   ✓ Inserted {len(cross_reactivity_data)} cross-reactivity rules")
    
    # Insert Drug Class Allergies
    drug_class_allergies_data = [
        {"drug_class": "Penicillin", "allergy_id": "allergy_1"},
        {"drug_class": "Penicillin", "allergy_id": "allergy_2"},
        {"drug_class": "Cephalosporin", "allergy_id": "allergy_5"},
        {"drug_class": "NSAID", "allergy_id": "allergy_6"},
        {"drug_class": "NSAID", "allergy_id": "allergy_3"},
        {"drug_class": "NSAID", "allergy_id": "allergy_11"},
        {"drug_class": "Sulfonamide", "allergy_id": "allergy_4"},
        {"drug_class": "Opioid", "allergy_id": "allergy_12"}
    ]
    
    for dca in drug_class_allergies_data:
        dca["_id"] = str(ObjectId())
        dca["created_at"] = datetime.now()
    
    db_manager.get_collection("drug_class_allergies").insert_many(drug_class_allergies_data)
    print(f"   ✓ Inserted {len(drug_class_allergies_data)} drug class allergies")
    
    # Insert Alternatives
    alternatives_data = [
        # Penicillin alternatives
        {"original_med_id": "med_1", "alternative_med_id": "med_8", "reason": "Macrolide antibiotic - safe for penicillin-allergic patients"},
        {"original_med_id": "med_1", "alternative_med_id": "med_9", "reason": "Alternative macrolide with similar spectrum"},
        {"original_med_id": "med_2", "alternative_med_id": "med_8", "reason": "Azithromycin as penicillin alternative"},
        {"original_med_id": "med_2", "alternative_med_id": "med_15", "reason": "Fluoroquinolone alternative for penicillin allergy"},
        
        # NSAID alternatives
        {"original_med_id": "med_5", "alternative_med_id": "med_12", "reason": "Acetaminophen for pain relief without NSAID risks"},
        {"original_med_id": "med_6", "alternative_med_id": "med_12", "reason": "Non-NSAID analgesic alternative"},
        {"original_med_id": "med_7", "alternative_med_id": "med_12", "reason": "Safer pain management option"},
        
        # Cephalosporin alternatives
        {"original_med_id": "med_3", "alternative_med_id": "med_8", "reason": "Macrolide alternative for cephalosporin allergy"},
        {"original_med_id": "med_3", "alternative_med_id": "med_15", "reason": "Fluoroquinolone as cephalosporin substitute"},
        {"original_med_id": "med_4", "alternative_med_id": "med_9", "reason": "Clarithromycin for cephalosporin-allergic patients"},
        
        # Sulfonamide alternatives
        {"original_med_id": "med_10", "alternative_med_id": "med_8", "reason": "Azithromycin instead of sulfonamide antibiotic"},
        {"original_med_id": "med_10", "alternative_med_id": "med_15", "reason": "Ciprofloxacin as sulfonamide alternative"},
        {"original_med_id": "med_11", "alternative_med_id": "med_9", "reason": "Macrolide alternative to sulfonamide"},
        
        # Opioid alternatives
        {"original_med_id": "med_14", "alternative_med_id": "med_12", "reason": "Non-opioid analgesic for codeine-allergic patients"},
        {"original_med_id": "med_13", "alternative_med_id": "med_12", "reason": "Acetaminophen for pain management"}
    ]
    
    for alt in alternatives_data:
        alt["_id"] = str(ObjectId())
        alt["created_at"] = datetime.now()
    
    db_manager.get_collection("alternatives").insert_many(alternatives_data)
    print(f"   ✓ Inserted {len(alternatives_data)} alternatives")
    
    # Insert Sample Prescriptions
    prescriptions_data = [
        # Safe prescriptions
        {"_id": "prescription_1", "patient_id": "patient_1", "med_id": "med_8", "dose": "500mg", "frequency": "Once daily", "start_date": "2026-03-15", "status": "Pending"},
        {"_id": "prescription_2", "patient_id": "patient_2", "med_id": "med_12", "dose": "500mg", "frequency": "Every 6 hours", "start_date": "2026-03-16", "status": "Pending"},
        {"_id": "prescription_3", "patient_id": "patient_5", "med_id": "med_15", "dose": "250mg", "frequency": "Twice daily", "start_date": "2026-03-17", "status": "Pending"},
        
        # Problematic prescriptions (will trigger alerts)
        {"_id": "prescription_4", "patient_id": "patient_1", "med_id": "med_1", "dose": "500mg", "frequency": "Three times daily", "start_date": "2026-03-18", "status": "Pending"},
        {"_id": "prescription_5", "patient_id": "patient_2", "med_id": "med_5", "dose": "400mg", "frequency": "Every 8 hours", "start_date": "2026-03-19", "status": "Pending"},
        {"_id": "prescription_6", "patient_id": "patient_3", "med_id": "med_10", "dose": "800mg", "frequency": "Twice daily", "start_date": "2026-03-20", "status": "Pending"},
        {"_id": "prescription_7", "patient_id": "patient_1", "med_id": "med_3", "dose": "250mg", "frequency": "Four times daily", "start_date": "2026-03-21", "status": "Pending"},
        {"_id": "prescription_8", "patient_id": "patient_4", "med_id": "med_4", "dose": "500mg", "frequency": "Twice daily", "start_date": "2026-03-22", "status": "Pending"}
    ]
    
    for prescription in prescriptions_data:
        prescription["created_at"] = datetime.now()
    
    db_manager.get_collection("prescriptions").insert_many(prescriptions_data)
    print(f"   ✓ Inserted {len(prescriptions_data)} prescriptions")
    
    print("🎯 Database seeding completed successfully!")


if __name__ == "__main__":
    setup_atlas_database()