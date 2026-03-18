"""
Streamlit Frontend for M21 Allergy Alert System
Streamlit Cloud + MongoDB Atlas Exclusive
"""
import streamlit as st
from datetime import datetime, date
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.models import *

# Configure Streamlit page
st.set_page_config(
    page_title="M21 Allergy Alert System",
    page_icon="⚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clinical shadcn-inspired design
st.markdown("""
<style>
    /* Import Inter font for clinical look */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header styling */
    .clinical-header {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    }
    
    .clinical-header h1 {
        color: #0f172a;
        font-weight: 600;
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .clinical-header p {
        color: #64748b;
        font-weight: 400;
        margin: 0.25rem 0;
    }
    
    /* Alert components */
    .alert-success {
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-left: 4px solid #22c55e;
        color: #15803d;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .alert-danger {
        background-color: #fef2f2;
        border: 1px solid #fecaca;
        border-left: 4px solid #ef4444;
        color: #dc2626;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .alert-warning {
        background-color: #fffbeb;
        border: 1px solid #fed7aa;
        border-left: 4px solid #f59e0b;
        color: #d97706;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .alert-info {
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;
        border-left: 4px solid #3b82f6;
        color: #1d4ed8;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Card components */
    .clinical-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    }
    
    .clinical-card h3 {
        color: #0f172a;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.125rem;
    }
    
    /* Status indicators */
    .status-connected {
        color: #22c55e;
        font-weight: 600;
    }
    
    .status-disconnected {
        color: #ef4444;
        font-weight: 600;
    }
    
    .status-warning {
        color: #f59e0b;
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        transition: background-color 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #2563eb;
    }
    
    /* Metric styling */
    .metric-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #64748b;
        font-weight: 500;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Table styling */
    .clinical-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    }
    
    .clinical-table th {
        background-color: #f8fafc;
        color: #374151;
        font-weight: 600;
        padding: 0.75rem;
        text-align: left;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .clinical-table td {
        padding: 0.75rem;
        border-bottom: 1px solid #f1f5f9;
        color: #374151;
    }
    
    .clinical-table tr:hover {
        background-color: #f8fafc;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8fafc;
    }
    
    /* Remove default streamlit styling */
    .css-1v0mbdj.etr89bj1 {
        display: none;
    }
    
    /* Footer styling */
    .clinical-footer {
        border-top: 1px solid #e2e8f0;
        padding-top: 2rem;
        margin-top: 3rem;
        text-align: center;
        color: #64748b;
        font-size: 0.875rem;
    }
    
    /* Form styling */
    .stSelectbox > div > div {
        border-radius: 6px;
        border: 1px solid #d1d5db;
    }
    
    .stTextInput > div > div > input {
        border-radius: 6px;
        border: 1px solid #d1d5db;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8fafc;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)


def make_api_request(endpoint, method="GET", data=None):
    """Make API request with error handling - Streamlit Cloud optimized"""
    try:
        # Direct database calls for cloud deployment efficiency
        return handle_direct_request(endpoint, method, data)
    except Exception as e:
        st.error(f"Request Error: {str(e)}")
        return None


def handle_direct_request(endpoint, method="GET", data=None):
    """Handle requests directly through database for Streamlit Cloud deployment"""
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
    
    elif endpoint == "/api/v1/drug-classes":
        return get_drug_classes_direct()
    
    elif endpoint.startswith("/api/v1/patient/") and endpoint.endswith("/allergies"):
        patient_id = endpoint.split("/")[4]
        return get_patient_allergies_direct(patient_id)
    
    elif endpoint == "/api/v1/stats":
        return get_stats_direct()
    
    elif endpoint.startswith("/api/v1/alerts/recent"):
        return get_recent_alerts_direct()
    
    elif endpoint.startswith("/api/v1/medication/"):
        med_id = endpoint.split("/")[4]
        return get_medication_details_direct(med_id)
    
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


def get_drug_classes_direct():
    """Get drug classes directly from database"""
    from shared.database import db_manager
    
    # Get unique drug classes with medication counts
    pipeline = [
        {"$group": {
            "_id": "$drug_class",
            "medication_count": {"$sum": 1},
            "medications": {"$push": "$med_name"}
        }},
        {"$project": {
            "drug_class": "$_id",
            "medication_count": "$medication_count",
            "medications": "$medications"
        }},
        {"$sort": {"drug_class": 1}}
    ]
    
    drug_classes = list(db_manager.get_collection("medications").aggregate(pipeline))
    
    return {"success": True, "drug_classes": drug_classes}


def get_patient_allergies_direct(patient_id):
    """Get patient allergies directly from database with robust handling"""
    from shared.database import db_manager
    from shared.models import get_age
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        # Get patient info
        patient = db_manager.get_collection("patients").find_one({"_id": patient_id})
        if not patient:
            logger.error(f"Patient not found: {patient_id}")
            return {"success": False, "error": "Patient not found"}
        
        # Get patient allergies with details
        # Added $ifNull to handle missing optional fields
        pipeline = [
            {"$match": {"patient_id": patient_id}},
            {"$lookup": {
                "from": "allergies",
                "localField": "allergy_id",
                "foreignField": "_id",
                "as": "allergy_details"
            }},
            {"$unwind": {"path": "$allergy_details", "preserveNullAndEmptyArrays": True}},
            {"$project": {
                "allergy_id": "$allergy_id",
                "allergy_name": {"$ifNull": ["$allergy_details.allergy_name", "Unknown Allergy"]},
                "allergy_type": {"$ifNull": ["$allergy_details.allergy_type", "Other"]},
                "date_recorded": {"$ifNull": ["$date_recorded", "N/A"]},
                "notes": {"$ifNull": ["$notes", ""]}
            }}
        ]
        
        allergies = list(db_manager.get_collection("patient_allergies").aggregate(pipeline))
        
        # Get risk profile (cross-reactivity)
        risk_pipeline = [
            {"$match": {"patient_id": patient_id}},
            {"$lookup": {
                "from": "cross_reactivity_rules",
                "localField": "allergy_id",
                "foreignField": "allergen_id",
                "as": "cross_rules"
            }},
            {"$unwind": {"path": "$cross_rules", "preserveNullAndEmptyArrays": False}},
            {"$lookup": {
                "from": "allergies",
                "localField": "allergy_id",
                "foreignField": "_id",
                "as": "allergy_details"
            }},
            {"$unwind": {"path": "$allergy_details", "preserveNullAndEmptyArrays": True}},
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
                "reactive_drug": "$reactive_med.med_name",
                "drug_class": "$reactive_med.drug_class"
            }}
        ]
        
        risk_profile = list(db_manager.get_collection("patient_allergies").aggregate(risk_pipeline))
        
        # Calculate age safely
        patient["age"] = get_age(patient.get("dob"))
        
        return {
            "success": True,
            "patient": patient,
            "allergies": allergies,
            "risk_profile": risk_profile
        }
    except Exception as e:
        logger.exception(f"Error fetching patient allergy data for {patient_id}: {str(e)}")
        return {"success": False, "error": str(e)}


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


def get_medication_details_direct(med_id):
    """Get medication details with alternatives and cross-reactivity"""
    from shared.database import db_manager
    
    # Get medication details
    medication = db_manager.get_collection("medications").find_one({"_id": med_id})
    if not medication:
        return {"success": False, "error": "Medication not found"}
    
    # Get alternatives
    alternatives_pipeline = [
        {"$match": {"original_med_id": med_id}},
        {"$lookup": {
            "from": "medications",
            "localField": "alternative_med_id",
            "foreignField": "_id",
            "as": "alt_med"
        }},
        {"$unwind": "$alt_med"},
        {"$project": {
            "med_name": "$alt_med.med_name",
            "drug_class": "$alt_med.drug_class",
            "reason": "$reason"
        }}
    ]
    
    alternatives = list(db_manager.get_collection("alternatives").aggregate(alternatives_pipeline))
    
    # Get cross-reactivity warnings
    cross_reactivity_pipeline = [
        {"$match": {"reactive_med_id": med_id}},
        {"$lookup": {
            "from": "allergies",
            "localField": "allergen_id",
            "foreignField": "_id",
            "as": "allergy"
        }},
        {"$unwind": "$allergy"},
        {"$project": {
            "allergy_name": "$allergy.allergy_name",
            "allergy_type": "$allergy.allergy_type",
            "risk_level": "$risk_level",
            "risk_score": "$risk_score"
        }}
    ]
    
    cross_reactivity = list(db_manager.get_collection("cross_reactivity_rules").aggregate(cross_reactivity_pipeline))
    
    return {
        "success": True,
        "medication": medication,
        "alternatives": alternatives,
        "cross_reactivity": cross_reactivity
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
    <div class="clinical-header">
        <h1>Module 21: Allergy-Aware Medication Alert System</h1>
        <p>Database Management Systems Project - IIT(ISM) Dhanbad</p>
        <p><strong>Technology Stack:</strong> Python • Streamlit • MongoDB Atlas</p>
        <p><strong>Deployment:</strong> Streamlit Cloud Ready</p>
    </div>
    """, unsafe_allow_html=True)


def prescription_validator():
    """Prescription Validator Page"""
    st.header("Prescription Validator")
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
        if st.button("Check & Submit Prescription", type="primary"):
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
                <h3>PRESCRIPTION APPROVED</h3>
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
                <h3>ALLERGY ALERT</h3>
                <p><strong>Alert Type:</strong> {result.get('alert_type', 'ALERT')}</p>
                <p><strong>Message:</strong> {result['message']}</p>
                <p><strong>Prescription ID:</strong> {result['prescription_id']}</p>
                <p><strong>Logged at:</strong> {result['logged_at']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display alternatives
            if result.get('alternatives'):
                st.subheader("Safe Alternatives")
                
                if result['alternatives']:
                    # Display alternatives in a clean format
                    for i, alt in enumerate(result['alternatives'], 1):
                        with st.container():
                            col1, col2, col3 = st.columns([2, 2, 4])
                            with col1:
                                st.markdown(f"**{i}. {alt['med_name']}**")
                            with col2:
                                st.markdown(f"*{alt['drug_class']}*")
                            with col3:
                                st.markdown(f"{alt['reason']}")
                            st.divider()
                else:
                    st.info("No alternatives available")
    
    # Information about the checking system
    st.subheader("How the 3-Level Cascade Check Works")
    st.write("""
    1. **Exact Match:** Is the prescribed drug exactly in the patient's allergy list?
    2. **Drug Class Match:** Does the drug belong to a drug class the patient is allergic to?
    3. **Cross-Reactivity:** Does the drug have known cross-reactivity above risk threshold (0.5)?
    
    If any check triggers → **ALERT** with safe alternatives  
    If all checks pass → **SAFE** with approval token
    """)


def create_allergy_network_graph(patient_id):
    """Create enhanced interactive network graph showing allergy-medication relationships"""
    from shared.database import db_manager
    import plotly.graph_objects as go
    import math
    
    # Get patient allergies
    patient_allergies = list(db_manager.get_collection("patient_allergies").find(
        {"patient_id": patient_id}
    ))
    
    if not patient_allergies:
        return None
    
    allergy_ids = [pa["allergy_id"] for pa in patient_allergies]
    
    # Get allergy details
    allergies = list(db_manager.get_collection("allergies").find(
        {"_id": {"$in": allergy_ids}}
    ))
    allergy_map = {a["_id"]: a for a in allergies}
    
    # Get cross-reactivity rules
    cross_rules = list(db_manager.get_collection("cross_reactivity_rules").find(
        {"allergen_id": {"$in": allergy_ids}}
    ))
    
    # Get drug class allergies
    drug_class_allergies = list(db_manager.get_collection("drug_class_allergies").find(
        {"allergy_id": {"$in": allergy_ids}}
    ))
    
    # Get medications involved in cross-reactivity
    med_ids = list(set([cr["reactive_med_id"] for cr in cross_rules]))
    medications = list(db_manager.get_collection("medications").find(
        {"_id": {"$in": med_ids}}
    )) if med_ids else []
    
    # Also get all medications by drug class
    drug_classes = list(set([dca["drug_class"] for dca in drug_class_allergies]))
    class_medications = list(db_manager.get_collection("medications").find(
        {"drug_class": {"$in": drug_classes}}
    )) if drug_classes else []
    
    # Merge and build med map
    all_meds = {m["_id"]: m for m in medications + class_medications}
    med_list = list(all_meds.values())
    
    # Build graph data structures
    nodes = []
    edges = []
    
    # 1. Center: Patient
    nodes.append({
        "id": "patient",
        "label": f"Patient",
        "type": "patient",
        "x": 0,
        "y": 0,
        "size": 35,
        "color": "#2563eb",
        "hover": "Patient Node"
    })
    
    # 2. Layer 1: Allergies (Inner-Middle Circle)
    num_allergies = len(allergies)
    for i, allergy in enumerate(allergies):
        angle = 2 * math.pi * i / num_allergies if num_allergies > 0 else 0
        r = 1.8
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        
        nodes.append({
            "id": f"allergy_{allergy['_id']}",
            "label": allergy["allergy_name"],
            "type": "allergy",
            "x": x,
            "y": y,
            "size": 25,
            "color": "#dc2626",
            "hover": f"Allergy: {allergy['allergy_name']}<br>Type: {allergy['allergy_type']}"
        })
        
        edges.append({
            "from": "patient",
            "to": f"allergy_{allergy['_id']}",
            "type": "has_allergy",
            "color": "#ef4444",
            "width": 3
        })
    
    # 3. Layer 2: Drug Classes (Outer-Middle Circle)
    drug_class_nodes = {}
    num_classes = len(drug_classes)
    for i, d_class in enumerate(drug_classes):
        angle = 2 * math.pi * i / num_classes + (math.pi / max(num_classes, 1)) if num_classes > 0 else 0
        r = 3.5
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        
        node_id = f"class_{d_class}"
        drug_class_nodes[d_class] = node_id
        nodes.append({
            "id": node_id,
            "label": d_class,
            "type": "drug_class",
            "x": x,
            "y": y,
            "size": 22,
            "color": "#ea580c",
            "hover": f"Drug Class: {d_class}<br>Allergic via selection"
        })
        
        # Connect allergies to drug classes
        for dca in drug_class_allergies:
            if dca["drug_class"] == d_class:
                edges.append({
                    "from": f"allergy_{dca['allergy_id']}",
                    "to": node_id,
                    "type": "class_match",
                    "color": "#f97316",
                    "width": 2,
                    "dash": "dash"
                })
    
    # 4. Layer 3: Medications (Outer Circle)
    num_meds = len(med_list)
    med_nodes = {}
    for i, med in enumerate(med_list):
        angle = 2 * math.pi * i / num_meds if num_meds > 0 else 0
        r = 5.5
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        
        node_id = f"med_{med['_id']}"
        med_nodes[med["_id"]] = node_id
        nodes.append({
            "id": node_id,
            "label": med["med_name"],
            "type": "medication",
            "x": x,
            "y": y,
            "size": 18,
            "color": "#7c3aed",
            "hover": f"Medication: {med['med_name']}<br>Class: {med['drug_class']}"
        })
        
        # Connect to drug class if it matches
        if med["drug_class"] in drug_class_nodes:
            edges.append({
                "from": drug_class_nodes[med["drug_class"]],
                "to": node_id,
                "type": "belongs_to",
                "color": "#94a3b8",
                "width": 1.5
            })
    
    # 5. Cross-Reactivity Edges (Direct Allergy to Medication)
    for cr in cross_rules:
        med_id = cr["reactive_med_id"]
        allergy_id = cr["allergen_id"]
        if f"allergy_{allergy_id}" in [n["id"] for n in nodes] and f"med_{med_id}" in [n["id"] for n in nodes]:
            risk_score = cr["risk_score"]
            color = "#b91c1c" if risk_score > 0.7 else "#d97706" if risk_score > 0.5 else "#15803d"
            width = 4 if risk_score > 0.7 else 2.5
            
            edges.append({
                "from": f"allergy_{allergy_id}",
                "to": f"med_{med_id}",
                "type": "cross_reactivity",
                "color": color,
                "width": width,
                "risk_score": risk_score,
                "hover": f"Cross-Reactivity Risk: {risk_score:.2f} ({cr['risk_level']})"
            })
    
    # Create Plotly traces
    fig_data = []
    
    # Helper to find node by ID
    node_map = {n["id"]: n for n in nodes}
    
    # Edge traces
    for edge in edges:
        from_node = node_map.get(edge["from"])
        to_node = node_map.get(edge["to"])
        
        if from_node and to_node:
            edge_trace = go.Scatter(
                x=[from_node["x"], to_node["x"], None],
                y=[from_node["y"], to_node["y"], None],
                mode='lines',
                line=dict(
                    width=edge["width"],
                    color=edge["color"],
                    dash=edge.get("dash", "solid")
                ),
                hoverinfo='text',
                text=edge.get("hover", edge["type"].replace("_", " ").title()),
                showlegend=False
            )
            fig_data.append(edge_trace)
    
    # Node traces by type for legend
    type_configs = {
        "patient": {"color": "#2563eb", "name": "Patient"},
        "allergy": {"color": "#dc2626", "name": "Allergies"},
        "drug_class": {"color": "#ea580c", "name": "Drug Classes"},
        "medication": {"color": "#7c3aed", "name": "Medications"}
    }
    
    for n_type, config in type_configs.items():
        type_nodes = [n for n in nodes if n["type"] == n_type]
        if type_nodes:
            node_trace = go.Scatter(
                x=[n["x"] for n in type_nodes],
                y=[n["y"] for n in type_nodes],
                mode='markers+text',
                marker=dict(
                    size=[n["size"] for n in type_nodes],
                    color=config["color"],
                    line=dict(width=2, color='white')
                ),
                text=[n["label"] for n in type_nodes],
                textposition="top center",
                textfont=dict(size=11, color='#1e293b', family='Inter, sans-serif'),
                hoverinfo='text',
                hovertext=[n["hover"] for n in type_nodes],
                name=config["name"],
                showlegend=True
            )
            fig_data.append(node_trace)
    
    fig = go.Figure(data=fig_data)
    
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#e2e8f0',
            borderwidth=1
        ),
        hovermode='closest',
        margin=dict(b=40, l=40, r=40, t=100),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-7, 7]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-7, 7]),
        plot_bgcolor='white',
        height=800,
        title=dict(
            text=f"AI-Powered Allergy Relationship Analysis",
            font=dict(size=24, family='Inter, sans-serif', color='#0f172a'),
            x=0.5,
            y=0.95
        ),
        annotations=[
            dict(
                text="<b>Outer Ring:</b> Medications to Avoid<br><b>Middle Ring:</b> Drug Classes & Cross-Reactions<br><b>Inner Ring:</b> Primary Allergies",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.01, y=-0.05,
                align="left",
                font=dict(size=12, color='#64748b')
            )
        ]
    )
    
    return fig


