# Module 21: Allergy-Aware Medication Alert System

**Technology Stack:** Python • Streamlit • MongoDB Atlas  
**Deployment:** Streamlit Cloud Exclusive

## 🚀 Cloud-Only Deployment

This system is designed exclusively for **Streamlit Cloud + MongoDB Atlas**. No local setup required!

### Quick Deploy (5 minutes):

1. **MongoDB Atlas Setup:**
   - Create free cluster at [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Get connection string
   - Configure network access (0.0.0.0/0)

2. **Streamlit Cloud Deploy:**
   - Push to GitHub
   - Deploy at [share.streamlit.io](https://share.streamlit.io)
   - Set main file: `src/module/m21-allergy-alert/streamlit_app.py`
   - Add MongoDB connection to secrets:
     ```toml
     MONGODB_URL = "mongodb+srv://username:password@cluster.mongodb.net/m21_allergy_alert?retryWrites=true&w=majority"
     ```

3. **Auto-Initialize:**
   - Database automatically sets up on first run
   - Creates 9 collections with test data
   - Ready to use immediately!

## 🎯 Features

### 3-Level Cascade Allergy Checking:
1. **Exact Match** - Direct drug-to-allergy comparison
2. **Drug Class Match** - Broad category checking  
3. **Cross-Reactivity** - Risk-scored interaction analysis

### Interactive Dashboard (5 Pages):
1. **💊 Prescription Validator** - Real-time allergy checking
2. **👤 Patient Allergies** - Complete profiles with risk assessment
3. **📋 Alert Log** - Audit trail with filtering
4. **📊 Statistics** - Interactive charts and KPIs
5. **💊 Medications** - Drug database browser

### Test Data Included:
- **5 Patients** with varied allergy profiles
- **16 Medications** across 6 drug classes
- **12 Allergies** with cross-reactivity rules
- **Complete scenarios** for all alert types

## 📁 Project Structure

```
m21-allergy-alert/
├── streamlit_app.py           # Main entry point
├── requirements.txt           # Atlas-optimized dependencies
├── .streamlit/
│   └── secrets.toml.example  # MongoDB connection template
├── frontend/
│   └── app.py               # Streamlit dashboard
├── shared/
│   ├── models.py            # Data models
│   └── database.py          # Atlas connection
├── database/
│   └── setup_db.py          # Database initialization
└── DEPLOYMENT_GUIDE.md      # Detailed instructions
```

## 🌐 Cloud Benefits

- **Zero Infrastructure** - No servers to manage
- **Auto Scaling** - Handles any traffic load
- **Global CDN** - Fast access worldwide
- **99.9% Uptime** - Enterprise reliability
- **Free Hosting** - No hosting costs
- **Instant Deploy** - Live in minutes

## 🔧 MongoDB Atlas Features

- **Free M0 Cluster** - 512MB storage (plenty for this project)
- **Advanced Aggregation** - Complex analytical queries
- **Automatic Backups** - Data protection included
- **Global Clusters** - Deploy worldwide
- **Real-time Monitoring** - Performance insights

Perfect for healthcare organizations wanting modern, cloud-native allergy checking without infrastructure complexity! 🏥✨