"""
Streamlit Frontend for M21 Allergy Alert System
Optimized for Streamlit Cloud deployment with MongoDB Atlas
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.models import *

# Configure Streamlit page
st.set_page_config(
    page_title="M21 Allergy Alert System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .alert-danger {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .code-block {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 4px;
        padding: 1rem;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 0.85rem;
        overflow-x: auto;
    }
</style>
""", unsafe_allow_html=True)


def make_api_request(endpoint, method="GET", data=None):
    """Make API request with error handling - Cloud compatible"""
    try:
        # For Streamlit Cloud, we'll use direct database calls instead of API
        # This is more efficient and doesn't require a separate backend service
        return handle_direct_request(endpoint, method, data)
    except Exception as e:
        st.error(f"Request Error: {str(e)}")
        return None


def handle_direct_request(endpoint, method="GET", data=None):
    """Handle requests directly through database for cloud deployment"""
    from shared.database import db_manager, allergy_service
    
    # Initialize database connection if not already done
    if not db_manager.client:
        if not db_manager.connect():
            raise Exception("Failed to connect to database")
    
    # Route requests to appropriate handlers
    if endpoint == "/health":
        return {"status": "OK", "database": "Connected"}
    
    elif endpoint == "/api/v1/patients":
        return get_patients_direct()
    
    elif endpoint == "/api/v1/medications":
        return get_medications_direct()
    
    elif endpoint.startswith("/api/v1/patient/") and endpoint.endswith("/allergies"):
        patient_id = endpoint.split("/")[3]
        return get_patient_allergies_direct(patient_id)
    
    elif endpoint == "/api/v1/stats":
        return get_stats_direct()
    
    elif endpoint.startswith("/api/v1/alerts/recent"):
        return get_recent_alerts_direct()
    
    elif endpoint == "/api/v1/validate" and method == "POST":
        return validate_prescription_direct(data)
    
    else:
        raise Exception(f"Endpoint not implemented: {endpoint}")


def get_patients_direct():
    """Get patients directly from database"""
    from shared.database import db_manager
    from shared.models import get_age
    
    patients = list(db_manager.get_collection("patients").find())
    for patient in patients:
        patient["age"] = get_age(patient["dob"])
        patient["patient_id"] = patient["_id"]
    
    return {"success": True, "patients": patients}


def get_medications_direct():
    """Get medications directly from database"""
    from shared.database import db_manager
    
    medications = list(db_manager.get_collection("medications").find())
    for med in medications:
        med["med_id"] = med["_id"]
    
    return {"success": True, "medications": medications}


def get_patient_allergies_direct(patient_id):
    """Get patient allergies directly from database"""
    from shared.database import db_manager
    from shared.models import get_age
    
    # Get patient info
    patient = db_manager.get_collection("patients").find_one({"_id": patient_id})
    if not patient:
        return {"success": False, "error": "Patient not found"}
    
    # Get patient allergies with details
    pipeline = [
        {"$match": {"patient_id": patient_id}},
        {"$lookup": {
            "from": "allergies",
            "localField": "allergy_id",
            "foreignField": "_id",
            "as": "allergy_details"
        }},
        {"$unwind": "$allergy_details"},
        {"$project": {
            "allergy_id": "$allergy_id",
            "allergy_name": "$allergy_details.allergy_name",
            "allergy_type": "$allergy_details.allergy_type",
            "date_recorded": "$date_recorded",
            "notes": "$notes"
        }}
    ]
    
    allergies = list(db_manager.get_collection("patient_allergies").aggregate(pipeline))
    
    # Get risk profile
    risk_pipeline = [
        {"$match": {"patient_id": patient_id}},
        {"$lookup": {
            "from": "cross_reactivity_rules",
            "localField": "allergy_id",
            "foreignField": "allergen_id",
            "as": "cross_rules"
        }},
        {"$unwind": {"path": "$cross_rules", "preserveNullAndEmptyArrays": True}},
        {"$lookup": {
            "from": "allergies",
            "localField": "allergy_id",
            "foreignField": "_id",
            "as": "allergy_details"
        }},
        {"$unwind": "$allergy_details"},
        {"$lookup": {
            "from": "medications",
            "localField": "cross_rules.reactive_med_id",
            "foreignField": "_id",
            "as": "reactive_med"
        }},
        {"$unwind": {"path": "$reactive_med", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "allergy_name": "$allergy_details.allergy_name",
            "allergy_type": "$allergy_details.allergy_type",
            "risk_level": "$cross_rules.risk_level",
            "risk_score": "$cross_rules.risk_score",
            "reactive_drug": "$reactive_med.med_name"
        }}
    ]
    
    risk_profile = list(db_manager.get_collection("patient_allergies").aggregate(risk_pipeline))
    
    patient["age"] = get_age(patient["dob"])
    
    return {
        "success": True,
        "patient": patient,
        "allergies": allergies,
        "risk_profile": risk_profile
    }