def allergy_profile():
    """Patient Allergy Profile Page"""
    st.header("Patient Allergy Profile Viewer")
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
            
            # Network Graph Visualization
            st.subheader("Allergy-Medication Relationship Network")
            st.write("Interactive visualization showing how patient allergies relate to medications through drug classes and cross-reactivity.")
            
            network_fig = create_allergy_network_graph(selected_patient_id)
            if network_fig:
                st.plotly_chart(network_fig, use_container_width=True)
                
                # Legend explanation
                with st.expander("How to Read This Graph"):
                    st.markdown("""
                    **Node Types:**
                    - 🔵 **Blue (Center)**: Patient
                    - 🔴 **Red (Inner Circle)**: Patient's allergies
                    - 🟠 **Orange (Middle Circle)**: Drug classes that match allergies
                    - 🟣 **Purple (Outer Circle)**: Medications to avoid
                    
                    **Connection Types:**
                    - **Solid Red Lines**: Direct allergy relationship
                    - **Dashed Orange Lines**: Drug class matches
                    - **Gray Lines**: Medication belongs to drug class
                    - **Colored Lines to Medications**: Cross-reactivity risk
                      - Dark Red: High risk (>0.7)
                      - Orange: Medium risk (0.5-0.7)
                      - Green: Low risk (<0.5)
                    
                    **Hover** over nodes and lines to see details!
                    """)
            else:
                st.info("No allergy relationships to visualize for this patient.")
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Known Allergies")
                if allergies:
                    # Display allergies without pandas
                    for allergy in allergies:
                        with st.expander(f"{allergy['allergy_name']} ({allergy['allergy_type']})"):
                            st.write(f"**Date Recorded:** {allergy['date_recorded']}")
                            st.write(f"**Notes:** {allergy.get('notes', 'No notes')}")
                else:
                    st.success("No known allergies recorded for this patient")
            
            with col2:
                st.subheader("Cross-Reactivity Risk Profile")
                high_risk_items = [item for item in risk_profile if item.get('reactive_drug') and item.get('risk_score', 0) > 0.5]
                
                if high_risk_items:
                    # Display risk items without pandas
                    for risk in high_risk_items:
                        risk_indicator = "CRITICAL" if risk.get('risk_level') == 'Critical' else "HIGH" if risk.get('risk_level') == 'High' else "MEDIUM"
                        with st.expander(f"[{risk_indicator}] {risk['allergy_name']} → {risk['reactive_drug']}"):
                            st.write(f"**Risk Level:** {risk.get('risk_level', 'Unknown')}")
                            st.write(f"**Risk Score:** {risk.get('risk_score', 0):.2f}")
                else:
                    st.success("No high-risk cross-reactivity medications found")
        else:
            st.error("Failed to load patient allergy data")


