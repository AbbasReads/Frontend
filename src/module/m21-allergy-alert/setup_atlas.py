#!/usr/bin/env python3
"""
Setup script for MongoDB Atlas deployment
"""
import streamlit as st
from shared.database import DatabaseManager
from database.setup_db import seed_data
import sys

def setup_atlas_database():
    """Setup MongoDB Atlas database with collections and seed data"""
    
    st.write("🔗 Connecting to MongoDB Atlas...")
    
    # Get connection string from Streamlit secrets
    if 'MONGODB_URL' not in st.secrets:
        st.error("❌ MongoDB connection string not found in secrets!")
        st.write("Please add your MongoDB Atlas connection string to Streamlit secrets:")
        st.code('MONGODB_URL = "mongodb+srv://username:password@cluster.mongodb.net/m21_allergy_alert?retryWrites=true&w=majority"')
        return False
    
    # Initialize database manager with Atlas connection
    db_manager = DatabaseManager(st.secrets["MONGODB_URL"])
    
    if not db_manager.connect():
        st.error("❌ Failed to connect to MongoDB Atlas")
        return False
    
    st.success("✅ Connected to MongoDB Atlas")
    
    # Check if database already has data
    existing_patients = db_manager.get_collection("patients").count_documents({})
    
    if existing_patients > 0:
        st.info(f"📊 Database already contains {existing_patients} patients")
        if st.button("🔄 Reset and Reseed Database"):
            st.write("🗑️ Dropping existing collections...")
            collections = ["patients", "allergies", "medications", "patient_allergies", 
                         "cross_reactivity_rules", "drug_class_allergies", "alternatives", 
                         "prescriptions", "alert_log"]
            
            for collection in collections:
                db_manager.get_collection(collection).drop()
            
            st.write("🌱 Seeding database with fresh data...")
            seed_data(db_manager)
            st.success("✅ Database reset and seeded successfully!")
    else:
        st.write("📊 Creating collections and indexes...")
        db_manager.create_indexes()
        
        st.write("🌱 Seeding database with test data...")
        seed_data(db_manager)
        st.success("✅ Database setup completed successfully!")
    
    # Display database stats
    st.write("📈 Database Statistics:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        patients_count = db_manager.get_collection("patients").count_documents({})
        st.metric("Patients", patients_count)
    
    with col2:
        medications_count = db_manager.get_collection("medications").count_documents({})
        st.metric("Medications", medications_count)
    
    with col3:
        allergies_count = db_manager.get_collection("allergies").count_documents({})
        st.metric("Allergies", allergies_count)
    
    return True

if __name__ == "__main__":
    st.title("🏥 M21 Atlas Database Setup")
    st.write("This tool helps you set up your MongoDB Atlas database for the M21 Allergy Alert System.")
    
    if st.button("🚀 Setup Database"):
        setup_atlas_database()