def get_stats_direct():
    """Get statistics directly from database"""
    from shared.database import db_manager
    
    # Alert type statistics
    alert_stats_pipeline = [
        {"$group": {
            "_id": "$alert_type",
            "total": {"$sum": 1}
        }},
        {"$project": {
            "alert_type": "$_id",
            "total": "$total"
        }},
        {"$sort": {"total": -1}}
    ]
    
    alert_statistics = list(db_manager.get_collection("alert_log").aggregate(alert_stats_pipeline))
    
    # Additional statistics
    total_patients = db_manager.get_collection("patients").count_documents({})
    total_medications = db_manager.get_collection("medications").count_documents({})
    total_prescriptions = db_manager.get_collection("prescriptions").count_documents({})
    
    patients_with_allergies = len(list(db_manager.get_collection("patient_allergies").distinct("patient_id")))
    
    high_risk_rules = db_manager.get_collection("cross_reactivity_rules").count_documents(
        {"risk_score": {"$gt": 0.7}}
    )
    
    # Prescription status breakdown
    prescription_stats_pipeline = [
        {"$group": {
            "_id": "$status",
            "count": {"$sum": 1}
        }}
    ]
    
    prescription_breakdown = list(db_manager.get_collection("prescriptions").aggregate(prescription_stats_pipeline))
    prescription_stats = {item["_id"]: item["count"] for item in prescription_breakdown}
    
    return {
        "success": True,
        "alert_statistics": alert_statistics,
        "additional_stats": {
            "total_patients": total_patients,
            "patients_with_allergies": patients_with_allergies,
            "total_medications": total_medications,
            "total_prescriptions": total_prescriptions,
            "high_risk_rules": high_risk_rules,
            "prescription_stats": prescription_stats
        }
    }


def get_recent_alerts_direct():
    """Get recent alerts directly from database"""
    from shared.database import db_manager
    
    pipeline = [
        {"$lookup": {
            "from": "patients",
            "localField": "patient_id",
            "foreignField": "_id",
            "as": "patient"
        }},
        {"$unwind": "$patient"},
        {"$lookup": {
            "from": "medications",
            "localField": "med_id",
            "foreignField": "_id",
            "as": "medication"
        }},
        {"$unwind": "$medication"},
        {"$lookup": {
            "from": "prescriptions",
            "localField": "prescription_id",
            "foreignField": "_id",
            "as": "prescription"
        }},
        {"$unwind": {"path": "$prescription", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "log_id": "$_id",
            "alert_type": "$alert_type",
            "patient_name": "$patient.name",
            "med_name": "$medication.med_name",
            "alert_message": "$alert_message",
            "logged_at": "$logged_at",
            "prescription_status": "$prescription.status"
        }},
        {"$sort": {"logged_at": -1}},
        {"$limit": 50}
    ]
    
    recent_alerts = list(db_manager.get_collection("alert_log").aggregate(pipeline))
    
    return {
        "success": True,
        "recent_alerts": recent_alerts
    }


