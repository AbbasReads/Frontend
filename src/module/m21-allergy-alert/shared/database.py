"""
MongoDB Atlas database connection and utilities
Streamlit Cloud + MongoDB Atlas Exclusive
No local development support
"""
import streamlit as st
from typing import Optional, List, Dict, Any
from pymongo import MongoClient, IndexModel
from pymongo.database import Database
from pymongo.collection import Collection
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """MongoDB database manager for M21 Allergy Alert System"""
    
    def __init__(self, connection_string: str = None, database_name: str = "m21_allergy_alert"):
        # Cloud-only: Use Streamlit secrets exclusively
        if connection_string:
            self.connection_string = connection_string
        elif hasattr(st, 'secrets') and 'MONGODB_URL' in st.secrets:
            self.connection_string = st.secrets["MONGODB_URL"]
        else:
            raise ValueError(
                "MongoDB Atlas connection string required! "
                "Please add MONGODB_URL to Streamlit Cloud secrets. "
                "This system only supports Streamlit Cloud + MongoDB Atlas deployment."
            )
        
        self.database_name = database_name
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        
    def connect(self) -> bool:
        """Establish connection to MongoDB Atlas and auto-initialize if needed"""
        try:
            # Validate connection string format for Atlas
            if not self.connection_string.startswith("mongodb+srv://"):
                raise ValueError("Connection string must be a MongoDB Atlas connection string (mongodb+srv://)")
            
            self.client = MongoClient(
                self.connection_string,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=10000,         # 10 second connection timeout
                socketTimeoutMS=20000,          # 20 second socket timeout
                retryWrites=True
            )
            self.db = self.client[self.database_name]
            
            # Test connection with ping
            self.client.admin.command('ping')
            logger.info(f"✅ Connected to MongoDB Atlas: {self.database_name}")
            
            # Auto-initialize database if empty
            self._auto_initialize()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ MongoDB Atlas connection failed: {e}")
            logger.error("Please check your connection string and network access in MongoDB Atlas")
            return False
    
    def _auto_initialize(self):
        """Auto-initialize database with test data if empty"""
        try:
            # Check if database has any patients (indicator of initialization)
            patients_count = self.get_collection("patients").count_documents({})
            
            if patients_count == 0:
                logger.info("🌱 Database is empty, initializing with test data...")
                
                # Create indexes
                self.create_indexes()
                
                # Import and run seeding
                from database.setup_db import seed_data
                seed_data(self)
                
                logger.info("✅ Database auto-initialization completed!")
            else:
                logger.info(f"📊 Database already initialized with {patients_count} patients")
                
        except Exception as e:
            logger.error(f"❌ Database auto-initialization failed: {e}")
            # Don't fail the connection, just log the error
    
    def disconnect(self):
        """Close MongoDB Atlas connection"""
        if self.client:
            self.client.close()
            logger.info("🔌 MongoDB Atlas connection closed")
    
    def get_collection(self, collection_name: str) -> Collection:
        """Get MongoDB collection"""
        if self.db is None:
            raise Exception("Database not connected")
        return self.db[collection_name]
    
    def create_indexes(self):
        """Create database indexes for better performance"""
        try:
            # Patients collection indexes
            patients = self.get_collection("patients")
            patients.create_index("name")
            
            # Patient allergies indexes
            patient_allergies = self.get_collection("patient_allergies")
            patient_allergies.create_index("patient_id")
            patient_allergies.create_index("allergy_id")
            patient_allergies.create_index([("patient_id", 1), ("allergy_id", 1)], unique=True)
            
            # Medications indexes
            medications = self.get_collection("medications")
            medications.create_index("med_name", unique=True)
            medications.create_index("drug_class")
            
            # Cross-reactivity rules indexes
            cross_reactivity = self.get_collection("cross_reactivity_rules")
            cross_reactivity.create_index("allergen_id")
            cross_reactivity.create_index("reactive_med_id")
            cross_reactivity.create_index("risk_score")
            
            # Drug class allergies indexes
            drug_class_allergies = self.get_collection("drug_class_allergies")
            drug_class_allergies.create_index("drug_class")
            drug_class_allergies.create_index("allergy_id")
            
            # Prescriptions indexes
            prescriptions = self.get_collection("prescriptions")
            prescriptions.create_index("patient_id")
            prescriptions.create_index("med_id")
            prescriptions.create_index("status")
            
            # Alert log indexes
            alert_log = self.get_collection("alert_log")
            alert_log.create_index("patient_id")
            alert_log.create_index("alert_type")
            alert_log.create_index("logged_at")
            
            logger.info("✅ Database indexes created successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to create indexes: {e}")
    
    def drop_database(self):
        """Drop the entire database (use with caution)"""
        if self.client:
            self.client.drop_database(self.database_name)
            logger.info(f"🗑️ Database {self.database_name} dropped")