def alert_log():
    """Alert Log Page"""
    st.header("Alert Log & Audit Trail")
    st.write("Complete history of all allergy checks and alerts generated by the system.")
    
    # Fetch recent alerts
    alerts_data = make_api_request("/api/v1/alerts/recent?limit=50")
    
    if alerts_data and alerts_data.get("success"):
        alerts = alerts_data["recent_alerts"]
        
        if alerts:
            # Process alerts without pandas
            alert_types = list(set(alert['alert_type'] for alert in alerts))
            patients = list(set(alert['patient_name'] for alert in alerts))
            
            # Add filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                selected_alert_type = st.selectbox("Filter by Alert Type", ["All"] + alert_types)
            
            with col2:
                selected_patient = st.selectbox("Filter by Patient", ["All"] + patients)
            
            with col3:
                st.metric("Total Alerts", len(alerts))
            
            # Apply filters
            filtered_alerts = alerts
            if selected_alert_type != "All":
                filtered_alerts = [a for a in filtered_alerts if a['alert_type'] == selected_alert_type]
            if selected_patient != "All":
                filtered_alerts = [a for a in filtered_alerts if a['patient_name'] == selected_patient]
            
            # Display filtered results
            st.subheader(f"Alert History ({len(filtered_alerts)} alerts)")
            
            # Display alerts without pandas
            for alert in filtered_alerts:
                alert_status = "CRITICAL" if alert['alert_type'] in ['EXACT_MATCH', 'CLASS_MATCH', 'CROSS_REACTIVITY'] else "SAFE"
                logged_time = datetime.fromisoformat(alert['logged_at'].replace('Z', '+00:00')) if isinstance(alert['logged_at'], str) else alert['logged_at']
                
                with st.expander(f"[{alert_status}] {alert['patient_name']} - {alert['med_name']} ({alert['alert_type']})"):
                    st.write(f"**Alert Type:** {alert['alert_type']}")
                    st.write(f"**Message:** {alert['alert_message']}")
                    st.write(f"**Prescription Status:** {alert.get('prescription_status', 'N/A')}")
                    st.write(f"**Logged:** {logged_time.strftime('%Y-%m-%d %H:%M:%S') if hasattr(logged_time, 'strftime') else str(logged_time)}")
            
        else:
            st.info("No alerts found in the system")
    else:
        st.error("Failed to load alert data")