def validate_prescription_direct(data):
    """Validate prescription directly through database"""
    from shared.database import db_manager, allergy_service
    from shared.models import generate_approval_token
    from bson import ObjectId
    from datetime import datetime
    
    # Create prescription record
    prescription_data = {
        "_id": str(ObjectId()),
        "patient_id": data["patient_id"],
        "med_id": data["med_id"],
        "dose": data["dose"],
        "frequency": data["frequency"],
        "start_date": data["start_date"],
        "status": "Pending",
        "created_at": datetime.now()
    }
    
    db_manager.get_collection("prescriptions").insert_one(prescription_data)
    prescription_id = prescription_data["_id"]
    
    # Perform allergy check
    check_result = allergy_service.perform_full_check(
        data["patient_id"], data["med_id"], prescription_id
    )
    
    # Prepare response
    response_data = {
        "status": check_result["status"],
        "alert_type": check_result.get("alert_type"),
        "message": check_result["message"],
        "prescription_id": prescription_id,
        "alternatives": check_result.get("alternatives", []),
        "logged_at": datetime.now().isoformat()
    }
    
    # Add approval token for safe prescriptions
    if check_result["status"] == "SAFE":
        response_data["approval_token"] = generate_approval_token(
            data["patient_id"], data["med_id"]
        )
    
    return response_data


def display_header():
    """Display main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Module 21: Allergy-Aware Medication Alert System</h1>
        <p>Database Management Systems Project - IIT(ISM) Dhanbad</p>
        <p><strong>Technology Stack:</strong> Python • Streamlit • MongoDB Atlas</p>
        <p><strong>Deployment:</strong> Streamlit Cloud Ready</p>
    </div>
    """, unsafe_allow_html=True)