class AllergyCheckService:
    """Service class for allergy checking logic"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        
    def check_exact_match(self, patient_id: str, med_id: str) -> bool:
        """Check 1: Exact drug-to-allergy match"""
        try:
            # Get patient allergies
            patient_allergies = list(self.db.get_collection("patient_allergies").find(
                {"patient_id": patient_id}
            ))
            
            if not patient_allergies:
                return False
            
            # Get allergy names
            allergy_ids = [pa["allergy_id"] for pa in patient_allergies]
            allergies = list(self.db.get_collection("allergies").find(
                {"_id": {"$in": allergy_ids}}
            ))
            
            # Get medication name
            medication = self.db.get_collection("medications").find_one({"_id": med_id})
            if not medication:
                return False
            
            # Check for exact match (case-insensitive)
            med_name_lower = medication["med_name"].lower()
            for allergy in allergies:
                if allergy["allergy_name"].lower() == med_name_lower:
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error in exact match check: {e}")
            return False
    
    def check_class_match(self, patient_id: str, med_id: str) -> bool:
        """Check 2: Drug class match"""
        try:
            # Get patient allergies
            patient_allergies = list(self.db.get_collection("patient_allergies").find(
                {"patient_id": patient_id}
            ))
            
            if not patient_allergies:
                return False
            
            # Get medication drug class
            medication = self.db.get_collection("medications").find_one({"_id": med_id})
            if not medication:
                return False
            
            # Check drug class allergies
            allergy_ids = [pa["allergy_id"] for pa in patient_allergies]
            drug_class_matches = list(self.db.get_collection("drug_class_allergies").find({
                "drug_class": {"$regex": f"^{medication['drug_class']}$", "$options": "i"},
                "allergy_id": {"$in": allergy_ids}
            }))
            
            return len(drug_class_matches) > 0
            
        except Exception as e:
            logger.error(f"Error in class match check: {e}")
            return False
    
    def check_cross_reactivity(self, patient_id: str, med_id: str, threshold: float = 0.5) -> bool:
        """Check 3: Cross-reactivity above threshold"""
        try:
            # Get patient allergies
            patient_allergies = list(self.db.get_collection("patient_allergies").find(
                {"patient_id": patient_id}
            ))
            
            if not patient_allergies:
                return False
            
            # Check cross-reactivity rules
            allergy_ids = [pa["allergy_id"] for pa in patient_allergies]
            cross_reactivity_matches = list(self.db.get_collection("cross_reactivity_rules").find({
                "allergen_id": {"$in": allergy_ids},
                "reactive_med_id": med_id,
                "risk_score": {"$gt": threshold}
            }))
            
            return len(cross_reactivity_matches) > 0
            
        except Exception as e:
            logger.error(f"Error in cross-reactivity check: {e}")
            return False
    
    def get_alternatives(self, med_id: str) -> List[Dict[str, Any]]:
        """Get safe alternatives for a medication"""
        try:
            alternatives = list(self.db.get_collection("alternatives").find(
                {"original_med_id": med_id}
            ))
            
            result = []
            for alt in alternatives:
                # Get alternative medication details
                alt_med = self.db.get_collection("medications").find_one(
                    {"_id": alt["alternative_med_id"]}
                )
                if alt_med:
                    result.append({
                        "med_name": alt_med["med_name"],
                        "drug_class": alt_med["drug_class"],
                        "reason": alt.get("reason", "Safe alternative")
                    })
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting alternatives: {e}")
            return []
    
    def perform_full_check(self, patient_id: str, med_id: str, prescription_id: str) -> Dict[str, Any]:
        """Perform complete 3-level allergy check"""
        try:
            # Get medication name for messages
            medication = self.db.get_collection("medications").find_one({"_id": med_id})
            med_name = medication["med_name"] if medication else "Unknown"
            
            # Check 1: Exact Match
            if self.check_exact_match(patient_id, med_id):
                result = {
                    "status": "ALERT",
                    "alert_type": "EXACT_MATCH",
                    "message": f"EXACT MATCH: Patient is directly allergic to {med_name}.",
                    "alternatives": self.get_alternatives(med_id)
                }
                self._log_alert(prescription_id, patient_id, med_id, "EXACT_MATCH", result["message"])
                return result
            
            # Check 2: Class Match
            if self.check_class_match(patient_id, med_id):
                result = {
                    "status": "ALERT",
                    "alert_type": "CLASS_MATCH",
                    "message": f"CLASS MATCH: {med_name} belongs to an allergenic drug class for this patient.",
                    "alternatives": self.get_alternatives(med_id)
                }
                self._log_alert(prescription_id, patient_id, med_id, "CLASS_MATCH", result["message"])
                return result
            
            # Check 3: Cross-Reactivity
            if self.check_cross_reactivity(patient_id, med_id):
                result = {
                    "status": "ALERT",
                    "alert_type": "CROSS_REACTIVITY",
                    "message": f"CROSS-REACTIVITY: High cross-reactivity risk detected for {med_name}.",
                    "alternatives": self.get_alternatives(med_id)
                }
                self._log_alert(prescription_id, patient_id, med_id, "CROSS_REACTIVITY", result["message"])
                return result
            
            # All checks passed
            result = {
                "status": "SAFE",
                "alert_type": "SAFE",
                "message": f"No allergy conflicts detected. {med_name} is safe for this patient.",
                "alternatives": []
            }
            self._log_alert(prescription_id, patient_id, med_id, "SAFE", result["message"])
            return result
            
        except Exception as e:
            logger.error(f"Error in full allergy check: {e}")
            return {
                "status": "ERROR",
                "alert_type": None,
                "message": f"Error performing allergy check: {str(e)}",
                "alternatives": []
            }
    
    def _log_alert(self, prescription_id: str, patient_id: str, med_id: str, alert_type: str, message: str):
        """Log alert to database"""
        try:
            alert_log = {
                "prescription_id": prescription_id,
                "patient_id": patient_id,
                "med_id": med_id,
                "alert_type": alert_type,
                "alert_message": message,
                "logged_at": datetime.now()
            }
            
            self.db.get_collection("alert_log").insert_one(alert_log)
            
            # Update prescription status based on alert type
            if alert_type in ["EXACT_MATCH", "CLASS_MATCH", "CROSS_REACTIVITY"]:
                status = "Rejected"
            elif alert_type == "SAFE":
                status = "Approved"
            else:
                status = "Pending"
            
            self.db.get_collection("prescriptions").update_one(
                {"_id": prescription_id},
                {"$set": {"status": status}}
            )
            
        except Exception as e:
            logger.error(f"Error logging alert: {e}")


# Global database manager instance
db_manager = DatabaseManager()
allergy_service = AllergyCheckService(db_manager)