def statistics_panel():
    """Statistics Panel Page"""
    st.header("System Statistics")
    st.write("Overview of allergy alerts, prescriptions, and system performance metrics.")
    
    # Fetch statistics
    stats_data = make_api_request("/api/v1/stats")
    
    if stats_data and stats_data.get("success"):
        alert_stats = stats_data["alert_statistics"]
        additional_stats = stats_data["additional_stats"]
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Patients", additional_stats["total_patients"])
        
        with col2:
            st.metric("Total Medications", additional_stats["total_medications"])
        
        with col3:
            st.metric("Total Prescriptions", additional_stats["total_prescriptions"])
        
        with col4:
            st.metric("High Risk Rules", additional_stats["high_risk_rules"])
        
        # Alert statistics charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Alert Type Distribution")
            if alert_stats:
                # Create simple bar chart data
                chart_data = {item['alert_type']: item['total'] for item in alert_stats}
                st.bar_chart(chart_data)
        
        with col2:
            st.subheader("Alert Breakdown")
            if alert_stats:
                # Display as metrics instead of pie chart
                for stat in alert_stats:
                    status_indicator = "CRITICAL" if stat['alert_type'] in ['EXACT_MATCH', 'CLASS_MATCH', 'CROSS_REACTIVITY'] else "SAFE"
                    st.metric(f"[{status_indicator}] {stat['alert_type']}", stat['total'])
        
        # Prescription status breakdown
        if additional_stats.get("prescription_stats"):
            st.subheader("Prescription Status")
            prescription_stats = additional_stats["prescription_stats"]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Approved", prescription_stats.get("Approved", 0))
            
            with col2:
                st.metric("Rejected", prescription_stats.get("Rejected", 0))
            
            with col3:
                st.metric("Pending", prescription_stats.get("Pending", 0))
        
        # Safety metrics
        st.subheader("Key Performance Indicators")
        
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
            st.metric("Safety Rate", f"{safety_rate:.1f}%")
        
        with col2:
            st.metric("Alert Rate", f"{alert_rate:.1f}%")
        
        with col3:
            st.metric("Total Checks", total_alerts)
        
    else:
        st.error("Failed to load statistics")


