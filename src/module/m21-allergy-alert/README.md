# Module 21: Allergy-Aware Medication Alert System

**Technology Stack:** Python • Streamlit • MongoDB Atlas  
**Deployment:** Streamlit Cloud Ready

## Overview

This module implements an Allergy-Aware Medication Alert System using Python, Streamlit, and MongoDB. The system is optimized for cloud deployment on Streamlit Cloud with MongoDB Atlas.

### Key Features
- **3-Level Cascade Checking:** Exact Match → Drug Class → Cross-Reactivity
- **Interactive Dashboard:** 5 comprehensive pages built with Streamlit
- **Cloud-Ready:** Optimized for Streamlit Cloud and MongoDB Atlas
- **Real-time Validation:** Instant allergy checking with visual feedback
- **Comprehensive Data:** 5 patients, 16 medications, 12 allergies with test scenarios

## 🚀 Quick Deployment

### For Streamlit Cloud + MongoDB Atlas:

1. **Setup MongoDB Atlas:**
   - Create free cluster at [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Get connection string
   - Configure network access (0.0.0.0/0 for Streamlit Cloud)

2. **Deploy to Streamlit Cloud:**
   - Push to GitHub
   - Deploy at [share.streamlit.io](https://share.streamlit.io)
   - Set main file: `src/module/m21-allergy-alert/streamlit_app.py`
   - Add MongoDB connection string to Streamlit secrets:
     ```toml
     MONGODB_URL = "mongodb+srv://username:password@cluster.mongodb.net/m21_allergy_alert?retryWrites=true&w=majority"
     ```

3. **Initialize Database:**
   - Run the setup tool in your deployed app
   - Creates all collections and seeds test data

### For Local Development:

```bash
# Install dependencies
pip install -r requirements.txt

# Start MongoDB locally
mongod

# Setup database
python database/setup_db.py

# Run Streamlit app
streamlit run streamlit_app.py
```

## 📁 Project Structure

```
m21-allergy-alert/
├── streamlit_app.py           # Main entry point for Streamlit Cloud
├── requirements.txt           # Cloud-optimized dependencies
├── packages.txt              # System packages for Streamlit Cloud
├── .streamlit/
│   └── secrets.toml.example  # Template for MongoDB connection
├── frontend/
│   └── app.py               # Main Streamlit dashboard
├── shared/
│   ├── models.py            # Pydantic data models
│   └── database.py          # MongoDB connection (Atlas compatible)
├── database/
│   └── setup_db.py          # Database initialization and seeding
├── setup_atlas.py           # Atlas database setup tool
└── DEPLOYMENT_GUIDE.md      # Detailed deployment instructions
```

## 🎯 Dashboard Features

1. **💊 Prescription Validator** - Interactive prescription submission with real-time allergy checking
2. **👤 Patient Allergies** - Complete allergy profiles with risk assessment
3. **📋 Alert Log** - Comprehensive audit trail with filtering
4. **📊 Statistics** - Interactive charts and system metrics
5. **💊 Medications** - Searchable drug database with alternatives

## 🔧 Technology Highlights

- **Streamlit:** Rapid dashboard development with interactive components
- **MongoDB Atlas:** Cloud-native NoSQL database with aggregation pipelines
- **Pydantic:** Type-safe data validation throughout the application
- **Plotly:** Interactive visualizations and charts
- **Cloud-Optimized:** Direct database calls instead of separate API layer

## 📊 Database Features

- **9 Collections:** Patients, allergies, medications, prescriptions, alerts, etc.
- **Advanced Aggregation:** Complex MongoDB pipelines for analytics
- **Optimized Indexing:** Performance-tuned for healthcare queries
- **Flexible Schema:** Easy to extend with new allergy types or medications

## 🏥 Healthcare Compliance

- **Complete Audit Trail:** All allergy checks logged with timestamps
- **Risk Assessment:** Quantified cross-reactivity scoring (0.0-1.0)
- **Safe Alternatives:** Automatic suggestion of compatible medications
- **Regulatory Ready:** Comprehensive logging for compliance requirements

## 🌐 Cloud Benefits

- **Zero Infrastructure:** No servers to manage
- **Auto Scaling:** Handles traffic spikes automatically
- **Global CDN:** Fast loading worldwide
- **Integrated Secrets:** Secure credential management
- **Continuous Deployment:** Auto-deploy from GitHub

Perfect for healthcare organizations wanting a modern, cloud-native allergy alert system without infrastructure complexity!