def prescription_validator():
    """Prescription Validator Page"""
    st.header("💊 Prescription Validator")
    st.write("Submit a new prescription to check for allergy conflicts using our 3-level cascade system.")
    
    # Fetch patients and medications
    patients_data = make_api_request("/api/v1/patients")
    medications_data = make_api_request("/api/v1/medications")
    
    if not patients_data or not medications_data:
        st.error("Failed to load data from API")
        return
    
    patients = patients_data.get("patients", [])
    medications = medications_data.get("medications", [])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Prescription Details")
        
        # Patient selection
        patient_options = {f"{p['name']} (Age: {p['age']}, {p['sex']})": p['_id'] for p in patients}
        selected_patient_display = st.selectbox("Select Patient", list(patient_options.keys()))
        selected_patient_id = patient_options[selected_patient_display] if selected_patient_display else None
        
        # Medication selection
        med_options = {f"{m['med_name']} ({m['drug_class']})": m['_id'] for m in medications}
        selected_med_display = st.selectbox("Select Medication", list(med_options.keys()))
        selected_med_id = med_options[selected_med_display] if selected_med_display else None
        
        # Prescription details
        dose = st.text_input("Dose", placeholder="e.g., 500mg")
        frequency = st.selectbox("Frequency", [
            "Once daily", "Twice daily", "Three times daily", "Four times daily",
            "Every 6 hours", "Every 8 hours", "Every 12 hours", "As needed"
        ])
        start_date = st.date_input("Start Date", value=date.today())
        
        # Submit button
        if st.button("🔍 Check & Submit Prescription", type="primary"):
            if all([selected_patient_id, selected_med_id, dose, frequency]):
                # Make validation request
                request_data = {
                    "patient_id": selected_patient_id,
                    "med_id": selected_med_id,
                    "dose": dose,
                    "frequency": frequency,
                    "start_date": start_date.isoformat()
                }
                
                with st.spinner("Performing allergy check..."):
                    result = make_api_request("/api/v1/validate", method="POST", data=request_data)
                
                if result:
                    st.session_state['validation_result'] = result
            else:
                st.error("Please fill in all required fields")
    
    with col2:
        # Display selected patient info
        if selected_patient_id:
            selected_patient = next((p for p in patients if p['_id'] == selected_patient_id), None)
            if selected_patient:
                st.info(f"""
                **Selected Patient:** {selected_patient['name']}  
                **Age:** {selected_patient['age']} • **Sex:** {selected_patient['sex']}  
                **DOB:** {selected_patient['dob']}
                """)
        
        # Display selected medication info
        if selected_med_id:
            selected_med = next((m for m in medications if m['_id'] == selected_med_id), None)
            if selected_med:
                st.info(f"""
                **Selected Medication:** {selected_med['med_name']}  
                **Class:** {selected_med['drug_class']}  
                **Active Ingredients:** {selected_med['active_ingredients']}
                """)
    
    # Display validation result
    if 'validation_result' in st.session_state:
        result = st.session_state['validation_result']
        
        if result['status'] == 'SAFE':
            st.markdown(f"""
            <div class="alert-success">
                <h3>✅ PRESCRIPTION APPROVED</h3>
                <p><strong>Status:</strong> {result['status']}</p>
                <p><strong>Message:</strong> {result['message']}</p>
                <p><strong>Prescription ID:</strong> {result['prescription_id']}</p>
                <p><strong>Approval Token:</strong> <code>{result.get('approval_token', 'N/A')}</code></p>
                <p><strong>Logged at:</strong> {result['logged_at']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-danger">
                <h3>⚠️ ALLERGY ALERT</h3>
                <p><strong>Alert Type:</strong> {result.get('alert_type', 'ALERT')}</p>
                <p><strong>Message:</strong> {result['message']}</p>
                <p><strong>Prescription ID:</strong> {result['prescription_id']}</p>
                <p><strong>Logged at:</strong> {result['logged_at']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display alternatives
            if result.get('alternatives'):
                st.subheader("🔄 Safe Alternatives")
                alt_df = pd.DataFrame(result['alternatives'])
                st.dataframe(alt_df, use_container_width=True)
    
    # Information about the checking system
    st.subheader("🔍 How the 3-Level Cascade Check Works")
    st.write("""
    1. **Exact Match:** Is the prescribed drug exactly in the patient's allergy list?
    2. **Drug Class Match:** Does the drug belong to a drug class the patient is allergic to?
    3. **Cross-Reactivity:** Does the drug have known cross-reactivity above risk threshold (0.5)?
    
    If any check triggers → **ALERT** with safe alternatives  
    If all checks pass → **SAFE** with approval token
    """)


def allergy_profile():
    """Patient Allergy Profile Page"""
    st.header("👤 Patient Allergy Profile Viewer")
    st.write("Select a patient to view their complete allergy profile and cross-reactivity risks.")
    
    # Fetch patients
    patients_data = make_api_request("/api/v1/patients")
    if not patients_data:
        st.error("Failed to load patients")
        return
    
    patients = patients_data.get("patients", [])
    
    # Patient selection
    patient_options = {f"{p['name']} (Age: {p['age']}, {p['sex']})": p['_id'] for p in patients}
    selected_patient_display = st.selectbox("Select Patient", [""] + list(patient_options.keys()))
    
    if selected_patient_display:
        selected_patient_id = patient_options[selected_patient_display]
        
        # Fetch patient allergy data
        allergy_data = make_api_request(f"/api/v1/patient/{selected_patient_id}/allergies")
        
        if allergy_data and allergy_data.get("success"):
            patient = allergy_data["patient"]
            allergies = allergy_data["allergies"]
            risk_profile = allergy_data["risk_profile"]
            
            # Display patient info
            st.info(f"""
            **Patient:** {patient['name']}  
            **Date of Birth:** {patient['dob']} • **Age:** {patient['age']} • **Sex:** {patient['sex']}
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🚨 Known Allergies")
                if allergies:
                    allergy_df = pd.DataFrame(allergies)
                    st.dataframe(allergy_df[['allergy_name', 'allergy_type', 'date_recorded', 'notes']], 
                               use_container_width=True)
                else:
                    st.success("✅ No known allergies recorded for this patient")
            
            with col2:
                st.subheader("⚠️ Cross-Reactivity Risk Profile")
                high_risk_items = [item for item in risk_profile if item.get('reactive_drug') and item.get('risk_score', 0) > 0.5]
                
                if high_risk_items:
                    risk_df = pd.DataFrame(high_risk_items)
                    st.dataframe(risk_df[['allergy_name', 'reactive_drug', 'risk_level', 'risk_score']], 
                               use_container_width=True)
                else:
                    st.success("✅ No high-risk cross-reactivity medications found")
        else:
            st.error("Failed to load patient allergy data")


def alert_log():
    """Alert Log Page"""
    st.header("📋 Alert Log & Audit Trail")
    st.write("Complete history of all allergy checks and alerts generated by the system.")
    
    # Fetch recent alerts
    alerts_data = make_api_request("/api/v1/alerts/recent?limit=50")
    
    if alerts_data and alerts_data.get("success"):
        alerts = alerts_data["recent_alerts"]
        
        if alerts:
            # Convert to DataFrame
            alerts_df = pd.DataFrame(alerts)
            
            # Add filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                alert_types = ["All"] + list(alerts_df['alert_type'].unique())
                selected_alert_type = st.selectbox("Filter by Alert Type", alert_types)
            
            with col2:
                patients = ["All"] + list(alerts_df['patient_name'].unique())
                selected_patient = st.selectbox("Filter by Patient", patients)
            
            with col3:
                st.metric("Total Alerts", len(alerts_df))
            
            # Apply filters
            filtered_df = alerts_df.copy()
            if selected_alert_type != "All":
                filtered_df = filtered_df[filtered_df['alert_type'] == selected_alert_type]
            if selected_patient != "All":
                filtered_df = filtered_df[filtered_df['patient_name'] == selected_patient]
            
            # Display filtered results
            st.subheader(f"🚨 Alert History ({len(filtered_df)} alerts)")
            
            # Format the dataframe for display
            display_df = filtered_df[['log_id', 'patient_name', 'med_name', 'alert_type', 
                                    'alert_message', 'prescription_status', 'logged_at']].copy()
            display_df['logged_at'] = pd.to_datetime(display_df['logged_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            st.dataframe(display_df, use_container_width=True)
            
        else:
            st.info("No alerts found in the system")
    else:
        st.error("Failed to load alert data")


def statistics_panel():
    """Statistics Panel Page"""
    st.header("📊 System Statistics")
    st.write("Overview of allergy alerts, prescriptions, and system performance metrics.")
    
    # Fetch statistics
    stats_data = make_api_request("/api/v1/stats")
    
    if stats_data and stats_data.get("success"):
        alert_stats = stats_data["alert_statistics"]
        additional_stats = stats_data["additional_stats"]
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Patients", additional_stats["total_patients"])
        
        with col2:
            st.metric("💊 Total Medications", additional_stats["total_medications"])
        
        with col3:
            st.metric("📋 Total Prescriptions", additional_stats["total_prescriptions"])
        
        with col4:
            st.metric("⚠️ High Risk Rules", additional_stats["high_risk_rules"])
        
        # Alert statistics charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚨 Alert Type Distribution")
            if alert_stats:
                alert_df = pd.DataFrame(alert_stats)
                fig = px.bar(alert_df, x='alert_type', y='total', 
                           title="Alert Types", color='alert_type')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📈 Alert Breakdown")
            if alert_stats:
                fig = px.pie(alert_df, values='total', names='alert_type', 
                           title="Alert Distribution")
                st.plotly_chart(fig, use_container_width=True)
        
        # Prescription status breakdown
        if additional_stats.get("prescription_stats"):
            st.subheader("💊 Prescription Status")
            prescription_stats = additional_stats["prescription_stats"]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("✅ Approved", prescription_stats.get("Approved", 0))
            
            with col2:
                st.metric("❌ Rejected", prescription_stats.get("Rejected", 0))
            
            with col3:
                st.metric("⏳ Pending", prescription_stats.get("Pending", 0))
        
        # Safety metrics
        st.subheader("🎯 Key Performance Indicators")
        
        total_alerts = sum(item['total'] for item in alert_stats)
        safe_count = next((item['total'] for item in alert_stats if item['alert_type'] == 'SAFE'), 0)
        
        if total_alerts > 0:
            safety_rate = (safe_count / total_alerts) * 100
            alert_rate = ((total_alerts - safe_count) / total_alerts) * 100
        else:
            safety_rate = 0
            alert_rate = 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("✅ Safety Rate", f"{safety_rate:.1f}%")
        
        with col2:
            st.metric("🚨 Alert Rate", f"{alert_rate:.1f}%")
        
        with col3:
            st.metric("📈 Total Checks", total_alerts)
        
    else:
        st.error("Failed to load statistics")


def medication_browser():
    """Medication Browser Page"""
    st.header("💊 Medication & Alternatives Browser")
    st.write("Explore medications, their drug classes, safe alternatives, and cross-reactivity information.")
    
    # Fetch medications and drug classes
    medications_data = make_api_request("/api/v1/medications")
    drug_classes_data = make_api_request("/api/v1/drug-classes")
    
    if not medications_data or not drug_classes_data:
        st.error("Failed to load medication data")
        return
    
    medications = medications_data.get("medications", [])
    drug_classes = drug_classes_data.get("drug_classes", [])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📋 Medication List")
        
        # Drug class filter
        class_options = ["All Classes"] + [dc["drug_class"] for dc in drug_classes]
        selected_class = st.selectbox("Filter by Drug Class", class_options)
        
        # Filter medications
        if selected_class != "All Classes":
            filtered_meds = [m for m in medications if m["drug_class"] == selected_class]
        else:
            filtered_meds = medications
        
        # Display medications
        for med in filtered_meds:
            if st.button(f"{med['med_name']} ({med['drug_class']})", key=med['_id']):
                st.session_state['selected_medication'] = med['_id']
    
    with col2:
        if 'selected_medication' in st.session_state:
            med_id = st.session_state['selected_medication']
            
            # Fetch medication details
            med_details = make_api_request(f"/api/v1/medication/{med_id}")
            
            if med_details and med_details.get("success"):
                medication = med_details["medication"]
                alternatives = med_details["alternatives"]
                cross_reactivity = med_details["cross_reactivity"]
                
                st.subheader("🔍 Medication Details")
                
                st.info(f"""
                **Name:** {medication['med_name']}  
                **Drug Class:** {medication['drug_class']}  
                **Active Ingredients:** {medication['active_ingredients']}  
                **Medication ID:** {medication['_id']}
                """)
                
                # Alternatives
                if alternatives:
                    st.subheader("🔄 Safe Alternatives")
                    alt_df = pd.DataFrame(alternatives)
                    st.dataframe(alt_df, use_container_width=True)
                
                # Cross-reactivity warnings
                if cross_reactivity:
                    st.subheader("⚠️ Cross-Reactivity Warnings")
                    cross_df = pd.DataFrame(cross_reactivity)
                    st.dataframe(cross_df, use_container_width=True)
                
                if not alternatives and not cross_reactivity:
                    st.success("✅ No specific alternatives or cross-reactivity warnings found for this medication.")
        else:
            st.info("👈 Select a medication from the list to view detailed information")
    
    # Drug class overview
    st.subheader("📊 Drug Class Overview")
    if drug_classes:
        class_df = pd.DataFrame(drug_classes)
        st.dataframe(class_df[['drug_class', 'medication_count', 'medications']], 
                   use_container_width=True)


def main():
    """Main Streamlit application"""
    display_header()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    pages = {
        "💊 Prescription Validator": prescription_validator,
        "👤 Patient Allergies": allergy_profile,
        "📋 Alert Log": alert_log,
        "📊 Statistics": statistics_panel,
        "💊 Medications": medication_browser
    }
    
    selected_page = st.sidebar.selectbox("Choose a page", list(pages.keys()))
    
    # API health check
    try:
        health_data = make_api_request("/health")
        if health_data and health_data.get("status") == "OK":
            st.sidebar.success("✅ Database Connected")
        else:
            st.sidebar.error("❌ Database Disconnected")
    except:
        st.sidebar.warning("⚠️ Connecting to Database...")
    
    # Display selected page
    pages[selected_page]()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p><strong>Features:</strong> 9 Collections • MongoDB Atlas • 3-Level Cascade Checking</p>
        <p><strong>Technology:</strong> Python • Streamlit • MongoDB Atlas • Plotly</p>
        <p><strong>Deployment:</strong> Streamlit Cloud + MongoDB Atlas</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()