def medication_browser():
    """Medication Browser Page"""
    st.header("Medication & Alternatives Browser")
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
        st.subheader("Medication List")
        
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
                
                st.subheader("Medication Details")
                
                st.info(f"""
                **Name:** {medication['med_name']}  
                **Drug Class:** {medication['drug_class']}  
                **Active Ingredients:** {medication['active_ingredients']}  
                **Medication ID:** {medication['_id']}
                """)
                
                # Alternatives
                if alternatives:
                    st.subheader("Safe Alternatives")
                    for alt in alternatives:
                        st.write(f"**{alt['med_name']}** ({alt['drug_class']}) - {alt['reason']}")
                
                # Cross-reactivity warnings
                if cross_reactivity:
                    st.subheader("Cross-Reactivity Warnings")
                    for cross in cross_reactivity:
                        risk_level = cross['risk_level']
                        st.write(f"**{cross['allergy_name']}** - {risk_level} (Score: {cross['risk_score']})")
                
                if not alternatives and not cross_reactivity:
                    st.success("No specific alternatives or cross-reactivity warnings found for this medication.")
        else:
            st.info("Select a medication from the list to view detailed information")
    
    # Drug class overview
    st.subheader("Drug Class Overview")
    if drug_classes:
        for drug_class in drug_classes:
            with st.expander(f"{drug_class['drug_class']} ({drug_class['medication_count']} medications)"):
                st.write(f"**Examples:** {', '.join(drug_class.get('medications', [])[:3])}")
                if len(drug_class.get('medications', [])) > 3:
                    st.write("...and more")


def main():
    """Main Streamlit application"""
    display_header()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    pages = {
        "Prescription Validator": prescription_validator,
        "Patient Allergies": allergy_profile,
        "Alert Log": alert_log,
        "Statistics": statistics_panel,
        "Medications": medication_browser
    }
    
    selected_page = st.sidebar.selectbox("Choose a page", list(pages.keys()))
    
    # API health check
    try:
        health_data = make_api_request("/health")
        if health_data and health_data.get("status") == "OK":
            st.sidebar.markdown('<p class="status-connected">Database Connected</p>', unsafe_allow_html=True)
        else:
            st.sidebar.markdown('<p class="status-disconnected">Database Disconnected</p>', unsafe_allow_html=True)
    except:
        st.sidebar.markdown('<p class="status-warning">Connecting to Database...</p>', unsafe_allow_html=True)
    
    # Display selected page
    pages[selected_page]()
    
    # Footer
    st.markdown("""
    <div class="clinical-footer">
        <p><strong>Features:</strong> 9 Collections • MongoDB Atlas • 3-Level Cascade Checking</p>
        <p><strong>Technology:</strong> Python • Streamlit • MongoDB Atlas • Plotly</p>
        <p><strong>Deployment:</strong> Streamlit Cloud + MongoDB Atlas</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()